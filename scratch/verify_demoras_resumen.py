import re
import sys

# 1. Check index.html
html = open('index.html', encoding='utf-8').read()
assert html.count('id="res_chartMotivos"') == 1, "res_chartMotivos ID count mismatch"
assert html.count('id="res_chartAreas"') == 1, "res_chartAreas ID count mismatch"
assert html.count('id="res_lblTotalMotivos"') == 1, "res_lblTotalMotivos ID count mismatch"
assert html.count('id="res_lblTotalAreas"') == 1, "res_lblTotalAreas ID count mismatch"
assert "BLOQUE 3: DEMORAS" in html, "Bloque 3 missing"
assert "4. SERVICIOS" in html, "Bloque 4 missing"
assert "resizeResumenDemoras" in html, "resizeResumenDemoras call in switchTab missing"

# 2. Check demoras.js
dem = open('js/demoras.js', encoding='utf-8').read()
assert "window.renderResumenDemoras = function" in dem, "renderResumenDemoras missing in demoras.js"
assert "window.resizeResumenDemoras = function" in dem, "resizeResumenDemoras missing in demoras.js"
assert "resChartMotivos" in dem, "resChartMotivos missing in demoras.js"
assert "resChartAreas" in dem, "resChartAreas missing in demoras.js"

# 3. Check resumen.js
res = open('js/resumen.js', encoding='utf-8').read()
assert "function updateDemorasBlock()" in res, "updateDemorasBlock missing in resumen.js"
assert "window.renderResumenDemoras" in res, "renderResumenDemoras call missing in resumen.js"

print("All integrity checks passed perfectly!")
