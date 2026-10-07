/**
 * control-emrf.js — Control de Partidas Abiertas SAP (Cuenta EM/RF 2101011001)
 * Réplica completa del proyecto tablero-milicic para el portal Abastecimiento.
 */

(function () {
  const JSON_URL = "data/partidas_emrf.json";
  
  // Estado global del módulo
  let allPositions = [];
  let metadata = null;
  let isInitialized = false;
  let currentSort = { col: 'Dias_Atraso', dir: 'desc' };
  let currentPage = 1;
  let pageSize = 50; // default 50 por página para óptimo rendimiento
  let lastGcSelected = new Set(["C01", "C07"]);

  // Formateadores
  function fmtCurrency(val) {
    if (val === null || val === undefined || isNaN(val)) return "$ 0,00";
    const num = Number(val);
    const parts = Math.abs(num).toFixed(2).split('.');
    const integerPart = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    const decimalPart = parts[1];
    const sign = num < 0 ? "-$ " : "$ ";
    return `${sign}${integerPart},${decimalPart}`;
  }

  function fmtInt(val) {
    if (val === null || val === undefined || isNaN(val)) return "0";
    return Number(val).toLocaleString("es-AR");
  }

  function fmtDate(isoStr) {
    if (!isoStr) return "-";
    const parts = String(isoStr).split('-');
    if (parts.length === 3) {
      return `${parts[2]}/${parts[1]}/${parts[0]}`;
    }
    return isoStr;
  }

  function getMultiSelectValues(selectId) {
    const el = document.getElementById(selectId);
    if (!el) return [];
    return Array.from(el.selectedOptions)
      .map(opt => opt.value)
      .filter(v => v !== "__ALL__" && v !== "");
  }

  function handleGcSelectChange() {
    const sel = document.getElementById("emrf_gcSelect");
    if (!sel) return;

    const currentSelected = Array.from(sel.selectedOptions).map(o => o.value);
    const hadAll = lastGcSelected.has("__ALL__");
    const hasAll = currentSelected.includes("__ALL__");

    if (!hadAll && hasAll) {
      // Usuario seleccionó "Todos" -> desmarcar todas las opciones individuales
      Array.from(sel.options).forEach(opt => {
        opt.selected = (opt.value === "__ALL__");
      });
    } else if (hadAll && currentSelected.length > 1) {
      // Tenía "Todos" y el usuario hizo click en una opción específica -> desmarcar "Todos"
      Array.from(sel.options).forEach(opt => {
        if (opt.value === "__ALL__") opt.selected = false;
      });
    } else if (currentSelected.length === 0) {
      // Si el usuario desmarcó todo, volver a marcar "Todos"
      const allOpt = Array.from(sel.options).find(o => o.value === "__ALL__");
      if (allOpt) allOpt.selected = true;
    }

    lastGcSelected = new Set(Array.from(sel.selectedOptions).map(o => o.value));
  }

  function populateSelect(selectId, items, defaultValues = [], hasAllOption = false) {
    const el = document.getElementById(selectId);
    if (!el) return;

    el.innerHTML = "";
    if (hasAllOption) {
      const allOpt = document.createElement("option");
      allOpt.value = "__ALL__";
      allOpt.textContent = "Todos";
      if (!defaultValues || defaultValues.length === 0) allOpt.selected = true;
      el.appendChild(allOpt);
    }

    items.forEach(item => {
      const opt = document.createElement("option");
      opt.value = item;
      opt.textContent = item;
      if (defaultValues && defaultValues.includes(item)) {
        opt.selected = true;
      }
      el.appendChild(opt);
    });
  }

  /* ==============================================================================
     CARGA DE DATOS (CON CACHÉ INDEXEDDB)
     ============================================================================== */
  async function loadData() {
    const loader = document.getElementById("emrf_loader");
    if (loader) loader.style.display = "flex";

    try {
      let rawJson = null;
      if (typeof window.fetchWithCache === 'function') {
        const cacheUrl = JSON_URL + (window.CACHE_BUSTER ? `?v=${window.CACHE_BUSTER}` : "");
        const text = await window.fetchWithCache(cacheUrl);
        rawJson = JSON.parse(text);
      } else {
        const resp = await fetch(JSON_URL);
        rawJson = await resp.json();
      }

      if (rawJson && rawJson.data) {
        allPositions = rawJson.data;
        metadata = rawJson.metadata || {};
      } else {
        throw new Error("Estructura de datos inválida en " + JSON_URL);
      }
    } catch (err) {
      console.error("[EMRF] Error al cargar partidas_emrf.json:", err);
      const msgEl = document.getElementById("emrf_msg");
      if (msgEl) {
        msgEl.innerHTML = `<div class="error"><b>Error de carga:</b> No se pudieron obtener los datos de EM/RF (${err.message}). Verifique la conexión o contacte al administrador.</div>`;
      }
    } finally {
      if (loader) loader.style.display = "none";
    }
  }

  /* ==============================================================================
     INICIALIZACIÓN DE FILTROS
     ============================================================================== */
  function setupFilters() {
    if (!allPositions || allPositions.length === 0) return;

    const fechaActEl = document.getElementById("emrf_fechaActualizacion");
    if (fechaActEl) {
      fechaActEl.textContent = window.LAST_UPDATE || metadata?.fecha_corte || "05/10/2026";
    }

    // 1. Sociedad (dropdown simple)
    const socSelect = document.getElementById("emrf_sociedadSelect");
    if (socSelect) {
      const socs = ["Todas (Consolidado)", ...new Set(allPositions.map(p => p.Sociedad))].filter(Boolean);
      socSelect.innerHTML = "";
      socs.forEach((s, idx) => {
        const opt = document.createElement("option");
        opt.value = s === "Todas (Consolidado)" ? "TODAS" : s;
        opt.textContent = s;
        if (idx === 0) opt.selected = true;
        socSelect.appendChild(opt);
      });
    }

    // 2. Estado Contable EM/RF
    const emrfOptions = [
      "TIENE RECEPCIÓN - FALTA FACTURA",
      "TIENE FACTURA - FALTA RECEPCIÓN",
      "COMPENSABLE (Saldo $0)"
    ];
    populateSelect("emrf_estadoSelect", emrfOptions, ["TIENE RECEPCIÓN - FALTA FACTURA"]);

    // 3. Grupo de Compras OC
    const gcs = [...new Set(allPositions.map(p => p.Grupo_Compras))]
      .filter(g => g && g !== "SIN GRUPO")
      .sort();
    const defaultGCs = gcs.filter(g => g === "C01" || g === "C07");
    populateSelect("emrf_gcSelect", gcs, defaultGCs.length > 0 ? defaultGCs : ["C01", "C07"], true);
    lastGcSelected = new Set(defaultGCs.length > 0 ? defaultGCs : ["C01", "C07"]);

    // 4. Estado de Vencimiento OC
    const vencOptions = ["VENCIDA", "VIGENTE", "SIN FECHA OC"];
    populateSelect("emrf_vencSelect", vencOptions, []);

    // 5. Operador OC
    const opOCs = [...new Set(allPositions.map(p => p.Operador_OC))]
      .filter(o => o && o !== "SIN ASIGNAR")
      .sort();
    populateSelect("emrf_operOcSelect", opOCs, []);

    // 6. Selector de filas
    const rowsSelect = document.getElementById("emrf_rowsPerPage");
    if (rowsSelect) {
      rowsSelect.value = "50";
      pageSize = 50;
    }
  }

  /* ==============================================================================
     APLICAR FILTROS
     ============================================================================== */
  function getFilteredData() {
    if (!allPositions || allPositions.length === 0) return [];

    const socVal = document.getElementById("emrf_sociedadSelect")?.value || "TODAS";
    const selEmrf = getMultiSelectValues("emrf_estadoSelect");
    const selGC = getMultiSelectValues("emrf_gcSelect");
    const selVenc = getMultiSelectValues("emrf_vencSelect");
    const selOperOC = getMultiSelectValues("emrf_operOcSelect");

    return allPositions.filter(p => {
      // 1. Sociedad
      if (socVal !== "TODAS" && p.Sociedad !== socVal) return false;

      // 2. Estado Contable EM/RF
      if (selEmrf.length > 0 && !selEmrf.includes(p.Grupo_EMRF)) return false;

      // 3. Grupo de Compras
      if (selGC.length > 0 && !selGC.includes(p.Grupo_Compras)) return false;

      // 4. Estado de Vencimiento
      if (selVenc.length > 0 && !selVenc.includes(p.Estado_Vencimiento)) return false;

      // 5. Operador OC
      if (selOperOC.length > 0 && !selOperOC.includes(p.Operador_OC)) return false;

      return true;
    });
  }

  /* ==============================================================================
     ACTUALIZAR MÉTRICAS Y KPIS
     ============================================================================== */
  function updateKPIs(filtered) {
    const totalPos = allPositions.length;
    const filtPos = filtered.length;
    const pct = totalPos > 0 ? ((filtPos / totalPos) * 100).toFixed(1) : "0.0";

    // Actualizar tarjeta única POSICIONES SELECCIONADAS (sin monto en pesos)
    const elCount = document.getElementById("emrf_kpiCount");
    const elPct = document.getElementById("emrf_kpiPct");

    if (elCount) elCount.textContent = fmtInt(filtPos);
    if (elPct) elPct.textContent = `${pct}% del total (${fmtInt(totalPos)})`;

    // Actualizar badge de sociedad en encabezado
    const socSelect = document.getElementById("emrf_sociedadSelect");
    const badgeSoc = document.getElementById("emrf_headerSocBadge");
    if (socSelect && badgeSoc) {
      const selectedText = socSelect.options[socSelect.selectedIndex]?.textContent || "Todas (Consolidado)";
      badgeSoc.textContent = selectedText;
    }

    // Actualizar título de la tabla
    const tableTitle = document.getElementById("emrf_tableCount");
    if (tableTitle) {
      tableTitle.textContent = fmtInt(filtPos);
    }
  }

  /* ==============================================================================
     ORDENAMIENTO Y RENDERIZADO DE TABLA
     ============================================================================== */
  function sortPositions(positions) {
    if (!currentSort.col) return positions;

    return [...positions].sort((a, b) => {
      let vA = a[currentSort.col];
      let vB = b[currentSort.col];

      if (vA === null || vA === undefined) vA = "";
      if (vB === null || vB === undefined) vB = "";

      // Comparación numérica
      if (typeof vA === "number" && typeof vB === "number") {
        return currentSort.dir === "asc" ? vA - vB : vB - vA;
      }

      // Comparación alfabética
      const sA = String(vA).toLowerCase();
      const sB = String(vB).toLowerCase();
      if (sA < sB) return currentSort.dir === "asc" ? -1 : 1;
      if (sA > sB) return currentSort.dir === "asc" ? 1 : -1;
      return 0;
    });
  }

  function renderTable(filtered) {
    const tbody = document.getElementById("emrf_tableBody");
    if (!tbody) return;

    const sorted = sortPositions(filtered);
    const totalRows = sorted.length;

    // Calcular páginas
    let rowsToShow = sorted;
    if (pageSize !== "TODAS") {
      const limit = parseInt(pageSize, 10);
      const totalPages = Math.ceil(totalRows / limit) || 1;
      if (currentPage > totalPages) currentPage = totalPages;
      if (currentPage < 1) currentPage = 1;

      const startIndex = (currentPage - 1) * limit;
      rowsToShow = sorted.slice(startIndex, startIndex + limit);

      updatePaginationControls(currentPage, totalPages, totalRows, startIndex, rowsToShow.length);
    } else {
      updatePaginationControls(1, 1, totalRows, 0, totalRows);
    }

    if (rowsToShow.length === 0) {
      tbody.innerHTML = `<tr><td colspan="13" style="text-align:center; padding: 2.5rem; color:#64748b; font-weight:600;">
        🔍 No se encontraron posiciones que coincidan con los filtros seleccionados.
      </td></tr>`;
      return;
    }

    let html = "";
    for (const r of rowsToShow) {
      const socClass = "badge-soc-" + (r.Sociedad || "").toLowerCase();
      const vencClass = r.Estado_Vencimiento === "VENCIDA" ? "badge-venc-vencida" :
                         r.Estado_Vencimiento === "VIGENTE" ? "badge-venc-vigente" : "badge-venc-sinfecha";

      const saldoClass = r.Saldo_Neto < 0 ? "saldo-negativo" : r.Saldo_Neto > 0 ? "saldo-positivo" : "saldo-cero";
      const diasClass = r.Dias_Atraso > 0 ? "dias-alerta" : "";

      html += `<tr>
        <td class="emrf-col-center"><span class="badge-soc ${socClass}">${r.Sociedad}</span></td>
        <td><strong>${r.Pedido}</strong></td>
        <td class="emrf-col-center">${r.Posicion}</td>
        <td title="${r.Proveedor}" style="max-width:220px; overflow:hidden; text-overflow:ellipsis;">${r.Proveedor}</td>
        <td class="emrf-col-center">${r.Grupo_Compras}</td>
        <td class="emrf-col-center">${r.Operador_OC}</td>
        <td class="emrf-col-center">${fmtDate(r.Fe_Contabilizacion)}</td>
        <td class="emrf-col-right ${diasClass}">${fmtInt(r.Dias_Atraso)}</td>
        <td class="emrf-col-right">${fmtCurrency(r.Total_Debe)}</td>
        <td class="emrf-col-right">${fmtCurrency(r.Total_Haber)}</td>
        <td class="emrf-col-right ${saldoClass}">${fmtCurrency(r.Saldo_Neto)}</td>
        <td class="emrf-col-center">${fmtDate(r.Fecha_Entrega_OC)}</td>
        <td class="emrf-col-center"><span class="badge-venc ${vencClass}">${r.Estado_Vencimiento}</span></td>
      </tr>`;
    }

    tbody.innerHTML = html;
  }

  function updatePaginationControls(currPage, totalPages, totalRows, startIdx, pageRowsCount) {
    const infoEl = document.getElementById("emrf_pageInfo");
    const prevBtn = document.getElementById("emrf_btnPrevPage");
    const nextBtn = document.getElementById("emrf_btnNextPage");
    const rangeEl = document.getElementById("emrf_pageRange");

    if (infoEl) {
      infoEl.textContent = `Página ${currPage} de ${totalPages}`;
    }

    if (rangeEl) {
      if (totalRows === 0) {
        rangeEl.textContent = "Mostrando 0 posiciones";
      } else if (pageSize === "TODAS") {
        rangeEl.textContent = `Mostrando el 100% (${fmtInt(totalRows)} posiciones)`;
      } else {
        const from = startIdx + 1;
        const to = startIdx + pageRowsCount;
        rangeEl.textContent = `Mostrando ${fmtInt(from)} - ${fmtInt(to)} de ${fmtInt(totalRows)} posiciones`;
      }
    }

    if (prevBtn) prevBtn.disabled = currPage <= 1 || pageSize === "TODAS";
    if (nextBtn) nextBtn.disabled = currPage >= totalPages || pageSize === "TODAS";
  }

  /* ==============================================================================
     EVENT HANDLERS Y DESCARGA EXCEL (CON EXCELJS - IDÉNTICO A STREAMLIT)
     ============================================================================== */
  function onFiltersChanged(e) {
    if (e && e.target && e.target.id === "emrf_gcSelect") {
      handleGcSelectChange();
    }
    currentPage = 1;
    const filtered = getFilteredData();
    updateKPIs(filtered);
    renderTable(filtered);
  }

  function clearFilters() {
    const socSelect = document.getElementById("emrf_sociedadSelect");
    if (socSelect) socSelect.value = "TODAS";

    populateSelect("emrf_estadoSelect", [
      "TIENE RECEPCIÓN - FALTA FACTURA",
      "TIENE FACTURA - FALTA RECEPCIÓN",
      "COMPENSABLE (Saldo $0)"
    ], ["TIENE RECEPCIÓN - FALTA FACTURA"]);

    const gcs = [...new Set(allPositions.map(p => p.Grupo_Compras))].filter(g => g && g !== "SIN GRUPO").sort();
    const defaultGCs = gcs.filter(g => g === "C01" || g === "C07");
    populateSelect("emrf_gcSelect", gcs, defaultGCs.length > 0 ? defaultGCs : ["C01", "C07"], true);
    lastGcSelected = new Set(defaultGCs.length > 0 ? defaultGCs : ["C01", "C07"]);

    populateSelect("emrf_vencSelect", ["VENCIDA", "VIGENTE", "SIN FECHA OC"], []);
    populateSelect("emrf_operOcSelect", [...new Set(allPositions.map(p => p.Operador_OC))].filter(o => o && o !== "SIN ASIGNAR").sort(), []);

    onFiltersChanged();
  }

  async function exportToExcel() {
    if (typeof ExcelJS === 'undefined') {
      alert("Error: La librería ExcelJS no está cargada. Refresque la página.");
      return;
    }

    const filtered = getFilteredData();
    if (!filtered || filtered.length === 0) {
      alert("No hay posiciones para exportar con los filtros seleccionados.");
      return;
    }

    const socVal = document.getElementById("emrf_sociedadSelect")?.value || "TODAS";
    const socName = socVal === "TODAS" ? "CONSOLIDADO" : socVal;
    const now = new Date();
    const timestampStr = now.toISOString().replace(/[-:T]/g, '').slice(0, 14);
    const filename = `CONTROL_EM_RF_${socName}_${timestampStr}.xlsx`;

    try {
      const workbook = new ExcelJS.Workbook();
      workbook.creator = "Portal Abastecimiento - Milicic";
      workbook.created = now;

      const worksheet = workbook.addWorksheet("Posiciones_Filtradas");

      // Columnas exactamente como Streamlit app.py
      const columnsDef = [
        { header: "Sociedad", key: "Sociedad", width: 12 },
        { header: "Pedido", key: "Pedido", width: 16 },
        { header: "POS", key: "POS", width: 8 },
        { header: "Proveedor", key: "Proveedor", width: 35 },
        { header: "GC", key: "GC", width: 8 },
        { header: "Operador_OC", key: "Operador_OC", width: 16 },
        { header: "FE CONT.", key: "FE_CONT", width: 14 },
        { header: "Dias_Atraso", key: "Dias_Atraso", width: 14 },
        { header: "Facturado (Debe)", key: "Facturado_Debe", width: 20 },
        { header: "Recepcionado (Haber)", key: "Recepcionado_Haber", width: 22 },
        { header: "Saldo_Neto", key: "Saldo_Neto", width: 18 },
        { header: "FE OC", key: "FE_OC", width: 14 },
        { header: "ESTADO", key: "ESTADO", width: 14 }
      ];

      worksheet.columns = columnsDef;

      // Estilo de encabezados
      const headerRow = worksheet.getRow(1);
      headerRow.height = 28;
      headerRow.font = { name: "Segoe UI", size: 10, bold: true, color: { argb: "FFFFFFFF" } };
      headerRow.fill = { type: "pattern", pattern: "solid", fgColor: { argb: "FF1B365D" } };
      headerRow.alignment = { vertical: "middle", horizontal: "center" };

      // Agregar filas
      filtered.forEach(p => {
        const row = worksheet.addRow({
          Sociedad: p.Sociedad,
          Pedido: p.Pedido,
          POS: p.Posicion,
          Proveedor: p.Proveedor,
          GC: p.Grupo_Compras,
          Operador_OC: p.Operador_OC,
          FE_CONT: p.Fe_Contabilizacion ? new Date(p.Fe_Contabilizacion) : null,
          Dias_Atraso: p.Dias_Atraso || 0,
          Facturado_Debe: p.Total_Debe || 0,
          Recepcionado_Haber: p.Total_Haber || 0,
          Saldo_Neto: p.Saldo_Neto || 0,
          FE_OC: p.Fecha_Entrega_OC ? new Date(p.Fecha_Entrega_OC) : null,
          ESTADO: p.Estado_Vencimiento
        });

        // Formatos de celdas
        // FE CONT. (col 7)
        const cellFeCont = row.getCell(7);
        if (cellFeCont.value) cellFeCont.numFmt = "DD/MM/YYYY";

        // Dias Atraso (col 8)
        row.getCell(8).numFmt = "#,##0";

        // Monedas (cols 9, 10, 11)
        row.getCell(9).numFmt = "$ #,##0.00";
        row.getCell(10).numFmt = "$ #,##0.00";
        row.getCell(11).numFmt = "$ #,##0.00";

        // FE OC (col 12)
        const cellFeOc = row.getCell(12);
        if (cellFeOc.value) cellFeOc.numFmt = "DD/MM/YYYY";
      });

      // Bordes y alineación de datos
      worksheet.eachRow((row, rowNumber) => {
        if (rowNumber > 1) {
          row.height = 20;
          row.alignment = { vertical: "middle" };
          row.getCell(1).alignment = { horizontal: "center" };
          row.getCell(3).alignment = { horizontal: "center" };
          row.getCell(5).alignment = { horizontal: "center" };
          row.getCell(6).alignment = { horizontal: "center" };
          row.getCell(7).alignment = { horizontal: "center" };
          row.getCell(8).alignment = { horizontal: "right" };
          row.getCell(9).alignment = { horizontal: "right" };
          row.getCell(10).alignment = { horizontal: "right" };
          row.getCell(11).alignment = { horizontal: "right" };
          row.getCell(12).alignment = { horizontal: "center" };
          row.getCell(13).alignment = { horizontal: "center" };
        }
      });

      // Descargar buffer
      const buffer = await workbook.xlsx.writeBuffer();
      const blob = new Blob([buffer], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(link.href);
    } catch (e) {
      console.error("[EMRF] Error al generar archivo Excel:", e);
      alert("Ocurrió un error al generar el archivo Excel: " + e.message);
    }
  }

  /* ==============================================================================
     MODAL DE GUÍA EXPLICATIVA (EM/RF)
     ============================================================================== */
  function showHelpModal() {
    if (typeof window.openHelp === 'function') {
      window.openHelp("Guía Operativa — Control de Partidas Abiertas SAP (EM/RF)", `
        <h4>¿Qué analiza este tablero?</h4>
        <p>Supervisa la cuenta puente de compensación de compras de SAP <strong>EM/RF (2101011001)</strong>, conciliando lo ingresado físicamente en almacén/obra (<strong>MIGO</strong>) contra lo facturado por el proveedor (<strong>MIRO</strong>), cruzado con las fechas pactadas en las Órdenes de Compra (OC).</p>
        
        <h4>📌 Estados Contables EM/RF</h4>
        <ul>
          <li><strong>📦 TIENE RECEPCIÓN - FALTA FACTURA:</strong> El almacén ya recepcionó la mercadería o servicio (<em>Haber</em> con saldo negativo), pero el proveedor aún no facturó o la factura no fue cargada en el sistema (<em>Debe</em> en $0,00).<br>👉 <strong>Acción:</strong> Reclamar la factura al proveedor o gestionar la carga en Cuentas por Pagar.</li>
          <li style="margin-top:6px;"><strong>📄 TIENE FACTURA - FALTA RECEPCIÓN:</strong> La factura del proveedor ya fue contabilizada en SAP (<em>Debe</em> positivo), pero en el almacén no consta el ingreso físico o remito (<em>Haber</em> en $0,00).<br>👉 <strong>Acción:</strong> Reclamar el remito o ingreso físico al almacén/obra para evitar riesgo financiero de pagar sin recibir.</li>
          <li style="margin-top:6px;"><strong>🟢 COMPENSABLE (Saldo $0):</strong> Lo facturado coincide exactamente con lo recepcionado (Saldo Neto $0,00).<br>👉 <strong>Acción:</strong> Listo para depurar y cerrar en SAP mediante la transacción <strong>F.13</strong>.</li>
        </ul>

        <h4>⚠️ Columna ESTADO de Entrega</h4>
        <p>Mide el cumplimiento de la <strong>fecha de entrega pactada de la OC</strong> (FE OC):</p>
        <ul>
          <li><strong>VENCIDA:</strong> La fecha prometida de entrega expiró respecto a la fecha de corte.</li>
          <li><strong>VIGENTE:</strong> El pedido aún se encuentra en plazo para su entrega.</li>
        </ul>

        <h4>⚙️ Filtros Iniciales por Defecto</h4>
        <p>Por defecto se muestran los pedidos con <strong>«TIENE RECEPCIÓN - FALTA FACTURA»</strong> de los Grupos de Compras <strong>C01 y C07</strong> (compras locales de obra). Puedes cambiar cualquier filtro desde el panel superior para analizar el universo completo.</p>
      `);
    } else {
      alert("Explicación de la cuenta EM/RF:\nSupervisa la cuenta 2101011001 conciliando MIGO contra MIRO.");
    }
  }

  /* ==============================================================================
     INICIALIZADOR PRINCIPAL (EXPUESTO EN WINDOW)
     ============================================================================== */
  window.initEMRF = async function () {
    if (isInitialized) {
      // Si ya está inicializado, sólo renderizamos de nuevo si es necesario
      const filtered = getFilteredData();
      updateKPIs(filtered);
      renderTable(filtered);
      return;
    }

    await loadData();
    setupFilters();

    // Listeners de filtros
    document.getElementById("emrf_sociedadSelect")?.addEventListener("change", onFiltersChanged);
    document.getElementById("emrf_estadoSelect")?.addEventListener("change", onFiltersChanged);
    document.getElementById("emrf_gcSelect")?.addEventListener("change", onFiltersChanged);
    document.getElementById("emrf_vencSelect")?.addEventListener("change", onFiltersChanged);
    document.getElementById("emrf_operOcSelect")?.addEventListener("change", onFiltersChanged);

    // Botones de acción
    document.getElementById("emrf_btnClearFilters")?.addEventListener("click", clearFilters);
    document.getElementById("emrf_btnExcel")?.addEventListener("click", exportToExcel);
    document.getElementById("emrf_btnHelp")?.addEventListener("click", showHelpModal);

    // Selector de filas y paginación
    const rowsSelect = document.getElementById("emrf_rowsPerPage");
    if (rowsSelect) {
      rowsSelect.addEventListener("change", (e) => {
        pageSize = e.target.value;
        currentPage = 1;
        const filtered = getFilteredData();
        renderTable(filtered);
      });
    }

    document.getElementById("emrf_btnPrevPage")?.addEventListener("click", () => {
      if (currentPage > 1) {
        currentPage--;
        const filtered = getFilteredData();
        renderTable(filtered);
        document.querySelector(".emrf-table-scroll")?.scrollTo({ top: 0, behavior: "smooth" });
      }
    });

    document.getElementById("emrf_btnNextPage")?.addEventListener("click", () => {
      currentPage++;
      const filtered = getFilteredData();
      renderTable(filtered);
      document.querySelector(".emrf-table-scroll")?.scrollTo({ top: 0, behavior: "smooth" });
    });

    // Clic en encabezados para ordenar
    document.querySelectorAll(".emrf-data-table thead th[data-col]").forEach(th => {
      th.addEventListener("click", () => {
        const col = th.getAttribute("data-col");
        if (currentSort.col === col) {
          currentSort.dir = currentSort.dir === "asc" ? "desc" : "asc";
        } else {
          currentSort.col = col;
          currentSort.dir = "asc";
        }

        // Actualizar iconos de ordenamiento
        document.querySelectorAll(".emrf-data-table thead th .sort-icon").forEach(span => span.textContent = "⇅");
        const iconSpan = th.querySelector(".sort-icon");
        if (iconSpan) {
          iconSpan.textContent = currentSort.dir === "asc" ? "▲" : "▼";
        }

        const filtered = getFilteredData();
        renderTable(filtered);
      });
    });

    isInitialized = true;
    onFiltersChanged();
  };
})();
