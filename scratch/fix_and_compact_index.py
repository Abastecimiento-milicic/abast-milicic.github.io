# -*- coding: utf-8 -*-

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Check if alternating empty lines
if len(lines) > 3000 and sum(1 for i in range(1, min(100, len(lines)), 2) if lines[i].strip() == '') > 40:
    lines = [lines[i] for i in range(0, len(lines), 2)]
    print(f"Compressed lines from double to {len(lines)}")

text = "".join(lines)

# Now apply compacting to panel-resumen
# 1. Top bar select and container
text = text.replace(
    '<select id="resumen_obraSelect" class="multi-select" style="min-width: 220px; height: 24px; padding: 0 6px; font-size: 11px; font-weight: 600; border: 1px solid #94a3b8; border-radius: 4px; background: #ffffff;">',
    '<select id="resumen_obraSelect" style="min-width: 220px; height: 24px !important; min-height: 24px !important; max-height: 24px !important; padding: 0 6px !important; font-size: 11px !important; font-weight: 600; border: 1px solid #94a3b8; border-radius: 4px; background: #ffffff; cursor: pointer;">'
)

# 2. Bloque 1 panel title and panel body
text = text.replace(
    '<section class="panel" style="margin-bottom: 20px;">\n        <div class="panel-title" style="display: flex; align-items: center; justify-content: space-between;">',
    '<section class="panel" style="margin-bottom: 10px;">\n        <div class="panel-title" style="display: flex; align-items: center; justify-content: space-between; padding: 6px 14px !important; min-height: 32px !important; font-size: 12px !important;">'
)
text = text.replace(
    '<div class="panel-body" style="padding: 16px 20px;">\n          <!-- Contenedor Flex de 2 Columnas -->',
    '<div class="panel-body" style="padding: 10px 14px !important;">\n          <!-- Contenedor Flex de 2 Columnas -->'
)

# 3. Bloque 2 panel title, select and panel body
text = text.replace(
    '<section class="panel" style="margin-bottom: 20px;">\n        <div class="panel-title" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">',
    '<section class="panel" style="margin-bottom: 10px;">\n        <div class="panel-title" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 6px; padding: 6px 14px !important; min-height: 32px !important; font-size: 12px !important;">'
)
text = text.replace(
    '<select id="resumen_mesCumplSelect" class="multi-select" style="min-width: 150px; height: 24px; padding: 0 6px; font-size: 11px; font-weight: 600; border: 1px solid #94a3b8; border-radius: 4px; background: #ffffff;">',
    '<select id="resumen_mesCumplSelect" style="min-width: 150px; height: 24px !important; min-height: 24px !important; max-height: 24px !important; padding: 0 6px !important; font-size: 11px !important; font-weight: 600; border: 1px solid #94a3b8; border-radius: 4px; background: #ffffff; cursor: pointer;">'
)
text = text.replace(
    '<div class="panel-body" style="padding: 16px 20px;">\n          <!-- Contenedor Flex de 2 Columnas: Acumulado 12 Meses vs Mensual -->',
    '<div class="panel-body" style="padding: 10px 14px !important;">\n          <!-- Contenedor Flex de 2 Columnas: Acumulado 12 Meses vs Mensual -->'
)

# Also check CRLF variants if needed
text = text.replace(
    '<section class="panel" style="margin-bottom: 20px;">\r\n        <div class="panel-title" style="display: flex; align-items: center; justify-content: space-between;">',
    '<section class="panel" style="margin-bottom: 10px;">\r\n        <div class="panel-title" style="display: flex; align-items: center; justify-content: space-between; padding: 6px 14px !important; min-height: 32px !important; font-size: 12px !important;">'
)
text = text.replace(
    '<div class="panel-body" style="padding: 16px 20px;">\r\n          <!-- Contenedor Flex de 2 Columnas -->',
    '<div class="panel-body" style="padding: 10px 14px !important;">\r\n          <!-- Contenedor Flex de 2 Columnas -->'
)
text = text.replace(
    '<section class="panel" style="margin-bottom: 20px;">\r\n        <div class="panel-title" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">',
    '<section class="panel" style="margin-bottom: 10px;">\r\n        <div class="panel-title" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 6px; padding: 6px 14px !important; min-height: 32px !important; font-size: 12px !important;">'
)
text = text.replace(
    '<div class="panel-body" style="padding: 16px 20px;">\r\n          <!-- Contenedor Flex de 2 Columnas: Acumulado 12 Meses vs Mensual -->',
    '<div class="panel-body" style="padding: 10px 14px !important;">\r\n          <!-- Contenedor Flex de 2 Columnas: Acumulado 12 Meses vs Mensual -->'
)

# Cache buster
text = text.replace('js/resumen.js?v=20261030_130200', 'js/resumen.js?v=20261030_130600')

with open('index.html', 'w', encoding='utf-8', newline='') as f:
    f.write(text)

print("SUCCESS: index.html updated and compacted cleanly.")
