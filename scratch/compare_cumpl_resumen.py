import sys, csv, re
sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect how cumplimiento.js filters data
# In cumplimiento.js, what filters/rules are applied by default?
# E.g.:
# - Which date is used for month?
# - Is "Medir cumplimiento arriba" on or off?
# - Which items/positions are excluded or included? (e.g. COMPROMETIDOS > 0? or TIPO DE ITEM? or ESTADO ITEM?)
# - How does CUMPLIMIENTO calculate AT %?

with open("data/CUMPLIMIENTO_OPTIMIZADO.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=';')
    rows = list(reader)

print(f"Total rows in CUMPLIMIENTO_OPTIMIZADO.csv: {len(rows)}")

# Filter for 223
rows_223 = [r for r in rows if '223' in r.get('CLIENTE', '')]
print(f"Rows for 223: {len(rows_223)}")

# Check dates / months for 223
months_fec_esp = {}
months_col_mes = {}
months_fec_cumpl = {}

for r in rows_223:
    mes_entrega = r.get('MES ENTREGA', '').strip()
    fec_esp = r.get('FECHA ENTREGA ESPERADA', '').strip()
    fec_cumpl = r.get('FECHA CUMPLIMIENTO FINAL UNIFICADA', '').strip()
    
    months_col_mes[mes_entrega] = months_col_mes.get(mes_entrega, 0) + 1

print("\nMES ENTREGA column counts for 223:")
for k, v in sorted(months_col_mes.items()):
    print(f"  {k!r}: {v}")
