# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

assert 'id="res_cumplAcumFTpct" style="font-size: 15px; font-weight: 800; color: #f59e0b; margin: 0 6px;"' in h
assert 'id="res_cumplFTpct" style="font-size: 15px; font-weight: 800; color: #f59e0b; margin: 0 6px;"' in h

with open('js/resumen.js', 'r', encoding='utf-8') as f:
    j = f.read()

assert 'elAcumFT.style.color = "#f59e0b"' in j
assert 'elFT.style.color = "#f59e0b"' in j

print("VERIFIED: Entregados FT is exactly #f59e0b (amber from Cumplimiento chart) everywhere.")
