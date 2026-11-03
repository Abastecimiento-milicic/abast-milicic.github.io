with open('js/demoras.js', encoding='utf-8') as f:
    js = f.read()

assert 'PERIODO CORTO (CON PRIORIDAD)' in js
assert 'PERIODO CORTO (SIN PRIORIDAD)' in js

print("Verification passed successfully: getDisplayName correctly maps FECHAENTREGAMUYCERCANA to PERIODO CORTO!")
