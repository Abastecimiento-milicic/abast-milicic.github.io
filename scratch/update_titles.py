# -*- coding: utf-8 -*-

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove Pantallazo Ejecutivo and change Obra visualizada to OBRA: Todas las Obras
old_top_bar_left = """          <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
            <span style="background: #e0f2fe; color: #0369a1; font-size: 9px; font-weight: 800; padding: 1px 6px; border-radius: 4px; text-transform: uppercase;">Pantallazo Ejecutivo</span>
            <div style="font-size: 12px; font-weight: 800; color: #0f172a;">
              Obra visualizada: <span id="resumen_lblObra" style="color: #2563eb;">Todas las Obras (Consolidado General)</span>
            </div>
          </div>"""

new_top_bar_left = """          <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
            <div style="font-size: 13px; font-weight: 800; color: #0f172a;">
              OBRA: <span id="resumen_lblObra" style="color: #2563eb;">Todas las Obras</span>
            </div>
          </div>"""

if old_top_bar_left in html:
    html = html.replace(old_top_bar_left, new_top_bar_left)
else:
    # Try normalized
    norm_html = html.replace('\r\n', '\n')
    norm_old = old_top_bar_left.replace('\r\n', '\n')
    norm_new = new_top_bar_left.replace('\r\n', '\n')
    if norm_old in norm_html:
        html = norm_html.replace(norm_old, norm_new)

# Dropdown default option
html = html.replace('<option value="__ALL__">Todas las Obras (Consolidado)</option>',
                    '<option value="__ALL__">Todas las Obras</option>')

# Enlarge titles of Bloque 1 and Bloque 2
html = html.replace(
    'padding: 6px 14px !important; min-height: 32px !important; font-size: 12px !important;',
    'padding: 8px 16px !important; min-height: 36px !important; font-size: 14px !important; font-weight: 800 !important;'
)

# Subcolumn titles font-size 11px -> 12px
html = html.replace(
    'font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; color: #475569; margin-bottom: 12px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px;',
    'font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; color: #334155; margin-bottom: 10px; border-bottom: 1px solid #e2e8f0; padding-bottom: 5px;'
)

# Cache-buster
html = html.replace('js/resumen.js?v=20261030_130600', 'js/resumen.js?v=20261030_131000')

with open('index.html', 'w', encoding='utf-8', newline='') as f:
    f.write(html)
print("SUCCESS: index.html updated with enlarged titles and clean OBRA label.")

# 2. Update js/resumen.js
with open('js/resumen.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace('<option value="__ALL__">Todas las Obras (Consolidado)</option>',
                '<option value="__ALL__">Todas las Obras</option>')
js = js.replace('"Todas las Obras (Consolidado General)"',
                '"Todas las Obras"')

with open('js/resumen.js', 'w', encoding='utf-8', newline='') as f:
    f.write(js)
print("SUCCESS: js/resumen.js updated with 'Todas las Obras'.")
