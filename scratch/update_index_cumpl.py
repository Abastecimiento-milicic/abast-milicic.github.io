# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = """      <!-- ESPACIO RESERVADO PARA 2. DEMORAS Y 3. SERVICIOS -->
      <section class="panel" style="border: 2px dashed #cbd5e1; background: #f8fafc; opacity: 0.85;">
        <div class="panel-body" style="padding: 16px 20px; font-size: 13px; color: #64748b; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
          <div>
            🔜 <strong>Próximos bloques:</strong> 2. DEMORAS (pedidos FT, días promedio) y 3. SERVICIOS (órdenes cumplidas vs pendientes).
          </div>
          <span style="background: #e2e8f0; color: #334155; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 4px;">Formato de texto limpio</span>
        </div>
      </section>"""

replacement = """      <!-- BLOQUE 2: CUMPLIMIENTO -->
      <section class="panel" style="margin-bottom: 20px;">
        <div class="panel-title" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span>🎯 2. CUMPLIMIENTO</span>
          </div>
          <div style="display: flex; align-items: center; gap: 6px; background: #f8fafc; border: 1px solid #cbd5e1; padding: 2px 8px; border-radius: 5px;">
            <label for="resumen_mesCumplSelect" style="font-size: 11px; font-weight: 700; color: #334155; white-space: nowrap;">
              📅 Mes:
            </label>
            <select id="resumen_mesCumplSelect" class="multi-select" style="min-width: 150px; height: 24px; padding: 0 6px; font-size: 11px; font-weight: 600; border: 1px solid #94a3b8; border-radius: 4px; background: #ffffff;">
              <option value="2026-09">Septiembre 2026</option>
            </select>
          </div>
        </div>

        <div class="panel-body" style="padding: 16px 20px;">
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px 16px;">
            <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px;">
              <li style="display: flex; align-items: center; font-size: 13px; color: #1e293b; flex-wrap: wrap;">
                <span style="font-size: 15px; margin-right: 8px;">📦</span>
                <strong>COMPROMETIDOS:</strong>
                <span id="res_cumplComprometidos" style="font-size: 15px; font-weight: 800; color: #2563eb; margin: 0 6px;">-</span>
                <span style="color: #64748b; font-size: 11px;">— Total del mes.</span>
              </li>

              <li style="display: flex; align-items: center; font-size: 13px; color: #1e293b; flex-wrap: wrap;">
                <span style="font-size: 15px; margin-right: 8px;">✅</span>
                <strong>A TIEMPO (AT):</strong>
                <span id="res_cumplATpct" style="font-size: 15px; font-weight: 800; color: #16a34a; margin: 0 6px;">-</span>
                <span style="color: #475569; font-size: 11px;">
                  Cant: <span id="res_cumplATqty" style="font-weight: 700; color: #0f172a;">-</span>
                  <span id="res_cumplATdiff" style="color: #16a34a; font-weight: 700; margin-left: 4px;">· - vs mes anterior</span>
                </span>
              </li>

              <li style="display: flex; align-items: center; font-size: 13px; color: #1e293b; flex-wrap: wrap;">
                <span style="font-size: 15px; margin-right: 8px;">⏳</span>
                <strong>FUERA DE TIEMPO (FT):</strong>
                <span id="res_cumplFTpct" style="font-size: 15px; font-weight: 800; color: #dc2626; margin: 0 6px;">-</span>
                <span style="color: #475569; font-size: 11px;">
                  Cant: <span id="res_cumplFTqty" style="font-weight: 700; color: #0f172a;">-</span>
                  <span id="res_cumplFTdiff" style="color: #16a34a; font-weight: 700; margin-left: 4px;">· - vs mes anterior</span>
                </span>
              </li>

              <li style="display: flex; align-items: center; font-size: 13px; color: #1e293b; flex-wrap: wrap;">
                <span style="font-size: 15px; margin-right: 8px;">🚫</span>
                <strong>NO ENTREGADOS (NE):</strong>
                <span id="res_cumplNEpct" style="font-size: 15px; font-weight: 800; color: #64748b; margin: 0 6px;">-</span>
                <span style="color: #475569; font-size: 11px;">
                  Cant: <span id="res_cumplNEqty" style="font-weight: 700; color: #0f172a;">-</span>
                  <span id="res_cumplNEdiff" style="color: #dc2626; font-weight: 700; margin-left: 4px;">· - vs mes anterior</span>
                </span>
              </li>

              <li style="display: flex; align-items: center; font-size: 13px; color: #1e293b; flex-wrap: wrap;">
                <span style="font-size: 15px; margin-right: 8px;">📅</span>
                <strong>DEMORA PROMEDIO:</strong>
                <span id="res_cumplDemoraAvg" style="font-size: 15px; font-weight: 800; color: #ea580c; margin: 0 6px;">-</span>
                <span style="color: #64748b; font-size: 11px;">— Promedio mes.</span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      <!-- ESPACIO RESERVADO PARA 3. SERVICIOS -->
      <section class="panel" style="border: 2px dashed #cbd5e1; background: #f8fafc; opacity: 0.85;">
        <div class="panel-body" style="padding: 12px 20px; font-size: 12px; color: #64748b; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
          <div>
            🔜 <strong>Próximo bloque:</strong> 3. SERVICIOS (órdenes cumplidas vs pendientes).
          </div>
          <span style="background: #e2e8f0; color: #334155; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px;">Formato de texto limpio</span>
        </div>
      </section>"""

if target in content:
    content = content.replace(target, replacement, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: index.html updated with CUMPLIMIENTO block.")
else:
    # Try normalizing line endings
    norm_content = content.replace('\r\n', '\n')
    norm_target = target.replace('\r\n', '\n')
    if norm_target in norm_content:
        norm_content = norm_content.replace(norm_target, replacement.replace('\r\n', '\n'), 1)
        # Preserve original CRLF
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(norm_content.replace('\n', '\r\n'))
        print("SUCCESS (normalized): index.html updated with CUMPLIMIENTO block.")
    else:
        print("ERROR: Target not found.")
