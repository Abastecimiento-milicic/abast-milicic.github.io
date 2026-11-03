import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

assert 'id="resumen_obraSelect" multiple size="6" class="multi-select"' in idx, "resumen_obraSelect not multi-select"
assert 'id="resumen_mesCumplSelect" multiple size="6" class="multi-select"' in idx, "resumen_mesCumplSelect not multi-select"
assert "txt.startsWith('todo')" in idx, "isAllOption not updated"
assert "js/demoras.js?v=20261102_153500" in idx, "cache buster for demoras not updated"
assert "js/resumen.js?v=20261102_153500" in idx, "cache buster for resumen not updated"

with open("js/resumen.js", "r", encoding="utf-8") as f:
    res = f.read()

assert '"26_314": "00026 / 00314 - CASA OLAVARRIA / SANTA FE"' in res, "OBRA_MAP 26_314 missing"
assert '"35_341": "00035 / 00341 - MOV SUELOS SAN LUIS"' in res, "OBRA_MAP 35_341 missing"
assert 'function getCanonicalObraCode' in res, "getCanonicalObraCode missing"
assert 'function getSelectedObras' in res, "getSelectedObras missing"
assert 'function getSelectedMeses' in res, "getSelectedMeses missing"

with open("js/demoras.js", "r", encoding="utf-8") as f:
    dem = f.read()

assert 'function getCanonicalObra' in dem, "getCanonicalObra in demoras missing"
assert 'obraList = clientCode.filter(c => c && c !== "__ALL__").map(getCanonicalObra)' in dem, "obraList filter missing"

with open("js/last-update.js", "r", encoding="utf-8") as f:
    lu = f.read()

assert '_v79_20261102_153500' in lu, "CACHE_BUSTER in last-update.js missing"

print("ALL ASSERTIONS PASSED SUCCESSFULLY!")
