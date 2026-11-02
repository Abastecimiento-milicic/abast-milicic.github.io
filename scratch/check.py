import sys
sys.stdout.reconfigure(encoding='utf-8')

html = open('index.html', encoding='utf-8').read()
pos_areas = html.find('id="res_chartAreas"')
pos_motivos = html.find('id="res_chartMotivos"')
print(f'pos_areas: {pos_areas}, pos_motivos: {pos_motivos}')
assert pos_areas != -1 and pos_motivos != -1
assert pos_areas < pos_motivos, "Demora por Area must come before Demoras Proyecto"

js = open('js/demoras.js', encoding='utf-8').read()
assert 'FEMC (CON PRIORIDAD)' in js
assert 'FEMC (SIN PRIORIDAD)' in js
assert '#0d6efd' in js

print("SUCCESS: Areas is on the LEFT, Demoras Proyecto is on the RIGHT, FEMC abbreviation and matching chart styling are applied!")
