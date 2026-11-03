import sys, csv, re
sys.stdout.reconfigure(encoding='utf-8')

def clean(v):
    return str(v or '').strip()

def extract_code(val):
    s = clean(val)
    m = re.search(r'\d+', s)
    return str(int(m.group(0))) if m else s

def get_canonical_obra(val):
    c = extract_code(val)
    if c in ("26", "314", "26_314", "00026", "00314"):
        return "26_314"
    if c in ("35", "341", "35_341", "00035", "00341"):
        return "35_341"
    return c

with open('data/CUMPLIMIENTO_OPTIMIZADO.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    count_26_314 = 0
    count_35_341 = 0
    for r in reader:
        c = get_canonical_obra(r.get('CLIENTE', ''))
        if c == '26_314': count_26_314 += 1
        if c == '35_341': count_35_341 += 1
    print(f"Demoras / Cumpl Rows for 26_314: {count_26_314}")
    print(f"Demoras / Cumpl Rows for 35_341: {count_35_341}")
