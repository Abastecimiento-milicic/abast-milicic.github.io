import sys, glob, csv, re
sys.stdout.reconfigure(encoding='utf-8')

print("Searching for 1500 in CSV files...")
for f in glob.glob('data/*.csv'):
    try:
        with open(f, 'r', encoding='utf-8-sig', errors='ignore') as fh:
            reader = csv.reader(fh, delimiter=';')
            headers = next(reader, [])
            for row_idx, row in enumerate(reader):
                for col_idx, val in enumerate(row):
                    if val.strip() in ('1', '0001', '1500', '01', '001') or '1500' in val:
                        col_name = headers[col_idx] if col_idx < len(headers) else f"col_{col_idx}"
                        if any(k in col_name.lower() for k in ['alm', 'centr', 'cli', 'obra', 'dest']):
                            print(f"  {f} row {row_idx}: {col_name} = {val!r}")
                            break
    except Exception as e:
        print(f"  Error reading {f}: {e}")

print("\nSearching in JS files for '1500' or 'Almacen 1'...")
for f in glob.glob('js/*.js'):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        text = fh.read()
    if '1500' in text:
        print(f"  Found '1500' in {f}")
    if 'Almacen 1' in text or 'Almacén 1' in text:
        print(f"  Found 'Almacen 1' in {f}")
