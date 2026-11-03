import sys, csv, re
sys.stdout.reconfigure(encoding='utf-8')

OBRA_MAP = {
    "26_314": "00026 / 00314 - CASA OLAVARRIA / SANTA FE",
    "35_341": "00035 / 00341 - MOV SUELOS SAN LUIS",
    "26": "00026 / 00314 - CASA OLAVARRIA / SANTA FE",
    "314": "00026 / 00314 - CASA OLAVARRIA / SANTA FE",
    "35": "00035 / 00341 - MOV SUELOS SAN LUIS",
    "341": "00035 / 00341 - MOV SUELOS SAN LUIS",
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

def clean(v):
    return str(v or '').strip()

def extract_code(val):
    s = clean(val)
    m = re.search(r'\d+', s)
    return str(int(m.group(0))) if m else s

def get_canonical_obra_code(code):
    if not code: return ""
    c = extract_code(code)
    if c in ("26", "314", "26_314", "00026", "00314"):
        return "26_314"
    if c in ("35", "341", "35_341", "00035", "00341"):
        return "35_341"
    return c

print("Testing canonical mapping:")
for test_val in ["0026", "0314", "26", "314", "00026 - SANTA FE", "00314 CASA Olavarria", "0035", "0341", "35", "341", "00341 Mov. Suelos San Luis", "00365 Rio Tinto"]:
    canon = get_canonical_obra_code(test_val)
    desc = OBRA_MAP.get(canon, f"Obra {canon}")
    print(f"  {test_val!r:30} -> canon: {canon:8} -> desc: {desc}")

# Check ANALISIS-MM
with open('data/ANALISIS-MM.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    mm_rows_26_314 = 0
    mm_rows_35_341 = 0
    for r in reader:
        c = get_canonical_obra_code(r.get('Almacén', ''))
        if c == '26_314': mm_rows_26_314 += 1
        if c == '35_341': mm_rows_35_341 += 1
    print(f"MM rows: 26_314={mm_rows_26_314}, 35_341={mm_rows_35_341}")

# Check STO NULO
with open('data/STO NULO.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    sto_rows_26_314 = 0
    sto_rows_35_341 = 0
    for r in reader:
        c = get_canonical_obra_code(r.get('Almacén', ''))
        if c == '26_314': sto_rows_26_314 += 1
        if c == '35_341': sto_rows_35_341 += 1
    print(f"STO NULO rows: 26_314={sto_rows_26_314}, 35_341={sto_rows_35_341}")

# Check CUMPLIMIENTO_OPTIMIZADO
with open('data/CUMPLIMIENTO_OPTIMIZADO.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, delimiter=';')
    cumpl_rows_26_314 = 0
    cumpl_rows_35_341 = 0
    for r in reader:
        c = get_canonical_obra_code(r.get('CLIENTE', ''))
        if c == '26_314': cumpl_rows_26_314 += 1
        if c == '35_341': cumpl_rows_35_341 += 1
    print(f"CUMPL rows: 26_314={cumpl_rows_26_314}, 35_341={cumpl_rows_35_341}")
