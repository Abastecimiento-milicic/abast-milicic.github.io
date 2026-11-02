# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('wasCollapsed = body.classList.contains')
print(text[idx:idx+1500].encode('ascii', 'replace').decode('ascii'))
