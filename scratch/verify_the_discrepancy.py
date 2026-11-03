import sys, csv, re
sys.stdout.reconfigure(encoding='utf-8')

with open("data/CUMPLIMIENTO_OPTIMIZADO.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=';')
    headers = reader.fieldnames
    rows = list(reader)

colFec_find = [h for h in headers if 'fecha' in h.lower()][0]
print(f"Header found by headers.find(/fecha/i): {colFec_find!r}")

# Let's calculate for 00223 in October 2026:
# Case 1: Filtering by FECHA ENTREGA ESPERADA = 2026-10 (like cumplimiento.js)
# Case 2: Filtering by FECHA DE EMISION NECESIDAD = 2026-10 (what resumen.js was doing)

def parse_date(s):
    if not s: return None
    m = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{4})', s.strip())
    if m:
        return f"{m.group(3)}-{m.group(2).zfill(2)}"
    return None

def calc_kpis(filtered_rows):
    at, ft, ne, tot = 0, 0, 0, 0
    for r in filtered_rows:
        at_val = float(r.get('ENTREGADOS AT', 0) or 0)
        ft_val = float(r.get('ENTREGADOS FT', 0) or 0)
        ne_val = float(r.get('NO ENTREGADOS', 0) or 0)
        comp = float(r.get('COMPROMETIDOS', 0) or 0)
        at += at_val
        ft += ft_val
        ne += ne_val
        tot += comp
    if not tot: tot = at + ft + ne
    pct_at = (at / tot * 100) if tot else 0
    return at, ft, ne, tot, pct_at

rows_223 = [r for r in rows if '223' in r.get('CLIENTE', '')]

# Case 1: FECHA ENTREGA ESPERADA in 2026-10
rows_fec_esp = [r for r in rows_223 if parse_date(r.get('FECHA ENTREGA ESPERADA', '')) == '2026-10']
at1, ft1, ne1, tot1, pct1 = calc_kpis(rows_fec_esp)
print(f"\nCASE 1: FECHA ENTREGA ESPERADA in 2026-10 (Cumplimiento Tab):")
print(f"  Total: {tot1}, AT: {at1}, FT: {ft1}, NE: {ne1}")
print(f"  % AT: {pct1:.1f}%")

# Case 2: FECHA DE EMISION NECESIDAD in 2026-10
rows_fec_emision = [r for r in rows_223 if parse_date(r.get('FECHA DE EMISION NECESIDAD', '')) == '2026-10']
at2, ft2, ne2, tot2, pct2 = calc_kpis(rows_fec_emision)
print(f"\nCASE 2: FECHA DE EMISION NECESIDAD in 2026-10 (Resumen Tab previously):")
print(f"  Total: {tot2}, AT: {at2}, FT: {ft2}, NE: {ne2}")
print(f"  % AT: {pct2:.1f}%")
