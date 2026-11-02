# -*- coding: utf-8 -*-

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Top bar OBRA label size
html = html.replace(
    '<div style="font-size: 13px; font-weight: 800; color: #0f172a;">\n              OBRA: <span id="resumen_lblObra" style="color: #2563eb;">Todas las Obras</span>\n            </div>',
    '<div style="font-size: 16px; font-weight: 800; color: #0f172a;">\n              OBRA: <span id="resumen_lblObra" style="color: #2563eb;">Todas las Obras</span>\n            </div>'
)

# Top bar select
html = html.replace(
    '<label for="resumen_obraSelect" style="font-size: 11px; font-weight: 700; color: #334155; white-space: nowrap;">',
    '<label for="resumen_obraSelect" style="font-size: 13px; font-weight: 700; color: #334155; white-space: nowrap;">'
)
html = html.replace(
    '<select id="resumen_obraSelect" style="min-width: 220px; height: 24px !important; min-height: 24px !important; max-height: 24px !important; padding: 0 6px !important; font-size: 11px !important; font-weight: 600; border: 1px solid #94a3b8; border-radius: 4px; background: #ffffff; cursor: pointer;">',
    '<select id="resumen_obraSelect" style="min-width: 260px; height: 30px !important; min-height: 30px !important; max-height: 30px !important; padding: 0 8px !important; font-size: 13px !important; font-weight: 700; border: 1px solid #94a3b8; border-radius: 5px; background: #ffffff; cursor: pointer;">'
)

# Bloque 1 and Bloque 2 panel-title: 14px -> 16px
html = html.replace(
    'padding: 8px 16px !important; min-height: 36px !important; font-size: 14px !important; font-weight: 800 !important;',
    'padding: 10px 18px !important; min-height: 42px !important; font-size: 16px !important; font-weight: 800 !important;'
)

# Month select in Bloque 2
html = html.replace(
    '<label for="resumen_mesCumplSelect" style="font-size: 11px; font-weight: 700; color: #334155; white-space: nowrap;">',
    '<label for="resumen_mesCumplSelect" style="font-size: 13px; font-weight: 700; color: #334155; white-space: nowrap;">'
)
html = html.replace(
    '<select id="resumen_mesCumplSelect" style="min-width: 150px; height: 24px !important; min-height: 24px !important; max-height: 24px !important; padding: 0 6px !important; font-size: 11px !important; font-weight: 600; border: 1px solid #94a3b8; border-radius: 4px; background: #ffffff; cursor: pointer;">',
    '<select id="resumen_mesCumplSelect" style="min-width: 170px; height: 30px !important; min-height: 30px !important; max-height: 30px !important; padding: 0 8px !important; font-size: 13px !important; font-weight: 700; border: 1px solid #94a3b8; border-radius: 5px; background: #ffffff; cursor: pointer;">'
)

# Subcolumn box titles: 12px -> 13.5px
html = html.replace(
    'font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; color: #334155; margin-bottom: 10px; border-bottom: 1px solid #e2e8f0; padding-bottom: 5px;',
    'font-size: 13.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; color: #1e293b; margin-bottom: 12px; border-bottom: 1.5px solid #e2e8f0; padding-bottom: 6px;'
)

# List items <li> in panel-resumen: font-size 13px -> 15px
# We can do this cleanly in panel-resumen section
start_res = html.find('id="panel-resumen"')
end_res = html.find('</section>\n\n  </main>', start_res)
if end_res == -1: end_res = html.find('</main>', start_res)

res_chunk = html[start_res:end_res]

# Replace li styling
res_chunk = res_chunk.replace(
    'font-size: 13px; color: #1e293b;',
    'font-size: 15px; color: #1e293b;'
)

# Replace icon size
res_chunk = res_chunk.replace(
    'font-size: 15px; margin-right: 8px;',
    'font-size: 18px; margin-right: 10px;'
)

# Replace value font-size 15px -> 18px
res_chunk = res_chunk.replace('font-size: 15px; font-weight: 800;', 'font-size: 18px; font-weight: 800;')
res_chunk = res_chunk.replace('margin: 0 6px;', 'margin: 0 8px;')

# Replace description font-size 11px -> 13px
res_chunk = res_chunk.replace('font-size: 11px;', 'font-size: 13px;')
res_chunk = res_chunk.replace('font-size: 10px;', 'font-size: 12px;')

html = html[:start_res] + res_chunk + html[end_res:]

# Cache buster
html = html.replace('js/resumen.js?v=20261030_131000', 'js/resumen.js?v=20261030_133000')

with open('index.html', 'w', encoding='utf-8', newline='') as f:
    f.write(html)
print("SUCCESS: index.html updated with enlarged typography.")

# 2. Update js/resumen.js
with open('js/resumen.js', 'r', encoding='utf-8') as f:
    js = f.read()

# In txtNuloHTML: font-size 15px -> 18px, subtext 11px -> 13px
js = js.replace(
    '<span style="font-size: 15px; font-weight: 800; color: #dc2626; margin: 0 6px;">',
    '<span style="font-size: 18px; font-weight: 800; color: #dc2626; margin: 0 8px;">'
)
js = js.replace(
    '<span style="color: #475569; font-size: 11px;">',
    '<span style="color: #475569; font-size: 13px;">'
)
js = js.replace(
    'padding: 1px 6px;',
    'padding: 2px 8px; font-size: 13px;'
)

with open('js/resumen.js', 'w', encoding='utf-8', newline='') as f:
    f.write(js)
print("SUCCESS: js/resumen.js updated with enlarged text sizes.")
