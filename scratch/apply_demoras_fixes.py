import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Update index.html - swap order of Demoras Proyecto and Demora por Area
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target_html = """                <!-- Izquierda: Demoras Proyecto (Motivos) -->
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
                </div>"""

repl_html = """                <!-- Izquierda: Demora por Área -->
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px 16px; display: flex; flex-direction: column;">
                  <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; border-bottom: 1.5px solid #e2e8f0; padding-bottom: 6px;">
                    <span style="font-size: 13.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; color: #1e293b;">
                      Demora por Área
                    </span>
                    <span id="res_lblTotalAreas" style="font-size: 12px; font-weight: 700; color: #475569; background: #e2e8f0; padding: 2px 8px; border-radius: 12px;">-</span>
                  </div>
                  <div id="res_chartAreas" style="width: 100%; height: 380px; min-height: 380px;"></div>
                </div>

                <!-- Derecha: Demoras Proyecto (Motivos) -->
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px 16px; display: flex; flex-direction: column;">
                  <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; border-bottom: 1.5px solid #e2e8f0; padding-bottom: 6px;">
                    <span style="font-size: 13.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; color: #1e293b;">
                      Demoras Proyecto (Motivos)
                    </span>
                    <span id="res_lblTotalMotivos" style="font-size: 12px; font-weight: 700; color: #475569; background: #e2e8f0; padding: 2px 8px; border-radius: 12px;">-</span>
                  </div>
                  <div id="res_chartMotivos" style="width: 100%; height: 380px; min-height: 380px;"></div>
                </div>"""

assert target_html in html, "target_html not found in index.html"
html = html.replace(target_html, repl_html, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html (swapped left/right cards)!")

# 2. Update js/demoras.js
with open('js/demoras.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 2.1 Update getDisplayName
old_getDisplayName = """  function getDisplayName(name) {
      if (name === "FECHAENTREGAMUYCERCANA CON PRIORIDAD") {
          return "FECHA ENTREGA MUY CERCANA (CON PRIORIDAD)";
      }
      if (name === "FECHAENTREGAMUYCERCANA SIN PRIORIDAD") {
          return "FECHA ENTREGA MUY CERCANA (SIN PRIORIDAD)";
      }
      const normalized = norm(name);
      if (normalized === norm("CADENA DE SUMINISTRO") || normalized === norm("CADENA DE SUMINISTROS")) {
          return "PROYECTO";
      }
      if (normalized === norm("BLEN")) {
          return "BLEND";
      }
      return name;
  }"""

new_getDisplayName = """  function getDisplayName(name) {
      if (name === "FECHAENTREGAMUYCERCANA CON PRIORIDAD" || name === "FECHA ENTREGA MUY CERCANA (CON PRIORIDAD)" || name === "FECHA DE ENTREGA MUY CERCANA (CON PRIORIDAD)") {
          return "FEMC (CON PRIORIDAD)";
      }
      if (name === "FECHAENTREGAMUYCERCANA SIN PRIORIDAD" || name === "FECHA ENTREGA MUY CERCANA (SIN PRIORIDAD)" || name === "FECHA DE ENTREGA MUY CERCANA (SIN PRIORIDAD)") {
          return "FEMC (SIN PRIORIDAD)";
      }
      const normalized = norm(name);
      if (normalized.includes("FECHA") && (normalized.includes("CERCANA") || normalized.includes("MUYCERCANA"))) {
          if (normalized.includes("CON PRIORIDAD") || normalized.includes("CONPRIORIDAD")) return "FEMC (CON PRIORIDAD)";
          if (normalized.includes("SIN PRIORIDAD") || normalized.includes("SINPRIORIDAD")) return "FEMC (SIN PRIORIDAD)";
          return "FEMC";
      }
      if (normalized === norm("CADENA DE SUMINISTRO") || normalized === norm("CADENA DE SUMINISTROS")) {
          return "PROYECTO";
      }
      if (normalized === norm("BLEN")) {
          return "BLEND";
      }
      return name;
  }"""

assert old_getDisplayName in js, "old_getDisplayName not found"
js = js.replace(old_getDisplayName, new_getDisplayName, 1)

# 2.2 Update window.renderResumenDemoras to match exact colors and chart type
old_render_start = "  window.renderResumenDemoras = function(targetMotivosId, targetAreasId, clientCode, ym) {"
assert old_render_start in js, "old_render_start not found"
idx_start = js.find(old_render_start)
idx_end = js.find("})();", idx_start)
assert idx_end != -1, "end of IIFE not found"

new_render = """  window.renderResumenDemoras = function(targetMotivosId, targetAreasId, clientCode, ym) {
      const elMotivos = document.getElementById(targetMotivosId);
      const elAreas = document.getElementById(targetAreasId);
      if (!elMotivos && !elAreas) return;

      // Si los datos todavía no cargaron, guardar pedido e inicializar carga
      if (!data || !data.length) {
          pendingResumen = { targetMotivosId, targetAreasId, clientCode, ym };
          const loadingHTML = `
              <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; min-height:300px; color:#64748b; font-size:13px; text-align:center; padding:20px;">
                  <span style="font-size:24px; margin-bottom:8px;">⏳</span>
                  <span>Cargando datos de demoras...</span>
              </div>
          `;
          if (elMotivos) elMotivos.innerHTML = loadingHTML;
          if (elAreas) elAreas.innerHTML = loadingHTML;
          if (!window.demorasInitialized && typeof window.initDemoras === "function") {
              window.initDemoras();
          }
          return;
      }

      // 1. Filtrar registros por Obra y Mes
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
      }

      // Paleta exacta de la pestaña Demoras
      const palette = [
          "#0d6efd", "#20c997", "#ffc107", "#6f42c1", "#fd7e14", "#198754", "#0dcaf0", "#6c757d"
      ];

      // ==========================================
      // 1. GRAFICO IZQUIERDA: DEMORA POR AREA
      // (Mismo tipo de grafico, colores y destaque que dem_chartAreas)
      // ==========================================
      if (elAreas && typeof echarts !== "undefined") {
          const areaMap = aggAreas(rows);
          const areaItems = [];
          for (const [k, v] of areaMap.entries()) {
              if (v > 0) areaItems.push({ name: k, value: v });
          }

          const totalAreas = areaItems.reduce((acc, it) => acc + (Number(it.value) || 0), 0) || 1;
          const maxAreaVal = Math.max(...areaItems.map(d => d.value), 0);

          const elLblAreas = document.getElementById("res_lblTotalAreas");
          if (elLblAreas) {
              const countReal = areaItems.reduce((acc, it) => acc + it.value, 0);
              elLblAreas.textContent = countReal > 0 ? `${fmtInt(countReal)} demoras` : "0 demoras";
          }

          if (!areaItems.length) {
              if (resChartAreas && typeof resChartAreas.dispose === "function") {
                  resChartAreas.dispose();
                  resChartAreas = null;
              }
              elAreas.innerHTML = `
                  <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; min-height:300px; color:#64748b; font-size:13.5px; text-align:center; padding:20px;">
                      <span style="font-size:32px; margin-bottom:8px;">✅</span>
                      <span style="font-weight:700; color:#1e293b;">Sin demoras por Área</span>
                      <span style="font-size:12px; color:#94a3b8; margin-top:2px;">para la obra y período seleccionado</span>
                  </div>
              `;
          } else {
              if (resChartAreas && typeof resChartAreas.dispose === "function") resChartAreas.dispose();
              resChartAreas = echarts.init(elAreas, null, { renderer: "canvas" });

              const stableAreaNames = [...areaItems.map(x => x.name)].sort((a, b) => a.localeCompare(b, "es"));
              const areaColorByName = new Map();
              stableAreaNames.forEach((name, i) => areaColorByName.set(name, palette[i % palette.length]));

              const dataWithColors = areaItems.map((it) => {
                  const isMax = it.value === maxAreaVal;
                  const baseColor = areaColorByName.get(it.name) || "#6c757d";
                  return {
                      ...it,
                      itemStyle: {
                          color: isMax ? "#dc3545" : baseColor,
                          borderWidth: isMax ? 4 : 2,
                          shadowBlur: isMax ? 14 : 0,
                          shadowColor: isMax ? "rgba(0,0,0,0.30)" : "rgba(0,0,0,0)"
                      }
                  };
              });

              const areasOption = {
                  tooltip: {
                      trigger: "item",
                      formatter: (p) => {
                          const pct = (p.value / totalAreas) * 100;
                          return `${getDisplayName(p.name)}: <b>${fmtInt(p.value)}</b> (${pct.toFixed(1).replace(".", ",")}%)`;
                      }
                  },
                  legend: {
                      orient: "vertical",
                      right: 10,
                      top: "middle",
                      type: "scroll",
                      itemWidth: 18,
                      itemHeight: 10,
                      formatter: (name) => {
                          const it = areaItems.find(x => x.name === name);
                          const v = it ? it.value : 0;
                          const pct = (v / totalAreas) * 100;
                          return `${getDisplayName(name)} - ${pct.toFixed(1).replace(".", ",")}%`;
                      },
                      textStyle: { fontSize: 12 }
                  },
                  series: [
                      {
                          name: "% demoras por área",
                          type: "pie",
                          radius: ["40%", "72%"],
                          center: ["35%", "50%"],
                          avoidLabelOverlap: true,
                          itemStyle: {
                              borderColor: "#fff",
                              borderWidth: 2
                          },
                          label: {
                              show: false
                          },
                          emphasis: {
                              scale: true,
                              scaleSize: 6,
                              label: {
                                  show: true,
                                  fontSize: 12,
                                  fontWeight: "bold",
                                  formatter: (p) => `${p.percent.toFixed(0)}%`
                              }
                          },
                          data: dataWithColors
                      }
                  ]
              };
              resChartAreas.setOption(areasOption, true);
              resChartAreas.resize();
          }
      }

      // ==========================================
      // 2. GRAFICO DERECHA: DEMORAS PROYECTO (MOTIVOS)
      // (Mismo tipo de grafico, colores y destaque que dem_chartMotivos)
      // ==========================================
      if (elMotivos && typeof echarts !== "undefined") {
          const sumsMap = aggMotivosProyecto(rows);
          const motivosItems = [];
          for (const [k, v] of sumsMap.entries()) {
              if (v > 0) motivosItems.push({ name: k, value: v });
          }

          const totalMotivos = motivosItems.reduce((acc, it) => acc + (Number(it.value) || 0), 0) || 1;
          const maxMotivoVal = Math.max(...motivosItems.map(d => d.value), 0);

          const elLblMotivos = document.getElementById("res_lblTotalMotivos");
          if (elLblMotivos) {
              const countReal = motivosItems.reduce((acc, it) => acc + it.value, 0);
              elLblMotivos.textContent = countReal > 0 ? `${fmtInt(countReal)} demoras` : "0 demoras";
          }

          if (!motivosItems.length) {
              if (resChartMotivos && typeof resChartMotivos.dispose === "function") {
                  resChartMotivos.dispose();
                  resChartMotivos = null;
              }
              elMotivos.innerHTML = `
                  <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; min-height:300px; color:#64748b; font-size:13.5px; text-align:center; padding:20px;">
                      <span style="font-size:32px; margin-bottom:8px;">✅</span>
                      <span style="font-weight:700; color:#1e293b;">Sin demoras de Proyecto</span>
                      <span style="font-size:12px; color:#94a3b8; margin-top:2px;">para la obra y período seleccionado</span>
                  </div>
              `;
          } else {
              if (resChartMotivos && typeof resChartMotivos.dispose === "function") resChartMotivos.dispose();
              resChartMotivos = echarts.init(elMotivos, null, { renderer: "canvas" });

              const stableNames = [...motivosItems.map(x => x.name)].sort((a, b) => a.localeCompare(b, "es"));
              const colorByName = new Map();
              stableNames.forEach((name, i) => {
                  if (name === "FECHAENTREGAMUYCERCANA CON PRIORIDAD" || name.includes("CON PRIORIDAD")) {
                      colorByName.set(name, "#dc3545");
                  } else if (name === "FECHAENTREGAMUYCERCANA SIN PRIORIDAD" || name.includes("SIN PRIORIDAD")) {
                      colorByName.set(name, "#e4606d");
                  } else {
                      colorByName.set(name, palette[i % palette.length]);
                  }
              });

              const dataPie = motivosItems.map((it) => {
                  const isMax = it.value === maxMotivoVal;
                  const baseColor = colorByName.get(it.name) || "#6c757d";
                  return {
                      ...it,
                      itemStyle: {
                          color: baseColor,
                          borderWidth: isMax ? 4 : 2,
                          shadowBlur: isMax ? 14 : 0,
                          shadowColor: isMax ? "rgba(0,0,0,0.30)" : "rgba(0,0,0,0)"
                      }
                  };
              });

              const motivosOption = {
                  tooltip: {
                      trigger: "item",
                      formatter: (p) => {
                          const pct = (p.value / totalMotivos) * 100;
                          return `${getDisplayName(p.name)}: <b>${fmtInt(p.value)}</b> (${pct.toFixed(1).replace(".", ",")}%)`;
                      }
                  },
                  legend: {
                      orient: "vertical",
                      right: 10,
                      top: "middle",
                      type: "scroll",
                      itemWidth: 18,
                      itemHeight: 10,
                      formatter: (name) => {
                          const it = motivosItems.find(x => x.name === name);
                          const v = it ? it.value : 0;
                          const pct = (v / totalMotivos) * 100;
                          return `${getDisplayName(name)} - ${pct.toFixed(1).replace(".", ",")}%`;
                      },
                      textStyle: { fontSize: 12 }
                  },
                  series: [
                      {
                          name: "Demoras proyecto",
                          type: "pie",
                          radius: ["60%", "86%"],
                          center: ["35%", "50%"],
                          avoidLabelOverlap: true,
                          itemStyle: {
                              borderColor: "#ffffff",
                              borderWidth: 2
                          },
                          label: {
                              show: false
                          },
                          emphasis: {
                              scale: true,
                              scaleSize: 6,
                              label: {
                                  show: true,
                                  fontSize: 12,
                                  fontWeight: "bold",
                                  formatter: (p) => `${p.percent.toFixed(0)}%`
                              }
                          },
                          data: dataPie
                      }
                  ]
              };
              resChartMotivos.setOption(motivosOption, true);
              resChartMotivos.resize();
          }
      }
  };
"""

js = js[:idx_start] + new_render + "\n" + js[idx_end:]

with open('js/demoras.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated js/demoras.js (colors, type of chart, FEMC abbreviation)!")
