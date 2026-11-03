import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("js/resumen.js", "r", encoding="utf-8") as f:
    res = f.read()

assert '00026 / 00314 - CASA OLAVARRIA / SANTA FE' not in res, "SANTA FE still present in name!"
assert '"26_314": "00026 / 00314 - CASA OLAVARRIA"' in res, "26_314 label incorrect!"
assert '"26": "00026 / 00314 - CASA OLAVARRIA"' in res, "26 label incorrect!"
assert '"314": "00026 / 00314 - CASA OLAVARRIA"' in res, "314 label incorrect!"

with open("js/last-update.js", "r", encoding="utf-8") as f:
    lu = f.read()

assert '_v80_20261102_155200' in lu, "v80 missing in last-update.js"

with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

assert '20261102_155200' in idx, "v80 missing in index.html"

# Run check_balance
for f in ['js/resumen.js', 'js/demoras.js', 'js/last-update.js']:
    with open(f, 'r', encoding='utf-8') as fh:
        c = fh.read()
    counts = {ch: c.count(ch) for ch in '{}()[]'}
    assert counts['{'] == counts['}'], f"Braces mismatch in {f}"
    assert counts['('] == counts[')'], f"Parentheses mismatch in {f}"
    assert counts['['] == counts[']'], f"Brackets mismatch in {f}"

print("ALL V80 CHECKS PASSED PERFECTLY!")
