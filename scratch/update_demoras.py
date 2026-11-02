import re
import sys

with open('js/demoras.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add variables
target1 = "  let chartMotivosResizeBound = false;"
repl1 = """  let chartMotivosResizeBound = false;

  let resChartMotivos = null;
  let resChartAreas = null;
  let pendingResumen = null;"""

assert target1 in code, "target1 not found"
code = code.replace(target1, repl1, 1)

# 2. Add extractCode and getCLI
target2 = """  function getMotivosList() {"""
repl2 = """  function extractCode(val) {
      const s = clean(val);
      const m = s.match(/\\d+/);
      return m ? String(parseInt(m[0], 10)) : s;
  }

  function getCLI(cliente) {
      if (!cliente) return "";
      const raw = cliente.trim();
      const rawUpper = raw.toUpperCase();
      if (rawUpper === "00029-AMPLIACION SEDE ROSARIO") return "00029MR";
      if (rawUpper === "00029 -AMPLIACION SEDE SJ") return "00029MM";
      if (rawUpper === "PROYECTO 371 VELADERO F8A") return "00371";
      if (rawUpper === "OBRA 374 TERMINAL PUNTA COLORADA") return "00374";
      if (rawUpper === "00375 YPF OLEODUCTO PR-LP") return "00375";
      if (rawUpper === "UTE 348" || rawUpper === "UTE 363") return rawUpper;
      
      const tokens = raw.split(/[\\s\\-\\/\\(\\),]+/);
      for (const t of tokens) {
        const digits = t.replace(/\\D/g, "");
        if (digits !== "") {
          let res = digits.padStart(5, "0");
          if (res === "00035") res = "00341";
          return res;
        }
      }
      return "";
  }

  function getMotivosList() {"""

assert target2 in code, "target2 not found"
code = code.replace(target2, repl2, 1)

# 3. Update initializeUIWithData to check hintEl and pendingResumen
target3 = """          getEl("dem2_clienteHint").textContent = `Columna cliente: ${CLIENT_COL}`;

          renderClientes();
          renderGC();
          applyAll();"""

repl3 = """          const hintEl = getEl("dem2_clienteHint");
          if (hintEl) hintEl.textContent = `Columna cliente: ${CLIENT_COL}`;

          renderClientes();
          renderGC();
          applyAll();

          if (pendingResumen) {
              const p = pendingResumen;
              pendingResumen = null;
              window.renderResumenDemoras(p.targetMotivosId, p.targetAreasId, p.clientCode, p.ym);
          }"""

assert target3 in code, "target3 not found"
code = code.replace(target3, repl3, 1)

# 4. Add window.renderResumenDemoras and window.resizeResumenDemoras before })();
resumen_func = '''
  /* =========================================================
     EXPOSE RESUMEN DASHBOARD INTEGRATION
     (Graficos circulares / donut con leyenda para pestana Resumen)
     - Izquierda: Demoras Proyecto (Motivos)
     - Derecha: Demora por Area
   ========================================================= */
  window.resizeResumenDemoras = function() {
      if (resChartMotivos && typeof resChartMotivos.resize === "function") resChartMotivos.resize();
      if (resChartAreas && typeof resChartAreas.resize === "function") resChartAreas.resize();
  };

  window.addEventListener("resize", () => {
      window.resizeResumenDemoras();
  });

  window.renderResumenDemoras = function(targetMotivosId, targetAreasId, clientCode, ym) {
      const elMotivos = document.getElementById(targetMotivosId);
      const elAreas = document.getElementById(targetAreasId);
      if (!elMotivos && !elAreas) return;

      // Si los datos todavia no cargaron, guardar pedido e inicializar carga
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

      const palette = [
          "#2563eb", "#0d9488", "#d97706", "#7c3aed", "#ea580c", 
          "#16a34a", "#0891b2", "#64748b", "#4f46e5", "#db2777"
      ];

      // ==========================================
      // A) GRAFICO IZQUIERDA: DEMORAS PROYECTO (MOTIVOS)
      // ==========================================
      if (elMotivos && typeof echarts !== "undefined") {
          const sumsMap = aggMotivosProyecto(rows);
          const motivosItems = [];
          for (const [k, v] of sumsMap.entries()) {
              if (v > 0) motivosItems.push({ name: k, value: v });
          }
          motivosItems.sort((a, b) => b.value - a.value);
          const totalMotivos = motivosItems.reduce((acc, it) => acc + it.value, 0);

          const elLblMotivos = document.getElementById("res_lblTotalMotivos");
          if (elLblMotivos) {
              elLblMotivos.textContent = totalMotivos > 0 ? `${fmtInt(totalMotivos)} demoras` : "0 demoras";
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
              if (!resChartMotivos || resChartMotivos.isDisposed()) {
                  resChartMotivos = echarts.init(elMotivos, null, { renderer: "canvas" });
              }

              const stableNames = [...motivosItems.map(x => x.name)].sort((a, b) => a.localeCompare(b, "es"));
              const colorByName = new Map();
              stableNames.forEach((name, i) => {
                  if (name === "FECHAENTREGAMUYCERCANA CON PRIORIDAD") {
                      colorByName.set(name, "#dc2626");
                  } else if (name === "FECHAENTREGAMUYCERCANA SIN PRIORIDAD") {
                      colorByName.set(name, "#f87171");
                  } else {
                      colorByName.set(name, palette[i % palette.length]);
                  }
              });

              const motivosChartData = motivosItems.map(it => ({
                  name: it.name,
                  value: it.value,
                  itemStyle: {
                      color: colorByName.get(it.name) || "#64748b"
                  }
              }));

              const motivosOption = {
                  tooltip: {
                      trigger: "item",
                      backgroundColor: "rgba(15, 23, 42, 0.94)",
                      borderColor: "#334155",
                      borderWidth: 1,
                      padding: [8, 12],
                      textStyle: { color: "#f8fafc", fontSize: 12 },
                      formatter: (p) => {
                          const pct = totalMotivos ? ((p.value / totalMotivos) * 100).toFixed(1).replace(".", ",") : "0";
                          return `
                              <div style="font-weight:700; font-size:12.5px; margin-bottom:4px; color:#e2e8f0; border-bottom:1px solid #475569; padding-bottom:3px;">
                                  ${getDisplayName(p.name)}
                              </div>
                              <div style="display:flex; justify-content:space-between; gap:16px; font-size:12px; margin-top:3px;">
                                  <span style="color:#cbd5e1;">Cantidad:</span>
                                  <b style="color:#ffffff;">${fmtInt(p.value)}</b>
                              </div>
                              <div style="display:flex; justify-content:space-between; gap:16px; font-size:12px; margin-top:2px;">
                                  <span style="color:#cbd5e1;">Participación:</span>
                                  <b style="color:#38bdf8;">${pct}%</b>
                              </div>
                          `;
                      }
                  },
                  legend: {
                      orient: "vertical",
                      right: 6,
                      top: "middle",
                      type: "scroll",
                      itemWidth: 12,
                      itemHeight: 12,
                      itemGap: 8,
                      textStyle: {
                          fontSize: 11,
                          color: "#334155"
                      },
                      pageIconColor: "#2563eb",
                      pageTextStyle: { color: "#64748b", fontSize: 10 },
                      formatter: (name) => {
                          const it = motivosItems.find(x => x.name === name);
                          const v = it ? it.value : 0;
                          const pct = totalMotivos ? ((v / totalMotivos) * 100).toFixed(1).replace(".", ",") : "0";
                          const shortName = getDisplayName(name);
                          return `${shortName}: ${fmtInt(v)} (${pct}%)`;
                      }
                  },
                  series: [
                      {
                          name: "Demoras Proyecto",
                          type: "pie",
                          radius: ["40%", "72%"],
                          center: ["28%", "50%"],
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
                                  fontSize: 13,
                                  fontWeight: "bold",
                                  color: "#1e293b",
                                  formatter: (p) => `${p.percent.toFixed(0)}%`
                              }
                          },
                          data: motivosChartData
                      }
                  ]
              };
              resChartMotivos.setOption(motivosOption, true);
              resChartMotivos.resize();
          }
      }

      // ==========================================
      // B) GRAFICO DERECHA: DEMORA POR AREA
      // ==========================================
      if (elAreas && typeof echarts !== "undefined") {
          const areaMap = aggAreas(rows);
          const areaItems = [];
          for (const [k, v] of areaMap.entries()) {
              if (v > 0) areaItems.push({ name: k, value: v });
          }
          areaItems.sort((a, b) => b.value - a.value);
          const totalAreas = areaItems.reduce((acc, it) => acc + it.value, 0);

          const elLblAreas = document.getElementById("res_lblTotalAreas");
          if (elLblAreas) {
              elLblAreas.textContent = totalAreas > 0 ? `${fmtInt(totalAreas)} demoras` : "0 demoras";
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
              if (!resChartAreas || resChartAreas.isDisposed()) {
                  resChartAreas = echarts.init(elAreas, null, { renderer: "canvas" });
              }

              const maxAreaVal = Math.max(...areaItems.map(d => d.value));
              const stableAreaNames = [...areaItems.map(x => x.name)].sort((a, b) => a.localeCompare(b, "es"));
              const areaColorByName = new Map();
              stableAreaNames.forEach((name, i) => {
                  areaColorByName.set(name, palette[i % palette.length]);
              });

              const areaChartData = areaItems.map(it => {
                  const isMax = (it.value === maxAreaVal && totalAreas > 0);
                  return {
                      name: it.name,
                      value: it.value,
                      itemStyle: {
                          color: isMax ? "#dc2626" : (areaColorByName.get(it.name) || "#64748b")
                      }
                  };
              });

              const areasOption = {
                  tooltip: {
                      trigger: "item",
                      backgroundColor: "rgba(15, 23, 42, 0.94)",
                      borderColor: "#334155",
                      borderWidth: 1,
                      padding: [8, 12],
                      textStyle: { color: "#f8fafc", fontSize: 12 },
                      formatter: (p) => {
                          const pct = totalAreas ? ((p.value / totalAreas) * 100).toFixed(1).replace(".", ",") : "0";
                          return `
                              <div style="font-weight:700; font-size:12.5px; margin-bottom:4px; color:#e2e8f0; border-bottom:1px solid #475569; padding-bottom:3px;">
                                  ${getDisplayName(p.name)}
                              </div>
                              <div style="display:flex; justify-content:space-between; gap:16px; font-size:12px; margin-top:3px;">
                                  <span style="color:#cbd5e1;">Cantidad:</span>
                                  <b style="color:#ffffff;">${fmtInt(p.value)}</b>
                              </div>
                              <div style="display:flex; justify-content:space-between; gap:16px; font-size:12px; margin-top:2px;">
                                  <span style="color:#cbd5e1;">Participación:</span>
                                  <b style="color:#38bdf8;">${pct}%</b>
                              </div>
                          `;
                      }
                  },
                  legend: {
                      orient: "vertical",
                      right: 6,
                      top: "middle",
                      type: "scroll",
                      itemWidth: 12,
                      itemHeight: 12,
                      itemGap: 8,
                      textStyle: {
                          fontSize: 11,
                          color: "#334155"
                      },
                      pageIconColor: "#2563eb",
                      pageTextStyle: { color: "#64748b", fontSize: 10 },
                      formatter: (name) => {
                          const it = areaItems.find(x => x.name === name);
                          const v = it ? it.value : 0;
                          const pct = totalAreas ? ((v / totalAreas) * 100).toFixed(1).replace(".", ",") : "0";
                          const shortName = getDisplayName(name);
                          return `${shortName}: ${fmtInt(v)} (${pct}%)`;
                      }
                  },
                  series: [
                      {
                          name: "Demora por Área",
                          type: "pie",
                          radius: ["40%", "72%"],
                          center: ["28%", "50%"],
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
                                  fontSize: 13,
                                  fontWeight: "bold",
                                  color: "#1e293b",
                                  formatter: (p) => `${p.percent.toFixed(0)}%`
                              }
                          },
                          data: areaChartData
                      }
                  ]
              };
              resChartAreas.setOption(areasOption, true);
              resChartAreas.resize();
          }
      }
  };
'''

idx_end = code.rfind("})();")
assert idx_end != -1, "end of IIFE not found"
code = code[:idx_end] + resumen_func + "\n})();"

with open('js/demoras.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Successfully updated js/demoras.js!")
