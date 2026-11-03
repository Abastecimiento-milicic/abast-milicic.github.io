import sys, csv
sys.stdout.reconfigure(encoding='utf-8')

for name in ['data/Stock Base Obra 0374.csv', 'data/Stock Base Obra 0378.csv']:
    try:
        with open(name, 'r', encoding='utf-8-sig', errors='ignore') as f:
            reader = csv.reader(f, delimiter=';')
            headers = next(reader)
            print(f"Headers in {name}:")
            for i, h in enumerate(headers):
                print(f"  [{i}] {h!r}")
            # print first 3 rows
            for _ in range(3):
                row = next(reader, None)
                if row: print("   Row:", row[:8])
    except Exception as e:
        print(f"Error {name}: {e}")
