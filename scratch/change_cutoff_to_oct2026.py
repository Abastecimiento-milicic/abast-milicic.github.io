import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Update js/demoras.js
with open('js/demoras.js', 'r', encoding='utf-8') as f:
    js_dem = f.read()

# Replace titles in formula modal
js_dem = js_dem.replace('<b>A partir de Noviembre 2026:</b>', '<b>A partir de Octubre 2026:</b>')
js_dem = js_dem.replace('<b>Anterior a Noviembre 2026 (Hasta Octubre 2026):</b>', '<b>Anterior a Octubre 2026 (Hasta Septiembre 2026):</b>')

# Replace calculation condition
old_cond_dem = """                      const isAftNov2026 = (fEntregaEsperada >= new Date(2026, 10, 1));

                      if (isAftNov2026) {
                        // A PARTIR DE NOVIEMBRE 2026"""

new_cond_dem = """                      const isAftOct2026 = (fEntregaEsperada >= new Date(2026, 9, 1));

                      if (isAftOct2026) {
                        // A PARTIR DE OCTUBRE 2026"""

assert old_cond_dem in js_dem, "old_cond_dem not found in demoras.js"
js_dem = js_dem.replace(old_cond_dem, new_cond_dem, 1)

old_comment_dem = "// ANTERIOR A NOVIEMBRE 2026 (REGLAS VIGENTES HASTA OCTUBRE 2026)"
new_comment_dem = "// ANTERIOR A OCTUBRE 2026 (REGLAS VIGENTES HASTA SEPTIEMBRE 2026)"
assert old_comment_dem in js_dem, "old_comment_dem not found in demoras.js"
js_dem = js_dem.replace(old_comment_dem, new_comment_dem, 1)

with open('js/demoras.js', 'w', encoding='utf-8') as f:
    f.write(js_dem)

print("Updated js/demoras.js cutoff to October 2026!")

# 2. Update js/clasificacion_logic.js
with open('js/clasificacion_logic.js', 'r', encoding='utf-8') as f:
    js_clas = f.read()

old_cond_clas = """                      var isAftNov2026 = (dtEntregaEsperada >= new Date(2026, 10, 1));
                      if (isAftNov2026) {
                          // A PARTIR DE NOVIEMBRE 2026"""

new_cond_clas = """                      var isAftOct2026 = (dtEntregaEsperada >= new Date(2026, 9, 1));
                      if (isAftOct2026) {
                          // A PARTIR DE OCTUBRE 2026"""

assert old_cond_clas in js_clas, "old_cond_clas not found in clasificacion_logic.js"
js_clas = js_clas.replace(old_cond_clas, new_cond_clas, 1)

old_comment_clas = "// ANTERIOR A NOVIEMBRE 2026"
new_comment_clas = "// ANTERIOR A OCTUBRE 2026"
assert old_comment_clas in js_clas, "old_comment_clas not found in clasificacion_logic.js"
js_clas = js_clas.replace(old_comment_clas, new_comment_clas, 1)

with open('js/clasificacion_logic.js', 'w', encoding='utf-8') as f:
    f.write(js_clas)

print("Updated js/clasificacion_logic.js cutoff to October 2026!")

# 3. Update js/last-update.js
with open('js/last-update.js', 'r', encoding='utf-8') as f:
    js_lu = f.read()

old_cb = 'window.CACHE_BUSTER = cb + "_v77_20261102_150000";'
new_cb = 'window.CACHE_BUSTER = cb + "_v78_20261102_150500";'

assert old_cb in js_lu, "old_cb not found in last-update.js"
js_lu = js_lu.replace(old_cb, new_cb, 1)

with open('js/last-update.js', 'w', encoding='utf-8') as f:
    f.write(js_lu)

print("Updated js/last-update.js CACHE_BUSTER to v78!")

# 4. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('?v=20261102_150000', '?v=20261102_150500')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html cache buster to 20261102_150500!")
