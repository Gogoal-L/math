#!/usr/bin/env python3
"""GitHub MathJax Markdown delimiter and elementary TeX structural checks.

Checks *source syntax*, not the correctness of equations or visual browser CSS.
For actual MathJax parsing use compile_mathjax.js with --dump-json.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

FENCE = re.compile(r'^\s{0,3}(?P<mark>`{3,}|~{3,})(?P<info>[^\n]*)$')
ALT_MATH = re.compile(r'(?<!\\)\$`([^`\n]+)`\$')
INLINE_MATH = re.compile(r'(?<!\\)(?<!\$)\$(?!\$)([^\n$]+?)(?<!\\)\$(?!\$)')
CODE_SPAN = re.compile(r'(`+)(?!`)(.*?)\1')
UNSUPPORTED = re.compile(r'\\[()\[\]]')
TEX_BEGIN = re.compile(r'\\begin\{([^{}]+)\}')
TEX_END = re.compile(r'\\end\{([^{}]+)\}')


def _tex_errors(expr: str, label: str) -> list[str]:
    out = []
    braces = 0
    for c in re.sub(r'\\[{}]', '', expr):
        if c == '{':
            braces += 1
        elif c == '}':
            braces -= 1
            if braces < 0:
                out.append(f'{label}: UNBALANCED_CLOSING_BRACE')
                braces = 0
    if braces:
        out.append(f'{label}: UNBALANCED_BRACES ({braces})')
    if len(re.findall(r'\\left\b', expr)) != len(re.findall(r'\\right\b', expr)):
        out.append(f'{label}: LEFT_RIGHT_DELIMITER_MISMATCH')
    if TEX_BEGIN.findall(expr) != TEX_END.findall(expr):
        out.append(f'{label}: BEGIN_END_ENV_MISMATCH')
    return out


def _split_source(source: str):
    """Yield display math or ordinary prose outside unrelated fenced code."""
    kind = 'text'
    marker = ''
    start = 0
    block = []
    for i, line in enumerate(source.splitlines(), 1):
        stripped = line.strip()
        m = FENCE.match(line)
        if kind == 'fence':
            if m and m['mark'][0] == marker[0] and len(m['mark']) >= len(marker):
                kind, marker = 'text', ''
            continue
        if kind == 'mathfence':
            if m and m['mark'][0] == marker[0] and len(m['mark']) >= len(marker):
                yield 'display', '\n'.join(block), start
                kind, marker, block = 'text', '', []
            else:
                block.append(line)
            continue
        if kind == 'dollar':
            if stripped == '$$':
                yield 'display', '\n'.join(block), start
                kind, block = 'text', []
            else:
                block.append(line)
            continue
        if m:
            marker = m['mark']
            kind = 'mathfence' if m['info'].strip().lower() == 'math' else 'fence'
            start = i
        elif stripped == '$$':
            kind = 'dollar'
            start = i
        else:
            yield 'text', line, i
    if kind in ('dollar', 'mathfence'):
        yield 'error', kind, start


def _process_text(line: str, no: int):
    found = []
    def protected(m):
        found.append({'kind': 'inline', 'line': no, 'tex': m[1]})
        return 'X'
    rem = ALT_MATH.sub(protected, line)
    rem = CODE_SPAN.sub('X', rem)
    def normal(m):
        found.append({'kind': 'inline', 'line': no, 'tex': m[1]})
        return 'X'
    rem = INLINE_MATH.sub(normal, rem)
    errors = []
    if UNSUPPORTED.search(rem):
        errors.append(f'line {no}: UNSUPPORTED_INLINE_TEX_DELIMITER, use $...$ or $`...`$')
    if re.search(r'(?<!\\)\\[A-Za-z]{2,}', rem):
        errors.append(f'line {no}: RAW_TEX_COMMAND_OUTSIDE_MATH')
    if re.search(r'(?<!\\)\$(?!\$)', rem):
        errors.append(f'line {no}: UNCLOSED_INLINE_OR_UNSUPPORTED_DOLLAR')
    return found, errors


def extract_math(source: str) -> list[dict]:
    extracted = []
    lines = source.splitlines()
    for kind, content, no in _split_source(source):
        if kind == 'display':
            item = {'kind': 'display', 'line': no, 'tex': content}
            preceding = no - 2  # no is 1-based index of opening math fence
            while preceding >= 0 and not lines[preceding].strip():
                preceding -= 1
            if preceding >= 0:
                label = re.fullmatch(
                    r'\*\*\(([A-Za-z]+\d+|\d+)\)\*\*',
                    lines[preceding].strip(),
                )
                if label:
                    item['label'] = label.group(1)
            extracted.append(item)
        elif kind == 'text':
            extracted.extend(_process_text(content, no)[0])
    return extracted


def audit_markdown(source: str, name='document') -> list[str]:
    errors = []
    lines = source.splitlines()
    if lines and lines[0].startswith('# ') and lines.count(lines[0]) != 1:
        errors.append(f'{name}: DUPLICATED_DOCUMENT_ROOT')
    for kind, content, no in _split_source(source):
        prefix = f'{name}:{no}'
        if kind == 'error':
            errors.append(f'{prefix}: UNCLOSED_{content.upper()}_BLOCK')
        elif kind == 'display':
            if not content.strip():
                errors.append(f'{prefix}: EMPTY_DISPLAY_MATH')
            if re.search(r'\\tag\{[^{}]+\}', content):
                errors.append(f'{prefix}: IN_MATH_TAG - move equation number outside MathJax block')
            errors += _tex_errors(content, prefix)
        else:
            fragments, source_errors = _process_text(content, no)
            errors += [f'{name}:{e}' for e in source_errors]
            for x in fragments:
                errors += _tex_errors(x['tex'], prefix)
    # Equation labels are ordinary Markdown, not MathJax tagged equations.
    labels = re.findall(r'(?m)^\*\*\(([A-Za-z]+\d+|\d+)\)\*\*\s*$', source)
    if len(labels) != len(set(labels)):
        errors.append(f'{name}: DUPLICATE_TAG in external equation labels')
    expected_prefixes = {
        'DPT_MATH_RESEARCH_MAP.md': 'M',
        '20261012_mixed_nuisance_goal_radius_formal_derivation.md': 'P',
        '20261012_second_order_goal_fiber.md': 'C',
    }
    prefix = expected_prefixes.get(Path(name).name)
    if prefix:
        numbered = [int(t[len(prefix):]) for t in labels if re.fullmatch(prefix + r'\d+', t)]
        if not numbered or numbered != list(range(1, len(numbered) + 1)):
            errors.append(f'{name}: NONSEQUENTIAL_TAG in external {prefix}-equation labels')
    # External labels must sit directly above a standalone math display.
    lines = source.splitlines()
    for number, line in enumerate(lines):
        if re.fullmatch(r'\*\*\((?:[A-Za-z]+\d+|\d+)\)\*\*', line.strip()):
            nxt = number + 1
            while nxt < len(lines) and not lines[nxt].strip():
                nxt += 1
            if nxt >= len(lines) or lines[nxt].strip() != '```math':
                errors.append(f'{name}:{number+1}: EXTERNAL_EQUATION_LABEL_NOT_FOLLOWED_BY_MATH_FENCE')

    return errors


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('files', nargs='+', type=Path)
    p.add_argument('--dump-json', help='Export fragments for independent MathJax parsing')
    a = p.parse_args()
    all_math, problems = [], []
    for file in a.files:
        source = file.read_text(encoding='utf8')
        report = audit_markdown(source, str(file))
        problems += report
        found = extract_math(source)
        all_math += [{**m, 'file': str(file)} for m in found]
        print(f'{file}: {len(found)} math fragments, {len(report)} errors')
    if a.dump_json:
        Path(a.dump_json).write_text(json.dumps(all_math, ensure_ascii=False), encoding='utf8')
    for e in problems:
        print('ERROR:', e)
    return 1 if problems else 0


if __name__ == '__main__':
    raise SystemExit(main())
