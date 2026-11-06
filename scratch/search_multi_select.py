import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'function\s+syncAllStMultiSelects[^{]*\{[^}]*\}', text)
print("syncAllStMultiSelects in index.html:", matches)

# Also search across js/*.js
import glob
for js_path in glob.glob("js/*.js"):
    with open(js_path, 'r', encoding='utf-8', errors='ignore') as f:
        t = f.read()
        if 'syncAllStMultiSelects' in t or 'convertSelectToPills' in t or 'pills' in t:
            print(f"Found in {js_path}")
