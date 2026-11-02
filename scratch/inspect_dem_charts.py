import re

with open('index.html', encoding='utf-8') as f:
    html = f.read()

for m in re.finditer(r'<div id="(dem_chart[^"]*)"([^>]*)>', html):
    print(m.group(1), m.group(2))
