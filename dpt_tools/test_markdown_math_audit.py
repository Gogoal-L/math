import unittest
from markdown_math_audit import audit_markdown, extract_math


class MarkdownMathAuditTests(unittest.TestCase):
    def test_literal_latex_parentheses_from_screenshot_are_rejected(self):
        src = r'实现的解码器可取 \(\widehat G(x)=(r^2-x^2)/2\)。'
        e = audit_markdown(src, 'map.md')
        self.assertTrue(any('UNSUPPORTED_INLINE' in q for q in e), e)

    def test_github_supported_inline_dollars_and_protected_code(self):
        src = (r'解码器 $\widehat G(x)=(r^2-x^2)/2$，'
               + r'还有 $`D^2G[v,v]`$ 和代码 `\(foo\)`。')
        self.assertEqual(audit_markdown(src, 'map.md'), [])
        self.assertEqual(len(extract_math(src)), 2)

    def test_math_fences_and_display_blocks(self):
        src = r'''Intro
**(M33)**

```math
\begin{aligned}
a &= b \\
c &= d
\end{aligned}
```

**(M34)**

```math
\boxed{x^2+y^2}
```
'''
        self.assertEqual(audit_markdown(src, 'map.md'), [])
        self.assertEqual([q['kind'] for q in extract_math(src)], ['display','display'])

    def test_mathjax_tag_is_rejected_even_if_tex_parser_accepts_it(self):
        src = r'**(M33)**' + '\n\n' + '```math\na=b\\tag{M33}\n```'
        errors = audit_markdown(src, 'DPT_MATH_RESEARCH_MAP.md')
        self.assertTrue(any('IN_MATH_TAG' in e for e in errors), errors)

    def test_external_label_must_have_formula_following_it(self):
        errors = audit_markdown('**(M1)**\n\nNot a formula', 'map.md')
        self.assertTrue(any('EXTERNAL_EQUATION_LABEL' in e for e in errors), errors)

    def test_bad_brackets_and_unclosed_display_fail(self):
        src = '\n'.join(['$$', r'\frac{1{2}', r'\tag{M33}'])
        e = audit_markdown(src, 'map.md')
        self.assertTrue(any('UNBALANCED' in q or 'UNCLOSED' in q for q in e), e)

    def test_does_not_flag_backslash_parens_in_code_fences(self):
        src = '```python\nfoo = r"\\(ignored\\)"\n```\n'
        self.assertEqual(audit_markdown(src, 'map.md'), [])

    def test_duplicate_equation_tags_rejected(self):
        src='**(M1)**\n\n```math\na=1\n```\n**(M1)**\n\n```math\nb=2\n```'
        errors=audit_markdown(src,'map.md')
        self.assertTrue(any('DUPLICATE_TAG' in e for e in errors),errors)

    def test_repository_map_numbering_gaps_rejected(self):
        src='**(M1)**\n\n```math\na=1\n```\n**(M3)**\n\n```math\nb=2\n```'
        errors=audit_markdown(src,'DPT_MATH_RESEARCH_MAP.md')
        self.assertTrue(any('NONSEQUENTIAL_TAG' in e for e in errors),errors)

    def test_reports_unclosed_inline_math(self):
        e = audit_markdown('一个未关闭的公式 $\\sqrt{x}', 'map.md')
        self.assertTrue(any('UNCLOSED_INLINE' in q for q in e), e)

    def test_reports_equation_left_right_mismatch(self):
        e = audit_markdown('$$\n\\left( a+b\n$$\n', 'map.md')
        self.assertTrue(any('LEFT_RIGHT' in q for q in e), e)

    def test_only_source_text_not_code_or_escaped_dollars(self):
        src = 'Pay \\$5 and use `\\foo` in code; math $x_1^2$ okay.'
        self.assertEqual(audit_markdown(src, 'map.md'), [])


if __name__=='__main__': unittest.main()
