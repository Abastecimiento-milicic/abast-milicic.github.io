import sys, glob, csv, re
sys.stdout.reconfigure(encoding='utf-8')

for f in glob.glob('data/*.csv'):
    with open(f, 'r', encoding='utf-8-sig', errors='ignore') as fh:
        reader = csv.reader(fh, delimiter=';')
        headers = next(reader, [])
        for row_idx, row in enumerate(reader):
            for col_idx, cell in enumerate(row):
                c = cell.strip()
                if c in ('1', '01', '001', '0001', '1500', '01500', 'Almacen 1', 'Almacén 1', 'Almacen 1500', 'Almacén 1500') or '1500' in c:
                    col_name = headers[col_idx] if col_idx < len(headers) else f"col_{col_idx}"
                    # Print anything where cell is 1 or 1500 or contains 1500
                    if any(term in col_name.lower() for term in ['alm', 'centr', 'cli', 'obra', 'ubic', 'dest', 'ped', 'soc']):
                        print(f"{f} [Row {row_idx}] Col: '{col_name}' -> Cell: '{cell}'")
