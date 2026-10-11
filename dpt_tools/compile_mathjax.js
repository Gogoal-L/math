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
        const tag = item.tex.match(/\\tag\{([^}]+)\}/);
        widths.push({ex: Number(m[1]), label: tag ? tag[1] : 'unnumbered',
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
for (const e of failures) console.error('MATHJAX_ERROR ' + e);
if (failures.length) process.exit(1);
