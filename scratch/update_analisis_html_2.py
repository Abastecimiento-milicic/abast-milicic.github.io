# -*- coding: utf-8 -*-
with open('analisis-mm.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('js/cache-utils.js?v=20261030_132500', 'js/cache-utils.js?v=20261030_133200')

with open('analisis-mm.html', 'w', encoding='utf-8', newline='') as f:
    f.write(text)

print("Updated cache-buster in analisis-mm.html to 133200.")
