import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("js/resumen.js", "r", encoding="utf-8") as f:
    code = f.read()

# Normalize to LF
is_crlf = "\r\n" in code
code_lf = code.replace("\r\n", "\n")

# 1. Date column
old_col = 'const colFec = cumplHeaders.find(h => /fecha/i.test(h)) || "FECHA ENTREGA ESPERADA";'
new_col = 'const colFec = cumplHeaders.find(h => /entrega\\s+esperada/i.test(h)) || "FECHA ENTREGA ESPERADA";'
assert old_col in code_lf, "old_col not found"
code_lf = code_lf.replace(old_col, new_col, 1)

# 2. Default month selection
old_month_sel = """    const hasSelection = Array.from(sel.selectedOptions).some(o => o.value !== "__ALL__");
    if (!hasSelection) {
      const optSep = Array.from(sel.options).find(o => o.value === "2026-09");
      if (optSep) {
        optSep.selected = true;
        if (sel.options[0]) sel.options[0].selected = false;
      } else if (sortedYM.length > 0) {
        sel.options[sel.options.length - 1].selected = true;
        if (sel.options[0]) sel.options[0].selected = false;
      } else {
        if (sel.options[0]) sel.options[0].selected = true;
      }
    }"""

new_month_sel = """    const hasSelection = Array.from(sel.selectedOptions).some(o => o.value !== "__ALL__");
    if (!hasSelection) {
      const explicitMonth = window.MES_POR_DEFECTO || (sortedYM.includes("2026-10") ? "2026-10" : null);
      const defMonth = (explicitMonth && sortedYM.includes(explicitMonth)) ? explicitMonth : (sortedYM.length > 0 ? sortedYM[sortedYM.length - 1] : null);
      if (defMonth) {
        const optDef = Array.from(sel.options).find(o => o.value === defMonth);
        if (optDef) {
          optDef.selected = true;
          if (sel.options[0]) sel.options[0].selected = false;
        }
      } else {
        if (sel.options[0]) sel.options[0].selected = true;
      }
    }"""

assert old_month_sel in code_lf, "old_month_sel not found"
code_lf = code_lf.replace(old_month_sel, new_month_sel, 1)

# 3. hookClearButton
old_clear_m = """      const selMes = document.getElementById("resumen_mesCumplSelect");
      if (selMes && selMes.options.length) {
        const hasSep = Array.from(selMes.options).some(o => o.value === "2026-09");
        [...selMes.options].forEach(opt => {
          opt.selected = hasSep ? (opt.value === "2026-09") : (opt.value === "__ALL__");
        });
        selMes.dispatchEvent(new Event("change", { bubbles: true }));
      }"""

new_clear_m = """      const selMes = document.getElementById("resumen_mesCumplSelect");
      if (selMes && selMes.options.length) {
        const defM = Array.from(selMes.options).some(o => o.value === "2026-10") ? "2026-10" : selMes.options[selMes.options.length - 1].value;
        [...selMes.options].forEach(opt => {
          opt.selected = (opt.value === defM);
        });
        selMes.dispatchEvent(new Event("change", { bubbles: true }));
      }"""

assert old_clear_m in code_lf, "old_clear_m not found"
code_lf = code_lf.replace(old_clear_m, new_clear_m, 1)

# Restore CRLF if it was CRLF
if is_crlf:
    code_lf = code_lf.replace("\n", "\r\n")

with open("js/resumen.js", "w", encoding="utf-8") as f:
    f.write(code_lf)

print("Updated js/resumen.js successfully")

# Bump cache buster to v82
with open("js/last-update.js", "r", encoding="utf-8") as f:
    lu = f.read()
lu = lu.replace("_v81_20261102_164500", "_v82_20261102_165500")
with open("js/last-update.js", "w", encoding="utf-8") as f:
    f.write(lu)

with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()
idx = idx.replace("js/demoras.js?v=20261102_164500", "js/demoras.js?v=20261102_165500")
idx = idx.replace("js/resumen.js?v=20261102_164500", "js/resumen.js?v=20261102_165500")
with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx)

print("Bumped cache buster to v82 successfully")
