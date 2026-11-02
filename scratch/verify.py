# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

assert 'id="panel-resumen"' in html
assert 'id="resumen_mesCumplSelect"' in html
assert 'id="res_cumplATpct"' in html
assert 'id="res_cumplFTdiff"' in html

with open('js/resumen.js', 'r', encoding='utf-8') as f:
    js = f.read()

assert 'function updateCumplimientoBlock' in js
assert 'getDiffInfo' in js

print("ALL CHECKS PASSED: Bloque Cumplimiento completamente integrado.")
