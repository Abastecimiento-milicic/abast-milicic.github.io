# -*- coding: utf-8 -*-

with open('js/resumen.js', 'r', encoding='utf-8') as f:
    js = f.read()

target_js = """  /* --- 2. BLOQUE CUMPLIMIENTO --- */
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

    // Orden cronológico de meses presentes en la obra seleccionada
    const allMonths = [...new Set(rowsBase.map(r => r._ym).filter(Boolean))].sort();
    const currYM = selectedYM || (allMonths.length ? allMonths[allMonths.length - 1] : null);

    // Identificar mes anterior cronológico para calcular la variación
    let prevYM = null;
    if (currYM && allMonths.length) {
      const idx = allMonths.indexOf(currYM);
      if (idx > 0) {
        prevYM = allMonths[idx - 1];
      }
    }

    // Filtrar filas del mes seleccionado y del mes anterior
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

    const mCurr = calcCumplMetrics(rowsCurr);
    const mPrev = calcCumplMetrics(rowsPrev);

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

    // Renderizar en el DOM
    setText("res_cumplComprometidos", fmtInt(mCurr.tot));

    // AT
    setText("res_cumplATpct", fmtPct01(mCurr.pctAt));
    setText("res_cumplATqty", fmtInt(mCurr.at));
    setText("res_cumplATdiff", diffATInfo.text);
    const elATdiff = document.getElementById("res_cumplATdiff");
    if (elATdiff) elATdiff.style.color = diffATInfo.color;
    const elAT = document.getElementById("res_cumplATpct");
    if (elAT) elAT.style.color = (mCurr.pctAt >= 0.78) ? "#16a34a" : "#dc2626";

    // FT
    setText("res_cumplFTpct", fmtPct01(mCurr.pctFt));
    setText("res_cumplFTqty", fmtInt(mCurr.ft));
    setText("res_cumplFTdiff", diffFTInfo.text);
    const elFTdiff = document.getElementById("res_cumplFTdiff");
    if (elFTdiff) elFTdiff.style.color = diffFTInfo.color;

    // NE
    setText("res_cumplNEpct", fmtPct01(mCurr.pctNe));
    setText("res_cumplNEqty", fmtInt(mCurr.ne));
    setText("res_cumplNEdiff", diffNEInfo.text);
    const elNEdiff = document.getElementById("res_cumplNEdiff");
    if (elNEdiff) elNEdiff.style.color = diffNEInfo.color;

    // Demora Promedio
    setText("res_cumplDemoraAvg", Math.round(mCurr.avgDem) + " d");
    const elDem = document.getElementById("res_cumplDemoraAvg");
    if (elDem) elDem.style.color = (mCurr.avgDem > 7) ? "#dc2626" : "#16a34a";
  }"""

replacement_js = """  /* --- 2. BLOQUE CUMPLIMIENTO --- */
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
    if (ltmMonths.length > 0) {
      const formatYM = (ym) => {
        const parts = ym.split("-");
        return `${parts[1]}/${parts[0]}`;
      };
      const rangoStr = `(${formatYM(ltmMonths[0])} - ${formatYM(ltmMonths[ltmMonths.length - 1])})`;
      setText("res_cumplAcumRango", rangoStr);
    } else {
      setText("res_cumplAcumRango", "");
    }

    setText("res_cumplAcumComprometidos", fmtInt(mLTM.tot));

    setText("res_cumplAcumATpct", fmtPct01(mLTM.pctAt));
    setText("res_cumplAcumATqty", fmtInt(mLTM.at));
    const elAcumAT = document.getElementById("res_cumplAcumATpct");
    if (elAcumAT) elAcumAT.style.color = (mLTM.pctAt >= 0.78) ? "#16a34a" : "#dc2626";

    setText("res_cumplAcumFTpct", fmtPct01(mLTM.pctFt));
    setText("res_cumplAcumFTqty", fmtInt(mLTM.ft));

    setText("res_cumplAcumNEpct", fmtPct01(mLTM.pctNe));
    setText("res_cumplAcumNEqty", fmtInt(mLTM.ne));

    setText("res_cumplAcumDemoraAvg", Math.round(mLTM.avgDem) + " d");
    const elAcumDem = document.getElementById("res_cumplAcumDemoraAvg");
    if (elAcumDem) elAcumDem.style.color = (mLTM.avgDem > 7) ? "#dc2626" : "#16a34a";

    /* --- 2.2 RENDERIZAR COLUMNA DERECHA: RENDIMIENTO MENSUAL --- */
    if (currYM) {
      const [y, m] = currYM.split("-");
      const mesNombre = MES_NOMBRES[m] || m;
      setText("res_cumplMesLabel", `${mesNombre} ${y}`);
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
    const elAT = document.getElementById("res_cumplATpct");
    if (elAT) elAT.style.color = (mCurr.pctAt >= 0.78) ? "#16a34a" : "#dc2626";

    // FT
    setText("res_cumplFTpct", fmtPct01(mCurr.pctFt));
    setText("res_cumplFTqty", fmtInt(mCurr.ft));
    setText("res_cumplFTdiff", diffFTInfo.text);
    const elFTdiff = document.getElementById("res_cumplFTdiff");
    if (elFTdiff) elFTdiff.style.color = diffFTInfo.color;

    // NE
    setText("res_cumplNEpct", fmtPct01(mCurr.pctNe));
    setText("res_cumplNEqty", fmtInt(mCurr.ne));
    setText("res_cumplNEdiff", diffNEInfo.text);
    const elNEdiff = document.getElementById("res_cumplNEdiff");
    if (elNEdiff) elNEdiff.style.color = diffNEInfo.color;

    // Demora Promedio
    setText("res_cumplDemoraAvg", Math.round(mCurr.avgDem) + " d");
    const elDem = document.getElementById("res_cumplDemoraAvg");
    if (elDem) elDem.style.color = (mCurr.avgDem > 7) ? "#dc2626" : "#16a34a";
  }"""

norm_js = js.replace('\r\n', '\n')
norm_target = target_js.replace('\r\n', '\n')
norm_replacement = replacement_js.replace('\r\n', '\n')

if norm_target in norm_js:
    norm_js = norm_js.replace(norm_target, norm_replacement, 1)
    with open('js/resumen.js', 'w', encoding='utf-8') as f:
        f.write(norm_js.replace('\n', '\r\n'))
    print("SUCCESS: js/resumen.js updated with 2-column LTM and Mensual logic.")
else:
    print("ERROR: Target for js/resumen.js not found.")
