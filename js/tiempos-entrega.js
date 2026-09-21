(function() {
  'use strict';

  /* ============================
     CONFIGURACIÓN DE OBRAS Y UMBRALES
  ============================ */
  const OBRAS_CONFIG = {
    "372": {
      code: "372",
      fullName: "00372 UTE 372 GEO POSCO II",
      displayName: "00372 - UTE 372 GEO POSCO II",
      limit: 16
    },
    "378": {
      code: "378",
      fullName: "00378 YPF – Oleoducto Cnel. Pringle",
      displayName: "00378 - YPF Oleoducto Cnel. Pringle",
      limit: 10
    },
    "377": {
      code: "377",
      fullName: "00377-YPF 3° loop",
      displayName: "00377 - YPF 3° loop",
      limit: 19
    },
    "374": {
      code: "374",
      fullName: "00374 TERMINAL PUNTA COLORADA",
      displayName: "00374 - TERMINAL PUNTA COLORADA",
      limit: 18
    },
    "341": {
      code: "341",
      fullName: "00341 Mov. Suelos San Luis",
      displayName: "00341 - Mov. Suelos San Luis",
      limit: 17
    },
    "223": {
      code: "223",
      fullName: "00223 Comp Amb Santa Fe",
      displayName: "00223 - Comp Amb Santa Fe",
      limit: 12
    }
  };

  const CATEGORIES = [
    "ABASTECIMIENTO OBRA",
    "COMPRAS ABASTECIMIENTOS",
    "COMPRAS EQUIPOS",
    "ZPAS/ZPOE"
  ];

  const MONTH_ORDER = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
  ];

  let rawData = [];
  let selectedObraKey = "372";
  let selectedMonths = new Set();
  let availableMonths = [];

  /* ============================
     HELPERS
  ============================ */
  function clean(v) {
    return (v ?? "").toString().trim();
  }

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

  function fmtPct(v) {
    if (v == null || isNaN(v)) return "0%";
    return Math.round(v) + "%";
  }

  function parseDateAny(s) {
    const t = clean(s);
    if (!t) return null;
    let m = t.match(/^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})$/);
    if (m) return new Date(+m[3], +m[2] - 1, +m[1]);
    m = t.match(/^(\d{4})[\/\-](\d{1,2})[\/\-](\d{1,2})$/);
    if (m) return new Date(+m[1], +m[2] - 1, +m[3]);
    return null;
  }

  function getRowCategory(r) {
    const cd = (r["CLASE DE DOC"] || "").trim().toUpperCase();
    const c2 = (r["CLASIFICACION 2"] || "").trim().toUpperCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    
    if (cd === "ZPAS" || cd === "ZPOE" || c2.includes("ALMACEN") || c2.includes("EQUIPOS MENORES")) {
      return "ZPAS/ZPOE";
    }
    if (c2.includes("LOCAL CS")) {
      return "ABASTECIMIENTO OBRA";
    }
    if (c2.includes("ABASTECIMIENTO")) {
      return "COMPRAS ABASTECIMIENTOS";
    }
    return "COMPRAS EQUIPOS";
  }

  /* ============================
     EXTRACCIÓN Y FILTRADO
  ============================ */
  function getRowsForCurrentObra() {
    const cfg = OBRAS_CONFIG[selectedObraKey];
    if (!cfg) return [];
    return rawData.filter(r => {
      const cli = clean(r["CLIENTE"] || r["CLIENTE / OBRA"]);
      return cli.includes(cfg.code);
    });
  }

  function getFilteredRows() {
    const obraRows = getRowsForCurrentObra();
    if (!selectedMonths.size) return obraRows;
    return obraRows.filter(r => {
      const m = clean(r["MES ENTREGA"]).toLowerCase();
      return selectedMonths.has(m);
    });
  }

  /* ============================
     CÁLCULO DE LA MATRIZ
  ============================ */
  function computeMatrix(rows) {
    const cfg = OBRAS_CONFIG[selectedObraKey];
    const thresh = cfg ? cfg.limit : 15;
    const groups = ["CRITICO", "POCO TIEMPO", "SIN PRIORIDAD"];

    const table = {};
    CATEGORIES.forEach(cat => {
      table[cat] = {};
      groups.forEach(grp => {
        table[cat][grp] = { at: 0, ft: 0, ne: 0, tot: 0, daysAt: [], daysFt: [] };
      });
    });

    rows.forEach(r => {
      const cat = getRowCategory(r);
      const prio = Math.round(toNumber(r["PRIORIDAD"]));
      
      const dEE = parseDateAny(r["FECHA ENTREGA ESPERADA"]);
      const dEN = parseDateAny(r["FECHA DE EMISION NECESIDAD"]);
      let diff = 0;
      if (dEE && dEN) {
        diff = Math.round((dEE - dEN) / (1000 * 60 * 60 * 24));
      }

      // Pedidos considerados CRÍTICOS: PRIORIDAD igual a 1, 2 o 20
      const isCritico = (prio === 1 || prio === 2 || prio === 20);

      let grp = "SIN PRIORIDAD";
      if (isCritico) {
        grp = "CRITICO";
      } else if (diff < thresh) {
        grp = "POCO TIEMPO";
      } else {
        grp = "SIN PRIORIDAD";
      }

      const at = Math.round(toNumber(r["ENTREGADOS AT"]));
      const ft = Math.round(toNumber(r["ENTREGADOS FT"]));
      const ne = Math.round(toNumber(r["NO ENTREGADOS"]));
      const tot = (at + ft + ne);

      if (table[cat] && table[cat][grp]) {
        table[cat][grp].at += at;
        table[cat][grp].ft += ft;
        table[cat][grp].ne += ne;
        table[cat][grp].tot += tot;
        if (at > 0 && dEE && dEN) table[cat][grp].daysAt.push(diff);
        if (ft > 0 && dEE && dEN) table[cat][grp].daysFt.push(diff);
      }
    });

    // Totales generales
    const totals = {};
    groups.forEach(grp => {
      totals[grp] = {
        at: CATEGORIES.reduce((s, cat) => s + table[cat][grp].at, 0),
        ft: CATEGORIES.reduce((s, cat) => s + table[cat][grp].ft, 0),
        ne: CATEGORIES.reduce((s, cat) => s + table[cat][grp].ne, 0),
        tot: CATEGORIES.reduce((s, cat) => s + table[cat][grp].tot, 0),
        daysAt: CATEGORIES.reduce((acc, cat) => acc.concat(table[cat][grp].daysAt), []),
        daysFt: CATEGORIES.reduce((acc, cat) => acc.concat(table[cat][grp].daysFt), [])
      };
    });

    return { table, totals, groups };
  }

  /* ============================
     RENDERIZADO DE TABLAS
  ============================ */
  function renderAll() {
    updateBanner();
    renderSlicer();
    const rows = getFilteredRows();
    const { table, totals } = computeMatrix(rows);
    renderTable1(table, totals);
    renderTable2(table, totals);
  }

  function updateBanner() {
    const cfg = OBRAS_CONFIG[selectedObraKey];
    const banner = document.getElementById("tiempos_banner");
    if (!banner || !cfg) return;
    banner.textContent = `PARA OBRA ${cfg.code} POCO TIEMPO < ${cfg.limit} DÍAS`;
  }

  function renderSlicer() {
    const listEl = document.getElementById("tiempos_slicer_list");
    if (!listEl) return;

    // Detectar meses disponibles para la obra activa
    const obraRows = getRowsForCurrentObra();
    const monthsFound = new Set(obraRows.map(r => clean(r["MES ENTREGA"]).toLowerCase()).filter(Boolean));
    
    // Orden cronológico
    availableMonths = MONTH_ORDER.filter(m => monthsFound.has(m));
    if (!availableMonths.length) {
      availableMonths = [...monthsFound].sort();
    }

    listEl.innerHTML = "";
    availableMonths.forEach(m => {
      const item = document.createElement("div");
      item.className = "tiempos-slicer-item" + (selectedMonths.has(m) ? " active" : "");
      
      const spanName = document.createElement("span");
      spanName.textContent = m;

      const spanCheck = document.createElement("span");
      spanCheck.textContent = selectedMonths.has(m) ? "✓" : "";
      spanCheck.style.fontSize = "0.75rem";

      item.appendChild(spanName);
      item.appendChild(spanCheck);

      item.addEventListener("click", (e) => {
        if (e.ctrlKey || e.metaKey) {
          if (selectedMonths.has(m)) {
            selectedMonths.delete(m);
            if (selectedMonths.size === 0) selectedMonths = new Set(availableMonths);
          } else {
            selectedMonths.add(m);
          }
        } else {
          if (selectedMonths.size === 1 && selectedMonths.has(m)) {
            selectedMonths = new Set(availableMonths);
          } else {
            selectedMonths.clear();
            selectedMonths.add(m);
          }
        }
        renderAll();
      });

      listEl.appendChild(item);
    });
  }

  function renderTable1(table, totals) {
    const tbody = document.getElementById("tiempos_tbody_cants");
    if (!tbody) return;

    let html = "";
    CATEGORIES.forEach(cat => {
      const cr = table[cat]["CRITICO"];
      const pt = table[cat]["POCO TIEMPO"];
      const sp = table[cat]["SIN PRIORIDAD"];

      html += `
        <tr>
          <td class="td-row-name">${cat}</td>
          <td class="td-val">${fmtInt(cr.at)}</td>
          <td class="td-val">${fmtInt(cr.ft)}</td>
          <td class="td-val">${fmtInt(cr.ne)}</td>
          <td class="td-val td-val-tot">${fmtInt(cr.tot)}</td>

          <td class="td-val">${fmtInt(pt.at)}</td>
          <td class="td-val">${fmtInt(pt.ft)}</td>
          <td class="td-val">${fmtInt(pt.ne)}</td>
          <td class="td-val td-val-tot">${fmtInt(pt.tot)}</td>

          <td class="td-val">${fmtInt(sp.at)}</td>
          <td class="td-val">${fmtInt(sp.ft)}</td>
          <td class="td-val">${fmtInt(sp.ne)}</td>
          <td class="td-val td-val-tot">${fmtInt(sp.tot)}</td>
        </tr>
      `;
    });

    // Total General
    const crT = totals["CRITICO"];
    const ptT = totals["POCO TIEMPO"];
    const spT = totals["SIN PRIORIDAD"];

    html += `
      <tr class="tr-total-general">
        <td class="td-row-name">Total general</td>
        <td class="td-val">${fmtInt(crT.at)}</td>
        <td class="td-val">${fmtInt(crT.ft)}</td>
        <td class="td-val">${fmtInt(crT.ne)}</td>
        <td class="td-val td-val-tot">${fmtInt(crT.tot)}</td>

        <td class="td-val">${fmtInt(ptT.at)}</td>
        <td class="td-val">${fmtInt(ptT.ft)}</td>
        <td class="td-val">${fmtInt(ptT.ne)}</td>
        <td class="td-val td-val-tot">${fmtInt(ptT.tot)}</td>

        <td class="td-val">${fmtInt(spT.at)}</td>
        <td class="td-val">${fmtInt(spT.ft)}</td>
        <td class="td-val">${fmtInt(spT.ne)}</td>
        <td class="td-val td-val-tot">${fmtInt(spT.tot)}</td>
      </tr>
    `;

    tbody.innerHTML = html;
  }

  function renderTable2(table, totals) {
    const tbody = document.getElementById("tiempos_tbody_pcts");
    if (!tbody) return;

    function pctCells(obj) {
      const t = obj.tot;
      const pAT = t ? (obj.at / t) * 100 : 0;
      const pFT = t ? (obj.ft / t) * 100 : 0;
      const pNE = t ? (obj.ne / t) * 100 : 0;
      const pTOT = t ? 100 : 0;
      return `
        <td class="td-val">${fmtPct(pAT)}</td>
        <td class="td-val">${fmtPct(pFT)}</td>
        <td class="td-val">${fmtPct(pNE)}</td>
        <td class="td-val td-val-tot">${pTOT}%</td>
      `;
    }

    let html = "";
    CATEGORIES.forEach(cat => {
      html += `
        <tr>
          <td class="td-row-name">${cat}</td>
          ${pctCells(table[cat]["CRITICO"])}
          ${pctCells(table[cat]["POCO TIEMPO"])}
          ${pctCells(table[cat]["SIN PRIORIDAD"])}
        </tr>
      `;
    });

    // Total General Pcts
    function pctCellsTot(obj) {
      const t = obj.tot;
      const pAT = t ? (obj.at / t) * 100 : 0;
      const pFT = t ? (obj.ft / t) * 100 : 0;
      const pNE = t ? (obj.ne / t) * 100 : 0;
      return `
        <td class="td-val">${fmtPct(pAT)}</td>
        <td class="td-val">${fmtPct(pFT)}</td>
        <td class="td-val">${fmtPct(pNE)}</td>
        <td class="td-val td-val-tot">1</td>
      `;
    }

    html += `
      <tr class="tr-total-general">
        <td class="td-row-name">Total general</td>
        ${pctCellsTot(totals["CRITICO"])}
        ${pctCellsTot(totals["POCO TIEMPO"])}
        ${pctCellsTot(totals["SIN PRIORIDAD"])}
      </tr>
    `;

    // Fila inferior: Promedio de Días totales
    function calcAvg(arr) {
      if (!arr || !arr.length) return "-";
      const s = arr.reduce((a, b) => a + b, 0);
      return Math.round(s / arr.length);
    }

    const avgCrAt = calcAvg(totals["CRITICO"].daysAt);
    const avgCrFt = calcAvg(totals["CRITICO"].daysFt);
    const avgPtAt = calcAvg(totals["POCO TIEMPO"].daysAt);
    const avgPtFt = calcAvg(totals["POCO TIEMPO"].daysFt);
    const avgSpAt = calcAvg(totals["SIN PRIORIDAD"].daysAt);
    const avgSpFt = calcAvg(totals["SIN PRIORIDAD"].daysFt);

    html += `
      <tr class="tr-promedio-dias">
        <td class="td-row-name" style="font-weight: 900; color: #1e3a8a;">Promedio de Dias totales</td>
        <td class="td-val"><span class="td-prom-badge">${avgCrAt}</span></td>
        <td class="td-val"><span class="td-prom-badge">${avgCrFt}</span></td>
        <td class="td-val" style="color: #94a3b8;">-</td>
        <td class="td-val" style="color: #94a3b8;">-</td>

        <td class="td-val"><span class="td-prom-badge">${avgPtAt}</span></td>
        <td class="td-val"><span class="td-prom-badge">${avgPtFt}</span></td>
        <td class="td-val" style="color: #94a3b8;">-</td>
        <td class="td-val" style="color: #94a3b8;">-</td>

        <td class="td-val"><span class="td-prom-badge">${avgSpAt}</span></td>
        <td class="td-val"><span class="td-prom-badge">${avgSpFt}</span></td>
        <td class="td-val" style="color: #94a3b8;">-</td>
        <td class="td-val" style="color: #94a3b8;">-</td>
      </tr>
    `;

    tbody.innerHTML = html;
  }

  /* ============================
     EXPORTAR A EXCEL
  ============================ */
  function exportToExcel() {
    const cfg = OBRAS_CONFIG[selectedObraKey];
    const obraName = cfg ? cfg.displayName : "Obra";
    const filename = `Tiempos_Prioridad_${cfg ? cfg.code : 'Export'}.xlsx`;

    const rows = getFilteredRows();
    const { table, totals } = computeMatrix(rows);

    const wb = new ExcelJS.Workbook();
    const ws = wb.addWorksheet("Tiempos y Prioridad");

    ws.addRow(["CLIENTE:", obraName, "", "REGLA:", `POCO TIEMPO < ${cfg ? cfg.limit : 15} DÍAS`]);
    ws.addRow([]);

    // Tabla 1
    ws.addRow(["CANTIDADES (VOLUMEN)"]);
    ws.addRow(["", "CRITICO", "", "", "", "SIN PRIORIDAD"]);
    ws.addRow(["", "", "", "", "", "POCO TIEMPO", "", "", "", "SIN PRIORIDAD"]);
    ws.addRow(["Etiquetas de fila", "AT", "FT", "NE", "TOT", "AT", "FT", "NE", "TOT", "AT", "FT", "NE", "TOT"]);

    CATEGORIES.forEach(cat => {
      const cr = table[cat]["CRITICO"];
      const pt = table[cat]["POCO TIEMPO"];
      const sp = table[cat]["SIN PRIORIDAD"];
      ws.addRow([cat, cr.at, cr.ft, cr.ne, cr.tot, pt.at, pt.ft, pt.ne, pt.tot, sp.at, sp.ft, sp.ne, sp.tot]);
    });

    const crT = totals["CRITICO"];
    const ptT = totals["POCO TIEMPO"];
    const spT = totals["SIN PRIORIDAD"];
    ws.addRow(["Total general", crT.at, crT.ft, crT.ne, crT.tot, ptT.at, ptT.ft, ptT.ne, ptT.tot, spT.at, spT.ft, spT.ne, spT.tot]);

    ws.addRow([]);
    ws.addRow(["PORCENTAJES Y PROMEDIO DE DIAS"]);
    ws.addRow(["", "CRITICO", "", "", "", "SIN PRIORIDAD"]);
    ws.addRow(["", "", "", "", "", "POCO TIEMPO", "", "", "", "SIN PRIORIDAD"]);
    ws.addRow(["Etiquetas de fila", "%AT", "%FT", "%NE", "%TOT", "%AT", "%FT", "%NE", "%TOT", "%AT", "%FT", "%NE", "%TOT"]);

    function pctVals(obj) {
      const t = obj.tot;
      return [
        t ? Math.round((obj.at / t) * 100) + "%" : "0%",
        t ? Math.round((obj.ft / t) * 100) + "%" : "0%",
        t ? Math.round((obj.ne / t) * 100) + "%" : "0%",
        t ? "100%" : "0%"
      ];
    }

    CATEGORIES.forEach(cat => {
      ws.addRow([cat, ...pctVals(table[cat]["CRITICO"]), ...pctVals(table[cat]["POCO TIEMPO"]), ...pctVals(table[cat]["SIN PRIORIDAD"])]);
    });

    ws.addRow([
      "Total general",
      totals["CRITICO"].tot ? Math.round((totals["CRITICO"].at / totals["CRITICO"].tot) * 100) + "%" : "0%",
      totals["CRITICO"].tot ? Math.round((totals["CRITICO"].ft / totals["CRITICO"].tot) * 100) + "%" : "0%",
      totals["CRITICO"].tot ? Math.round((totals["CRITICO"].ne / totals["CRITICO"].tot) * 100) + "%" : "0%",
      "1",
      totals["POCO TIEMPO"].tot ? Math.round((totals["POCO TIEMPO"].at / totals["POCO TIEMPO"].tot) * 100) + "%" : "0%",
      totals["POCO TIEMPO"].tot ? Math.round((totals["POCO TIEMPO"].ft / totals["POCO TIEMPO"].tot) * 100) + "%" : "0%",
      totals["POCO TIEMPO"].tot ? Math.round((totals["POCO TIEMPO"].ne / totals["POCO TIEMPO"].tot) * 100) + "%" : "0%",
      "1",
      totals["SIN PRIORIDAD"].tot ? Math.round((totals["SIN PRIORIDAD"].at / totals["SIN PRIORIDAD"].tot) * 100) + "%" : "0%",
      totals["SIN PRIORIDAD"].tot ? Math.round((totals["SIN PRIORIDAD"].ft / totals["SIN PRIORIDAD"].tot) * 100) + "%" : "0%",
      totals["SIN PRIORIDAD"].tot ? Math.round((totals["SIN PRIORIDAD"].ne / totals["SIN PRIORIDAD"].tot) * 100) + "%" : "0%",
      "1"
    ]);

    function calcAvg(arr) {
      if (!arr || !arr.length) return "";
      return Math.round(arr.reduce((a, b) => a + b, 0) / arr.length);
    }

    ws.addRow([
      "Promedio de Dias totales",
      calcAvg(totals["CRITICO"].daysAt), calcAvg(totals["CRITICO"].daysFt), "", "",
      calcAvg(totals["POCO TIEMPO"].daysAt), calcAvg(totals["POCO TIEMPO"].daysFt), "", "",
      calcAvg(totals["SIN PRIORIDAD"].daysAt), calcAvg(totals["SIN PRIORIDAD"].daysFt), "", ""
    ]);

    wb.xlsx.writeBuffer().then(buffer => {
      const blob = new Blob([buffer], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = filename;
      link.click();
    });
  }

  /* ============================
     INICIALIZACIÓN
  ============================ */
  window.initTiemposEntrega = function() {
    if (window.tiemposEntregaInitialized) return;
    window.tiemposEntregaInitialized = true;

    const selectObra = document.getElementById("tiempos_obraSelect");
    if (selectObra) {
      selectObra.innerHTML = "";
      Object.keys(OBRAS_CONFIG).forEach(k => {
        const opt = document.createElement("option");
        opt.value = k;
        opt.textContent = OBRAS_CONFIG[k].displayName;
        if (k === selectedObraKey) opt.selected = true;
        selectObra.appendChild(opt);
      });

      selectObra.addEventListener("change", (e) => {
        selectedObraKey = e.target.value;
        // Restablecer meses al cambiar de obra para mostrar todos los disponibles
        selectedMonths.clear();
        const obraRows = getRowsForCurrentObra();
        obraRows.forEach(r => {
          const m = clean(r["MES ENTREGA"]).toLowerCase();
          if (m) selectedMonths.add(m);
        });
        renderAll();
      });
    }

    // Botones del Slicer
    document.getElementById("tiempos_btn_select_all")?.addEventListener("click", () => {
      selectedMonths = new Set(availableMonths);
      renderAll();
    });

    document.getElementById("tiempos_btn_clear_all")?.addEventListener("click", () => {
      selectedMonths = new Set(availableMonths);
      renderAll();
    });

    // Botón exportar Excel
    document.getElementById("tiempos_btn_export")?.addEventListener("click", () => {
      exportToExcel();
    });

    // Cargar datos
    const cacheKey = "processed_cumplimiento_" + window.CACHE_BUSTER;
    if (window.getCachedData) {
      window.getCachedData(cacheKey).then(cached => {
        if (cached && cached.data && cached.data.length) {
          rawData = cached.data;
          onDataReady();
        } else {
          loadCsv();
        }
      }).catch(() => loadCsv());
    } else {
      loadCsv();
    }

    async function loadCsv() {
      const csvUrl = "data/CUMPLIMIENTO_OPTIMIZADO.csv";
      try {
        let text = "";
        if (window.fetchWithCache) {
          text = await window.fetchWithCache(csvUrl + "?t=" + window.CACHE_BUSTER);
        } else {
          const res = await fetch(csvUrl + "?t=" + window.CACHE_BUSTER);
          text = await res.text();
        }
        const parsed = Papa.parse(text, { delimiter: ";", header: true, skipEmptyLines: true });
        rawData = parsed.data || [];
        onDataReady();
      } catch (err) {
        console.error("Error al cargar datos para Tiempos:", err);
        const banner = document.getElementById("tiempos_banner");
        if (banner) banner.textContent = "Error al cargar datos del reporte.";
      }
    }

    function onDataReady() {
      // Inicializar con todos los meses de la obra seleccionada
      const obraRows = getRowsForCurrentObra();
      selectedMonths.clear();
      obraRows.forEach(r => {
        const m = clean(r["MES ENTREGA"]).toLowerCase();
        if (m) selectedMonths.add(m);
      });
      renderAll();
    }
  };

})();
