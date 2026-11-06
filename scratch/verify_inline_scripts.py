import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check script tags in index.html
import re
scripts = re.findall(r'<script\b[^>]*>([\s\S]*?)</script>', html)
print(f"Total inline scripts in index.html: {len(scripts)}")

for i, s in enumerate(scripts):
    counts = {ch: s.count(ch) for ch in '{}()[]'}
    ok = (counts['{'] == counts['}'] and counts['('] == counts[')'] and counts['['] == counts[']'])
    if not ok:
        print(f"Script {i+1} has unbalanced brackets:")
        print('  {}:', counts['{'] == counts['}'], str(counts['{']) + ' vs ' + str(counts['}']))
        print('  ():', counts['('] == counts[')'], str(counts['(']) + ' vs ' + str(counts[')']))
        print('  []:', counts['['] == counts[']'], str(counts['[']) + ' vs ' + str(counts[']']))
    else:
        print(f"Script {i+1} balance OK")

print("Verification complete.")
