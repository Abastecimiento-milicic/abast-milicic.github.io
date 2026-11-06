import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('js/servicios.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = 'window.initServicios = function() {'
replacement = '''window.resetServiciosFilters = function() {
    ["serv_clienteSelect", "serv_clasif2Select", "serv_gcocSelect", "serv_grupoCompraSelect", "serv_estadoItemSelect"].forEach(id => {
      const el = document.getElementById(id) || document.getElementById(id.replace('serv_', ''));
      if (el) {
        [...el.options].forEach((o, i) => o.selected = (i === 0 || o.value === "__ALL__"));
      }
    });
    applyAll();
    if (typeof window.syncAllStMultiSelects === "function") window.syncAllStMultiSelects();
  };

  window.initServicios = function() {'''

if target in code:
    code = code.replace(target, replacement, 1)
    with open('js/servicios.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("js/servicios.js updated successfully")
else:
    print("Could not find target in js/servicios.js")
