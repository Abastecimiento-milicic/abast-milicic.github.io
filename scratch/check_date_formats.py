import sys, csv, re
sys.stdout.reconfigure(encoding='utf-8')

with open("data/CUMPLIMIENTO_OPTIMIZADO.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=';')
    unparsed = []
    formats = set()
    for row_idx, r in enumerate(reader):
        val = r.get('FECHA ENTREGA ESPERADA', '').strip()
        if not val: continue
        m_slash = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{4})', val)
        m_dash = re.match(r'^(\d{4})-(\d{1,2})-(\d{1,2})', val)
        if m_slash:
            formats.add("D/M/YYYY")
        elif m_dash:
            formats.add("YYYY-MM-DD")
        else:
            unparsed.append((row_idx, val))

print(f"Formats found: {formats}")
print(f"Unparsed count: {len(unparsed)}")
if unparsed:
    print(f"Sample unparsed: {unparsed[:5]}")
