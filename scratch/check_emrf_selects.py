import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("js/control-emrf.js", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'(\w+Select)', text)
print("Selects in control-emrf.js:", set(matches))
