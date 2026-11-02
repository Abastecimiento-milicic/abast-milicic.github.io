# -*- coding: utf-8 -*-

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Acumulado FT & NE
html = html.replace('id="res_cumplAcumFTpct" style="font-size: 15px; font-weight: 800; color: #dc2626; margin: 0 6px;"',
                    'id="res_cumplAcumFTpct" style="font-size: 15px; font-weight: 800; color: #ea580c; margin: 0 6px;"')
html = html.replace('id="res_cumplAcumNEpct" style="font-size: 15px; font-weight: 800; color: #64748b; margin: 0 6px;"',
                    'id="res_cumplAcumNEpct" style="font-size: 15px; font-weight: 800; color: #dc2626; margin: 0 6px;"')

# Mensual FT & NE
html = html.replace('id="res_cumplFTpct" style="font-size: 15px; font-weight: 800; color: #dc2626; margin: 0 6px;"',
                    'id="res_cumplFTpct" style="font-size: 15px; font-weight: 800; color: #ea580c; margin: 0 6px;"')
html = html.replace('id="res_cumplNEpct" style="font-size: 15px; font-weight: 800; color: #64748b; margin: 0 6px;"',
                    'id="res_cumplNEpct" style="font-size: 15px; font-weight: 800; color: #dc2626; margin: 0 6px;"')

# Cache-buster
html = html.replace('js/resumen.js?v=20261030_125300', 'js/resumen.js?v=20261030_125700')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html colors and version.")

# 2. Update js/resumen.js
with open('js/resumen.js', 'r', encoding='utf-8') as f:
    js = f.read()

target_js_block = """    setText("res_cumplAcumFTpct", fmtPct01(mLTM.pctFt));
    setText("res_cumplAcumFTqty", fmtInt(mLTM.ft));

    setText("res_cumplAcumNEpct", fmtPct01(mLTM.pctNe));
    setText("res_cumplAcumNEqty", fmtInt(mLTM.ne));"""

replacement_js_block = """    setText("res_cumplAcumFTpct", fmtPct01(mLTM.pctFt));
    setText("res_cumplAcumFTqty", fmtInt(mLTM.ft));
    const elAcumFT = document.getElementById("res_cumplAcumFTpct");
    if (elAcumFT) elAcumFT.style.color = "#ea580c"; // Naranja

    setText("res_cumplAcumNEpct", fmtPct01(mLTM.pctNe));
    setText("res_cumplAcumNEqty", fmtInt(mLTM.ne));
    const elAcumNE = document.getElementById("res_cumplAcumNEpct");
    if (elAcumNE) elAcumNE.style.color = "#dc2626"; // Rojo"""

js_norm = js.replace('\r\n', '\n')
target_norm = target_js_block.replace('\r\n', '\n')
repl_norm = replacement_js_block.replace('\r\n', '\n')

if target_norm in js_norm:
    js_norm = js_norm.replace(target_norm, repl_norm, 1)

target_mensual = """    // FT
    setText("res_cumplFTpct", fmtPct01(mCurr.pctFt));
    setText("res_cumplFTqty", fmtInt(mCurr.ft));
    setText("res_cumplFTdiff", diffFTInfo.text);
    const elFTdiff = document.getElementById("res_cumplFTdiff");
    if (elFTdiff) elFTdiff.style.color = diffFTInfo.color;

    // NE
    setText("res_cumplNEpct", fmtPct01(mCurr.pctNe));
    setText("res_cumplNEqty", fmtInt(mCurr.ne));
    setText("res_cumplNEdiff", diffNEInfo.text);
    const elNEdiff = document.getElementById("res_cumplNEdiff");
    if (elNEdiff) elNEdiff.style.color = diffNEInfo.color;"""

repl_mensual = """    // FT
    setText("res_cumplFTpct", fmtPct01(mCurr.pctFt));
    setText("res_cumplFTqty", fmtInt(mCurr.ft));
    setText("res_cumplFTdiff", diffFTInfo.text);
    const elFTdiff = document.getElementById("res_cumplFTdiff");
    if (elFTdiff) elFTdiff.style.color = diffFTInfo.color;
    const elFT = document.getElementById("res_cumplFTpct");
    if (elFT) elFT.style.color = "#ea580c"; // Naranja

    // NE
    setText("res_cumplNEpct", fmtPct01(mCurr.pctNe));
    setText("res_cumplNEqty", fmtInt(mCurr.ne));
    setText("res_cumplNEdiff", diffNEInfo.text);
    const elNEdiff = document.getElementById("res_cumplNEdiff");
    if (elNEdiff) elNEdiff.style.color = diffNEInfo.color;
    const elNE = document.getElementById("res_cumplNEpct");
    if (elNE) elNE.style.color = "#dc2626"; // Rojo"""

target_mensual_norm = target_mensual.replace('\r\n', '\n')
repl_mensual_norm = repl_mensual.replace('\r\n', '\n')

if target_mensual_norm in js_norm:
    js_norm = js_norm.replace(target_mensual_norm, repl_mensual_norm, 1)

with open('js/resumen.js', 'w', encoding='utf-8') as f:
    f.write(js_norm.replace('\n', '\r\n'))
print("Updated js/resumen.js with orange for FT and red for NE.")
