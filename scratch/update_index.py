import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

target1 = """        <div class="st-filters-stack">
          <div class="filter">
            <label>Cliente / Obra:</label>
            <select id="resumen_obraSelect" class="st-select" style="width: 100%; height: 38px; padding: 6px 10px; font-size: 0.88rem; font-weight: 600; border: 1px solid #cbd5e1; border-radius: 6px; background-color: #ffffff; cursor: pointer;">
              <option value="__ALL__">Todas las Obras</option>
            </select>
            <div class="hint">Filtrar métricas por obra o almacén</div>
          </div>

          <div class="filter">
            <label>Mes Evaluado:</label>
            <select id="resumen_mesCumplSelect" class="st-select" style="width: 100%; height: 38px; padding: 6px 10px; font-size: 0.88rem; font-weight: 600; border: 1px solid #cbd5e1; border-radius: 6px; background-color: #ffffff; cursor: pointer;">
              <option value="2026-09">Septiembre 2026</option>
            </select>
            <div class="hint">Período para rendimiento mensual</div>
          </div>
        </div>"""

replacement1 = """        <div class="st-filters-stack">
          <div class="filter">
            <label>Cliente / Obra:</label>
            <select id="resumen_obraSelect" multiple size="6" class="multi-select">
              <option value="__ALL__">Todas las Obras</option>
            </select>
            <div class="hint">Filtrar métricas por obra o almacén</div>
          </div>

          <div class="filter">
            <label>Mes Evaluado:</label>
            <select id="resumen_mesCumplSelect" multiple size="6" class="multi-select">
              <option value="__ALL__">Todos los Meses</option>
            </select>
            <div class="hint">Período para rendimiento mensual</div>
          </div>
        </div>"""

target_crlf = target1.replace("\r\n", "\n").replace("\n", "\r\n")
target_lf = target1.replace("\r\n", "\n")

if target_crlf in content:
    content = content.replace(target_crlf, replacement1.replace("\r\n", "\n").replace("\n", "\r\n"), 1)
    print("Replaced target1 with CRLF")
elif target_lf in content:
    content = content.replace(target_lf, replacement1.replace("\r\n", "\n"), 1)
    print("Replaced target1 with LF")
else:
    print("target1 NOT FOUND!")

# Update isAllOption
old_is_all = "return val === '' || val === '__ALL__' || txt === 'todos' || txt === 'todas';"
new_is_all = "return val === '' || val === '__ALL__' || txt.startsWith('todo') || txt.startsWith('toda');"
if old_is_all in content:
    content = content.replace(old_is_all, new_is_all, 1)
    print("Replaced isAllOption")
else:
    print("old_is_all not found")

# Update placeholder
old_ph = "ph.textContent = 'Todos';"
new_ph = "ph.textContent = allOpt ? (allOpt.textContent || 'Todos') : 'Todos';"
if old_ph in content:
    content = content.replace(old_ph, new_ph, 1)
    print("Replaced placeholder")
else:
    print("old_ph not found")

# Update tab switch
old_tab_res = """        if (tabName === 'resumen') {
          if (typeof window.initResumen === 'function') {
            window.initResumen();
          }"""

new_tab_res = """        if (tabName === 'resumen') {
          if (typeof window.initResumen === 'function') {
            window.initResumen();
          }
          if (typeof window.syncAllStMultiSelects === 'function') {
            window.syncAllStMultiSelects();
          }"""

if old_tab_res.replace("\r\n", "\n").replace("\n", "\r\n") in content:
    content = content.replace(old_tab_res.replace("\r\n", "\n").replace("\n", "\r\n"), new_tab_res.replace("\r\n", "\n").replace("\n", "\r\n"), 1)
    print("Updated tab switch (CRLF)")
elif old_tab_res.replace("\r\n", "\n") in content:
    content = content.replace(old_tab_res.replace("\r\n", "\n"), new_tab_res.replace("\r\n", "\n"), 1)
    print("Updated tab switch (LF)")
else:
    print("old_tab_res not found")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Done updating index.html")
