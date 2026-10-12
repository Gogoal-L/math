#!/usr/bin/env node
// Compiles extracted project Markdown formulas with MathJax, GitHub's math engine.
// This validates engine-level TeX parsing, not a browser CSS screenshot or proof.
const fs = require('fs');
const {mathjax} = require('mathjax-full/js/mathjax.js');
const {TeX} = require('mathjax-full/js/input/tex.js');
const {SVG} = require('mathjax-full/js/output/svg.js');
const {liteAdaptor} = require('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require('mathjax-full/js/handlers/html.js');
const {AllPackages} = require('mathjax-full/js/input/tex/AllPackages.js');

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const tex = new TeX({packages: AllPackages, tags: 'all'});
const doc = mathjax.document('', {InputJax: tex, OutputJax: new SVG({fontCache: 'none'})});
const input = process.argv[2];
if (!input) {
  console.error('Usage: node compile_mathjax.js equations.json');
  process.exit(2);
}
const equations = JSON.parse(fs.readFileSync(input, 'utf8'));
const failures = [];
const widths = [];
for (const item of equations) {
  try {
    tex.reset();
    const node = doc.convert(item.tex, {display: item.kind === 'display'});
    const html = adaptor.outerHTML(node);
    if (html.includes('<merror') || html.includes('data-mjx-error')) {
      failures.push(item.file + ':' + item.line + ' emitted MathJax error');
    }
    if (item.kind === 'display') {
      const m = html.match(/min-width:\s*([0-9.]+)ex/);
      if (m) {
        widths.push({ex: Number(m[1]), label: item.label || 'unnumbered',
                     file: item.file, line: item.line});
      }
    }
  } catch (error) {
    failures.push(item.file + ':' + item.line + ': ' + error.message);
  }
}
widths.sort((a, b) => b.ex - a.ex);
console.log('MathJax compiled ' + equations.length + ' equations, '
            + failures.length + ' parser errors');
console.log('Widest display equations (ex units): ' + JSON.stringify(widths.slice(0, 15)));
// MathJax 3 does not reliably wrap wide display equations. An SVG min-width
// above the declared conservative 75ex cap is a layout regression even when
// TeX parses without errors. This is not a substitute for mobile screenshots.
const MAX_DISPLAY_WIDTH_EX = 75;
const overwide = widths.filter(w => w.ex > MAX_DISPLAY_WIDTH_EX);
for (const w of overwide) {
  failures.push(w.file + ':' + w.line + ' ' + w.label +
      ' display width ' + w.ex + 'ex exceeds ' + MAX_DISPLAY_WIDTH_EX + 'ex');
}
for (const e of failures) console.error('MATHJAX_ERROR ' + e);
if (failures.length) process.exit(1);
