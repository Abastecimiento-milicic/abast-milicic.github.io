import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("js/resumen.js", "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find('hasSelection')
print(repr(code[idx-10:idx+350]))
