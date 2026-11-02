# -*- coding: utf-8 -*-
with open('scratch/panel_resumen_dump.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(200, min(290, len(lines))):
    print(f"{i+1}: {lines[i].encode('ascii', 'replace').decode('ascii')}", end='')
