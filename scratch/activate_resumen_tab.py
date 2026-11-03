with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = '<button class="tab" data-tab="resumen" onclick="window.switchTab(\'resumen\')" style="display: none;">RESUMEN</button>'
repl = '<button class="tab" data-tab="resumen" onclick="window.switchTab(\'resumen\')">RESUMEN</button>'

assert target in html, "Target not found"
html = html.replace(target, repl, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Activated Resumen tab button in index.html successfully!")
