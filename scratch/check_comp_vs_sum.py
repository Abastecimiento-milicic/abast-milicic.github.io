import sys, csv
sys.stdout.reconfigure(encoding='utf-8')

with open("data/CUMPLIMIENTO_OPTIMIZADO.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=';')
    diff_count = 0
    total_rows = 0
    for r in reader:
        total_rows += 1
        comp = float(r.get('COMPROMETIDOS', 0) or 0)
        at = float(r.get('ENTREGADOS AT', 0) or 0)
        ft = float(r.get('ENTREGADOS FT', 0) or 0)
        ne = float(r.get('NO ENTREGADOS', 0) or 0)
        if comp != (at + ft + ne):
            diff_count += 1

print(f"Total rows: {total_rows}. Rows where COMPROMETIDOS != (AT+FT+NE): {diff_count}")
