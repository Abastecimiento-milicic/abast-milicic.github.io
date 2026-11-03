import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("js/demoras.js", "r", encoding="utf-8") as f:
    content = f.read()

target = """      // 1. Filtrar registros por Obra y Mes
      let rows = data;
      if (clientCode && clientCode !== "__ALL__") {
          const targetCode = extractCode(clientCode);
          rows = rows.filter(r => {
              const val = r[CLIENT_COL] || "";
              return extractCode(val) === targetCode || extractCode(getCLI(val)) === targetCode;
          });
      }
      if (ym && ym !== "__ALL__") {
          rows = rows.filter(r => getMonthKeyFromRow(r) === ym);
      }"""

replacement = """      // Helper normalizador canónico para unificación en resumen
      function getCanonicalObra(val) {
          const c = extractCode(val);
          if (c === "26" || c === "314" || c === "26_314" || c === "00026" || c === "00314") return "26_314";
          if (c === "35" || c === "341" || c === "35_341" || c === "00035" || c === "00341") return "35_341";
          return c;
      }

      // 1. Filtrar registros por Obra y Mes
      let rows = data;

      // Normalizar clientCode (puede ser array de códigos o string simple)
      let obraList = [];
      if (Array.isArray(clientCode)) {
          obraList = clientCode.filter(c => c && c !== "__ALL__").map(getCanonicalObra);
      } else if (clientCode && clientCode !== "__ALL__") {
          obraList = [getCanonicalObra(clientCode)];
      }

      if (obraList.length > 0) {
          const obraSet = new Set(obraList);
          rows = rows.filter(r => {
              const val = r[CLIENT_COL] || "";
              const cVal = getCanonicalObra(val);
              const cCli = getCanonicalObra(getCLI(val));
              return obraSet.has(cVal) || obraSet.has(cCli);
          });
      }

      // Normalizar ym (puede ser array de meses o string simple)
      let ymList = [];
      if (Array.isArray(ym)) {
          ymList = ym.filter(m => m && m !== "__ALL__");
      } else if (ym && ym !== "__ALL__") {
          ymList = [ym];
      }

      if (ymList.length > 0) {
          const ymSet = new Set(ymList);
          rows = rows.filter(r => ymSet.has(getMonthKeyFromRow(r)));
      }"""

target_crlf = target.replace("\r\n", "\n").replace("\n", "\r\n")
target_lf = target.replace("\r\n", "\n")

if target_crlf in content:
    content = content.replace(target_crlf, replacement.replace("\r\n", "\n").replace("\n", "\r\n"), 1)
    print("Replaced in demoras.js (CRLF)")
elif target_lf in content:
    content = content.replace(target_lf, replacement.replace("\r\n", "\n"), 1)
    print("Replaced in demoras.js (LF)")
else:
    print("Target NOT found in demoras.js!")

with open("js/demoras.js", "w", encoding="utf-8") as f:
    f.write(content)

print("Finished updating demoras.js")
