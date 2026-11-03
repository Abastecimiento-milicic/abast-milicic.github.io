import sys, glob, re
sys.stdout.reconfigure(encoding='utf-8')

for f in glob.glob('js/*.js'):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        text = fh.read()
    # Find all places that construct options with "Almacen" or "Almacén"
    matches = re.findall(r'.{0,40}(?:Almac[eé]n\s*\d+|Obra\s*\/\s*Almac[eé]n\s*\d+).{0,40}', text, re.IGNORECASE)
    if matches:
        print(f"=== {f} ===")
        for m in matches:
            print("  ", m.strip())
