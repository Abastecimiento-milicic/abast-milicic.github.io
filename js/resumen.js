/**
 * resumen.js
 * Módulo para la pestaña "RESUMEN" (Pantallazo Ejecutivo por Obra)
 * Unifica Análisis MM (cruzado con STO NULO) y Cumplimiento de Pedidos (Acumulado 12M vs Mensual).
 */

(function () {
  "use strict";

  const CSV_MM_URL = "data/ANALISIS-MM.csv";
  const CSV_STONULO_URL = "data/STO NULO.csv";
  const CSV_CUMPL_URL = "data/CUMPLIMIENTO_OPTIMIZADO.csv";
  const DELIM = ";";

  let mmRawData = null;
  let mmHeaders = [];
  let stoNuloRawData = null;
  let stoNuloHeaders = [];
  let cumplRawData = null;
  let cumplHeaders = [];
  let isDataLoading = false;

  // Clave / Códigos normalizados de obra a nombres representativos
  const OBRA_MAP = {
    "26": "00026 - SANTA FE",
    "35": "00035 - SAN LUIS",
    "223": "00223 - COMP AMB SANTA FE",
    "314": "00314 - CASA OLAVARRIA",
    "341": "00341 - MOV SUELOS SAN LUIS",
    "365": "00365 - RIO TINTO",
    "368": "00368 - ACUEDUCTO TBH",
    "372": "00372 - UTE POSCO II",
    "374": "00374 - TERMINAL PUNTA COLORADA",
    "375": "00375 - OLEODUCTO PR-LP",
    "376": "00376 - VELADERO FASE 8B",
    "377": "00377 - YPF 3ER LOOP",
    "378": "00378 - OLEODUCTO PRINGLES",
    "379": "00379 - VELADERO FASE 8C"
  };

  const MES_NOMBRES = {
    "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril",
    "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
    "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
  };

  const clean = (v) => (v ?? "").toString().replace(/^\uFEFF/, "").replace(/\s+/g, " ").trim();

  function toNumber(v) {
    let x = clean(v);
    if (!x) return 0;
    x = x.replace(/\s/g, "");
    if (x.includes(",")) x = x.replace(/\./g, "").replace(",", ".");
    const n = Number(x);
    return Number.isFinite(n) ? n : 0;
  }

  function fmtInt(n) {
    return Number(n || 0).toLocaleString("es-AR", { maximumFractionDigits: 0 });
  }

  function fmtPct01(n) {
    if (!Number.isFinite(n) || isNaN(n)) return "0,0%";
    return (n * 100).toFixed(1).replace(".", ",") + "%";
  }

  function setText(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text ?? "";
  }

  function setHTML(id, html) {
    const el = document.getElementById(id);
    if (el) el.innerHTML = html ?? "";
  }

  // Normalizar código de almacén a número sin ceros iniciales
  function extractCode(val) {
    const s = clean(val);
    const m = s.match(/\d+/);
    return m ? String(parseInt(m[0], 10)) : s;
  }

  // Parsear fecha DD/MM/YYYY o YYYY-MM a "YYYY-MM"
  function parseYearMonth(s) {
    const t = clean(s);
    if (!t) return null;
    const mSlash = t.match(/^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})$/);
    if (mSlash) {
      return `${mSlash[3]}-${mSlash[2].padStart(2, '0')}`;
    }
    const mDash = t.match(/^(\d{4})[\/\-](\d{1,2})/);
    if (mDash) {
      return `${mDash[1]}-${mDash[2].padStart(2, '0')}`;
    }
    return null;
  }

  /* ============================
     CARGA DE DATOS
  ============================ */
  function parseCSV(text) {
    const lines = text.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
    if (!lines.length) return { headers: [], rows: [] };
    const headers = lines[0].split(DELIM).map(clean);
    const rows = [];
    for (let i = 1; i < lines.length; i++) {
      const parts = lines[i].split(DELIM);
      const row = {};
      for (let j = 0; j < headers.length; j++) {
        row[headers[j]] = clean(parts[j]);
      }
      rows.push(row);
    }
    return { headers, rows };
  }

  async function loadResumenData() {
    if (mmRawData && stoNuloRawData && cumplRawData) {
      updateResumen();
      return;
    }
    if (isDataLoading) return;
    isDataLoading = true;

    const loader = document.getElementById("resumen_loader");
    if (loader) loader.style.display = "flex";

    try {
      const fetchCSV = async (url) => {
        if (typeof window.fetchWithCache === "function") {
          return await window.fetchWithCache(url);
        }
        const res = await fetch(url + "?t=" + Date.now());
        if (!res.ok) throw new Error(`HTTP ${res.status} al cargar ${url}`);
        return await res.text();
      };

      const [textMM, textStoNulo, textCumpl] = await Promise.all([
        fetchCSV(CSV_MM_URL),
        fetchCSV(CSV_STONULO_URL),
        fetchCSV(CSV_CUMPL_URL)
      ]);

      const parsedMM = parseCSV(textMM);
      mmHeaders = parsedMM.headers;
      mmRawData = parsedMM.rows;

      const parsedStoNulo = parseCSV(textStoNulo);
      stoNuloHeaders = parsedStoNulo.headers;
      stoNuloRawData = parsedStoNulo.rows;

      const parsedCumpl = parseCSV(textCumpl);
      cumplHeaders = parsedCumpl.headers;
      cumplRawData = parsedCumpl.rows;

      // Pre-calcular _ym en cumplimiento para agilizar cálculos
      const colFec = cumplHeaders.find(h => /fecha/i.test(h)) || "FECHA ENTREGA ESPERADA";
      cumplRawData.forEach(r => {
        r._ym = parseYearMonth(r[colFec]);
      });

      renderObrasSelect();
      renderMesesCumplSelect();
      hookClearButton();
      updateResumen();
    } catch (err) {
      console.error("[Resumen] Error al cargar datos:", err);
      const msg = document.getElementById("resumen_msg");
      if (msg) msg.innerHTML = `<div class="error" style="color: #ef4444; font-weight: bold; padding: 10px;">Error al cargar datos de Resumen: ${err.message}</div>`;
    } finally {
      isDataLoading = false;
      if (loader) loader.style.display = "none";
    }
  }

  /* ============================
     SELECTORES
  ============================ */
  function renderObrasSelect() {
    const sel = document.getElementById("resumen_obraSelect");
    if (!sel) return;

    const codes = new Set();

    if (mmRawData) {
      const colAlm = mmHeaders.find(h => /almac[eé]n/i.test(h)) || "Almacén";
      mmRawData.forEach(r => {
        const c = extractCode(r[colAlm]);
        if (c && c !== "0") codes.add(c);
      });
    }

    if (cumplRawData) {
      cumplRawData.forEach(r => {
        const c = extractCode(r["CLIENTE"]);
        if (c && c !== "0") codes.add(c);
      });
    }

    const sortedCodes = [...codes].sort((a, b) => {
      const na = parseInt(a, 10);
      const nb = parseInt(b, 10);
      if (!isNaN(na) && !isNaN(nb)) return na - nb;
      return a.localeCompare(b);
    });

    const currentVal = sel.value || "__ALL__";
    sel.innerHTML = `<option value="__ALL__">Todas las Obras</option>`;

    sortedCodes.forEach(code => {
      const opt = document.createElement("option");
      opt.value = code;
      opt.textContent = OBRA_MAP[code] || `Obra / Almacén ${code}`;
      sel.appendChild(opt);
    });

    sel.value = currentVal;
    sel.onchange = () => updateResumen();
  }

  function renderMesesCumplSelect() {
    const sel = document.getElementById("resumen_mesCumplSelect");
    if (!sel || !cumplRawData) return;

    const ymSet = new Set();
    cumplRawData.forEach(r => {
      if (r._ym) ymSet.add(r._ym);
    });

    const sortedYM = [...ymSet].sort();

    sel.innerHTML = "";
    sortedYM.forEach(ym => {
      const [year, month] = ym.split("-");
      const opt = document.createElement("option");
      opt.value = ym;
      const nombreMes = MES_NOMBRES[month] || month;
      opt.textContent = `${nombreMes} ${year}`;
      sel.appendChild(opt);
    });

    if (ymSet.has("2026-09")) {
      sel.value = "2026-09";
    } else if (sortedYM.length > 0) {
      sel.value = sortedYM[sortedYM.length - 1];
    }

    sel.onchange = () => { updateCumplimientoBlock(); updateDemorasBlock(); };
  }

  function hookClearButton() {
    const btn = document.getElementById("resumen_btnClearFilters");
    if (!btn) return;
    btn.onclick = () => {
      const selObra = document.getElementById("resumen_obraSelect");
      if (selObra) selObra.value = "__ALL__";
      const selMes = document.getElementById("resumen_mesCumplSelect");
      if (selMes && selMes.options.length) {
        const hasSep = Array.from(selMes.options).some(o => o.value === "2026-09");
        selMes.value = hasSep ? "2026-09" : selMes.options[selMes.options.length - 1].value;
      }
      updateResumen();
    };
  }

  /* ============================
     CÁLCULO Y RENDERIZADO GENERAL
  ============================ */
  function updateResumen() {
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
  }

  /* --- 1. BLOQUE ANÁLISIS MM --- */
  function updateMMBlock() {
    if (!mmRawData) return;

    const sel = document.getElementById("resumen_obraSelect");
    const selectedCode = sel ? sel.value : "__ALL__";

    const colAlmMM = mmHeaders.find(h => /almac[eé]n/i.test(h)) || "Almacén";
    const colMat = mmHeaders.find(h => /^material$/i.test(h)) || "Material";
    const colLibre = mmHeaders.find(h => /libre utilizaci/i.test(h) && !/valor/i.test(h) && !/[aá]rea/i.test(h)) || "Libre utilización";
    const colEstado = mmHeaders.find(h => /^estado$/i.test(h)) || "Estado";

    let rowsMM = mmRawData;
    if (selectedCode && selectedCode !== "__ALL__") {
      rowsMM = mmRawData.filter(r => extractCode(r[colAlmMM]) === selectedCode);
    }

    const obraLabel = (selectedCode === "__ALL__")
      ? "Todas las Obras"
      : (OBRA_MAP[selectedCode] || `Obra / Almacén ${selectedCode}`);

    setText("resumen_lblObra", obraLabel);

    let totalMat = 0;
    let dispMat = 0;
    let cantStockNulo = 0;
    let cantMenorPP = 0;
    let cantMayorPP = 0;
    let cantMayorMax = 0;

    for (const r of rowsMM) {
      const mat = clean(r[colMat]);
      if (!mat) continue;

      totalMat++;

      const libre = toNumber(r[colLibre]);
      if (libre > 0) dispMat++;

      const estado = clean(r[colEstado]).toUpperCase();
      if (estado.includes("NULO") || estado.startsWith("01")) {
        cantStockNulo++;
      } else if (estado.includes("MENOR") || estado.startsWith("02")) {
        cantMenorPP++;
      } else if (estado.includes("MAYOR A STOCK") || estado.includes("STOCK MAX") || estado.startsWith("04")) {
        cantMayorMax++;
      } else if (estado.includes("MAYOR") || estado.startsWith("03")) {
        cantMayorPP++;
      }
    }

    const pctDisp = totalMat ? (dispMat / totalMat) : 0;
    const pctNulo = totalMat ? (cantStockNulo / totalMat) : 0;
    const pctMenorPP = totalMat ? (cantMenorPP / totalMat) : 0;
    const pctMayorPP = totalMat ? (cantMayorPP / totalMat) : 0;
    const pctMayorMax = totalMat ? (cantMayorMax / totalMat) : 0;

    // Cruzar con STO NULO
    let nuloSinPedido = 0;
    let nuloConPedido = 0;

    if (stoNuloRawData && stoNuloRawData.length) {
      const colAlmNulo = stoNuloHeaders.find(h => /almac[eé]n/i.test(h)) || "Almacén";
      const colTipoDoc = stoNuloHeaders.find(h => /tipo doc/i.test(h)) || "TIPO DOC";

      let rowsNulo = stoNuloRawData;
      if (selectedCode && selectedCode !== "__ALL__") {
        rowsNulo = stoNuloRawData.filter(r => extractCode(r[colAlmNulo]) === selectedCode);
      }

      for (const rn of rowsNulo) {
        const td = clean(rn[colTipoDoc]).toUpperCase();
        if (td === "SIN PEDIDO") {
          nuloSinPedido++;
        } else {
          nuloConPedido++;
        }
      }
    }

    setText("res_txtTotal", fmtInt(totalMat));
    setText("res_txtDisp", fmtInt(dispMat));
    setText("res_txtPct", fmtPct01(pctDisp));
    const isDispGood = (pctDisp >= 0.90);
    const elDisp = document.getElementById("res_txtPct");
    if (elDisp) elDisp.style.color = isDispGood ? "#16a34a" : "#dc2626";
    const rowDisp = document.getElementById("res_rowDispPct");
    if (rowDisp) {
      rowDisp.style.border = isDispGood ? "1.5px solid #16a34a" : "1.5px solid #dc2626";
      rowDisp.style.background = isDispGood ? "#f0fdf4" : "#fef2f2";
    }

    const txtNuloHTML = `
      <span style="font-size: 18px; font-weight: 800; color: #dc2626; margin: 0 8px;">${fmtInt(cantStockNulo)} (${fmtPct01(pctNulo)})</span>
      <span style="color: #475569; font-size: 13px;">
        de los cuales <mark style="background-color: #fef08a; color: #854d0e; padding: 2px 8px; font-size: 13px; border-radius: 4px; font-weight: 800; border: 1px solid #facc15;">${fmtInt(nuloSinPedido)} ESTÁN SIN PEDIDO</mark> (${fmtInt(nuloConPedido)} con pedido en curso).
      </span>
    `;
    setHTML("res_wrapNulo", txtNuloHTML);

    setText("res_txtMenorPP", `${fmtInt(cantMenorPP)} (${fmtPct01(pctMenorPP)})`);
    setText("res_txtMayorPP", `${fmtInt(cantMayorPP)} (${fmtPct01(pctMayorPP)})`);
    setText("res_txtMayorMax", `${fmtInt(cantMayorMax)} (${fmtPct01(pctMayorMax)})`);
  }

  /* --- 2. BLOQUE CUMPLIMIENTO --- */
  function updateCumplimientoBlock() {
    if (!cumplRawData) return;

    const selObra = document.getElementById("resumen_obraSelect");
    const selectedCode = selObra ? selObra.value : "__ALL__";

    const selMes = document.getElementById("resumen_mesCumplSelect");
    const selectedYM = selMes ? selMes.value : null;

    // 1. Filtrar por Obra seleccionada
    let rowsBase = cumplRawData;
    if (selectedCode && selectedCode !== "__ALL__") {
      rowsBase = cumplRawData.filter(r => extractCode(r["CLIENTE"]) === selectedCode);
    }

    // Orden cronológico de meses presentes
    const allMonths = [...new Set(rowsBase.map(r => r._ym).filter(Boolean))].sort();
    const currYM = selectedYM || (allMonths.length ? allMonths[allMonths.length - 1] : null);

    // Identificar mes anterior cronológico para calcular la variación mensual
    let prevYM = null;
    if (currYM && allMonths.length) {
      const idx = allMonths.indexOf(currYM);
      if (idx > 0) {
        prevYM = allMonths[idx - 1];
      }
    }

    // Identificar últimos 12 meses cronológicos hasta currYM (LTM)
    let ltmMonths = [];
    if (currYM && allMonths.length) {
      const idx = allMonths.indexOf(currYM);
      if (idx >= 0) {
        ltmMonths = allMonths.slice(Math.max(0, idx - 11), idx + 1);
      }
    }
    if (!ltmMonths.length) {
      ltmMonths = allMonths.slice(-12);
    }

    // Filtrar filas
    const rowsLTM = rowsBase.filter(r => ltmMonths.includes(r._ym));
    const rowsCurr = currYM ? rowsBase.filter(r => r._ym === currYM) : [];
    const rowsPrev = prevYM ? rowsBase.filter(r => r._ym === prevYM) : [];

    // Helper cálculo de métricas de cumplimiento
    function calcCumplMetrics(rows) {
      let tot = 0, at = 0, ft = 0, ne = 0, sumDem = 0, cntDem = 0;
      for (const r of rows) {
        const cTot = toNumber(r["COMPROMETIDOS"]);
        const cAt = toNumber(r["ENTREGADOS AT"]);
        const cFt = toNumber(r["ENTREGADOS FT"]);
        const cNe = toNumber(r["NO ENTREGADOS"]);

        tot += cTot;
        at += cAt;
        ft += cFt;
        ne += cNe;

        const dem = toNumber(r["DIAS DE DEMORA"]);
        if (dem > 0) {
          sumDem += dem;
          cntDem++;
        }
      }
      if (!tot) tot = at + ft + ne;
      const pctAt = tot ? (at / tot) : 0;
      const pctFt = tot ? (ft / tot) : 0;
      const pctNe = tot ? (ne / tot) : 0;
      const avgDem = cntDem ? (sumDem / cntDem) : 0;
      return { tot, at, ft, ne, pctAt, pctFt, pctNe, avgDem };
    }

    const mLTM = calcCumplMetrics(rowsLTM);
    const mCurr = calcCumplMetrics(rowsCurr);
    const mPrev = calcCumplMetrics(rowsPrev);

    /* --- 2.1 RENDERIZAR COLUMNA IZQUIERDA: ACUMULADO ÚLTIMOS 12 MESES --- */
    const elRango = document.getElementById("res_cumplAcumRango");
    if (ltmMonths.length > 0) {
      const formatYM = (ym) => {
        const parts = ym.split("-");
        return `${parts[1]}/${parts[0]}`;
      };
      const rangoStr = `(${formatYM(ltmMonths[0])} - ${formatYM(ltmMonths[ltmMonths.length - 1])})`;
      setText("res_cumplAcumRango", rangoStr);
      if (elRango) elRango.style.display = "inline-block";
    } else {
      setText("res_cumplAcumRango", "");
      if (elRango) elRango.style.display = "none";
    }

    setText("res_cumplAcumComprometidos", fmtInt(mLTM.tot));

    setText("res_cumplAcumATpct", fmtPct01(mLTM.pctAt));
    setText("res_cumplAcumATqty", fmtInt(mLTM.at));
    const isAcumGood = (mLTM.pctAt >= 0.78);
    const elAcumAT = document.getElementById("res_cumplAcumATpct");
    if (elAcumAT) elAcumAT.style.color = isAcumGood ? "#16a34a" : "#dc2626";
    const rowAcumAT = document.getElementById("res_cumplAcumRowAT");
    if (rowAcumAT) {
      rowAcumAT.style.border = isAcumGood ? "1.5px solid #16a34a" : "1.5px solid #dc2626";
      rowAcumAT.style.background = isAcumGood ? "#f0fdf4" : "#fef2f2";
    }

    // FUERA DE TIEMPO: Naranja (#ea580c)
    setText("res_cumplAcumFTpct", fmtPct01(mLTM.pctFt));
    setText("res_cumplAcumFTqty", fmtInt(mLTM.ft));
    const elAcumFT = document.getElementById("res_cumplAcumFTpct");
    if (elAcumFT) elAcumFT.style.color = "#f59e0b";

    // NO ENTREGADOS: Rojo (#dc2626)
    setText("res_cumplAcumNEpct", fmtPct01(mLTM.pctNe));
    setText("res_cumplAcumNEqty", fmtInt(mLTM.ne));
    const elAcumNE = document.getElementById("res_cumplAcumNEpct");
    if (elAcumNE) elAcumNE.style.color = "#dc2626";

    setText("res_cumplAcumDemoraAvg", Math.round(mLTM.avgDem) + " d");
    const elAcumDem = document.getElementById("res_cumplAcumDemoraAvg");
    if (elAcumDem) elAcumDem.style.color = (mLTM.avgDem > 7) ? "#dc2626" : "#16a34a";

    /* --- 2.2 RENDERIZAR COLUMNA DERECHA: RENDIMIENTO MENSUAL --- */
    if (currYM) {
      const [y, m] = currYM.split("-");
      const mesNombre = MES_NOMBRES[m] || m;
      setText("res_cumplMesLabel", `${mesNombre} ${y}`);
      setText("res_cumplMesSide", `${mesNombre} ${y}`);
    }

    // Helper cálculo de variaciones vs mes anterior
    function getDiffInfo(currVal, prevVal, hasPrev, isPositiveMetric) {
      if (!hasPrev) return { text: "· - vs mes anterior", color: "#64748b" };
      const diff = (currVal - prevVal) * 100;
      if (Math.abs(diff) < 0.05) return { text: "· = 0,0% vs mes anterior", color: "#64748b" };
      const arrow = diff > 0 ? "▲" : "▼";
      const absVal = Math.abs(diff).toFixed(1).replace(".", ",");
      const isGood = isPositiveMetric ? (diff > 0) : (diff < 0);
      const color = isGood ? "#16a34a" : "#dc2626";
      return {
        text: `· ${arrow} ${absVal}% vs mes anterior`,
        color
      };
    }

    const hasPrev = rowsPrev.length > 0;
    const diffATInfo = getDiffInfo(mCurr.pctAt, mPrev.pctAt, hasPrev, true);
    const diffFTInfo = getDiffInfo(mCurr.pctFt, mPrev.pctFt, hasPrev, false);
    const diffNEInfo = getDiffInfo(mCurr.pctNe, mPrev.pctNe, hasPrev, false);

    setText("res_cumplComprometidos", fmtInt(mCurr.tot));

    // AT
    setText("res_cumplATpct", fmtPct01(mCurr.pctAt));
    setText("res_cumplATqty", fmtInt(mCurr.at));
    setText("res_cumplATdiff", diffATInfo.text);
    const elATdiff = document.getElementById("res_cumplATdiff");
    if (elATdiff) elATdiff.style.color = diffATInfo.color;
    const isCurrGood = (mCurr.pctAt >= 0.78);
    const elAT = document.getElementById("res_cumplATpct");
    if (elAT) elAT.style.color = isCurrGood ? "#16a34a" : "#dc2626";
    const rowCurrAT = document.getElementById("res_cumplRowAT");
    if (rowCurrAT) {
      rowCurrAT.style.border = isCurrGood ? "1.5px solid #16a34a" : "1.5px solid #dc2626";
      rowCurrAT.style.background = isCurrGood ? "#f0fdf4" : "#fef2f2";
    }

    // FT: Naranja (#ea580c)
    setText("res_cumplFTpct", fmtPct01(mCurr.pctFt));
    setText("res_cumplFTqty", fmtInt(mCurr.ft));
    setText("res_cumplFTdiff", diffFTInfo.text);
    const elFTdiff = document.getElementById("res_cumplFTdiff");
    if (elFTdiff) elFTdiff.style.color = diffFTInfo.color;
    const elFT = document.getElementById("res_cumplFTpct");
    if (elFT) elFT.style.color = "#f59e0b";

    // NE: Rojo (#dc2626)
    setText("res_cumplNEpct", fmtPct01(mCurr.pctNe));
    setText("res_cumplNEqty", fmtInt(mCurr.ne));
    setText("res_cumplNEdiff", diffNEInfo.text);
    const elNEdiff = document.getElementById("res_cumplNEdiff");
    if (elNEdiff) elNEdiff.style.color = diffNEInfo.color;
    const elNE = document.getElementById("res_cumplNEpct");
    if (elNE) elNE.style.color = "#dc2626";

    // Demora Promedio
    setText("res_cumplDemoraAvg", Math.round(mCurr.avgDem) + " d");
    const elDem = document.getElementById("res_cumplDemoraAvg");
    if (elDem) elDem.style.color = (mCurr.avgDem > 7) ? "#dc2626" : "#16a34a";
  }

  // Hook global de inicialización
  window.initResumen = function () {
    loadResumenData();
    if (!window.demorasInitialized && typeof window.initDemoras === "function") {
      window.initDemoras();
    }
    updateDemorasBlock();
  };

})();
