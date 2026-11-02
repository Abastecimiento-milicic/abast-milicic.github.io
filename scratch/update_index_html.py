with open('index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add Bloque 3: DEMORAS and change reserved block to 4. SERVICIOS
target1 = """          <!-- ESPACIO RESERVADO PARA 3. SERVICIOS -->
          <section class="panel" style="border: 2px dashed #cbd5e1; background: #f8fafc; opacity: 0.85;">
            <div class="panel-body" style="padding: 12px 20px; font-size: 12px; color: #64748b; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
              <div>
                🔜 <strong>Próximo bloque:</strong> 3. SERVICIOS (órdenes cumplidas vs pendientes).
              </div>
              <span style="background: #e2e8f0; color: #334155; font-size: 12px; font-weight: 700; padding: 2px 8px; border-radius: 4px;">Formato de texto limpio</span>
            </div>
          </section>"""

repl1 = """          <!-- BLOQUE 3: DEMORAS -->
          <section class="panel" style="margin-bottom: 14px;">
            <div class="panel-title" style="display: flex; align-items: center; justify-content: space-between; padding: 10px 18px !important; min-height: 42px !important; font-size: 16px !important; font-weight: 800 !important;">
              <div style="display: flex; align-items: center; gap: 8px;">
                <span>⏱️ 3. DEMORAS</span>
              </div>
              <span style="font-size: 13px; font-weight: 600; color: #64748b; text-transform: uppercase;">Fuente: PEDIDOS COMPRAS (CUMPLIMIENTO)</span>
            </div>
            <div class="panel-body" style="padding: 16px 18px !important;">
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(440px, 1fr)); gap: 20px; align-items: stretch;">
                
                <!-- Izquierda: Demoras Proyecto (Motivos) -->
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px 16px; display: flex; flex-direction: column;">
                  <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; border-bottom: 1.5px solid #e2e8f0; padding-bottom: 6px;">
                    <span style="font-size: 13.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; color: #1e293b;">
                      Demoras Proyecto (Motivos)
                    </span>
                    <span id="res_lblTotalMotivos" style="font-size: 12px; font-weight: 700; color: #475569; background: #e2e8f0; padding: 2px 8px; border-radius: 12px;">-</span>
                  </div>
                  <div id="res_chartMotivos" style="width: 100%; height: 360px; min-height: 360px;"></div>
                </div>

                <!-- Derecha: Demora por Área -->
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px 16px; display: flex; flex-direction: column;">
                  <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; border-bottom: 1.5px solid #e2e8f0; padding-bottom: 6px;">
                    <span style="font-size: 13.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; color: #1e293b;">
                      Demora por Área
                    </span>
                    <span id="res_lblTotalAreas" style="font-size: 12px; font-weight: 700; color: #475569; background: #e2e8f0; padding: 2px 8px; border-radius: 12px;">-</span>
                  </div>
                  <div id="res_chartAreas" style="width: 100%; height: 360px; min-height: 360px;"></div>
                </div>

              </div>
            </div>
          </section>

          <!-- ESPACIO RESERVADO PARA 4. SERVICIOS -->
          <section class="panel" style="border: 2px dashed #cbd5e1; background: #f8fafc; opacity: 0.85;">
            <div class="panel-body" style="padding: 12px 20px; font-size: 12px; color: #64748b; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
              <div>
                🔜 <strong>Próximo bloque:</strong> 4. SERVICIOS (órdenes cumplidas vs pendientes).
              </div>
              <span style="background: #e2e8f0; color: #334155; font-size: 12px; font-weight: 700; padding: 2px 8px; border-radius: 4px;">Formato de texto limpio</span>
            </div>
          </section>"""

assert target1 in code, "target1 not found in index.html"
code = code.replace(target1, repl1, 1)

# 2. Update script tags: demoras.js before resumen.js and bump cache busters
target2 = """  <script src="js/resumen.js?v=20261030_144000"></script>
  <script src="js/cumplimiento.js?v=20261029_125545"></script>
  <script src="js/cumplimiento-arriba.js?v=20261029_125545"></script>
  <script src="js/analisis-mm.js?v=20261030_132500"></script>
  <script src="js/evolucion.js?v=20261029_125545"></script>
  <script src="js/demoras.js?v=20261029_125545"></script>"""

repl2 = """  <script src="js/demoras.js?v=20261030_152000"></script>
  <script src="js/resumen.js?v=20261030_152000"></script>
  <script src="js/cumplimiento.js?v=20261029_125545"></script>
  <script src="js/cumplimiento-arriba.js?v=20261029_125545"></script>
  <script src="js/analisis-mm.js?v=20261030_132500"></script>
  <script src="js/evolucion.js?v=20261029_125545"></script>"""

assert target2 in code, "target2 not found in index.html"
code = code.replace(target2, repl2, 1)

# 3. In switchTab, ensure resize for demoras charts when opening resumen
target3 = """        if (tabName === 'resumen') {
          if (typeof window.initResumen === 'function') {
            window.initResumen();
          }
        }"""

repl3 = """        if (tabName === 'resumen') {
          if (typeof window.initResumen === 'function') {
            window.initResumen();
          }
          setTimeout(() => {
            if (typeof window.resizeResumenDemoras === 'function') window.resizeResumenDemoras();
          }, 150);
        }"""

assert target3 in code, "target3 not found in index.html"
code = code.replace(target3, repl3, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("Successfully updated index.html!")
