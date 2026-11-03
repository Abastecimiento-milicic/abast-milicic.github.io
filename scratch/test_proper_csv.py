import sys, csv, re
sys.stdout.reconfigure(encoding='utf-8')

def clean(v): return str(v or '').strip()
def extract_code(val):
    s = clean(val)
    m = re.search(r'\d+', s)
    return str(int(m.group(0))) if m else s

with open("data/ANALISIS-MM.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=';')
    alm_col = "Almacén"
    codes = set()
    for row in reader:
        v = row.get(alm_col, '')
        c = extract_code(v)
        codes.add((c, v))

print("Unique (code, raw_val) in Almacén with proper CSV reader:")
for c, v in sorted(codes):
    print(f"  Code: {c:10} Raw: {v!r}")
