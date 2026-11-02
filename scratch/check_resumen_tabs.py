import re

with open('index.html', encoding='utf-8') as f:
    html = f.read()

matches = re.findall(r'<[^>]*switchTab\([\'"]resumen[\'"][^>]*>', html)
print('Matches:', matches)
