import sys, csv, re
sys.stdout.reconfigure(encoding='utf-8')

def clean(v):
    return str(v or '').strip()

def extract_code(val):
    s = clean(val)
    m = re.search(r'\d+', s)
    return str(int(m.group(0))) if m else s

print("--- ANALISIS-MM.csv ---")
with open('data/ANALISIS-MM.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    alm_col = [h for h in reader.fieldnames if 'almac' in h.lower()][0]
    alm_counts = {}
    for r in reader:
        v = r.get(alm_col, '')
        c = extract_code(v)
        alm_counts[c] = alm_counts.get(c, 0) + 1
    for k in sorted(alm_counts.keys()):
        if k in ('1', '1500'):
            print(f"  Found in MM: raw value/code '{k}': {alm_counts[k]} rows")

print("--- STO NULO.csv ---")
with open('data/STO NULO.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    alm_col = [h for h in reader.fieldnames if 'almac' in h.lower()][0]
    alm_counts = {}
    for r in reader:
        v = r.get(alm_col, '')
        c = extract_code(v)
        alm_counts[c] = alm_counts.get(c, 0) + 1
    for k in sorted(alm_counts.keys()):
        if k in ('1', '1500'):
            print(f"  Found in STO NULO: raw value/code '{k}': {alm_counts[k]} rows")

print("--- CUMPLIMIENTO_OPTIMIZADO.csv ---")
with open('data/CUMPLIMIENTO_OPTIMIZADO.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    client_col = [h for h in reader.fieldnames if 'cliente' in h.lower() or 'cli' in h.lower()][0]
    alm_counts = {}
    examples = {}
    for r in reader:
        v = r.get(client_col, '')
        c = extract_code(v)
        alm_counts[c] = alm_counts.get(c, 0) + 1
        if c in ('1', '1500') and c not in examples:
            examples[c] = (v, r)
    for k in sorted(alm_counts.keys()):
        if k in ('1', '1500'):
            print(f"  Found in CUMPLIMIENTO: code '{k}': {alm_counts[k]} rows. Example raw: {examples[k][0]!r}")
            # print some columns of that row
            ex = examples[k][1]
            print(f"    Sample fields: VA={ex.get('DOCUMENTO DE VENTAS','')}, POS={ex.get('POSICION','')}, TEXTO={ex.get('DENOMINACION MATERIAL','')}, PROV={ex.get('NOMBRE 1','')}")
