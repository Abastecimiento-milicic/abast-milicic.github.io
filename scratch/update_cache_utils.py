# -*- coding: utf-8 -*-

with open('js/cache-utils.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = """          const rawVal = (typeof rowData[colIdx - 1] === 'string' && /^\\d{1,3}(\\.\\d{3})+$/.test(rowData[colIdx - 1].trim())) ? rowData[colIdx - 1].trim().replace(/\\./g, '') : rowData[colIdx - 1];
          if (rawVal !== "" && !isNaN(rawVal) && typeof rawVal !== 'boolean') {
            const num = Number(rawVal);
            cell.value = num;
            cell.alignment = { vertical: 'middle', horizontal: 'right' };
            if (Number.isInteger(num)) {
              cell.numFmt = '0';
            } else {
              cell.numFmt = '0.00';
            }
          }"""

replacement = """          const hName = (headers[colIdx - 1] || "").trim();
          let rawVal = rowData[colIdx - 1];
          if (typeof rawVal === 'string') {
            rawVal = rawVal.replace(/^\\uFEFF/, "").trim();
          }

          // Proteger columnas que deben ser estrictamente texto (códigos, IDs, números de pieza con letras como 8E5529)
          const isCodeOrIdCol = /^(Material|Centro|Almac[eé]n|Ubicaci[oó]n|Caract\\.planif\\.nec|Unidad|Moneda|Tipo|Fabricante|Pieza|Numero|Grupo|Id|Doc|Pedido|SolPed)/i.test(hName);

          let isNumeric = false;
          let numVal = null;

          if (!isCodeOrIdCol && rawVal !== "" && rawVal !== null && rawVal !== undefined) {
            let strVal = String(rawVal).trim();
            // Códigos con ceros a la izquierda (ej: "0365", "01") se mantienen como texto
            if (!/^0\\d+/.test(strVal)) {
              if (/^\\d{1,3}(\\.\\d{3})+$/.test(strVal)) {
                strVal = strVal.replace(/\\./g, '');
              } else if (/^\\d{1,3}(\\.\\d{3})+,\\d+$/.test(strVal)) {
                strVal = strVal.replace(/\\./g, '').replace(',', '.');
              } else if (/^-?\\d+,\\d+$/.test(strVal)) {
                strVal = strVal.replace(',', '.');
              }

              // Validar estrictamente número real finito (evita que códigos con 'E' como 8E5529 generen Infinity)
              if (/^-?\\d+(\\.\\d+)?$/.test(strVal)) {
                const n = Number(strVal);
                if (Number.isFinite(n) && !isNaN(n) && Math.abs(n) < 1e15) {
                  isNumeric = true;
                  numVal = n;
                }
              }
            }
          }

          if (isNumeric && numVal !== null) {
            cell.value = numVal;
            cell.alignment = { vertical: 'middle', horizontal: 'right' };
            if (Number.isInteger(numVal)) {
              cell.numFmt = '#,##0';
            } else {
              cell.numFmt = '#,##0.00';
            }
          } else {
            cell.value = (rawVal === null || rawVal === undefined) ? "" : rawVal;
          }"""

code_norm = code.replace('\r\n', '\n')
target_norm = target.replace('\r\n', '\n')
repl_norm = replacement.replace('\r\n', '\n')

if target_norm in code_norm:
    code_norm = code_norm.replace(target_norm, repl_norm, 1)
    with open('js/cache-utils.js', 'w', encoding='utf-8', newline='') as f:
        f.write(code_norm)
    print("SUCCESS: js/cache-utils.js updated with robust number and text parsing.")
else:
    print("ERROR: Target not found in js/cache-utils.js")
