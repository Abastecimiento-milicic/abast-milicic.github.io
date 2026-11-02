with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = '<button class="tab" data-tab="resumen" onclick="window.switchTab(\'resumen\')">RESUMEN</button>'
repl = '<button class="tab" data-tab="resumen" onclick="window.switchTab(\'resumen\')" style="display: none;">RESUMEN</button>'

assert target in html, "Target button not found in index.html"
html = html.replace(target, repl, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully hid the Resumen tab button!")
