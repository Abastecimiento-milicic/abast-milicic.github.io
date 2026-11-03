import sys, csv, re
sys.stdout.reconfigure(encoding='utf-8')

with open("data/ANALISIS-MM.csv", "r", encoding="utf-8-sig") as f:
    text = f.read()

lines = [l.strip() for l in text.splitlines() if l.strip()]
mm_headers = [h.strip() for h in lines[0].split(";")]
print(f"Total lines in ANALISIS-MM.csv: {len(lines)}")

def clean(v): return str(v or '').strip()
def extract_code(val):
    s = clean(val)
    m = re.search(r'\d+', s)
    return str(int(m.group(0))) if m else s

col_alm = "Almacén"
alm_idx = mm_headers.index(col_alm)
print(f"Almacén is column index: {alm_idx}")

for line_num, l in enumerate(lines[1:], start=2):
    parts = l.split(";")
    if len(parts) > alm_idx:
        raw_val = parts[alm_idx]
        c = extract_code(raw_val)
        if c in ("1", "1500"):
            print(f"MM Line {line_num}: Almacén cell={raw_val!r}, full line length={len(parts)}")
            print(f"  Line snippet: {l[:120]}")
    else:
        print(f"MM Line {line_num}: line has only {len(parts)} parts!")

# Check CUMPLIMIENTO_OPTIMIZADO
with open("data/CUMPLIMIENTO_OPTIMIZADO.csv", "r", encoding="utf-8-sig") as f:
    text = f.read()

lines_c = [l.strip() for l in text.splitlines() if l.strip()]
c_headers = [h.strip() for h in lines_c[0].split(";")]
c_idx = c_headers.index("CLIENTE")

for line_num, l in enumerate(lines_c[1:], start=2):
    parts = l.split(";")
    if len(parts) > c_idx:
        raw_val = parts[c_idx]
        c = extract_code(raw_val)
        if c in ("1", "1500"):
            print(f"CUMPL Line {line_num}: CLIENTE cell={raw_val!r}")
            print(f"  Line snippet: {l[:120]}")
