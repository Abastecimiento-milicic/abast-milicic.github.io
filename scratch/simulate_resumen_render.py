import sys, csv, re
sys.stdout.reconfigure(encoding='utf-8')

def clean(v):
    return str(v or '').strip()

def extract_code(val):
    s = clean(val)
    m = re.search(r'\d+', s)
    return str(int(m.group(0))) if m else s

def get_canonical_obra_code(val):
    if not val: return ""
    c = extract_code(val)
    if c in ("26", "314", "26_314", "00026", "00314", "0026", "0314"): return "26_314"
    if c in ("35", "341", "35_341", "00035", "00341", "0035", "0341"): return "35_341"
    return c

# 1. Load ANALISIS-MM.csv exactly as PapaParse or parseCSV does
with open("data/ANALISIS-MM.csv", "r", encoding="utf-8-sig") as f:
    text = f.read()

lines = [l.strip() for l in text.splitlines() if l.strip()]
mm_headers = [clean(h) for h in lines[0].split(";")]
mm_raw_data = []
for l in lines[1:]:
    parts = l.split(";")
    row = {mm_headers[i]: clean(parts[i]) if i < len(parts) else "" for i in range(len(mm_headers))}
    mm_raw_data.append(row)

# 2. Load CUMPLIMIENTO_OPTIMIZADO.csv
with open("data/CUMPLIMIENTO_OPTIMIZADO.csv", "r", encoding="utf-8-sig") as f:
    text = f.read()

lines = [l.strip() for l in text.splitlines() if l.strip()]
cumpl_headers = [clean(h) for h in lines[0].split(";")]
cumpl_raw_data = []
for l in lines[1:]:
    parts = l.split(";")
    row = {cumpl_headers[i]: clean(parts[i]) if i < len(parts) else "" for i in range(len(cumpl_headers))}
    cumpl_raw_data.append(row)

# 3. Exactly what renderObrasSelect() does:
codes = set()
col_alm = None
for h in mm_headers:
    if re.search(r'almac[eé]n', h, re.IGNORECASE):
        col_alm = h
        break
if not col_alm: col_alm = "Almacén"
print(f"col_alm detected: {col_alm!r}")

for r in mm_raw_data:
    c = get_canonical_obra_code(r[col_alm])
    if c and c != "0":
        codes.add(c)

for r in cumpl_raw_data:
    c = get_canonical_obra_code(r.get("CLIENTE", ""))
    if c and c != "0":
        codes.add(c)

def get_num(s):
    m = re.search(r'\d+', s)
    return int(m.group(0)) if m else 99999

sorted_codes = sorted(list(codes), key=get_num)
print(f"\nFinal sortedCodes in renderObrasSelect():")
OBRA_MAP = {
    "26_314": "00026 / 00314 - CASA OLAVARRIA",
    "35_341": "00035 / 00341 - MOV SUELOS SAN LUIS",
    "223": "00223 - COMP AMB SANTA FE",
    "365": "00365 - RIO TINTO",
    "368": "00368 - ACUEDUCTO TBH",
    "372": "00372 - UTE POSCO II",
    "374": "00374 - TERMINAL PUNTA COLORADA",
    "375": "00375 - OLEODUCTO PR-LP",
    "376": "00376 - VELADERO FASE 8B",
    "377": "00377 - YPF 3ER LOOP",
    "378": "00378 - OLEODUCTO PRINGLES",
    "379": "00379 - VELADERO FASE 8C"
}
for code in sorted_codes:
    label = OBRA_MAP.get(code, f"Obra / Almacén {code}")
    print(f"  value={code:10} label={label}")
