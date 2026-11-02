# -*- coding: utf-8 -*-
with open('js/cache-utils.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.lower().find('saveasexcel')
if idx != -1:
    print(text[idx+5500:idx+8000].encode('ascii', 'replace').decode('ascii'))
