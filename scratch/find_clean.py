# -*- coding: utf-8 -*-
with open('js/analisis-mm.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function clean(')
if idx == -1:
    idx = text.find('clean =')
print(text[idx:idx+300])
