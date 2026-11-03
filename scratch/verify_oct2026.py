with open('js/demoras.js', encoding='utf-8') as f:
    js_dem = f.read()

assert 'A partir de Octubre 2026' in js_dem
assert 'Anterior a Octubre 2026' in js_dem
assert 'new Date(2026, 9, 1)' in js_dem
assert 'isAftOct2026' in js_dem

with open('js/clasificacion_logic.js', encoding='utf-8') as f:
    js_clas = f.read()

assert 'new Date(2026, 9, 1)' in js_clas
assert 'isAftOct2026' in js_clas

print("Verification passed successfully! October 2026 cutoff confirmed.")
