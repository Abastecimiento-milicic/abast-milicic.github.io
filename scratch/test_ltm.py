import csv

def to_num(v):
    if not v: return 0.0
    v = v.replace(' ', '').replace('.', '').replace(',', '.')
    try: return float(v)
    except: return 0.0

rows = []
with open('data/CUMPLIMIENTO_OPTIMIZADO.csv', 'r', encoding='utf-8') as f:
    r = csv.DictReader(f, delimiter=';')
    for row in r:
        fec = row.get('FECHA ENTREGA ESPERADA', '').strip()
        parts = fec.split('/')
        if len(parts) == 3:
            row['_ym'] = f"{parts[2]}-{parts[1].zfill(2)}"
            rows.append(row)

ltm_months = ['2025-10', '2025-11', '2025-12', '2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06', '2026-07', '2026-08', '2026-09']
rows_ltm = [r for r in rows if r['_ym'] in ltm_months]

def calc(subrows):
    tot = sum(to_num(r.get('COMPROMETIDOS', 0)) for r in subrows)
    at = sum(to_num(r.get('ENTREGADOS AT', 0)) for r in subrows)
    ft = sum(to_num(r.get('ENTREGADOS FT', 0)) for r in subrows)
    ne = sum(to_num(r.get('NO ENTREGADOS', 0)) for r in subrows)
    dias = [to_num(r.get('DIAS DE DEMORA', 0)) for r in subrows if to_num(r.get('DIAS DE DEMORA', 0)) > 0]
    avg_dem = sum(dias) / len(dias) if dias else 0
    return {
        'tot': tot,
        'at': at,
        'ft': ft,
        'ne': ne,
        'pct_at': (at/tot*100) if tot else 0,
        'pct_ft': (ft/tot*100) if tot else 0,
        'pct_ne': (ne/tot*100) if tot else 0,
        'avg_dem': avg_dem
    }

res_ltm = calc(rows_ltm)
print("Consolidado LTM (12 meses):")
print("Total Comprometidos:", res_ltm['tot'])
print(f"AT: {res_ltm['pct_at']:.1f}% ({res_ltm['at']})")
print(f"FT: {res_ltm['pct_ft']:.1f}% ({res_ltm['ft']})")
print(f"NE: {res_ltm['pct_ne']:.1f}% ({res_ltm['ne']})")
print(f"Demora promedio: {res_ltm['avg_dem']:.1f} d")
