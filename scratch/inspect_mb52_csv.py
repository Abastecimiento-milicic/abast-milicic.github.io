import sys
sys.stdout.reconfigure(encoding='utf-8')

# First check CSV
csv_path = "data/Almacen MB52/Combinados/MB52_CONSOLIDADO_COMBINADO.csv"
import csv

with open(csv_path, 'r', encoding='latin1', errors='ignore') as f:
    reader = csv.reader(f, delimiter=';')
    headers = next(reader)
    print("CSV Headers:", headers)
    for row in reader:
        if '1001789' in row:
            print("Found 1001789 in CSV:")
            for h, v in zip(headers, row):
                print(f"  {h}: {v}")
            break
