# -*- coding: utf-8 -*-

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace FT color with #f59e0b
html = html.replace('id="res_cumplAcumFTpct" style="font-size: 15px; font-weight: 800; color: #ea580c; margin: 0 6px;"',
                    'id="res_cumplAcumFTpct" style="font-size: 15px; font-weight: 800; color: #f59e0b; margin: 0 6px;"')
html = html.replace('id="res_cumplFTpct" style="font-size: 15px; font-weight: 800; color: #ea580c; margin: 0 6px;"',
                    'id="res_cumplFTpct" style="font-size: 15px; font-weight: 800; color: #f59e0b; margin: 0 6px;"')

# Cache buster
html = html.replace('js/resumen.js?v=20261030_125900', 'js/resumen.js?v=20261030_130200')

with open('index.html', 'w', encoding='utf-8', newline='') as f:
    f.write(html)
print("index.html updated with #f59e0b for FT.")

# 2. Update js/resumen.js
with open('js/resumen.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace('elAcumFT.style.color = "#ea580c"', 'elAcumFT.style.color = "#f59e0b"')
js = js.replace('elFT.style.color = "#ea580c"', 'elFT.style.color = "#f59e0b"')

with open('js/resumen.js', 'w', encoding='utf-8', newline='') as f:
    f.write(js)
print("js/resumen.js updated with #f59e0b for FT.")
