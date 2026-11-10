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
  const CSV_ARRIBA_URL = "data/Base_Final_365_372.csv";
  const CSV_SERV_URL = "data/SERVICIOS OBRA.csv";
  const CSV_EVOL_URL = "data/EVOLUCION.csv";
  const JSON_EMRF_URL = "data/partidas_emrf.json";
  const DEFAULT_EMRF_GCS = ["C01", "C07", "C02"];
  const DELIM = ";";

  let mmRawData = null;
  let mmHeaders = [];
  let stoNuloRawData = null;
  let stoNuloHeaders = [];
  let cumplRawData = null;
  let cumplHeaders = [];
  let arribaRawData = null;
  let servRawData = null;
  let evolRawData = null;
  let emrfRawData = null;
  let chartEvolMMInstance = null;
  let chartTendCumplInstance = null;
  let isResumenArribaActive = false;
  let isObraExcludeMode = false;
  let isDataLoading = false;

  // Clave / Códigos normalizados de obra a nombres representativos
  const OBRAS_LIMIT_MAP = {
    "372": 16,
    "378": 10,
    "377": 19,
    "376": 9,
    "379": 9,
    "374": 18,
    "365": 16,
    "341": 17,
    "314": 12,
    "223": 12
  };

  function parseDateAny(s) {
    const t = clean(s);
    if (!t) return null;
    let m = t.match(/^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})$/);
    if (m) return new Date(+m[3], +m[2] - 1, +m[1]);
    m = t.match(/^(\d{4})[\/\-](\d{1,2})[\/\-](\d{1,2})$/);
    if (m) return new Date(+m[1], +m[2] - 1, +m[3]);
    return null;
  }

  const OBRA_MAP = {
    "26_314": "00026 / 00314 - CASA OLAVARRIA",
    "35_341": "00035 / 00341 - MOV SUELOS SAN LUIS",
    "26": "00026 / 00314 - CASA OLAVARRIA",
    "314": "00026 / 00314 - CASA OLAVARRIA",
    "35": "00035 / 00341 - MOV SUELOS SAN LUIS",
    "341": "00035 / 00341 - MOV SUELOS SAN LUIS",
    "223": "00223 - COMP AMB SANTA FE",
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

  // Normalizar código de almacén u obra unificando 26/314 y 35/341
  function getCanonicalObraCode(val) {
    if (!val) return "";
    const c = extractCode(val);
    if (c === "26" || c === "314" || c === "26_314" || c === "00026" || c === "00314" || c === "0026" || c === "0314") return "26_314";
    if (c === "35" || c === "341" || c === "35_341" || c === "00035" || c === "00341" || c === "0035" || c === "0341") return "35_341";
    return c;
  }

  // Helpers para obtener array de selecciones activas
  function getSelectedObras() {
    const sel = document.getElementById("resumen_obraSelect");
    if (!sel) return [];
    const picked = [...sel.selectedOptions].map(o => o.value).filter(v => v && v !== "__ALL__");
    if (!isObraExcludeMode) {
      return picked;
    }
    // En modo EXCLUIR: si eligió 1 o más obras, devolver todas las demás obras disponibles menos las elegidas
    if (picked.length === 0) return [];
    const pickedSet = new Set(picked);
    const allAvailable = [...sel.options]
      .map(o => o.value)
      .filter(v => v && v !== "__ALL__" && !pickedSet.has(v));
    return allAvailable;
  }

  function getSelectedAnios() {
    const sel = document.getElementById("resumen_anioSelect");
    if (!sel) return [];
    return [...sel.selectedOptions].map(o => o.value).filter(v => v && v !== "__ALL__");
  }

  function getSelectedMeses() {
    const sel = document.getElementById("resumen_mesCumplSelect");
    if (!sel) return [];
    return [...sel.selectedOptions].map(o => o.value).filter(v => v && v !== "__ALL__");
  }

  function getSelectedGcEmrf() {
    const sel = document.getElementById("resumen_gcEmrfSelect");
    if (!sel) return [];
    return [...sel.selectedOptions].map(o => o.value).filter(v => v && v !== "__ALL__");
  }

  function getSelectedCumplInlineMes() {
    const sel = document.getElementById("res_cumplInlineMesSelect");
    if (!sel || !sel.value || sel.value === "__ALL__") return [];
    return [sel.value];
  }

  function getEffectiveMeses() {
    const selMeses = getSelectedMeses();
    const selAnios = getSelectedAnios();
    if (selMeses.length > 0) {
      if (selAnios.length > 0) {
        return selMeses.filter(ym => selAnios.some(y => ym.startsWith(y + "-")));
      }
      return selMeses;
    }
    if (selAnios.length > 0 && cumplRawData) {
      const ymSet = new Set();
      cumplRawData.forEach(r => {
        if (r._ym && selAnios.some(y => r._ym.startsWith(y + "-"))) {
          ymSet.add(r._ym);
        }
      });
      if (arribaRawData) {
        arribaRawData.forEach(r => {
          if (r._ym && selAnios.some(y => r._ym.startsWith(y + "-"))) {
            ymSet.add(r._ym);
          }
        });
      }
      return [...ymSet].sort();
    }
    return [];
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
    if (typeof Papa !== "undefined" && typeof Papa.parse === "function") {
      const res = Papa.parse(text, {
        delimiter: DELIM,
        skipEmptyLines: true
      });
      const data = res.data || [];
      if (!data.length) return { headers: [], rows: [] };
      const headers = data[0].map(clean);
      const rows = [];
      for (let i = 1; i < data.length; i++) {
        const parts = data[i];
        if (!parts || !parts.length || (parts.length === 1 && !parts[0])) continue;
        const row = {};
        for (let j = 0; j < headers.length; j++) {
          row[headers[j]] = clean(parts[j]);
        }
        rows.push(row);
      }
      return { headers, rows };
    }

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
        const cb = window.CACHE_BUSTER || Date.now();
        const fullUrl = url.includes("?") ? url : (encodeURI(url) + "?t=" + cb);
        if (typeof window.fetchWithCache === "function") {
          return await window.fetchWithCache(fullUrl);
        }
        const res = await fetch(fullUrl);
        if (!res.ok) throw new Error(`HTTP ${res.status} al cargar ${url}`);
        return await res.text();
      };

      const [textMM, textStoNulo, textCumpl, textArriba, textServ, textEmrf, textEvol] = await Promise.all([
        fetchCSV(CSV_MM_URL),
        fetchCSV(CSV_STONULO_URL),
        fetchCSV(CSV_CUMPL_URL),
        fetchCSV(CSV_ARRIBA_URL).catch(() => ""),
        fetchCSV(CSV_SERV_URL).catch(() => ""),
        fetchCSV(JSON_EMRF_URL).catch(() => ""),
        fetchCSV(CSV_EVOL_URL).catch(() => "")
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
      const colFec = cumplHeaders.find(h => /entrega\s+esperada/i.test(h)) || "FECHA ENTREGA ESPERADA";
      cumplRawData.forEach(r => {
        r._ym = parseYearMonth(r[colFec]);
      });

      if (textArriba && textArriba.length > 50) {
        const parsedArriba = parseCSV(textArriba);
        const colFecArr = parsedArriba.headers.find(h => /entrega\s+esperada/i.test(h)) || "FECHA ENTREGA ESPERADA";
        arribaRawData = parsedArriba.rows.map(r => {
          r._ym = parseYearMonth(r[colFecArr]);
          return r;
        }).filter(r => r._ym && r._ym !== "2025-09" && r._ym >= "2025-10");
      } else {
        arribaRawData = [];
      }

      if (textServ && textServ.length > 50) {
        const parsedServ = parseCSV(textServ);
        servRawData = parsedServ.rows;
      } else {
        servRawData = [];
      }

      if (textEvol && textEvol.length > 50) {
        const parsedEvol = parseCSV(textEvol);
        evolRawData = parsedEvol.rows;
      } else {
        evolRawData = [];
      }

      if (textEmrf && textEmrf.length > 20) {
        try {
          const parsedEmrf = JSON.parse(textEmrf);
          emrfRawData = (parsedEmrf && Array.isArray(parsedEmrf.data)) ? parsedEmrf.data : [];
        } catch (e) {
          console.warn("[Resumen] Error al parsear partidas_emrf.json:", e);
          emrfRawData = [];
        }
      } else {
        emrfRawData = [];
      }

      renderObrasSelect();
      renderAniosSelect();
      renderMesesCumplSelect();
      renderCumplInlineMesSelect(true);
      setObraExcludeMode(false);
      renderCumplInlineMesSelect(true);
      renderGcEmrfSelect(true);
      const selVencEmrf = document.getElementById("res_emrfInlineVencSelect");
      if (selVencEmrf) selVencEmrf.value = "VENCIDA";
      hookClearButton();
      hookExcludeObraButton();
      hookArribaButtons();
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
        const c = getCanonicalObraCode(r[colAlm]);
        if (c && c !== "0" && c !== "1" && c !== "1500") codes.add(c);
      });
    }

    if (cumplRawData) {
      cumplRawData.forEach(r => {
        const c = getCanonicalObraCode(r["CLIENTE"]);
        if (c && c !== "0" && c !== "1" && c !== "1500") codes.add(c);
      });
    }

    const sortedCodes = [...codes].sort((a, b) => {
      const getNum = (str) => {
        const m = str.match(/\d+/);
        return m ? parseInt(m[0], 10) : 99999;
      };
      return getNum(a) - getNum(b);
    });

    const prevSelected = [...sel.selectedOptions].map(o => o.value);

    sel.innerHTML = `<option value="__ALL__">Todas las Obras</option>`;

    sortedCodes.forEach(code => {
      const opt = document.createElement("option");
      opt.value = code;
      opt.textContent = OBRA_MAP[code] || `Obra / Almacén ${code}`;
      if (prevSelected.includes(code)) {
        opt.selected = true;
      }
      sel.appendChild(opt);
    });

    if (!prevSelected.length || prevSelected.includes("__ALL__") || !sel.selectedOptions.length) {
      if (sel.options[0]) sel.options[0].selected = true;
    }

    sel.onchange = () => updateResumen();

    const pillsCont = document.getElementById("obraPillsContainer");
    if (pillsCont) {
      const isAllSelected = !prevSelected.length || prevSelected.includes("__ALL__");
      let pillsHtml = `<span class="filter-pill ${isAllSelected ? 'active' : ''}" data-val="__ALL__" onclick="window.selectResumenObraPill(this, '__ALL__')">Todas las Obras</span>`;
      sortedCodes.forEach(code => {
        const isSel = prevSelected.includes(code);
        const label = OBRA_MAP[code] || `Obra ${code}`;
        pillsHtml += `<span class="filter-pill ${isSel ? 'active' : ''}" data-val="${code}" onclick="window.selectResumenObraPill(this, '${code}')">${label}</span>`;
      });
      pillsCont.innerHTML = pillsHtml;
    }

    if (typeof window.syncAllStMultiSelects === "function") {
      window.syncAllStMultiSelects();
    }
  }

  function renderAniosSelect() {
    const sel = document.getElementById("resumen_anioSelect");
    if (!sel || !cumplRawData) return;

    const yearSet = new Set();
    cumplRawData.forEach(r => {
      if (r._ym) {
        const y = r._ym.split("-")[0];
        if (y) yearSet.add(y);
      }
    });

    const sortedYears = [...yearSet].sort();
    const prevSelected = [...sel.selectedOptions].map(o => o.value).filter(v => v && v !== "__ALL__");

    sel.innerHTML = `<option value="__ALL__">Todos los Años</option>`;
    sortedYears.forEach(year => {
      const opt = document.createElement("option");
      opt.value = year;
      opt.textContent = year;
      if (prevSelected.includes(year)) {
        opt.selected = true;
      }
      sel.appendChild(opt);
    });

    if (!prevSelected.length || !sel.selectedOptions.length) {
      if (sel.options[0]) sel.options[0].selected = true;
    }

    sel.onchange = () => {
      renderMesesCumplSelect(true);
      updateCumplimientoBlock();
      updateDemorasBlock();
      updateTiemposBlock();
    };

    const pillsCont = document.getElementById("anioPillsContainer");
    if (pillsCont) {
      const isAllSelected = !prevSelected.length || prevSelected.includes("__ALL__");
      let pillsHtml = `<span class="filter-pill ${isAllSelected ? 'active' : ''}" data-val="__ALL__" onclick="window.selectResumenAnioPill(this, '__ALL__')">Todos</span>`;
      sortedYears.forEach(year => {
        const isSel = prevSelected.includes(year);
        pillsHtml += `<span class="filter-pill ${isSel ? 'active' : ''}" data-val="${year}" onclick="window.selectResumenAnioPill(this, '${year}')">${year}</span>`;
      });
      pillsCont.innerHTML = pillsHtml;
    }

    if (typeof window.syncAllStMultiSelects === "function") {
      window.syncAllStMultiSelects();
    }
  }

  function renderMesesCumplSelect(resetToAllOnYearChange = false) {
    const sel = document.getElementById("resumen_mesCumplSelect");
    if (!sel || !cumplRawData) return;

    const selectedAnios = getSelectedAnios();

    const ymSet = new Set();
    cumplRawData.forEach(r => {
      if (r._ym) {
        if (!selectedAnios.length || selectedAnios.some(y => r._ym.startsWith(y + "-"))) {
          ymSet.add(r._ym);
        }
      }
    });

    const sortedYM = [...ymSet].sort();

    const prevSelected = resetToAllOnYearChange
      ? []
      : [...sel.selectedOptions].map(o => o.value).filter(v => v && v !== "__ALL__");

    sel.innerHTML = `<option value="__ALL__">Todos los Meses</option>`;
    sortedYM.forEach(ym => {
      const [year, month] = ym.split("-");
      const opt = document.createElement("option");
      opt.value = ym;
      const nombreMes = MES_NOMBRES[month] || month;
      opt.textContent = `${nombreMes} ${year}`;
      if (prevSelected.includes(ym)) {
        opt.selected = true;
      }
      sel.appendChild(opt);
    });

    const hasSelection = Array.from(sel.selectedOptions).some(o => o.value !== "__ALL__");
    if (!hasSelection && sel.options[0]) {
      sel.options[0].selected = true;
    }

    sel.onchange = () => { updateCumplimientoBlock(); updateDemorasBlock(); updateTiemposBlock(); };

    const pillsCont = document.getElementById("mesPillsContainer");
    if (pillsCont) {
      const isAllSelected = !hasSelection;
      let pillsHtml = `<span class="filter-pill ${isAllSelected ? 'active' : ''}" data-val="__ALL__" onclick="window.selectResumenMesPill(this, '__ALL__')">Todos</span>`;
      [...sortedYM].reverse().forEach(ym => {
        const [year, month] = ym.split("-");
        const nombreMes = MES_NOMBRES[month] || month;
        const isSel = prevSelected.includes(ym);
        pillsHtml += `<span class="filter-pill ${isSel ? 'active' : ''}" data-val="${ym}" onclick="window.selectResumenMesPill(this, '${ym}')">${nombreMes} ${year}</span>`;
      });
      pillsCont.innerHTML = pillsHtml;
    }

    if (typeof window.syncAllStMultiSelects === "function") {
      window.syncAllStMultiSelects();
    }
  }

  function renderCumplInlineMesSelect(resetToDefault = false) {
    const sel = document.getElementById("res_cumplInlineMesSelect");
    if (!sel || !cumplRawData) return;

    const ymSet = new Set();
    cumplRawData.forEach(r => {
      if (r._ym) ymSet.add(r._ym);
    });
    if (arribaRawData) {
      arribaRawData.forEach(r => {
        if (r._ym) ymSet.add(r._ym);
      });
    }

    const sortedYM = [...ymSet].sort();
    const prevVal = resetToDefault ? "" : sel.value;

    sel.innerHTML = `<option value="__ALL__">Todos los Meses</option>`;
    sortedYM.forEach(ym => {
      const [year, month] = ym.split("-");
      const opt = document.createElement("option");
      opt.value = ym;
      const nombreMes = MES_NOMBRES[month] || month;
      opt.textContent = `${nombreMes} ${year}`;
      sel.appendChild(opt);
    });

    if (!resetToDefault && prevVal && Array.from(sel.options).some(o => o.value === prevVal)) {
      sel.value = prevVal;
    } else if (sortedYM.includes("2026-10")) {
      sel.value = "2026-10";
    } else if (sortedYM.length > 0) {
      sel.value = sortedYM[sortedYM.length - 1];
    } else {
      sel.value = "__ALL__";
    }

    sel.onchange = () => {
      updateCumplimientoBlock();
    };
  }

  function renderGcEmrfSelect(resetToDefault = false) {
    const sel = document.getElementById("resumen_gcEmrfSelect");
    if (!sel) return;

    const gcSet = new Set(DEFAULT_EMRF_GCS);
    if (emrfRawData && emrfRawData.length) {
      emrfRawData.forEach(r => {
        const g = clean(r.Grupo_Compras);
        if (g && g !== "SIN GRUPO") gcSet.add(g);
      });
    }

    const otherGcs = [...gcSet].filter(g => !DEFAULT_EMRF_GCS.includes(g)).sort((a, b) =>
      a.localeCompare(b, "es", { numeric: true })
    );
    const orderedGcs = [...DEFAULT_EMRF_GCS, ...otherGcs];

    const prevSelected = resetToDefault
      ? [...DEFAULT_EMRF_GCS]
      : [...sel.selectedOptions].map(o => o.value).filter(v => v && v !== "__ALL__");

    const hadAllSelected = !resetToDefault && Array.from(sel.selectedOptions).some(o => o.value === "__ALL__");

    sel.innerHTML = `<option value="__ALL__">Todos los Grupos</option>`;
    orderedGcs.forEach(gc => {
      const opt = document.createElement("option");
      opt.value = gc;
      opt.textContent = gc;
      if (!hadAllSelected && prevSelected.includes(gc)) {
        opt.selected = true;
      }
      sel.appendChild(opt);
    });

    const hasSpecific = Array.from(sel.options).some(o => o.value !== "__ALL__" && o.selected);
    if (!hasSpecific && sel.options[0]) {
      sel.options[0].selected = true;
    }

    sel.onchange = () => {
      updateEmrfBlock();
    };

    const pillsCont = document.getElementById("gcEmrfPillsContainer");
    if (pillsCont) {
      let pillsHtml = `<span class="filter-pill ${hadAllSelected ? 'active' : ''}" data-val="__ALL__" onclick="window.selectResumenGcPill(this, '__ALL__')">Todos</span>`;
      orderedGcs.forEach(gc => {
        const isSel = !hadAllSelected && prevSelected.includes(gc);
        pillsHtml += `<span class="filter-pill ${isSel ? 'active' : ''}" data-val="${gc}" onclick="window.selectResumenGcPill(this, '${gc}')">${gc}</span>`;
      });
      pillsCont.innerHTML = pillsHtml;
    }

    if (typeof window.syncAllStMultiSelects === "function") {
      window.syncAllStMultiSelects();
    }
  }

  function hookClearButton() {
    const btn = document.getElementById("resumen_btnClearFilters");
    if (!btn) return;
    btn.onclick = () => {
      const selObra = document.getElementById("resumen_obraSelect");
      if (selObra) {
        [...selObra.options].forEach((opt, idx) => {
          opt.selected = (opt.value === "__ALL__" || idx === 0);
        });
        selObra.dispatchEvent(new Event("change", { bubbles: true }));
      }
      const selAnio = document.getElementById("resumen_anioSelect");
      if (selAnio) {
        [...selAnio.options].forEach((opt, idx) => {
          opt.selected = (opt.value === "__ALL__" || idx === 0);
        });
        renderMesesCumplSelect(false);
      }
      const selMes = document.getElementById("resumen_mesCumplSelect");
      if (selMes && selMes.options.length) {
        [...selMes.options].forEach((opt, idx) => {
          opt.selected = (opt.value === "__ALL__" || idx === 0);
        });
        selMes.dispatchEvent(new Event("change", { bubbles: true }));
      }
      renderGcEmrfSelect(true);
      if (isResumenArribaActive) {
        setResumenArribaMode(false);
      } else {
        updateResumen();
      }
      // Resetear clases activas de las pastillas interactivas
      const obraPills = document.querySelectorAll("#obraPillsContainer .filter-pill");
      obraPills.forEach((p, idx) => {
        if (p.getAttribute("data-val") === "__ALL__" || idx === 0) p.classList.add("active");
        else p.classList.remove("active");
        p.style.display = "inline-flex";
      });
      const qInput = document.getElementById("resumen_obraQuickSearch");
      if (qInput) qInput.value = "";

      const anioPills = document.querySelectorAll("#anioPillsContainer .filter-pill");
      anioPills.forEach((p, idx) => {
        if (p.getAttribute("data-val") === "__ALL__" || idx === 0) p.classList.add("active");
        else p.classList.remove("active");
      });

      const mesPills = document.querySelectorAll("#mesPillsContainer .filter-pill");
      mesPills.forEach((p, idx) => {
        if (p.getAttribute("data-val") === "__ALL__" || idx === 0) p.classList.add("active");
        else p.classList.remove("active");
      });

      const gcPills = document.querySelectorAll("#gcEmrfPillsContainer .filter-pill");
      gcPills.forEach(p => {
        const v = p.getAttribute("data-val");
        p.classList.toggle("active", DEFAULT_EMRF_GCS.includes(v));
      });

      const sw = document.getElementById("switchArriba");
      if (sw) sw.classList.remove("active");

      if (typeof window.syncAllStMultiSelects === "function") {
        setTimeout(() => window.syncAllStMultiSelects(), 30);
      }
    };
  }

  function setObraExcludeMode(active) {
    isObraExcludeMode = !!active;
    const btn = document.getElementById("resumen_btnExcludeObra");
    const wrap = document.getElementById("resumen_obraFilterWrap");
    const hint = document.getElementById("resumen_obraHint");
    if (btn) {
      btn.classList.toggle("is-active", isObraExcludeMode);
      btn.innerHTML = isObraExcludeMode ? "🚫 Excluir: ON" : "🚫 Excluir: OFF";
    }
    if (wrap) {
      wrap.classList.toggle("is-exclude-mode", isObraExcludeMode);
    }
    if (hint) {
      hint.textContent = isObraExcludeMode
        ? "Modo EXCLUIR activo: se omiten las obras marcadas"
        : "Elegí obras o activá «Excluir» para omitir una";
    }
  }

  function hookExcludeObraButton() {
    const btn = document.getElementById("resumen_btnExcludeObra");
    if (!btn) return;
    btn.onclick = () => {
      setObraExcludeMode(!isObraExcludeMode);
      updateResumen();
    };
  }

  function setResumenArribaMode(active) {
    isResumenArribaActive = !!active;
    const btn = document.getElementById("resumen_btnArriba");
    if (btn) {
      if (isResumenArribaActive) {
        btn.classList.add("btn-active");
        btn.innerHTML = "↩ Volver a cumplimiento estándar";
      } else {
        btn.classList.remove("btn-active");
        btn.innerHTML = "🏔️ Medir cumplimiento arriba";
      }
    }
    const sw = document.getElementById("switchArriba");
    if (sw) {
      sw.classList.toggle("active", isResumenArribaActive);
    }

    updateCumplimientoBlock();
    updateTiemposBlock();
  }

  /* ==========================================================================
     MÉTODOS PÚBLICOS DE PASTILLAS Y FILTROS INTERACTIVOS TIPO PROTOTIPO
     ========================================================================== */
  window.selectResumenObraPill = function(el, code) {
    const sel = document.getElementById("resumen_obraSelect");
    if (!sel) return;
    const pillsCont = document.getElementById("obraPillsContainer");

    if (code === "__ALL__") {
      if (pillsCont) {
        pillsCont.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("active"));
      }
      el.classList.add("active");
      [...sel.options].forEach((o, idx) => {
        o.selected = (o.value === "__ALL__" || idx === 0);
      });
    } else {
      const allPill = pillsCont ? pillsCont.querySelector('[data-val="__ALL__"]') : null;
      if (allPill) allPill.classList.remove("active");

      if (pillsCont) {
        pillsCont.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("active"));
      }
      el.classList.add("active");

      [...sel.options].forEach(o => {
        o.selected = (o.value === code);
      });
    }
    updateResumen();
  };

  window.filterResumenObraPills = function(query) {
    const text = (query || "").toLowerCase().trim();
    const pills = document.querySelectorAll("#obraPillsContainer .filter-pill");
    pills.forEach(pill => {
      const val = pill.getAttribute("data-val");
      if (val === "__ALL__" || pill.textContent.toLowerCase().includes(text)) {
        pill.style.display = "inline-flex";
      } else {
        pill.style.display = "none";
      }
    });
  };

  window.selectResumenAnioPill = function(el, year) {
    const sel = document.getElementById("resumen_anioSelect");
    if (!sel) return;
    const pillsCont = document.getElementById("anioPillsContainer");
    if (pillsCont) {
      pillsCont.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("active"));
    }
    el.classList.add("active");
    [...sel.options].forEach(o => {
      o.selected = (year === "__ALL__" ? (o.value === "__ALL__") : (o.value === year));
    });
    renderMesesCumplSelect(true);
    updateCumplimientoBlock();
    updateDemorasBlock();
    updateTiemposBlock();
  };

  window.selectResumenMesPill = function(el, ym) {
    const sel = document.getElementById("resumen_mesCumplSelect");
    if (!sel) return;
    const pillsCont = document.getElementById("mesPillsContainer");
    if (pillsCont) {
      pillsCont.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("active"));
    }
    el.classList.add("active");
    [...sel.options].forEach(o => {
      o.selected = (ym === "__ALL__" ? (o.value === "__ALL__") : (o.value === ym));
    });
    updateCumplimientoBlock();
    updateDemorasBlock();
    updateTiemposBlock();
  };

  window.selectResumenGcPill = function(el, gc) {
    const sel = document.getElementById("resumen_gcEmrfSelect");
    if (!sel) return;
    const pillsCont = document.getElementById("gcEmrfPillsContainer");
    if (gc === "__ALL__") {
      if (pillsCont) {
        pillsCont.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("active"));
      }
      el.classList.add("active");
      [...sel.options].forEach((o, i) => o.selected = (i === 0 || o.value === "__ALL__"));
    } else {
      const allPill = pillsCont ? pillsCont.querySelector('[data-val="__ALL__"]') : null;
      if (allPill) allPill.classList.remove("active");
      el.classList.toggle("active");
      const activeVals = Array.from(pillsCont.querySelectorAll(".filter-pill.active")).map(p => p.getAttribute("data-val"));
      if (!activeVals.length) {
        if (allPill) allPill.classList.add("active");
        [...sel.options].forEach((o, i) => o.selected = (i === 0));
      } else {
        [...sel.options].forEach(o => {
          o.selected = activeVals.includes(o.value);
        });
      }
    }
    updateEmrfBlock();
  };

  window.toggleResumenArribaSwitch = function() {
    setResumenArribaMode(!isResumenArribaActive);
  };

  window.toggleResumenExcludeObra = function() {
    setObraExcludeMode(!isObraExcludeMode);
    updateResumen();
  };

  function hookArribaButtons() {
    const btn = document.getElementById("resumen_btnArriba");
    if (btn) {
      btn.onclick = () => {
        setResumenArribaMode(!isResumenArribaActive);
      };
    }
  }

  /* ============================
     CÁLCULO Y RENDERIZADO GENERAL
  ============================ */
  function updateResumen() {
    updateMMBlock();
    updateCumplimientoBlock();
    updateDemorasBlock();
    updateTiemposBlock();
    updateServiciosBlock();
    updateEmrfBlock();
  }

  /* --- 5. BLOQUE CONTROL DE PARTIDAS (.div6) --- */
  let emrfVencBound = false;
  function bindEmrfVencSelect() {
    if (emrfVencBound) return;
    const sel = document.getElementById("res_emrfInlineVencSelect");
    if (!sel) return;
    emrfVencBound = true;
    sel.addEventListener("change", () => {
      updateEmrfBlock();
    });
  }

  function updateEmrfBlock() {
    if (!emrfRawData) return;
    bindEmrfVencSelect();

    const selectedGCs = getSelectedGcEmrf();
    const selVencEl = document.getElementById("res_emrfInlineVencSelect");
    const vencFilter = selVencEl ? selVencEl.value : "VENCIDA";

    const btnWrap = document.getElementById("res_emrfVencBtnWrap");
    if (btnWrap) {
      btnWrap.classList.remove("is-vencida", "is-novencida", "is-all");
      if (vencFilter === "VENCIDA") btnWrap.classList.add("is-vencida");
      else if (vencFilter === "NO_VENCIDA") btnWrap.classList.add("is-novencida");
      else btnWrap.classList.add("is-all");
    }

    let rows = emrfRawData;
    if (selectedGCs.length > 0) {
      const gcSet = new Set(selectedGCs.map(clean));
      rows = rows.filter(r => gcSet.has(clean(r.Grupo_Compras)));
    }

    if (vencFilter === "VENCIDA") {
      rows = rows.filter(r => clean(r.Estado_Vencimiento) === "VENCIDA");
    } else if (vencFilter === "NO_VENCIDA") {
      rows = rows.filter(r => clean(r.Estado_Vencimiento) !== "VENCIDA");
    }

    const badgeEl = document.getElementById("res_emrf_gc_badge");
    if (badgeEl) {
      if (selectedGCs.length === 0) {
        badgeEl.textContent = "GC: TODOS LOS GRUPOS";
      } else if (selectedGCs.length <= 4) {
        badgeEl.textContent = "GC: " + selectedGCs.join(", ");
      } else {
        badgeEl.textContent = `GC: ${selectedGCs.length} GRUPOS`;
      }
    }

    let faltaFact = 0;
    let faltaRecep = 0;

    for (const r of rows) {
      const grp = clean(r.Grupo_EMRF);
      if (grp === "TIENE RECEPCIÓN - FALTA FACTURA") faltaFact++;
      else if (grp === "TIENE FACTURA - FALTA RECEPCIÓN") faltaRecep++;
    }

    const total = faltaFact + faltaRecep;
    const pctFF = total ? (faltaFact / total) : 0;
    const pctFR = total ? (faltaRecep / total) : 0;

    setText("res_emrfTotal", fmtInt(total));
    setText("res_emrfFaltaFact", `${fmtInt(faltaFact)} (${fmtPct01(pctFF)})`);
    setText("res_emrfFaltaRecep", `${fmtInt(faltaRecep)} (${fmtPct01(pctFR)})`);
  }

  /* --- 4. BLOQUE SERVICIOS (.div5) CON TOOLTIPS DE SUBCATEGORÍAS (ESTADO ITEM) --- */
  let servBreakdownsByCat = {};
  let servTooltipsBound = false;

  function getServItemBadgeClass(estadoItem) {
    const val = clean(estadoItem).toUpperCase();
    const rojos = ["ADJUDICADO", "ADJUDICADO PARCIAL", "RESPONDIDO", "INCOMPLETO", "SIN TRATAMIENTO"];
    const verdes = ["CUMPLIDO", "ALMACENADO", "CONSUMIDO PARCIAL"];
    if (verdes.includes(val)) return "res-ft-badge-verde";
    if (rojos.includes(val)) return "res-ft-badge-rojo";
    return "res-ft-badge-azul";
  }

  function ensureServTooltipDOM() {
    let tip = document.getElementById("res_servFloatingTooltip");
    if (!tip) {
      tip = document.createElement("div");
      tip.id = "res_servFloatingTooltip";
      tip.className = "res-floating-tooltip";
      document.body.appendChild(tip);
    }
    return tip;
  }

  function bindServiciosTooltips() {
    if (servTooltipsBound) return;
    servTooltipsBound = true;

    const pills = document.querySelectorAll("#panel-resumen .res-serv-pill[data-serv-cat]");
    pills.forEach(pill => {
      pill.addEventListener("mouseenter", () => {
        const cat = pill.getAttribute("data-serv-cat");
        const info = servBreakdownsByCat[cat];
        if (!info) return;
        const tip = ensureServTooltipDOM();
        tip.innerHTML = info.html;
        tip.style.display = "block";

        const rect = pill.getBoundingClientRect();
        const tipRect = tip.getBoundingClientRect();
        let top = rect.top - tipRect.height - 8;
        if (top < 8) {
          top = rect.bottom + 8;
        }
        let left = rect.left + (rect.width / 2) - (tipRect.width / 2);
        if (left < 8) left = 8;
        if (left + tipRect.width > window.innerWidth - 8) {
          left = window.innerWidth - tipRect.width - 8;
        }
        tip.style.top = `${Math.round(top)}px`;
        tip.style.left = `${Math.round(left)}px`;
      });

      pill.addEventListener("mouseleave", () => {
        const tip = document.getElementById("res_servFloatingTooltip");
        if (tip) tip.style.display = "none";
      });
    });
  }

  function buildSubcatTooltipHTML(title, totalCount, mapCounts, extraNote = "") {
    const entries = Object.entries(mapCounts).sort((a, b) => b[1] - a[1]);
    if (entries.length === 0) {
      return `
        <div class="res-ft-header">
          <span>${title}</span>
          <span style="color:#2563eb;">0 pos.</span>
        </div>
        <div style="font-size:10.5px; color:#64748b; font-style:italic;">Sin posiciones para el filtro actual</div>
      `;
    }
    const itemsHtml = entries.map(([subcat, cnt]) => {
      const pct = totalCount > 0 ? fmtPct01(cnt / totalCount) : "0,0%";
      const bCls = getServItemBadgeClass(subcat);
      return `
        <li class="res-ft-row">
          <span class="res-ft-badge ${bCls}">${subcat}</span>
          <span class="res-ft-val">${fmtInt(cnt)} <span class="res-ft-pct">(${pct})</span></span>
        </li>
      `;
    }).join("");

    return `
      <div class="res-ft-header">
        <span>${title}</span>
        <span style="color:#0d9488;">${fmtInt(totalCount)} pos.</span>
      </div>
      <div class="res-ft-sub">Subcategorías (ESTADO ITEM):</div>
      <ul class="res-ft-list">${itemsHtml}</ul>
      ${extraNote ? `<div style="margin-top:6px; padding-top:4px; border-top:1px dashed #cbd5e1; font-size:9.5px; color:#475569;">${extraNote}</div>` : ""}
    `;
  }

  function updateServiciosBlock() {
    if (!servRawData) return;
    bindServiciosTooltips();

    const selectedObras = getSelectedObras();

    let rows = servRawData;
    if (selectedObras.length > 0) {
      const obraSet = new Set(selectedObras.map(getCanonicalObraCode));
      rows = servRawData.filter(r => obraSet.has(getCanonicalObraCode(r["CLIENTE"])));
    }

    const total = rows.length;
    let enCurso = 0;
    let proxVencer = 0;
    let vencido = 0;
    let totRecep = 0;
    let pedInfo = 0;
    let sinTrat = 0;

    const mapTotal = {};
    const mapEnCurso = {};
    const mapTotRecep = {};
    const mapVencidos = {};
    const mapProxVencer = {};
    const mapSinTratInfo = {};

    const inc = (obj, k) => { obj[k] = (obj[k] || 0) + 1; };

    for (const r of rows) {
      const estServ = clean(r["Estado Servicio"]);
      const estItem = clean(r["ESTADO ITEM"]).toUpperCase() || "SIN ESTADO ITEM";

      inc(mapTotal, estItem);

      if (estServ === "En curso") {
        enCurso++;
        inc(mapEnCurso, estItem);
      } else if (estServ.includes("Próximo a vencer") || estServ.includes("Proximo a vencer")) {
        proxVencer++;
        inc(mapProxVencer, estItem);
      } else if (estServ.includes("Vencido")) {
        vencido++;
        inc(mapVencidos, estItem);
      } else if (estServ.includes("Total recepcionado")) {
        totRecep++;
        inc(mapTotRecep, estItem);
      } else if (estServ.includes("Pedido de Info")) {
        pedInfo++;
        inc(mapSinTratInfo, `PED. INFO → ${estItem}`);
      }

      if (estItem === "SIN TRATAMIENTO") {
        sinTrat++;
        if (!estServ.includes("Pedido de Info")) {
          inc(mapSinTratInfo, `SIN TRAT. (${estServ})`);
        }
      }
    }

    const pctEnCurso = total ? (enCurso / total) : 0;
    const pctProx = total ? (proxVencer / total) : 0;
    const pctVenc = total ? (vencido / total) : 0;
    const pctTotRec = total ? (totRecep / total) : 0;

    setText("res_serv_total_badge", `${fmtInt(total)} pos.`);
    setText("res_servTotal", fmtInt(total));
    setText("res_servEnCurso", `${fmtInt(enCurso)} (${fmtPct01(pctEnCurso)})`);
    setText("res_servTotRecep", `${fmtInt(totRecep)} (${fmtPct01(pctTotRec)})`);
    setText("res_servVencido", `${fmtInt(vencido)} (${fmtPct01(pctVenc)})`);
    setText("res_servProxVencer", `${fmtInt(proxVencer)} (${fmtPct01(pctProx)})`);
    setText("res_servSinTrat", fmtInt(sinTrat + pedInfo));
    setText("res_servSinTratNote", `(${fmtInt(sinTrat)} sin trat. · ${fmtInt(pedInfo)} ped. info)`);

    // Construir los desgloses por ESTADO ITEM para cada tarjeta de Servicios
    servBreakdownsByCat = {
      TOTAL: {
        html: buildSubcatTooltipHTML("📋 Total Servicios", total, mapTotal)
      },
      EN_CURSO: {
        html: buildSubcatTooltipHTML("🟢 En Curso", enCurso, mapEnCurso)
      },
      RECEP_TOTAL: {
        html: buildSubcatTooltipHTML("🟠 En curso - Total recepcionado", totRecep, mapTotRecep)
      },
      VENCIDOS: {
        html: buildSubcatTooltipHTML("🔴 Vencido con cant. pend. a recep.", vencido, mapVencidos)
      },
      PROX_VENCER: {
        html: buildSubcatTooltipHTML("🟡 En curso - Próximo a vencer", proxVencer, mapProxVencer)
      },
      SIN_TRAT_INFO: {
        html: buildSubcatTooltipHTML(
          "🟣 Sin Tratamiento / Pedido de Info",
          sinTrat + pedInfo,
          mapSinTratInfo,
          `Incluye <b>${fmtInt(sinTrat)}</b> ítems con Estado Ítem «SIN TRATAMIENTO» y <b>${fmtInt(pedInfo)}</b> con Estado Servicio «Pedido de Info».`
        )
      }
    };

    const rowVenc = document.getElementById("res_servRowVencido");
    const elVenc = document.getElementById("res_servVencido");
    if (rowVenc) {
      rowVenc.style.border = vencido > 0 ? "1.5px solid #dc2626" : "1.5px solid #16a34a";
      rowVenc.style.background = vencido > 0 ? "#fef2f2" : "#f0fdf4";
    }
    if (elVenc) {
      elVenc.style.color = vencido > 0 ? "#dc2626" : "#16a34a";
    }
  }

  /* --- 4. BLOQUE TIEMPOS / PRIORIDAD (RESUMEN PORCENTAJES Y PROMEDIO DE DÍAS) --- */
  function updateTiemposBlock() {
    if (!cumplRawData) return;
    const tbody = document.getElementById("res_tiempos_tbody_pcts");
    if (!tbody) return;

    const selectedObras = getSelectedObras();
    const selectedMeses = getEffectiveMeses();

    // Actualizar badge de umbral de Poco Tiempo según Obra seleccionada
    const ruleBadge = document.getElementById("res_tiempos_rule_badge");
    if (ruleBadge) {
      if (selectedObras.length === 1) {
        const code = getCanonicalObraCode(selectedObras[0]);
        const lim = OBRAS_LIMIT_MAP[code] || 15;
        ruleBadge.textContent = `PARA OBRA ${code} POCO TIEMPO < ${lim} DÍAS`;
      } else if (selectedObras.length > 1) {
        ruleBadge.textContent = `POCO TIEMPO (${selectedObras.length} OBRAS)`;
      } else {
        ruleBadge.textContent = "POCO TIEMPO TODAS LAS OBRAS";
      }
    }

    // Fuente de datos (respeta modo Arriba para 365 y 372 si está activo)
    let sourceData = cumplRawData;
    if (isResumenArribaActive && arribaRawData && arribaRawData.length > 0) {
      const nonArribaBase = cumplRawData.filter(r => {
        const c = getCanonicalObraCode(r["CLIENTE"]);
        return c !== "365" && c !== "372";
      });
      const mappedArriba = arribaRawData.map(r => ({
        ...r,
        "COMPROMETIDOS": r["COMPROMETIDOS"],
        "ENTREGADOS AT": r["ENTREGADOS AT FINAL"] ?? r["ENTREGADOS AT"],
        "ENTREGADOS FT": r["ENTREGADOS FT FINAL"] ?? r["ENTREGADOS FT"],
        "NO ENTREGADOS": r["NO ENTREGADOS FINAL"] ?? r["NO ENTREGADOS"],
        "DIAS DE DEMORA": r["DEMORA FINAL"] ?? r["DIAS DE DEMORA"]
      }));
      sourceData = [...nonArribaBase, ...mappedArriba];
    }

    let rows = sourceData;
    if (selectedObras.length > 0) {
      const obraSet = new Set(selectedObras.map(getCanonicalObraCode));
      rows = rows.filter(r => obraSet.has(getCanonicalObraCode(r["CLIENTE"])));
    }
    if (selectedMeses.length > 0) {
      const mesSet = new Set(selectedMeses);
      rows = rows.filter(r => r._ym && mesSet.has(r._ym));
    }

    const groups = ["CRITICO", "POCO TIEMPO", "SIN PRIORIDAD"];
    const totals = {};
    groups.forEach(grp => {
      totals[grp] = { at: 0, ft: 0, ne: 0, tot: 0, daysAt: [], daysFt: [] };
    });

    const colFecEE = cumplHeaders.find(h => /entrega\s+esperada/i.test(h)) || "FECHA ENTREGA ESPERADA";
    const colFecEN = cumplHeaders.find(h => /emisi[oó]n\s+necesidad/i.test(h)) || "FECHA DE EMISION NECESIDAD";

    for (const r of rows) {
      const prio = Math.round(toNumber(r["PRIORIDAD"]));
      const dEE = parseDateAny(r[colFecEE] || r["FECHA ENTREGA ESPERADA"]);
      const dEN = parseDateAny(r[colFecEN] || r["FECHA DE EMISION NECESIDAD"]);
      let diff = 0;
      if (dEE && dEN) {
        diff = Math.round((dEE - dEN) / (1000 * 60 * 60 * 24));
      }

      const obraCode = getCanonicalObraCode(r["CLIENTE"]);
      const thresh = OBRAS_LIMIT_MAP[obraCode] || 15;
      const isCritico = (prio === 1 || prio === 2 || prio === 20);

      let grp = "SIN PRIORIDAD";
      if (isCritico) {
        grp = "CRITICO";
      } else if (diff < thresh) {
        grp = "POCO TIEMPO";
      }

      const at = Math.round(toNumber(r["ENTREGADOS AT"]));
      const ft = Math.round(toNumber(r["ENTREGADOS FT"]));
      const ne = Math.round(toNumber(r["NO ENTREGADOS"]));
      const tot = at + ft + ne;

      totals[grp].at += at;
      totals[grp].ft += ft;
      totals[grp].ne += ne;
      totals[grp].tot += tot;
      if (at > 0 && dEE && dEN) totals[grp].daysAt.push(diff);
      if (ft > 0 && dEE && dEN) totals[grp].daysFt.push(diff);
    }

    function fmtPctInt(v) {
      if (v == null || isNaN(v)) return "0%";
      return Math.round(v) + "%";
    }

    function pctCellsTot(obj) {
      const t = obj.tot;
      const pAT = t ? (obj.at / t) * 100 : 0;
      const pFT = t ? (obj.ft / t) * 100 : 0;
      const pNE = t ? (obj.ne / t) * 100 : 0;
      const pTOT = t ? "100%" : "0%";
      return `
        <td class="td-val">${fmtPctInt(pAT)}</td>
        <td class="td-val">${fmtPctInt(pFT)}</td>
        <td class="td-val">${fmtPctInt(pNE)}</td>
        <td class="td-val td-val-tot">${pTOT}</td>
      `;
    }

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

    tbody.innerHTML = `
      <tr class="tr-total-general">
        <td class="td-row-name">Total general</td>
        ${pctCellsTot(totals["CRITICO"])}
        ${pctCellsTot(totals["POCO TIEMPO"])}
        ${pctCellsTot(totals["SIN PRIORIDAD"])}
      </tr>
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
  }

  /* --- 3. BLOQUE DEMORAS --- */
  function updateDemorasBlock() {
    const selectedObras = getSelectedObras();
    const effectiveMeses = getEffectiveMeses();

    if (typeof window.renderResumenDemoras === "function") {
      window.renderResumenDemoras("res_chartMotivos", "res_chartAreas", selectedObras, effectiveMeses);
    }
  }

  /* --- 1. BLOQUE ANÁLISIS MM --- */
  function updateMMBlock() {
    if (!mmRawData) return;

    const selectedObras = getSelectedObras();

    const colAlmMM = mmHeaders.find(h => /almac[eé]n/i.test(h)) || "Almacén";
    const colMat = mmHeaders.find(h => /^material$/i.test(h)) || "Material";
    const colLibre = mmHeaders.find(h => /libre utilizaci/i.test(h) && !/valor/i.test(h) && !/[aá]rea/i.test(h)) || "Libre utilización";
    const colEstado = mmHeaders.find(h => /^estado$/i.test(h)) || "Estado";

    let rowsMM = mmRawData;
    if (selectedObras.length > 0) {
      const obraSet = new Set(selectedObras.map(getCanonicalObraCode));
      rowsMM = mmRawData.filter(r => obraSet.has(getCanonicalObraCode(r[colAlmMM])));
    }

    let obraLabel = "Todas las Obras";
    if (selectedObras.length === 1) {
      obraLabel = OBRA_MAP[selectedObras[0]] || `Obra / Almacén ${selectedObras[0]}`;
    } else if (selectedObras.length > 1) {
      if (selectedObras.length <= 2) {
        obraLabel = selectedObras.map(c => OBRA_MAP[c] || c).join(" + ");
      } else {
        obraLabel = `${selectedObras.length} Obras Seleccionadas`;
      }
    }

    setText("resumen_lblObra", obraLabel);
    const elLblObra = document.getElementById("resumen_lblObra");
    if (elLblObra) {
      elLblObra.title = selectedObras.map(c => OBRA_MAP[c] || c).join(", ");
    }

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
    let nuloVencidos = 0;

    if (stoNuloRawData && stoNuloRawData.length) {
      const colAlmNulo = stoNuloHeaders.find(h => /almac[eé]n/i.test(h)) || "Almacén";
      const colTipoDoc = stoNuloHeaders.find(h => /tipo doc/i.test(h)) || "TIPO DOC";
      const colFecEE = stoNuloHeaders.find(h => /entrega\s+esperada/i.test(h)) || "FECHA ENTREGA ESPERADA";

      const now = new Date();
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

      let rowsNulo = stoNuloRawData;
      if (selectedObras.length > 0) {
        const obraSet = new Set(selectedObras.map(getCanonicalObraCode));
        rowsNulo = stoNuloRawData.filter(r => obraSet.has(getCanonicalObraCode(r[colAlmNulo])));
      }

      for (const rn of rowsNulo) {
        const td = clean(rn[colTipoDoc]).toUpperCase();
        if (td === "SIN PEDIDO") {
          nuloSinPedido++;
        } else {
          nuloConPedido++;
          const dEE = parseDateAny(rn[colFecEE] || rn["FECHA ENTREGA ESPERADA"]);
          if (dEE && dEE < today) {
            nuloVencidos++;
          }
        }
      }
    }

    setText("res_txtTotal", fmtInt(totalMat));
    setText("res_txtTotal_card", fmtInt(totalMat));
    setText("res_txtDisp", fmtInt(dispMat));
    setText("res_txtPct", fmtPct01(pctDisp));

    const isDispGood = (Math.round((pctDisp || 0) * 1000) / 10 >= 90);

    const rad = document.getElementById("res_radial_circle");
    if (rad) {
      const p = Math.max(0, Math.min(100, ((pctDisp || 0) * 100)));
      const offset = 188.5 * (1 - (p / 100));
      rad.style.strokeDashoffset = offset;
      rad.style.stroke = isDispGood ? "#0f766e" : "#dc2626";
    }
    const tagDispStatus = document.getElementById("res_tagDispStatus");
    if (tagDispStatus) {
      tagDispStatus.textContent = isDispGood ? "En Rango" : "Bajo Objetivo";
      tagDispStatus.style.background = isDispGood ? "var(--success-bg, #f0fdfa)" : "var(--danger-bg, #fef2f2)";
      tagDispStatus.style.color = isDispGood ? "var(--success-text, #0f766e)" : "var(--danger-text, #b91c1c)";
      tagDispStatus.style.borderColor = isDispGood ? "var(--success-border, #ccfbf1)" : "var(--danger-border, #fecaca)";
    }
    const elDisp = document.getElementById("res_txtPct");
    if (elDisp) elDisp.style.setProperty("color", isDispGood ? "#16a34a" : "#dc2626", "important");
    const rowDisp = document.getElementById("res_rowDispPct");
    if (rowDisp) {
      rowDisp.style.border = isDispGood ? "1px solid #ccfbf1" : "1px solid #fecaca";
      rowDisp.style.background = isDispGood ? "#f0fdfa" : "#fef2f2";
    }
    const barDispFill = document.getElementById("res_disp_bar_fill");
    if (barDispFill) {
      const pctClamped = Math.max(0, Math.min(100, (pctDisp || 0)));
      barDispFill.style.width = pctClamped + "%";
      barDispFill.style.background = isDispGood ? "#0f766e" : "#dc2626";
    }

    const txtNuloHTML = `
      <ul style="list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 2px; font-size: 10.5px; color: #334155;">
        <li style="display: flex; align-items: center; gap: 5px;">
          <span style="color: #dc2626; font-weight: 900;">•</span>
          <span id="res_txtNulo" class="res-val" style="color: #dc2626; margin: 0 !important;">${fmtInt(cantStockNulo)} (${fmtPct01(pctNulo)})</span>
        </li>
        <li style="display: flex; align-items: center; gap: 5px;">
          <span style="color: #dc2626; font-weight: 900;">•</span>
          <mark style="background-color: #fef08a; color: #854d0e; padding: 0px 5px; font-size: 10px; border-radius: 3px; font-weight: 800; border: 1px solid #facc15;">${fmtInt(nuloSinPedido)} SIN PEDIDO</mark>
        </li>
        <li style="display: flex; align-items: center; gap: 5px; flex-wrap: wrap;">
          <span style="color: #dc2626; font-weight: 900;">•</span>
          <span>de los <strong style="color: #0f172a;">${fmtInt(nuloConPedido)}</strong> pedidos &rarr; <strong style="color: #dc2626;">${fmtInt(nuloVencidos)} con fecha de entrega vencida.</strong></span>
        </li>
      </ul>
    `;
    setHTML("res_wrapNulo", txtNuloHTML);

    setText("res_txtMenorPP", `${fmtInt(cantMenorPP)} (${fmtPct01(pctMenorPP)})`);
    setText("res_txtMayorPP", `${fmtInt(cantMayorPP)} (${fmtPct01(pctMayorPP)})`);
    setText("res_txtMayorMax", `${fmtInt(cantMayorMax)} (${fmtPct01(pctMayorMax)})`);

    const bMenor = document.getElementById("res_barMenorPP");
    if (bMenor) bMenor.style.width = Math.max(0, Math.min(100, (pctMenorPP || 0) * 100)) + "%";
    const bMayor = document.getElementById("res_barMayorPP");
    if (bMayor) bMayor.style.width = Math.max(0, Math.min(100, (pctMayorPP || 0) * 100)) + "%";
    const bMax = document.getElementById("res_barMayorMax");
    if (bMax) bMax.style.width = Math.max(0, Math.min(100, (pctMayorMax || 0) * 100)) + "%";

    renderMiniEvolMMChart(selectedObras);
  }

  function renderMiniEvolMMChart(selectedObras) {
    const el = document.getElementById("res_chartEvolMM");
    if (!el || typeof window.echarts === "undefined" || !evolRawData) return;

    if (!chartEvolMMInstance) {
      chartEvolMMInstance = window.echarts.init(el, null, { renderer: "canvas" });
    }

    let rows = evolRawData;
    if (selectedObras && selectedObras.length > 0) {
      const obraSet = new Set(selectedObras.map(getCanonicalObraCode));
      rows = evolRawData.filter(r => obraSet.has(getCanonicalObraCode(r["Obra"] || r["OBRA"])));
    }

    const monthMap = {};
    for (const r of rows) {
      const ym = parseYearMonth(r["Fecha"] || r["FECHA"]);
      if (!ym) continue;
      const rawPct = clean(r["% disponibilidad"] || r["% DISPONIBILIDAD"]).replace("%", "");
      const val = toNumber(rawPct);
      if (!monthMap[ym]) monthMap[ym] = { sum: 0, count: 0 };
      monthMap[ym].sum += val;
      monthMap[ym].count += 1;
    }

    const months = Object.keys(monthMap).sort();
    const values = months.map(m => {
      const obj = monthMap[m];
      return obj.count ? +(obj.sum / obj.count).toFixed(1) : 0;
    });

    const shortLabels = months.map(ym => {
      const [y, m] = ym.split("-");
      return `${m}/${y.slice(-2)}`;
    });

    chartEvolMMInstance.setOption({
      animation: true,
      animationDuration: 400,
      grid: { left: 6, right: 6, top: 8, bottom: 16, containLabel: false },
      tooltip: {
        trigger: "axis",
        confine: true,
        backgroundColor: "rgba(15, 23, 42, 0.92)",
        borderColor: "#0d9488",
        borderWidth: 1,
        padding: [4, 8],
        textStyle: { color: "#ffffff", fontSize: 10.5 },
        formatter: (params) => {
          const p = params && params[0];
          if (!p) return "";
          return `<b>${p.name}</b><br/>Disponibilidad: <b>${String(p.value).replace(".", ",")}%</b>`;
        }
      },
      xAxis: {
        type: "category",
        data: shortLabels,
        boundaryGap: false,
        axisLine: { lineStyle: { color: "#cbd5e1" } },
        axisTick: { show: false },
        axisLabel: {
          show: true,
          fontSize: 8.5,
          color: "#64748b",
          interval: Math.max(0, Math.floor(shortLabels.length / 4) - 1)
        }
      },
      yAxis: {
        type: "value",
        min: (v) => Math.max(0, Math.floor(v.min - 8)),
        max: 100,
        splitLine: { show: true, lineStyle: { color: "#f1f5f9", type: "dashed" } },
        axisLabel: { show: false },
        axisLine: { show: false },
        axisTick: { show: false }
      },
      series: [
        {
          name: "% Disponibilidad",
          type: "line",
          smooth: 0.35,
          symbol: "circle",
          symbolSize: 4,
          label: { show: false },
          lineStyle: { width: 2.2, color: "#0d9488" },
          itemStyle: { color: "#0d9488" },
          areaStyle: {
            color: new window.echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: "rgba(13, 148, 136, 0.32)" },
              { offset: 1, color: "rgba(13, 148, 136, 0.03)" }
            ])
          },
          markLine: {
            silent: true,
            symbol: "none",
            label: {
              show: true,
              position: "insideEndTop",
              formatter: "Obj 90%",
              fontSize: 8,
              fontWeight: 600,
              color: "rgba(100, 116, 139, 0.85)",
              backgroundColor: "rgba(255, 255, 255, 0.65)",
              padding: [0, 2],
              borderRadius: 2
            },
            lineStyle: { color: "rgba(100, 116, 139, 0.55)", type: "dashed", width: 1.1 },
            data: [{ yAxis: 90 }]
          },
          data: values
        }
      ]
    }, true);
  }

  /* --- 2. BLOQUE CUMPLIMIENTO --- */
  function updateCumplimientoBlock() {
    if (!cumplRawData) return;

    const selectedObras = getSelectedObras();
    // Para ACUMULADO 12 MESES: usa los filtros de la barra lateral izquierda (Año y Mes Evaluado)
    const sidebarMeses = getEffectiveMeses();
    // Para PERÍODO EVALUADO (derecha): usa EXCLUSIVAMENTE su filtro individual #res_cumplInlineMesSelect
    const inlineMeses = getSelectedCumplInlineMes();
    const selectedMeses = inlineMeses;
    const rawSelectedMeses = inlineMeses;
    const selectedAnios = [];

    // Determinar fuente de datos según modo Base vs. Cumplimiento Arriba (Obras 365 y 372)
    let sourceData = cumplRawData;
    if (isResumenArribaActive && arribaRawData && arribaRawData.length > 0) {
      const nonArribaBase = cumplRawData.filter(r => {
        const c = getCanonicalObraCode(r["CLIENTE"]);
        return c !== "365" && c !== "372";
      });
      const mappedArriba = arribaRawData.map(r => ({
        ...r,
        "COMPROMETIDOS": r["COMPROMETIDOS"],
        "ENTREGADOS AT": r["ENTREGADOS AT FINAL"] ?? r["ENTREGADOS AT"],
        "ENTREGADOS FT": r["ENTREGADOS FT FINAL"] ?? r["ENTREGADOS FT"],
        "NO ENTREGADOS": r["NO ENTREGADOS FINAL"] ?? r["NO ENTREGADOS"],
        "DIAS DE DEMORA": r["DEMORA FINAL"] ?? r["DIAS DE DEMORA"]
      }));
      sourceData = [...nonArribaBase, ...mappedArriba];
    }

    // 1. Filtrar por Obra seleccionada
    let rowsBase = sourceData;
    if (selectedObras.length > 0) {
      const obraSet = new Set(selectedObras.map(getCanonicalObraCode));
      rowsBase = sourceData.filter(r => obraSet.has(getCanonicalObraCode(r["CLIENTE"])));
    }

    // Orden cronológico de meses presentes
    const allMonths = [...new Set(rowsBase.map(r => r._ym).filter(Boolean))].sort();

    // Meses evaluados para la columna derecha (PERÍODO EVALUADO -> filtro individual)
    const evalMonths = inlineMeses.length > 0 ? inlineMeses : allMonths;

    // Identificar mes anterior si se seleccionó exactamente 1 mes en el filtro individual para calcular variación
    let prevYM = null;
    if (inlineMeses.length === 1 && allMonths.length) {
      const idx = allMonths.indexOf(inlineMeses[0]);
      if (idx > 0) {
        prevYM = allMonths[idx - 1];
      }
    }

    // Identificar últimos 12 meses cronológicos (LTM) para ACUMULADO 12 MESES según filtros de la barra lateral
    const defaultRefYM = allMonths.length > 1 ? allMonths[allMonths.length - 2] : (allMonths[0] || null);
    const refYM = sidebarMeses.length ? sidebarMeses[sidebarMeses.length - 1] : defaultRefYM;
    let ltmMonths = [];
    if (refYM && allMonths.length) {
      ltmMonths = allMonths.filter(m => m <= refYM).slice(-12);
    }
    if (!ltmMonths.length) {
      ltmMonths = (allMonths.length > 1 ? allMonths.slice(0, -1) : allMonths).slice(-12);
    }

    // Filtrar filas
    const rowsLTM = rowsBase.filter(r => ltmMonths.includes(r._ym));
    const evalMonthsSet = new Set(evalMonths);
    const rowsCurr = rowsBase.filter(r => evalMonthsSet.has(r._ym));
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
    const isAcumGood = (Math.round(mLTM.pctAt * 1000) / 10 >= 78);
    const elAcumAT = document.getElementById("res_cumplAcumATpct");
    if (elAcumAT) elAcumAT.style.setProperty("color", isAcumGood ? "#16a34a" : "#dc2626", "important");
    const rowAcumAT = document.getElementById("res_cumplAcumRowAT");
    if (rowAcumAT) {
      rowAcumAT.style.border = isAcumGood ? "1.5px solid #16a34a" : "1.5px solid #dc2626";
      rowAcumAT.style.background = isAcumGood ? "#f0fdf4" : "#fef2f2";
    }

    // Actualizar anillo radial y etiqueta de objetivo para Acumulado
    const radAcum = document.getElementById("res_radial_circle_acum");
    if (radAcum) {
      const pAcum = Math.max(0, Math.min(100, (mLTM.pctAt * 100)));
      const offsetAcum = 188.5 * (1 - (pAcum / 100));
      radAcum.style.strokeDashoffset = offsetAcum;
      radAcum.style.stroke = isAcumGood ? "#0f766e" : "#dc2626";
    }
    const tagAcumStatus = document.getElementById("res_tagAcumStatus");
    if (tagAcumStatus) {
      tagAcumStatus.textContent = isAcumGood ? "En Objetivo" : "Bajo Objetivo";
      tagAcumStatus.style.background = isAcumGood ? "var(--success-bg, #f0fdfa)" : "var(--danger-bg, #fef2f2)";
      tagAcumStatus.style.color = isAcumGood ? "var(--success-text, #0f766e)" : "var(--danger-text, #b91c1c)";
      tagAcumStatus.style.borderColor = isAcumGood ? "var(--success-border, #ccfbf1)" : "var(--danger-border, #fecaca)";
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
    let mesLabel = "Todos los Meses";
    if (rawSelectedMeses.length === 0 && selectedAnios.length > 0) {
      mesLabel = selectedAnios.length === 1
        ? `Año ${selectedAnios[0]}`
        : `Años ${selectedAnios.join(", ")}`;
    } else if (selectedMeses.length === 1) {
      const [y, m] = selectedMeses[0].split("-");
      mesLabel = `${MES_NOMBRES[m] || m} ${y}`;
    } else if (selectedMeses.length > 1) {
      if (selectedMeses.length <= 2) {
        mesLabel = selectedMeses.map(ym => {
          const [y, m] = ym.split("-");
          return `${MES_NOMBRES[m] || m} ${y}`;
        }).join(", ");
      } else {
        mesLabel = `${selectedMeses.length} Meses Seleccionados`;
      }
    }
    setText("res_cumplMesLabel", mesLabel);
    setText("res_cumplMesSide", mesLabel);
    const elMesSide = document.getElementById("res_cumplMesSide");
    if (elMesSide) {
      elMesSide.title = selectedMeses.map(ym => {
        const [y, m] = ym.split("-");
        return `${MES_NOMBRES[m] || m} ${y}`;
      }).join(", ");
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

    const hasPrev = (selectedMeses.length === 1 && rowsPrev.length > 0);
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

    const isCurrGood = (Math.round(mCurr.pctAt * 1000) / 10 >= 78);
    const elAT = document.getElementById("res_cumplATpct");
    if (elAT) elAT.style.setProperty("color", isCurrGood ? "#16a34a" : "#dc2626", "important");
    const rowCurrAT = document.getElementById("res_cumplRowAT");
    if (rowCurrAT) {
      rowCurrAT.style.border = isCurrGood ? "1.5px solid #16a34a" : "1.5px solid #dc2626";
      rowCurrAT.style.background = isCurrGood ? "#f0fdf4" : "#fef2f2";
    }

    // Actualizar anillo radial y etiqueta de objetivo para Período Seleccionado
    const radCurr = document.getElementById("res_radial_circle_curr");
    if (radCurr) {
      const pCurr = Math.max(0, Math.min(100, (mCurr.pctAt * 100)));
      const offsetCurr = 188.5 * (1 - (pCurr / 100));
      radCurr.style.strokeDashoffset = offsetCurr;
      radCurr.style.stroke = isCurrGood ? "#0f766e" : "#dc2626";
    }
    const tagCurrStatus = document.getElementById("res_tagCurrStatus");
    if (tagCurrStatus) {
      tagCurrStatus.textContent = isCurrGood ? "En Objetivo" : "Bajo Objetivo";
      tagCurrStatus.style.background = isCurrGood ? "var(--success-bg, #f0fdfa)" : "var(--danger-bg, #fef2f2)";
      tagCurrStatus.style.color = isCurrGood ? "var(--success-text, #0f766e)" : "var(--danger-text, #b91c1c)";
      tagCurrStatus.style.borderColor = isCurrGood ? "var(--success-border, #ccfbf1)" : "var(--danger-border, #fecaca)";
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
    const elNE = document.getElementById("res_cumplNEpct");
    if (elNE) elNE.style.color = "#dc2626";

    // Demora Promedio
    setText("res_cumplDemoraAvg", Math.round(mCurr.avgDem) + " d");
    const elDem = document.getElementById("res_cumplDemoraAvg");
    if (elDem) elDem.style.setProperty("color", (mCurr.avgDem > 7) ? "#dc2626" : "#16a34a", "important");

    renderMiniCumplTrendChart(rowsBase, ltmMonths);
  }

  function renderMiniCumplTrendChart(rowsBase, ltmMonths) {
    const el = document.getElementById("res_chartTendenciaCumpl");
    if (!el || typeof window.echarts === "undefined") return;

    if (!chartTendCumplInstance) {
      chartTendCumplInstance = window.echarts.init(el, null, { renderer: "canvas" });
    }

    const months = (ltmMonths && ltmMonths.length) ? ltmMonths : [];
    const monthStats = {};
    months.forEach(m => { monthStats[m] = { at: 0, ft: 0, ne: 0, tot: 0 }; });

    for (const r of rowsBase) {
      const m = r._ym;
      if (!m || !monthStats[m]) continue;
      const at = toNumber(r["ENTREGADOS AT"]);
      const ft = toNumber(r["ENTREGADOS FT"]);
      const ne = toNumber(r["NO ENTREGADOS"]);
      let tot = toNumber(r["COMPROMETIDOS"]);
      if (!tot) tot = at + ft + ne;
      monthStats[m].at += at;
      monthStats[m].ft += ft;
      monthStats[m].ne += ne;
      monthStats[m].tot += tot;
    }

    const MES_CORTO = {
      "01": "ene", "02": "feb", "03": "mar", "04": "abr",
      "05": "may", "06": "jun", "07": "jul", "08": "ago",
      "09": "sep", "10": "oct", "11": "nov", "12": "dic"
    };
    const shortLabels = months.map(ym => {
      const [y, m] = ym.split("-");
      return `${MES_CORTO[m] || m}${y.slice(-2)}`;
    });

    const pctAtData = [];

    months.forEach(m => {
      const s = monthStats[m];
      const pAt = s.tot ? +((s.at / s.tot) * 100).toFixed(1) : 0;
      pctAtData.push(pAt);
    });

    // Configuración idéntica a la Imagen 2 de referencia (% AT vs Meta 78%)
    chartTendCumplInstance.setOption({
      backgroundColor: "transparent",
      animation: true,
      animationDuration: 400,
      grid: { left: 34, right: 30, top: 16, bottom: 20, containLabel: false },
      tooltip: {
        trigger: "axis",
        confine: true,
        backgroundColor: "rgba(15, 23, 42, 0.94)",
        borderColor: "#334155",
        borderWidth: 1,
        padding: [6, 10],
        textStyle: { color: "#ffffff", fontSize: 11 },
        formatter: (params) => {
          if (!params || !params.length) return "";
          const name = params[0].name || "";
          let lines = params.map(p => `${p.marker} ${p.seriesName}: <b>${String(p.value).replace(".", ",")}%</b>`);
          return `<div style="font-weight:700;margin-bottom:3px;">Período ${name}</div>` + lines.join("<br/>");
        }
      },
      xAxis: {
        type: "category",
        data: shortLabels,
        boundaryGap: false,
        axisLine: { lineStyle: { color: "#cbd5e1" } },
        axisTick: { show: false },
        axisLabel: {
          show: true,
          fontSize: 9.5,
          fontWeight: 600,
          color: "#64748b",
          interval: 0,
          hideOverlap: true
        }
      },
      yAxis: {
        type: "value",
        min: value => Math.max(0, Math.min(65, Math.floor((value.min - 5) / 5) * 5)),
        max: value => Math.min(100, Math.max(95, Math.ceil((value.max + 5) / 5) * 5)),
        interval: 10,
        splitLine: { show: true, lineStyle: { color: "#f1f5f9" } },
        axisLabel: {
          show: true,
          formatter: "{value}%",
          color: "#64748b",
          fontSize: 9.5
        },
        axisLine: { show: false },
        axisTick: { show: false }
      },
      series: [
        {
          name: "%AT Real",
          type: "line",
          smooth: 0.35,
          symbol: "circle",
          symbolSize: 6,
          showSymbol: true,
          lineStyle: { width: 2.6, color: "#0f766e" },
          itemStyle: { color: "#0f766e", borderWidth: 2, borderColor: "#ffffff" },
          areaStyle: {
            color: new window.echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: "rgba(15, 118, 110, 0.18)" },
              { offset: 1, color: "rgba(15, 118, 110, 0.0)" }
            ])
          },
          markLine: {
            symbol: ["none", "none"],
            silent: true,
            data: [{
              yAxis: 78,
              label: {
                show: true,
                formatter: "Meta 78%",
                position: "insideEndTop",
                color: "#0f766e",
                fontSize: 9.5,
                fontWeight: 700
              },
              lineStyle: { type: "dashed", color: "#0f766e", width: 1.5 }
            }]
          },
          data: pctAtData
        }
      ]
    }, true);
  }

  window.resizeResumenMiniCharts = function () {
    if (chartEvolMMInstance) chartEvolMMInstance.resize();
    if (chartTendCumplInstance) chartTendCumplInstance.resize();
  };

  window.addEventListener("resize", () => {
    if (typeof window.resizeResumenMiniCharts === "function") {
      window.resizeResumenMiniCharts();
    }
  });

  // Hook global de inicialización
    // Filtro rápido de obras para el buscador del sidebar en Tablero
  window.filterResumenObraSelect = function(query) {
    const sel = document.getElementById("resumen_obraSelect");
    if (!sel) return;
    const q = (query || "").toLowerCase().trim();
    Array.from(sel.options).forEach(opt => {
      if (opt.value === "__ALL__") {
        opt.style.display = "";
        return;
      }
      const match = opt.text.toLowerCase().includes(q);
      opt.style.display = match ? "" : "none";
    });
  };

  window.initResumen = function () {
    loadResumenData();
    if (!window.demorasInitialized && typeof window.initDemoras === "function") {
      window.initDemoras();
    }
    updateDemorasBlock();
  };

})();
