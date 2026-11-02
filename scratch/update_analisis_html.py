# -*- coding: utf-8 -*-
with open('analisis-mm.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('js/cache-utils.js?v=20261029_125545', 'js/cache-utils.js?v=20261030_132500')
text = text.replace('js/analisis-mm.js?v=20261029_125545', 'js/analisis-mm.js?v=20261030_132500')

with open('analisis-mm.html', 'w', encoding='utf-8', newline='') as f:
    f.write(text)

print("Updated analisis-mm.html cache-busters.")
