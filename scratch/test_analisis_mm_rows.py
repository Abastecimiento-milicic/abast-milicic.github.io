# -*- coding: utf-8 -*-
import csv

with open('data/ANALISIS-MM.csv', 'r', encoding='utf-8') as f:
    r = csv.reader(f, delimiter=';')
    headers = next(r)
    rows = list(r)

print("Headers count:", len(headers))
print("Headers:", headers)
print("Rows count:", len(rows))

# Check for rows with different length
diff_len = [i for i, row in enumerate(rows) if len(row) != len(headers)]
print("Rows with different length:", len(diff_len))
if diff_len:
    print("First 5 diff len rows:", [(i, len(rows[i])) for i in diff_len[:5]])

# Check for any values with special chars or problems
problem_vals = []
for i, row in enumerate(rows):
    for j, val in enumerate(row):
        h = headers[j] if j < len(headers) else f"Col{j}"
        v = val.strip()
        # check what Number(v) would do in JS
        raw_val = v
        # /^\d{1,3}(\.\d{3})+$/
        # in JS, what if raw_val has commas?
        if ',' in v:
            # what does JS do with "12,50"?
            # in JS: Number("12,50") is NaN!
            pass
        if v.upper() in ('INFINITY', '-INFINITY', 'NAN'):
            problem_vals.append((i, h, v))

print("Problem vals:", problem_vals)
