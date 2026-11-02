# -*- coding: utf-8 -*-
with open('js/cumplimiento.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('name: "No entregados"')
if idx != -1:
    print(text[idx:idx+400])
