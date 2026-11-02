# -*- coding: utf-8 -*-
with open('js/cache-utils.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Check for duplicate const/let in saveAsExcel
idx = text.find('window.saveAsExcel')
body = text[idx:]

# Simple scope check or parse
print("Checking js/cache-utils.js...")
import re

# Look for 'const ' and 'let '
tokens = re.findall(r'(?:const|let)\s+([a-zA-Z0-9_$]+)', text)
print(f"Total declared vars: {len(tokens)}")

# Check duplicate const hName
assert text.count('const hName') == 1, f"Expected 1 const hName, found {text.count('const hName')}"
print("ASSERTION PASSED: const hName is unique!")
