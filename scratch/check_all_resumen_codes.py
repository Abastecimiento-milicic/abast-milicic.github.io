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

# Check MM
codes_mm = {}
with open('data/ANALISIS-MM.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    alm_col = [h for h in reader.fieldnames if 'almac' in h.lower()][0]
    for r in reader:
        raw = r.get(alm_col, '')
        c = get_canonical_obra_code(raw)
        if c and c != "0":
            codes_mm.setdefault(c, set()).add(raw)

print("Codes from ANALISIS-MM:")
for k, v in sorted(codes_mm.items()):
    print(f"  Code: {k:10} from raw values: {v}")

# Check CUMPLIMIENTO
codes_cumpl = {}
with open('data/CUMPLIMIENTO_OPTIMIZADO.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    client_col = 'CLIENTE'
    for r in reader:
        raw = r.get(client_col, '')
        c = get_canonical_obra_code(raw)
        if c and c != "0":
            codes_cumpl.setdefault(c, set()).add(raw)

print("\nCodes from CUMPLIMIENTO_OPTIMIZADO:")
for k, v in sorted(codes_cumpl.items()):
    if len(v) > 3:
        sample = list(v)[:3]
        print(f"  Code: {k:10} (count={len(v)}) sample raw: {sample}")
    else:
        print(f"  Code: {k:10} from raw values: {v}")
