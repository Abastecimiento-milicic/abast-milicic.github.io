/**
 * cumplimiento-arriba.js
 * Módulo complementario independiente para evaluar el "Cumplimiento Arriba"
 * (llegada efectiva a mina) en las obras 00365 (Río Tinto) y 00372 (Posco II).
 *
 * Mantiene intacto js/cumplimiento.js y se activa/desactiva mediante el botón
 * #cumpl_btnArriba.
 */

(function () {
  "use strict";

  const CSV_ARRIBA_URL = "data/Base_Final_365_372.csv";
  const XLSX_ARRIBA_URL = "data/Base_Final_365_372.xlsx";
  const TARGET_OBRAS = ["00365", "00372", "365", "372"];

  let isArribaActive = false;
  let arribaRawRows = null;
  let arribaHeaders = [];
  let isLoading = false;

  const COLORS = {
    blue: "#3b82f6",
    green: "#10b981",
    amber: "#f59e0b",
    red: "#ef4444",
    purple: "#7c3aed"
  };

  /* ============================
     HELPERS
  ============================ */
  const clean = (v) => (v ?? "").toString().trim();

  function setText(id, txt) {
    const el = document.getElementById(id);
    if (el) el.textContent = txt ?? "";
  }

  function toNumber(v) {
    let x = clean(v);
    if (!x) return 0;
    x = x.replace(/\s/g, "");
    if (x.includes(",")) x = x.replace(/\./g, "").replace(",", ".");
    const n = Number(x);
    return Number.isFinite(n) ? n : 0;
  }

  function toNumAny(v) {
    if (v == null) return NaN;
    if (typeof v === "number") return v;
    let s = String(v).trim();
    if (!s) return NaN;
    if (s.includes(",")) {
      s = s.replace(/\./g, "").replace(",", ".");
    }
    const n = parseFloat(s);
    return isNaN(n) ? NaN : n;
  }

  function fmtInt(n) {
    return Number(n || 0).toLocaleString("es-AR", { maximumFractionDigits: 0 });
  }

  function fmtPct01(x) {
    if (!isFinite(x)) return "-";
    return (x * 100).toFixed(1).replace(".", ",") + "%";
  }

  function _fmtPct(v) {
    if (v == null || isNaN(v)) return "";
    const n = Math.round(v * 10) / 10;
    return n.toString().replace(".", ",") + "%";
  }

  function _fmtNum1(v) {
    if (v == null || isNaN(v)) return "";
    const n = Math.round(v * 10) / 10;
    return n.toString().replace(".", ",");
  }

  function parseDateAny(s) {
    const t = clean(s);
    if (!t) return null;

    const slashIdx1 = t.indexOf("/");
    if (slashIdx1 !== -1) {
      const slashIdx2 = t.indexOf("/", slashIdx1 + 1);
      if (slashIdx2 !== -1) {
        const d = parseInt(t.substring(0, slashIdx1), 10);
        const m = parseInt(t.substring(slashIdx1 + 1, slashIdx2), 10);
        const y = parseInt(t.substring(slashIdx2 + 1, slashIdx2 + 5), 10);
        if (y > 1900 && m >= 1 && m <= 12 && d >= 1 && d <= 31) {
          return new Date(y, m - 1, d);
        }
      }
    }

    if (/^\d{4,5}$/.test(t)) {
      const serial = parseInt(t, 10);
      if (serial > 30000 && serial < 60000) {
        const utcDays = serial - 25569;
        const ms = utcDays * 86400 * 1000;
        const d = new Date(ms);
        return new Date(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate());
      }
    }

    let m = t.match(/^(\d{4})[\/\-](\d{1,2})[\/\-](\d{1,2})$/);
    if (m) return new Date(+m[1], +m[2] - 1, +m[3]);

    return null;
  }

  function monthKey(d) {
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
  }

  function getMonthKeyFromRow(r) {
    if (r._ym) return r._ym;
    const s = r["FECHA ENTREGA ESPERADA"];
    if (!s) return null;
    const t = clean(s);
    if (!t) return null;

    const slashIdx1 = t.indexOf("/");
    if (slashIdx1 !== -1) {
      const slashIdx2 = t.indexOf("/", slashIdx1 + 1);
      if (slashIdx2 !== -1) {
        const m = t.substring(slashIdx1 + 1, slashIdx2).padStart(2, "0");
        const y = t.substring(slashIdx2 + 1, slashIdx2 + 5);
        if (y.length === 4) return `${y}-${m}`;
      }
    }
    const d = parseDateAny(t);
    return d ? monthKey(d) : null;
  }

  function avgDelay(rows) {
    let s = 0, c = 0;
    for (let i = 0; i < rows.length; i++) {
      const r = rows[i];
      if (r._hasDemora) {
        s += r._demora;
        c++;
      }
    }
    return c ? (s / c) : NaN;
  }

  function getSelValues(id) {
    const sel = document.getElementById(id);
    if (!sel) return [];
    const vals = [...sel.selectedOptions].map(o => o.value);
    if (!vals.length || vals.includes("__ALL__")) return [];
    return vals.filter(v => v !== "");
  }

  function getHiddenChartMonths() {
    const listEl = document.getElementById("cumpl_filterMesesList");
    const hidden = new Set();
    if (listEl) {
      listEl.querySelectorAll('input[type="checkbox"]').forEach(chk => {
        if (!chk.checked) {
          hidden.add(chk.value);
        }
      });
    }
    return hidden;
  }

  /* ============================
     FETCH & PRELOAD DATA
  ============================ */
  let arribaLoadingPromise = null;

  async function loadArribaData(isPreload = false) {
    if (arribaRawRows) return arribaRawRows;
    if (arribaLoadingPromise) return arribaLoadingPromise;
    isLoading = true;

    const btn = document.getElementById("cumpl_btnArriba");
    const origText = btn ? btn.innerHTML : "";
    if (btn && !isPreload) btn.innerHTML = "⏳ Cargando datos arriba...";

    arribaLoadingPromise = (async () => {
      try {
        let rawData = null;
        let fields = [];

        // 1. Usar dataset compartido en memoria si ya fue cargado por Tablero (resumen.js)
        if (window._sharedArribaData && window._sharedArribaData.rows && window._sharedArribaData.rows.length) {
          rawData = window._sharedArribaData.rows;
          fields = window._sharedArribaData.headers || [];
        }

        // 2. Intentar cargar CSV con fetchWithCache + PapaParse
        if (!rawData) {
          try {
            const urlCsv = CSV_ARRIBA_URL + "?t=" + (window.CACHE_BUSTER || Date.now());
            let text = "";
            if (typeof window.fetchWithCache === "function") {
              text = await window.fetchWithCache(urlCsv);
            } else {
              const resp = await fetch(urlCsv);
              if (resp.ok) text = await resp.text();
            }

            if (text && text.length > 50 && !text.trim().startsWith("<")) {
              const parsed = Papa.parse(text, {
                header: true,
                delimiter: ";",
                skipEmptyLines: true,
                transformHeader: (h) => (h || "").trim().replace(/^\ufeff/, "")
              });
              if (parsed.data && parsed.data.length) {
                fields = parsed.meta.fields || [];
                rawData = parsed.data;
                window._sharedArribaData = { headers: fields, rows: rawData };
              }
            }
          } catch (eCsv) {
            console.warn("[Cumplimiento Arriba] CSV no disponible o error al parsear:", eCsv);
          }
        }

        // 3. Fallback a XLSX únicamente si CSV falló completamente
        if (!rawData && typeof ExcelJS !== "undefined") {
          try {
            const urlXlsx = XLSX_ARRIBA_URL + "?t=" + (window.CACHE_BUSTER || Date.now());
            const resp = await fetch(urlXlsx);
            if (resp.ok) {
              const buffer = await resp.arrayBuffer();
              const wb = new ExcelJS.Workbook();
              await wb.xlsx.load(buffer);
              const ws = wb.worksheets[0];
              const headers = [];
              const dataRows = [];
              ws.eachRow({ includeEmpty: false }, (row, rowNumber) => {
                if (rowNumber === 1) {
                  row.eachCell({ includeEmpty: true }, (cell, colNumber) => {
                    headers[colNumber - 1] = clean(cell.value).replace(/^\ufeff/, "");
                  });
                } else {
                  const obj = {};
                  row.eachCell({ includeEmpty: true }, (cell, colNumber) => {
                    const h = headers[colNumber - 1];
                    if (h) {
                      let v = cell.value;
                      if (v instanceof Date) {
                        v = `${String(v.getDate()).padStart(2, "0")}/${String(v.getMonth() + 1).padStart(2, "0")}/${v.getFullYear()}`;
                      } else if (v && typeof v === "object" && v.text) {
                        v = v.text;
                      } else if (v && typeof v === "object" && v.result !== undefined) {
                        v = v.result;
                      }
                      obj[h] = clean(v);
                    }
                  });
                  dataRows.push(obj);
                }
              });
              fields = headers;
              rawData = dataRows;
              window._sharedArribaData = { headers: fields, rows: rawData };
            }
          } catch (eXlsx) {
            console.error("[Cumplimiento Arriba] Error cargando XLSX:", eXlsx);
          }
        }

        if (!rawData || !rawData.length) {
          throw new Error("El archivo Base Final 365 372 no pudo cargarse o está vacío.");
        }

        arribaHeaders = fields;

        // Normalización y pre-cálculo rápido de campos numéricos y claves
        // 1. Filas de Mina Arriba para las obras 365 y 372
        const targetArribaRows = [];
        for (let i = 0; i < rawData.length; i++) {
          const r = rawData[i];
          const mk = r._ym || getMonthKeyFromRow(r);
          if (!mk || mk === "2025-09" || mk < "2025-10") continue;

          const c2Raw = clean(r["CLASIFICACION 2"]);
          const c2Upper = c2Raw.toUpperCase();
          const c2Norm = (c2Upper.includes("ALMACEN") || c2Upper.includes("ALMACÉN") || c2Upper.includes("EQUIPOS MENORES")) ? "ALMACÉN" : c2Raw;

          const at = toNumber(r["ENTREGADOS AT FINAL"]);
          const ft = toNumber(r["ENTREGADOS FT FINAL"]);
          const no = toNumber(r["NO ENTREGADOS FINAL"]);
          let comp = toNumber(r["COMPROMETIDOS"]);
          if (!comp) comp = at + ft + no;
          const dem = toNumAny(r["DEMORA FINAL"]);

          targetArribaRows.push({
            ...r,
            "CLASIFICACION 2": c2Norm,
            _ym: mk,
            _cliente: clean(r["CLIENTE"] || r["CLIENTE / OBRA"]),
            _clasif2: c2Norm,
            _gcoc: clean(r["GRUPO DE COMPRA OC"]),
            _centro: clean(r["CENTRO"]),
            _at: at,
            _ft: ft,
            _no: no,
            _comp: comp,
            _demora: isNaN(dem) ? 0 : dem,
            _hasDemora: (!isNaN(dem) && dem > 0)
          });
        }

        // 2. Filas de todas las demás obras desde la base estándar
        const stdData = (window.getCumplimientoData ? window.getCumplimientoData() : []);
        const otherStandardRows = [];
        for (let i = 0; i < stdData.length; i++) {
          const r = stdData[i];
          const cli = clean(r["CLIENTE"] || r["CLIENTE / OBRA"]);
          if (TARGET_OBRAS.some(t => cli.includes(t))) continue;

          const c2Raw = clean(r["CLASIFICACION 2"]);
          const c2Upper = c2Raw.toUpperCase();
          const c2Norm = (c2Upper.includes("ALMACEN") || c2Upper.includes("ALMACÉN") || c2Upper.includes("EQUIPOS MENORES")) ? "ALMACÉN" : c2Raw;

          const mk = r._ym || getMonthKeyFromRow(r);
          const at = toNumber(r["ENTREGADOS AT"]);
          const ft = toNumber(r["ENTREGADOS FT"]);
          const no = toNumber(r["NO ENTREGADOS"]);
          let comp = toNumber(r["COMPROMETIDOS"]);
          if (!comp) comp = at + ft + no;
          const dem = toNumAny(r["DIAS DE DEMORA"] || r["DEMORA FINAL"]);

          otherStandardRows.push({
            ...r,
            "CLIENTE": cli,
            "CLASIFICACION 2": c2Norm,
            "ENTREGADOS AT FINAL": r["ENTREGADOS AT"],
            "ENTREGADOS FT FINAL": r["ENTREGADOS FT"],
            "NO ENTREGADOS FINAL": r["NO ENTREGADOS"],
            "DEMORA FINAL": r["DIAS DE DEMORA"] || r["DEMORA FINAL"],
            "COMPROMETIDOS": r["COMPROMETIDOS"],
            _ym: mk,
            _cliente: cli,
            _clasif2: c2Norm,
            _gcoc: clean(r["GRUPO DE COMPRA OC"]),
            _centro: clean(r["CENTRO"]),
            _at: at,
            _ft: ft,
            _no: no,
            _comp: comp,
            _demora: isNaN(dem) ? 0 : dem,
            _hasDemora: (!isNaN(dem) && dem > 0)
          });
        }

        // 3. Dataset unificado
        arribaRawRows = otherStandardRows.concat(targetArribaRows);
        return arribaRawRows;
      } finally {
        isLoading = false;
        arribaLoadingPromise = null;
        if (btn && origText && btn.innerHTML.includes("Cargando")) {
          btn.innerHTML = origText;
        }
      }
    })();

    return arribaLoadingPromise;
  }

  /* ============================
     FILTRADO RÁPIDO
  ============================ */
  function getFilteredRows(noMes = false) {
    if (!arribaRawRows) return [];
    let rows = arribaRawRows;

    // Filtro CLIENTE / OBRA
    const selClientes = getSelValues("cumpl_clienteSelect");
    if (selClientes.length) {
      const setCli = new Set(selClientes);
      rows = rows.filter(r => setCli.has(r._cliente));
    }

    // Filtro CLASIFICACIÓN
    const selC2 = getSelValues("cumpl_clasif2Select");
    if (selC2.length) {
      const setC2 = new Set(selC2);
      rows = rows.filter(r => setC2.has(r._clasif2));
    }

    // Filtro GC OC
    const selGc = getSelValues("cumpl_gcocSelect");
    if (selGc.length) {
      const setGc = new Set(selGc);
      rows = rows.filter(r => setGc.has(r._gcoc));
    }

    // Filtro CENTRO
    const selCentros = getSelValues("centroSelect");
    if (selCentros.length) {
      const setCentros = new Set(selCentros);
      rows = rows.filter(r => setCentros.has(r._centro));
    }

    // Filtro MES
    if (!noMes) {
      const selMes = getSelValues("cumpl_mesSelect");
      if (selMes.length) {
        const setMes = new Set(selMes);
        rows = rows.filter(r => setMes.has(r._ym));
      }
    }

    return rows;
  }

  /* ============================
     CÁLCULO DE KPIS
  ============================ */
  function calcTotalsArriba(rows) {
    let at = 0, ft = 0, no = 0, total = 0;
    for (let i = 0; i < rows.length; i++) {
      const r = rows[i];
      at += (r._at || 0);
      ft += (r._ft || 0);
      no += (r._no || 0);
      total += (r._comp || 0);
    }
    if (!total) total = at + ft + no;
    return { at, ft, no, total };
  }

  function updateKPIsArriba() {
    const rowsBase = getFilteredRows(true); // Sin filtro de mes para acumulados

    // Filtrar para el acumulado: excluir el mes vigente y tomar los 12 meses anteriores
    const mSet = new Set();
    for (let i = 0; i < rowsBase.length; i++) {
      if (rowsBase[i]._ym) mSet.add(rowsBase[i]._ym);
    }
    const uniqueMonths = [...mSet].sort();
    if (uniqueMonths.length > 0) {
      uniqueMonths.pop();
    }
    const allowedMonths = new Set(uniqueMonths.slice(-12));
    const rowsAcumulado = rowsBase.filter(r => allowedMonths.has(r._ym));

    const t = calcTotalsArriba(rowsAcumulado);

    const pctAT = t.total ? t.at / t.total : NaN;
    const pctFT = t.total ? t.ft / t.total : NaN;
    const pctNO = t.total ? t.no / t.total : NaN;

    // Tarjeta ACUMULADO (12 meses)
    const colAcumTag = document.querySelector(".col-acum .cumpl-col-tag");
    if (colAcumTag) colAcumTag.textContent = "ACUMULADO (MINA ARRIBA)";
    const colAcumSub = document.querySelector(".col-acum .cumpl-col-sub");
    if (colAcumSub) colAcumSub.textContent = "Últimos 12 meses (365 y 372 en Mina)";

    setText("cumpl_kpiTotal", fmtInt(t.total));

    setText("cumpl_kpiATpct", fmtPct01(pctAT));
    setText("cumpl_kpiATqty", `Cant: ${fmtInt(t.at)}`);
    const elAT = document.getElementById("cumpl_kpiATpct");
    if (elAT) elAT.style.setProperty("color", (isFinite(pctAT) && (Math.round(pctAT * 1000) / 10) >= 78) ? "#16a34a" : "#ef4444", "important");

    setText("cumpl_kpiFTpct", fmtPct01(pctFT));
    setText("cumpl_kpiFTqty", `Cant: ${fmtInt(t.ft)}`);

    setText("cumpl_kpiNOpct", fmtPct01(pctNO));
    setText("cumpl_kpiNOqty", `Cant: ${fmtInt(t.no)}`);

    const avgG = avgDelay(rowsAcumulado);
    setText("cumpl_kpiDemoraAvg", isNaN(avgG) ? "-" : (Math.round(avgG) + " d"));
    const elDemG = document.getElementById("cumpl_kpiDemoraAvg");
    if (elDemG) elDemG.style.color = (!isNaN(avgG) && avgG > 7) ? "#ef4444" : "#16a34a";

    // Tarjeta MES SELECCIONADO
    const ms = getSelValues("cumpl_mesSelect");
    let rowsMes = [];
    if (ms.length) {
      const setMes = new Set(ms);
      rowsMes = rowsBase.filter(r => setMes.has(r._ym));
    } else {
      const allMonths = [...mSet].sort();
      const lastMonth = allMonths[allMonths.length - 1];
      if (lastMonth) {
        rowsMes = rowsBase.filter(r => r._ym === lastMonth);
      } else {
        rowsMes = rowsBase;
      }
    }

    const tm = calcTotalsArriba(rowsMes);
    const pctATm = tm.total ? tm.at / tm.total : NaN;
    const pctFTm = tm.total ? tm.ft / tm.total : NaN;
    const pctNOm = tm.total ? tm.no / tm.total : NaN;

    setText("cumpl_kpiTotalMes", fmtInt(tm.total));

    setText("cumpl_kpiATmes", fmtPct01(pctATm));
    const elATm = document.getElementById("cumpl_kpiATmes");
    if (elATm) elATm.style.setProperty("color", (isFinite(pctATm) && (Math.round(pctATm * 1000) / 10) >= 78) ? "#16a34a" : "#ef4444", "important");
    setText("cumpl_kpiATmesSub", `Cant: ${fmtInt(tm.at)}`);

    setText("cumpl_kpiFTmes", fmtPct01(pctFTm));
    setText("cumpl_kpiFTmesSub", `Cant: ${fmtInt(tm.ft)}`);

    setText("cumpl_kpiNOmes", fmtPct01(pctNOm));
    setText("cumpl_kpiNOmesSub", `Cant: ${fmtInt(tm.no)}`);

    const avgM = avgDelay(rowsMes);
    setText("cumpl_kpiDemoraMes", isNaN(avgM) ? "-" : (Math.round(avgM) + " d"));
    const elDemM = document.getElementById("cumpl_kpiDemoraMes");
    if (elDemM) elDemM.style.color = (!isNaN(avgM) && avgM > 7) ? "#ef4444" : "#16a34a";
  }

  /* ============================
     GRÁFICOS ECHARTS (ESTILO IDÉNTICO A CUMPLIMIENTO.JS)
  ============================ */
  function renderChartsArriba() {
    if (!window.echarts) return;
    const rows = getFilteredRows(true);

    const agg = new Map();
    const monthsSet = new Set();

    for (let i = 0; i < rows.length; i++) {
      const r = rows[i];
      const mk = r._ym;
      if (!mk) continue;
      monthsSet.add(mk);

      let c = agg.get(mk);
      if (!c) {
        c = { at: 0, ft: 0, no: 0, comp: 0, demSum: 0, demCnt: 0 };
        agg.set(mk, c);
      }

      c.at += (r._at || 0);
      c.ft += (r._ft || 0);
      c.no += (r._no || 0);
      c.comp += (r._comp || 0);

      if (r._hasDemora) {
        c.demSum += r._demora;
        c.demCnt += 1;
      }
    }

    const hiddenMonths = getHiddenChartMonths();
    const months = [...monthsSet].sort().filter(m => !hiddenMonths.has(m));

    const elMes = document.getElementById("cumpl_chartMes");
    const elTend = document.getElementById("cumpl_chartTendencia");
    const chartMes = (elMes && window.echarts) ? (echarts.getInstanceByDom(elMes) || echarts.init(elMes)) : null;
    const chartTendencia = (elTend && window.echarts) ? (echarts.getInstanceByDom(elTend) || echarts.init(elTend)) : null;

    if (months.length === 0) {
      if (chartMes) {
        chartMes.clear();
        chartMes.setOption({
          title: {
            show: true,
            text: "No hay meses seleccionados para mostrar",
            left: "center",
            top: "middle",
            textStyle: { color: "#64748b", fontSize: 13, fontWeight: "normal" }
          },
          xAxis: { show: false, type: "category", data: [] },
          yAxis: { show: false, type: "value" },
          series: []
        }, true);
      }
      if (chartTendencia) {
        chartTendencia.clear();
        chartTendencia.setOption({
          title: {
            show: true,
            text: "No hay meses seleccionados para mostrar",
            left: "center",
            top: "middle",
            textStyle: { color: "#64748b", fontSize: 13, fontWeight: "normal" }
          },
          xAxis: { show: false, type: "category", data: [] },
          yAxis: { show: false, type: "value" },
          series: []
        }, true);
      }
      return;
    }

    const qAT = months.map(m => agg.get(m)?.at ?? 0);
    const qFT = months.map(m => agg.get(m)?.ft ?? 0);
    const qNO = months.map(m => agg.get(m)?.no ?? 0);

    const pAT = qAT.map((v, i) => { const t = qAT[i] + qFT[i] + qNO[i]; return t ? (v / t) * 100 : 0; });
    const pFT = qFT.map((v, i) => { const t = qAT[i] + qFT[i] + qNO[i]; return t ? (v / t) * 100 : 0; });
    const pNO = qNO.map((v, i) => { const t = qAT[i] + qFT[i] + qNO[i]; return t ? (v / t) * 100 : 0; });

    const avgDem = months.map(m => {
      const c = agg.get(m);
      return (c && c.demCnt) ? (c.demSum / c.demCnt) : null;
    });

    const pAT_acum = [];
    let sumATAcum = 0, sumCompAcum = 0;
    for (let i = 0; i < months.length; i++) {
      const c = agg.get(months[i]);
      sumATAcum += (c?.at ?? 0);
      sumCompAcum += (c?.comp || (c?.at + c?.ft + c?.no) || 0);
      pAT_acum.push(sumCompAcum ? (sumATAcum / sumCompAcum) * 100 : 0);
    }

    // Construcción de la línea objetivo segmentada (Obj 78% para 2026, Obj 75% para 2025)
    const lineSegments = [];
    if (months.length === 1) {
      const anoActual = parseInt(months[0].substring(0, 4), 10);
      const hActual = (anoActual >= 2026) ? 78 : 75;
      lineSegments.push({
        yAxis: hActual,
        label: {
          show: true,
          formatter: `Obj ${hActual}%`,
          fontWeight: 800,
          fontSize: 11,
          position: "end",
          backgroundColor: "#374151",
          color: "#fff",
          padding: [4, 6],
          borderRadius: 4
        }
      });
    } else {
      for (let i = 0; i < months.length - 1; i++) {
        const anoActual = parseInt(months[i].substring(0, 4), 10);
        const hActual = (anoActual >= 2026) ? 78 : 75;
        const isLastSegment = (i === months.length - 2);
        const anoSig = parseInt(months[i + 1].substring(0, 4), 10);
        const hSig = (anoSig >= 2026) ? 78 : 75;
        const showLabelOnHorizontal = isLastSegment && (hActual === hSig);

        lineSegments.push([
          { 
            xAxis: i, 
            yAxis: hActual, 
            label: showLabelOnHorizontal ? {
              show: true,
              formatter: `Obj ${hSig}%`,
              fontWeight: 800,
              fontSize: 11,
              position: "end",
              offset: [35, 0],
              backgroundColor: "#374151",
              color: "#fff",
              padding: [4, 6],
              borderRadius: 4
            } : { show: false }
          },
          { xAxis: i + 1, yAxis: hActual }
        ]);

        if (hActual !== hSig) {
          const showLabelOnVertical = isLastSegment;
          lineSegments.push([
            { 
              xAxis: i + 1, 
              yAxis: hActual, 
              label: showLabelOnVertical ? {
                show: true,
                formatter: `Obj ${hSig}%`,
                fontWeight: 800,
                fontSize: 11,
                position: "end",
                offset: [35, 0],
                backgroundColor: "#374151",
                color: "#fff",
                padding: [4, 6],
                borderRadius: 4
              } : { show: false }
            },
            { xAxis: i + 1, yAxis: hSig }
          ]);
        }
      }
    }

    // 1. Gráfico Stacked Bar (Mensual)
    if (chartMes) {
      const optionMes = {
        title: { show: false },
        animation: true,
        animationDuration: 800,
        animationDurationUpdate: 600,
        animationEasing: "cubicOut",
        animationEasingUpdate: "cubicOut",
        grid: { left: 56, right: 70, top: 55, bottom: 62 },
        tooltip: {
          trigger: "axis",
          axisPointer: { type: "shadow" },
          confine: true,
          backgroundColor: "transparent",
          borderColor: "transparent",
          shadowColor: "transparent",
          shadowBlur: 0,
          borderWidth: 0,
          padding: 0,
          formatter: (params) => {
            const axis = params?.[0]?.axisValue ?? "";
            const byName = Object.fromEntries(params.map(p => [p.seriesName, p]));
            const at = byName["Entregados AT"];
            const ft = byName["Entregados FT"];
            const ne = byName["No entregados"];
            const acum = byName["%AT Acumulado"];
            const dem = byName["Promedio días de demora"];

            let html = `
              <div style="font-family: var(--font-body), sans-serif; padding: 10px 14px; min-width: 190px; background: #ffffff; border-radius: 8px; box-shadow: var(--shadow-xl); border: 1.5px solid var(--border-light); color: var(--text-main);">
                <div style="font-family: var(--font-main), sans-serif; font-weight: 800; font-size: 0.9rem; margin-bottom: 8px; border-bottom: 1.5px solid var(--border-light); padding-bottom: 6px; color: var(--text-main); letter-spacing: 0.02em;">
                  📅 ${axis}
                </div>
                <div style="display: flex; flex-direction: column; gap: 6px;">
            `;

            if (at) {
              html += `
                <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.8rem; gap: 15px;">
                  <span style="display: inline-flex; align-items: center; gap: 6px; font-weight: 600; color: var(--text-muted);">
                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #10b981;"></span>
                    A Tiempo
                  </span>
                  <span style="font-weight: 800; color: var(--text-main);">${fmtInt(qAT[at.dataIndex])} <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 500;">(${_fmtNum1(at.value)}%)</span></span>
                </div>
              `;
            }
            if (ft) {
              html += `
                <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.8rem; gap: 15px;">
                  <span style="display: inline-flex; align-items: center; gap: 6px; font-weight: 600; color: var(--text-muted);">
                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #f59e0b;"></span>
                    Fuera Tiempo
                  </span>
                  <span style="font-weight: 800; color: var(--text-main);">${fmtInt(qFT[ft.dataIndex])} <span style="font-size: 0.75rem; color: var(--text-muted); font-weight: 500;">(${_fmtNum1(ft.value)}%)</span></span>
                </div>
              `;
            }
            if (ne) {
              html += `
                <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.8rem; gap: 15px;">
                  <span style="display: inline-flex; align-items: center; gap: 6px; font-weight: 600; color: var(--text-muted);">
                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #ef4444;"></span>
                    No Entregados
                  </span>
                  <span style="font-weight: 800; color: #ef4444;">${fmtInt(qNO[ne.dataIndex])} <span style="font-size: 0.75rem; color: #ef4444; font-weight: 600;">(${_fmtNum1(ne.value)}%)</span></span>
                </div>
              `;
            }
            if (acum) {
              html += `
                <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.8rem; border-top: 1.5px solid var(--border-light); padding-top: 6px; margin-top: 2px; gap: 15px;">
                  <span style="display: inline-flex; align-items: center; gap: 6px; font-weight: 600; color: var(--text-muted);">
                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #7c3aed;"></span>
                    % AT Acum.
                  </span>
                  <span style="font-weight: 800; color: #7c3aed;">${_fmtNum1(acum.value)}%</span>
                </div>
              `;
            }
            if (dem && dem.value != null && !isNaN(dem.value)) {
              html += `
                <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.8rem; border-top: 1.5px solid var(--border-light); padding-top: 6px; margin-top: 2px; gap: 15px;">
                  <span style="display: inline-flex; align-items: center; gap: 6px; font-weight: 600; color: var(--text-muted);">
                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #3b82f6;"></span>
                    Demora Prom.
                  </span>
                  <span style="font-weight: 800; color: #2563eb;">${Math.round(dem.value)} días</span>
                </div>
              `;
            }

            html += `
                </div>
              </div>
            `;
            return html;
          }
        },
        legend: {
          bottom: 12,
          left: "center",
          itemWidth: 14,
          itemHeight: 10,
          textStyle: { fontWeight: 800 }
        },
        xAxis: {
          type: "category",
          data: months,
          axisTick: { alignWithLabel: true },
          axisLabel: {
            interval: 0,
            rotate: 0,
            fontSize: 10,
            fontWeight: 700
          }
        },
        yAxis: [
          {
            type: "value",
            min: 0,
            max: 100,
            axisLabel: { formatter: "{value}%" },
            splitLine: { lineStyle: { color: "rgba(15,23,42,0.10)" } }
          },
          {
            type: "value",
            name: "Días de demora",
            nameTextStyle: { padding: [0, 0, 15, 0] },
            position: "right",
            axisLabel: { fontWeight: 700 },
            splitLine: { show: false },
            boundaryGap: [0, '25%']
          }
        ],
        series: [
          {
            name: "Entregados AT",
            type: "bar",
            stack: "pct",
            data: pAT.map(v => {
              const val = +(+v).toFixed(4);
              if (Math.round(val) < 78) {
                return {
                  value: val,
                  itemStyle: {
                    borderColor: '#dc2626',
                    borderWidth: 2,
                    borderType: 'solid',
                    borderRadius: [6, 6, 0, 0]
                  }
                };
              }
              return val;
            }),
            barMaxWidth: 52,
            itemStyle: {
              color: {
                type: "linear",
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [
                  { offset: 0, color: "#10b981" },
                  { offset: 1, color: "#047857" }
                ]
              },
              borderRadius: [6, 6, 0, 0]
            },
            label: {
              show: true,
              position: "insideBottom", 
              distance: 10,
              fontWeight: 900,
              fontSize: 11,
              lineHeight: 12,
              formatter: (p) => {
                const i = p.dataIndex;
                const pct = +p.value || 0;
                const q = (qAT)[i] || 0;
                if (!q) return "";
                if (pct < 6) return "";
                const pctRound = Math.round(pct);
                if (pctRound < 78) return `{warn|${fmtInt(q)}\n⚠ (${pctRound}%)}`;
                return `${fmtInt(q)}\n(${pctRound}%)`;
              },
              rich: {
                warn: {
                  fontWeight: 950,
                  color: "#7f1d1d",
                  backgroundColor: "rgba(254, 202, 202, 0.9)",
                  borderColor: "#b91c1c",
                  borderWidth: 1.5,
                  borderRadius: 4,
                  padding: [2, 4],
                  fontSize: 11,
                  lineHeight: 14,
                  align: 'center'
                }
              },
              color: "#ffffff",
              backgroundColor: "rgba(0,0,0,0.15)",
              borderRadius: 4,
              padding: [2, 4]
            },
            labelLayout: { hideOverlap: true },
            emphasis: { disabled: true },
            markLine: {
              silent: true,
              symbol: ["none", "none"],
              lineStyle: { type: "dashed", width: 2, color: "#374151" },
              clip: false,
              data: lineSegments
            },
            z: 1,
            zlevel: 0
          },
          {
            name: "Entregados FT",
            type: "bar",
            stack: "pct",
            data: pFT.map(v => +(+v).toFixed(4)),
            barMaxWidth: 52,
            itemStyle: {
              color: {
                type: "linear",
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [
                  { offset: 0, color: "#f59e0b" },
                  { offset: 1, color: "#d97706" }
                ]
              }
            },
            label: {
              show: true,
              position: "insideTop", 
              distance: 4,
              color: "#111",
              fontWeight: 950,
              fontSize: 11,
              lineHeight: 12,
              formatter: (p) => {
                const i = p.dataIndex;
                const pct = +p.data || 0;
                const q = (qFT)[i] || 0;
                if (!q) return "";
                if (pct < 8) return ""; 
                return `${fmtInt(q)}\n(${Math.round(pct)}%)`;
              }
            },
            labelLayout: { hideOverlap: true },
            emphasis: { disabled: true },
            z: 1,
            zlevel: 0
          },
          {
            name: "No entregados",
            type: "bar",
            stack: "pct",
            data: pNO.map(v => +(+v).toFixed(4)),
            barMaxWidth: 52,
            itemStyle: {
              color: {
                type: "linear",
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [
                  { offset: 0, color: "#f87171" },
                  { offset: 1, color: "#ef4444" }
                ]
              }
            },
            label: {
              show: true,
              position: "top", 
              distance: 2,
              color: "#fff",
              fontWeight: 900,
              fontSize: 11,
              lineHeight: 12,
              backgroundColor: "rgba(239, 68, 68, 0.9)", 
              padding: [2, 4],
              borderRadius: 3,
              formatter: (p) => {
                const i = p.dataIndex;
                const pct = +p.data || 0;
                const q = (qNO)[i] || 0;
                if (!q) return "";
                return `${fmtInt(q)} (${Math.round(pct)}%)`;
              }
            },
            labelLayout: { hideOverlap: false },
            emphasis: { disabled: true },
            z: 1,
            zlevel: 0
          },
          {
            name: "%AT Acumulado",
            type: "line",
            data: pAT_acum.map(v => +(+v).toFixed(2)),
            showSymbol: true,         
            symbol: "circle",         
            symbolSize: 7,            
            showAllSymbol: true,      
            lineStyle: { 
              width: 3.5,         
              type: "solid",      
              color: "#7c3aed"    
            },
            itemStyle: { color: "#7c3aed", borderColor: "#fff", borderWidth: 2 },
            label: {
              show: true,             
              position: "bottom",   
              distance: 6,          
              formatter: (p) => {
                const val = +p.data;
                if (val == null || isNaN(val)) return "";
                return val.toFixed(2).replace(".", ",") + "%";
              },
              backgroundColor: "rgba(255, 255, 255, 0.85)", 
              padding: [2, 4],                             
              borderRadius: 3,                             
              borderColor: "rgba(124, 58, 237, 0.25)",      
              borderWidth: 1,
              textStyle: { fontWeight: 850, color: "#6d28d9", fontSize: 10 }
            },
            emphasis: {
              disabled: false,
              scale: false, 
              label: {
                show: true, 
                position: "bottom",
                formatter: (p) => {
                  const val = +p.data;
                  if (val == null || isNaN(val)) return "";
                  return val.toFixed(2).replace(".", ",") + "%";
                },
                textStyle: { fontWeight: 850, color: "#6d28d9", fontSize: 10 }
              }
            },
            z: 6
          },
          {
            name: "Promedio días de demora",
            type: "line",
            yAxisIndex: 1,
            data: avgDem,
            symbol: "circle",
            symbolSize: 7,          
            showSymbol: true,       
            connectNulls: true,
            lineStyle: { width: 3, color: COLORS.blue },
            itemStyle: { color: COLORS.blue, borderColor: "#fff", borderWidth: 2 },
            label: {
              show: true,
              position: "top",      
              distance: 8,
              backgroundColor: "rgba(255,255,255,0.85)", 
              padding: [2, 4],
              borderRadius: 4,
              fontWeight: 950,
              color: "#0b1220",
              formatter: (p) => (p.data == null || isNaN(p.data)) ? "" : `${Math.round(p.data)} d`
            },
            markLine: {
              silent: true,
              symbol: ["none", "none"],
              label: {
                show: true,
                formatter: "Lím 7 d",
                fontWeight: 800,
                fontSize: 11,
                position: "end",
                backgroundColor: '#374151',
                color: '#fff',
                padding: [4, 6],
                borderRadius: 4
              },
              lineStyle: { type: "dashed", width: 2, color: "#374151" },
              data: [{ yAxis: 7 }]
            },
            z: 10
          }
        ]
      };
      chartMes.setOption(optionMes, true);
    }

    // 2. Gráfico Tendencia (Con Línea Acumulado y SIN Línea de No Entregados)
    if (chartTendencia) {
      const optionTend = {
        title: { show: false },
        animation: true,
        animationDuration: 800,
        animationDurationUpdate: 600,
        animationEasing: "cubicOut",
        animationEasingUpdate: "cubicOut",
        grid: { left: 56, right: 18, top: 16, bottom: 62 },
        tooltip: {
          trigger: "axis",
          confine: true,
          backgroundColor: "transparent",
          borderColor: "transparent",
          shadowColor: "transparent",
          shadowBlur: 0,
          borderWidth: 0,
          padding: 0,
          formatter: (params) => {
            const axis = params?.[0]?.axisValue ?? "";
            let html = `
              <div style="font-family: var(--font-body), sans-serif; padding: 10px 14px; min-width: 190px; background: #ffffff; border-radius: 8px; box-shadow: var(--shadow-xl); border: 1.5px solid var(--border-light); color: var(--text-main);">
                <div style="font-family: var(--font-main), sans-serif; font-weight: 800; font-size: 0.9rem; margin-bottom: 8px; border-bottom: 1.5px solid var(--border-light); padding-bottom: 6px; color: var(--text-main); letter-spacing: 0.02em;">
                  📅 Tendencia: ${axis}
                </div>
                <div style="display: flex; flex-direction: column; gap: 6px;">
            `;
            for (const p of params) {
              const color = p.color || "#0d9488";
              html += `
                <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.8rem; gap: 15px;">
                  <span style="display: inline-flex; align-items: center; gap: 6px; font-weight: 600; color: var(--text-muted);">
                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: ${color};"></span>
                    ${p.seriesName}
                  </span>
                  <span style="font-weight: 800; color: var(--text-main);">${_fmtNum1(p.data)}%</span>
                </div>
              `;
            }
            html += `
                </div>
              </div>
            `;
            return html;
          }
        },
        legend: {
          bottom: 12,
          left: "center",
          itemWidth: 14,
          itemHeight: 10,
          textStyle: { fontWeight: 800 }
        },
        xAxis: {
          type: "category",
          data: months,
          axisLabel: {
            interval: 0,
            rotate: 0,
            fontSize: 10,
            fontWeight: 700
          }
        },
        yAxis: {
          type: "value",
          min: 0, max: 100,
          axisLabel: { formatter: "{value}%" },
          splitLine: { lineStyle: { color: "rgba(15, 23, 42, 0.10)" } }
        },
        series: [
          {
            name: "A Tiempo %",
            type: "line",
            data: pAT.map(v => +(+v).toFixed(2)),
            symbolSize: 7,
            lineStyle: { width: 3, color: COLORS.green },
            itemStyle: { color: COLORS.green, borderColor: "#fff", borderWidth: 2 },
            label: {
              show: true,
              position: "top",
              formatter: (p) => {
                const v = +p.data || 0;
                const vRound1 = Math.round(v * 10) / 10;
                return (vRound1 < 78) ? `{warn|⚠ ${_fmtPct(v)}}` : `{ok|${_fmtPct(v)}}`;
              },
              rich: {
                ok: { fontWeight: 900, color: COLORS.green },
                warn: { fontWeight: 950, color: "#7f1d1d", backgroundColor: "rgba(239,68,68,0.18)", borderColor: "#ef4444", borderWidth: 1, borderRadius: 4, padding: [2, 4] }
              }
            },
            zlevel: 5, z: 5
          },
          {
            name: "Fuera Tiempo %",
            type: "line",
            data: pFT.map(v => +(+v).toFixed(2)),
            symbolSize: 7,
            lineStyle: { width: 3, color: COLORS.amber },
            itemStyle: { color: COLORS.amber, borderColor: "#fff", borderWidth: 2 },
            label: { show: true, position: "top", fontWeight: 900, formatter: (p) => _fmtPct(p.data) },
            zlevel: 5, z: 5
          },
          {
            name: "%AT Acumulado",
            type: "line",
            data: pAT_acum.map(v => +(+v).toFixed(2)),
            symbolSize: 7,
            lineStyle: { width: 3.5, color: COLORS.purple },
            itemStyle: { color: COLORS.purple, borderColor: "#fff", borderWidth: 2 },
            label: {
              show: true,
              position: "bottom",
              distance: 6,
              formatter: (p) => _fmtPct(p.data),
              backgroundColor: "rgba(255, 255, 255, 0.9)",
              padding: [2, 4],
              borderRadius: 3,
              borderColor: "rgba(124, 58, 237, 0.3)",
              borderWidth: 1,
              color: "#6d28d9",
              fontWeight: 900
            },
            zlevel: 6, z: 6
          }
        ]
      };
      chartTendencia.setOption(optionTend, true);
    }
  }

  /* ============================
     APPLY ALL ARRIBA
  ============================ */
  function applyArribaAll() {
    if (!isArribaActive) return;
    updateKPIsArriba();
    renderChartsArriba();
  }

  /* ============================
     DESCARGA NO ENTREGADOS ARRIBA
  ============================ */
  function downloadNoEntregadosArriba() {
    const rows = getFilteredRows(false);
    const noRows = rows.filter(r => toNumber(r["NO ENTREGADOS FINAL"]) > 0);

    if (!noRows.length) {
      alert("No hay NO ENTREGADOS en Mina para el filtro actual.");
      return;
    }

    // Asegurar que cada fila tenga la columna LOTE explícita
    noRows.forEach(r => {
      if (!r["LOTE"]) {
        r["LOTE"] = r["MB51 para consultas 2.Lote"] || r["Lote"] || "";
      }
    });

    let cols = arribaHeaders.length ? [...arribaHeaders] : Object.keys(noRows[0]);
    if (!cols.includes("LOTE")) {
      const idxDesc = cols.indexOf("DESCRIPCION ITEM");
      if (idxDesc !== -1) {
        cols.splice(idxDesc + 1, 0, "LOTE");
      } else {
        cols.unshift("LOTE");
      }
    }

    const escapeCSV = (v) => {
      const s = (v ?? "").toString();
      if (/[;"\n\r]/.test(s)) return `"${s.replace(/"/g, '""')}"`;
      return s;
    };

    const headerLine = cols.map(escapeCSV).join(";");
    const dataLines = noRows.map(r => cols.map(c => escapeCSV(r[c])).join(";"));
    const csvContent = "\ufeff" + [headerLine, ...dataLines].join("\r\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `NO_ENTREGADOS_MINA_ARRIBA_${Date.now()}.csv`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  /* ============================
     TOGGLE ARRIBA MODE
  ============================ */
  async function toggleArribaMode() {
    const btn = document.getElementById("cumpl_btnArriba");
    const sw = document.getElementById("cumpl_switchArriba");
    const row = document.getElementById("cumpl_toggleRowArriba");

    if (!isArribaActive) {
      // Feedback visual instantáneo (0ms)
      if (sw) sw.classList.add("active");
      if (row) row.classList.add("active");
      if (btn) {
        btn.classList.add("btn-active");
        btn.innerHTML = "↩ Volver a cumplimiento estándar";
      }

      if (!arribaRawRows) {
        if (sw) sw.classList.add("loading");
        try {
          await loadArribaData();
        } catch (err) {
          console.error("[Cumplimiento Arriba] Error al cargar modo arriba:", err);
          if (sw) {
            sw.classList.remove("active");
            sw.classList.remove("loading");
          }
          if (row) row.classList.remove("active");
          if (btn) {
            btn.classList.remove("btn-active");
            btn.innerHTML = "🏔️ Medir cumplimiento arriba";
          }
          alert("Error al cargar datos de Medición Arriba: " + err.message);
          return;
        } finally {
          if (sw) sw.classList.remove("loading");
        }
      }

      isArribaActive = true;
      applyArribaAll();
    } else {
      isArribaActive = false;

      if (btn) {
        btn.classList.remove("btn-active");
        btn.innerHTML = "🏔️ Medir cumplimiento arriba";
      }
      if (sw) {
        sw.classList.remove("active");
        sw.classList.remove("loading");
      }
      if (row) {
        row.classList.remove("active");
      }

      const colAcumTag = document.querySelector(".col-acum .cumpl-col-tag");
      if (colAcumTag) colAcumTag.textContent = "ACUMULADO";
      const colAcumSub = document.querySelector(".col-acum .cumpl-col-sub");
      if (colAcumSub) colAcumSub.textContent = "Últimos 12 meses";

      if (typeof window.reapplyCumplimientoAll === "function") {
        window.reapplyCumplimientoAll();
      } else {
        const selCliente = document.getElementById("cumpl_clienteSelect");
        if (selCliente) {
          selCliente.dispatchEvent(new Event("change"));
        }
      }
    }
  }

  window.toggleCumplArribaMode = toggleArribaMode;
  window.isCumplArribaActive = () => isArribaActive;
  window.applyCumplArribaAll = applyArribaAll;

  /* ============================
     PRELOAD EN SEGUNDO PLANO
  ============================ */
  function scheduleBackgroundPreload() {
    const trigger = () => {
      if (arribaRawRows || arribaLoadingPromise) return;
      loadArribaData(true).catch(e => {
        console.warn("[Cumplimiento Arriba] Preload silencioso:", e);
      });
    };

    if (typeof window.requestIdleCallback === "function") {
      window.requestIdleCallback(() => setTimeout(trigger, 400), { timeout: 3000 });
    } else {
      setTimeout(trigger, 1200);
    }
  }

  window.addEventListener("cumplimientoDataReady", () => {
    scheduleBackgroundPreload();
  });

  /* ============================
     INIT & EVENT LISTENERS
  ============================ */
  function initArriba() {
    const btn = document.getElementById("cumpl_btnArriba");
    if (btn) {
      btn.addEventListener("click", () => {
        toggleArribaMode();
      });
    }

    const filterIds = [
      "cumpl_clienteSelect",
      "cumpl_clasif2Select",
      "cumpl_gcocSelect",
      "centroSelect",
      "cumpl_mesSelect"
    ];

    filterIds.forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener("change", () => {
          if (isArribaActive) {
            setTimeout(() => {
              if (isArribaActive) applyArribaAll();
            }, 25);
          }
        });
      }
    });

    // Sincronizar el filtro de meses del gráfico (embudo de meses visibles)
    const filterMesesDropdown = document.getElementById("cumpl_filterMesesDropdown");
    if (filterMesesDropdown) {
      filterMesesDropdown.addEventListener("change", () => {
        if (isArribaActive) {
          setTimeout(() => {
            if (isArribaActive) applyArribaAll();
          }, 25);
        }
      });
      filterMesesDropdown.addEventListener("click", (e) => {
        const id = e.target ? e.target.id : "";
        if (id === "cumpl_filterMesesSelectAll" || id === "cumpl_filterMesesInvert" || id === "cumpl_filterMesesReset") {
          if (isArribaActive) {
            setTimeout(() => {
              if (isArribaActive) applyArribaAll();
            }, 25);
          }
        }
      });
    }

    const btnResetMeses = document.getElementById("cumpl_filterMesesReset");
    if (btnResetMeses) {
      btnResetMeses.addEventListener("click", () => {
        if (isArribaActive) {
          setTimeout(() => {
            if (isArribaActive) applyArribaAll();
          }, 25);
        }
      });
    }

    const btnDownloadNO = document.getElementById("cumpl_btnDownloadNO");
    if (btnDownloadNO) {
      btnDownloadNO.addEventListener("click", (e) => {
        if (isArribaActive) {
          e.stopImmediatePropagation();
          e.preventDefault();
          downloadNoEntregadosArriba();
        }
      }, true);
    }

    // Iniciar intento de preload en background
    scheduleBackgroundPreload();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initArriba);
  } else {
    initArriba();
  }

})();
