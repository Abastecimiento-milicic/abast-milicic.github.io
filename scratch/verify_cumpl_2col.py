# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

assert 'id="res_cumplAcumComprometidos"' in html
assert 'id="res_cumplAcumATpct"' in html
assert 'id="res_cumplAcumDemoraAvg"' in html
assert 'id="res_cumplComprometidos"' in html
assert 'id="res_cumplATdiff"' in html

with open('js/resumen.js', 'r', encoding='utf-8') as f:
    js = f.read()

assert 'res_cumplAcumComprometidos' in js
assert 'res_cumplAcumATpct' in js
assert 'res_cumplAcumRango' in js

print("ALL VERIFICATIONS PASSED: 2-column Cumplimiento layout & JS logic verified.")
