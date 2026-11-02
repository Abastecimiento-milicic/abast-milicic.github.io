# -*- coding: utf-8 -*-
with open('analisis-mm.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<script src="[^"]+"', text)
for m in matches:
    print(m)
