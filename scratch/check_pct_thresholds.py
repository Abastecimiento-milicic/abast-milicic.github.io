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

# Check all clients and their LTM and monthly percentages!
clients = sorted(list(set(r.get('CLIENTE', '') for r in rows if r.get('CLIENTE', ''))))
for cli in clients:
    sub_all = [r for r in rows if r.get('CLIENTE', '') == cli]
    months = sorted(list(set(r['_ym'] for r in sub_all if r['_ym'])))
    
    # In cumplimiento.js: uniqueMonths.pop(), then slice(-12)
    m_cumpl_ltm = months[:-1][-12:] if len(months) > 1 else months
    sub_cumpl_ltm = [r for r in sub_all if r['_ym'] in m_cumpl_ltm]
    at_c = sum(float(r.get('ENTREGADOS AT', 0) or 0) for r in sub_cumpl_ltm)
    tot_c = sum(float(r.get('COMPROMETIDOS', 0) or 0) for r in sub_cumpl_ltm)
    pct_c = (at_c / tot_c) if tot_c else 0
    
    # Check if any month or LTM has pct between 0.775 and 0.785, or >= 0.78
    print(f"Client: {cli:35} | Cumpl LTM: {pct_c*100:.2f}% (is >=0.78? {pct_c >= 0.78})")
    for m in months[-4:]:
        sub_m = [r for r in sub_all if r['_ym'] == m]
        at_m = sum(float(r.get('ENTREGADOS AT', 0) or 0) for r in sub_m)
        tot_m = sum(float(r.get('COMPROMETIDOS', 0) or 0) for r in sub_m)
        pct_m = (at_m / tot_m) if tot_m else 0
        if 0.77 <= pct_m <= 0.80 or pct_m >= 0.78:
            print(f"   Month {m}: {pct_m*100:.4f}% (display: {pct_m*100:.1f}%, >=0.78: {pct_m >= 0.78})")
