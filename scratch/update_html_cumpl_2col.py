# -*- coding: utf-8 -*-
import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Pattern for panel-body inside Bloque 2
target_html = """        <div class="panel-body" style="padding: 16px 20px;">
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
        </div>"""

replacement_html = """        <div class="panel-body" style="padding: 16px 20px;">
          <!-- Contenedor Flex de 2 Columnas: Acumulado 12 Meses vs Mensual -->
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 24px; align-items: start;">
            
            <!-- Columna Izquierda: Acumulado Últimos 12 Meses -->
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px 16px;">
              <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; color: #475569; margin-bottom: 12px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
                <span>Acumulado Últimos 12 Meses:</span>
                <span id="res_cumplAcumRango" style="font-size: 10px; font-weight: 700; color: #64748b; text-transform: none;"></span>
              </div>
              <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px;">
                <li style="display: flex; align-items: center; font-size: 13px; color: #1e293b; flex-wrap: wrap;">
                  <span style="font-size: 15px; margin-right: 8px;">📦</span>
                  <strong>COMPROMETIDOS:</strong>
                  <span id="res_cumplAcumComprometidos" style="font-size: 15px; font-weight: 800; color: #2563eb; margin: 0 6px;">-</span>
                  <span style="color: #64748b; font-size: 11px;">— Total últimos 12 meses.</span>
                </li>

                <li style="display: flex; align-items: center; font-size: 13px; color: #1e293b; flex-wrap: wrap;">
                  <span style="font-size: 15px; margin-right: 8px;">✅</span>
                  <strong>A TIEMPO (AT):</strong>
                  <span id="res_cumplAcumATpct" style="font-size: 15px; font-weight: 800; color: #16a34a; margin: 0 6px;">-</span>
                  <span style="color: #475569; font-size: 11px;">
                    Cant: <span id="res_cumplAcumATqty" style="font-weight: 700; color: #0f172a;">-</span>
                  </span>
                </li>

                <li style="display: flex; align-items: center; font-size: 13px; color: #1e293b; flex-wrap: wrap;">
                  <span style="font-size: 15px; margin-right: 8px;">⏳</span>
                  <strong>FUERA DE TIEMPO (FT):</strong>
                  <span id="res_cumplAcumFTpct" style="font-size: 15px; font-weight: 800; color: #dc2626; margin: 0 6px;">-</span>
                  <span style="color: #475569; font-size: 11px;">
                    Cant: <span id="res_cumplAcumFTqty" style="font-weight: 700; color: #0f172a;">-</span>
                  </span>
                </li>

                <li style="display: flex; align-items: center; font-size: 13px; color: #1e293b; flex-wrap: wrap;">
                  <span style="font-size: 15px; margin-right: 8px;">🚫</span>
                  <strong>NO ENTREGADOS (NE):</strong>
                  <span id="res_cumplAcumNEpct" style="font-size: 15px; font-weight: 800; color: #64748b; margin: 0 6px;">-</span>
                  <span style="color: #475569; font-size: 11px;">
                    Cant: <span id="res_cumplAcumNEqty" style="font-weight: 700; color: #0f172a;">-</span>
                  </span>
                </li>

                <li style="display: flex; align-items: center; font-size: 13px; color: #1e293b; flex-wrap: wrap;">
                  <span style="font-size: 15px; margin-right: 8px;">📅</span>
                  <strong>DEMORA PROMEDIO:</strong>
                  <span id="res_cumplAcumDemoraAvg" style="font-size: 15px; font-weight: 800; color: #ea580c; margin: 0 6px;">-</span>
                  <span style="color: #64748b; font-size: 11px;">— Promedio 12 meses.</span>
                </li>
              </ul>
            </div>

            <!-- Columna Derecha: Rendimiento Mensual -->
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px 16px;">
              <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; color: #475569; margin-bottom: 12px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px;">
                Rendimiento Mensual (<span id="res_cumplMesLabel" style="color: #2563eb;">Septiembre 2026</span>):
              </div>
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
        </div>"""

norm_html = html.replace('\r\n', '\n')
norm_target = target_html.replace('\r\n', '\n')
norm_replacement = replacement_html.replace('\r\n', '\n')

if norm_target in norm_html:
    norm_html = norm_html.replace(norm_target, norm_replacement, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(norm_html.replace('\n', '\r\n'))
    print("SUCCESS: index.html 2-column layout updated for Bloque 2.")
else:
    print("ERROR: Target for index.html not found.")
