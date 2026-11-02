with open('js/resumen.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update updateResumen
target1 = """  function updateResumen() {
    updateMMBlock();
    updateCumplimientoBlock();
  }"""

repl1 = """  function updateResumen() {
    updateMMBlock();
    updateCumplimientoBlock();
    updateDemorasBlock();
  }

  /* --- 3. BLOQUE DEMORAS --- */
  function updateDemorasBlock() {
    const selObra = document.getElementById("resumen_obraSelect");
    const selectedCode = selObra ? selObra.value : "__ALL__";
    const selMes = document.getElementById("resumen_mesCumplSelect");
    const selectedYM = selMes ? selMes.value : "__ALL__";

    if (typeof window.renderResumenDemoras === "function") {
      window.renderResumenDemoras("res_chartMotivos", "res_chartAreas", selectedCode, selectedYM);
    }
  }"""

assert target1 in code, "target1 not found in resumen.js"
code = code.replace(target1, repl1, 1)

# 2. Update sel.onchange in renderMesesCumplSelect
target2 = "    sel.onchange = () => updateCumplimientoBlock();"
repl2 = "    sel.onchange = () => { updateCumplimientoBlock(); updateDemorasBlock(); };"
assert target2 in code, "target2 not found in resumen.js"
code = code.replace(target2, repl2, 1)

# 3. Update window.initResumen
target3 = """  // Hook global de inicialización
  window.initResumen = function () {
    loadResumenData();
  };"""

repl3 = """  // Hook global de inicialización
  window.initResumen = function () {
    loadResumenData();
    if (!window.demorasInitialized && typeof window.initDemoras === "function") {
      window.initDemoras();
    }
    updateDemorasBlock();
  };"""
assert target3 in code, "target3 not found in resumen.js"
code = code.replace(target3, repl3, 1)

with open('js/resumen.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Successfully updated js/resumen.js!")
