import sys, csv, re
sys.stdout.reconfigure(encoding='utf-8')

with open("data/CUMPLIMIENTO_OPTIMIZADO.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=';')
    rows = list(reader)

def parse_date(s):
    if not s: return None
    m = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{4})', s.strip())
    if m:
        return f"{m.group(3)}-{m.group(2).zfill(2)}"
    return None

for r in rows:
    r['_ym'] = parse_date(r.get('FECHA ENTREGA ESPERADA', ''))

# Group by CLIENTE and Month
print("Testing Obra 0223 across all months:")
months_223 = sorted(list(set(r['_ym'] for r in rows if '223' in r.get('CLIENTE', '') and r['_ym'])))

for m in months_223:
    sub = [r for r in rows if '223' in r.get('CLIENTE', '') and r['_ym'] == m]
    at = sum(float(r.get('ENTREGADOS AT', 0) or 0) for r in sub)
    ft = sum(float(r.get('ENTREGADOS FT', 0) or 0) for r in sub)
    ne = sum(float(r.get('NO ENTREGADOS', 0) or 0) for r in sub)
    tot = sum(float(r.get('COMPROMETIDOS', 0) or 0) for r in sub)
    pct = (at / tot * 100) if tot else 0
    print(f"  Month {m}: Total={tot:3.0f}, AT={at:3.0f}, FT={ft:3.0f}, NE={ne:3.0f} -> AT%={pct:.1f}%")
