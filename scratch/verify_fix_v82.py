import sys, csv, re
sys.stdout.reconfigure(encoding='utf-8')

# Run check_balance
for f in ['js/resumen.js', 'js/demoras.js', 'js/last-update.js']:
    with open(f, 'r', encoding='utf-8') as fh:
        c = fh.read()
    counts = {ch: c.count(ch) for ch in '{}()[]'}
    assert counts['{'] == counts['}'], f"Braces mismatch in {f}"
    assert counts['('] == counts[')'], f"Parentheses mismatch in {f}"
    assert counts['['] == counts[']'], f"Brackets mismatch in {f}"

print("Brackets balanced!")

with open("js/resumen.js", "r", encoding="utf-8") as f:
    res = f.read()

assert 'cumplHeaders.find(h => /entrega\\s+esperada/i.test(h))' in res
assert '2026-10' in res

print("Verification passed successfully!")
