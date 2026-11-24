/**
 * ==============================================================================
 * CONTROL DE MOVIMIENTOS MB51 (SAP) - FRONTEND CONTROLLER
 * ==============================================================================
 * Carga data/control_movimientos_mb51.json consolidado a partir de MB51 2025 y MB51 2026.
 * Filtros ubicados en la BARRA LATERAL (Sidebar) con SELECCIÓN MÚLTIPLE simultánea
 * para: Año, Mes, Almacén, Clase de Movimiento (CMv), Centro y búsqueda por Usuario.
 * Muestra la tabla de usuarios únicos por mes (sin conteos de cantidades ni duplicados).
 * Exporta el listado completo de movimientos individuales de SAP MB51 según los filtros activos.
 */

(function() {
  'use strict';

  let rawData = null;
  let isInitialized = false;
  let currentView = 'chronological'; // 'chronological' | 'matrix'
  let filteredRecords = [];
  let currentPage = 1;
  let pageSize = 50;

  const MONTH_NAMES = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
  ];

  const MONTH_SHORT = [
    'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
    'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'
  ];

  const CMV_DESCRIPTIONS = {
    '101': '101 - Entrada de mercancías p. pedido',
    '102': '102 - Anulación ent. mercancías p. pedido',
    '107': '107 - Entrada en stock bloqueado',
    '108': '108 - Anulación entrada stock bloqueado',
    '122': '122 - Devolución a proveedor',
    '161': '161 - Devolución por pedido de compras',
    '201': '201 - Consumo para centro de coste',
    '202': '202 - Anulación consumo p. centro coste',
    '261': '261 - Consumo p. orden de fabricación',
    '262': '262 - Anulación consumo p. orden fab.',
    '301': '301 - Traspaso centro a centro (1 paso)',
    '302': '302 - Anulación traspaso centro a centro',
    '303': '303 - Salida traspaso de centro a centro',
    '305': '305 - Entrada traspaso centro a centro',
    '311': '311 - Traspaso entre almacenes (1 paso)',
    '312': '312 - Anulación traspaso entre almacenes',
    '321': '321 - Traspaso de control calidad a libre',
    '322': '322 - Anulación traspaso control calidad',
    '343': '343 - Traspaso de stock bloqueado a libre',
    '344': '344 - Anulación traspaso stock bloqueado',
    '501': '501 - Entrada sin pedido de compra',
    '502': '502 - Anulación entrada sin pedido',
    '541': '541 - Salida p. subcontratación',
    '542': '542 - Anulación salida subcontratación',
    '551': '551 - Salida por desguace/merma',
    '552': '552 - Anulación salida por desguace',
    '601': '601 - Salida de mercancías p. entrega',
    '602': '602 - Anulación salida mercancías entrega',
    '701': '701 - Diferencia de inventario +',
    '702': '702 - Diferencia de inventario -'
  };

  /**
   * Helper para obtener valores seleccionados de un select múltiple
   */
  function getSelectedValues(selectEl) {
    if (!selectEl) return [];
    const values = [];
    for (let i = 0; i < selectEl.options.length; i++) {
      const opt = selectEl.options[i];
      if (opt.selected) {
        const val = String(opt.value || '').trim();
        if (val !== '' && val !== '__ALL__' && val.toLowerCase() !== 'todos') {
          values.push(val);
        }
      }
    }
    return values;
  }

  /**
   * Parsea fecha de Fe.contabilización (YYYY-MM-DD o DD/MM/YYYY) a año y mes
   */
  function parseDateParts(feStr) {
    if (!feStr) return { y: null, m: null };
    const s = String(feStr).trim().slice(0, 10);
    if (s.includes('-')) {
      const p = s.split('-');
      if (p.length >= 2) {
        return { y: parseInt(p[0], 10), m: parseInt(p[1], 10) };
      }
    } else if (s.includes('/')) {
      const p = s.split('/');
      if (p.length >= 3) {
        if (p[0].length === 4) {
          return { y: parseInt(p[0], 10), m: parseInt(p[1], 10) };
        }
        return { y: parseInt(p[2], 10), m: parseInt(p[1], 10) };
      }
    }
    return { y: null, m: null };
  }

  /**
   * Inicialización del panel de Control de Movimientos
   */
  window.initControlMovimientos = async function() {
    if (isInitialized && rawData) {
      if (typeof window.syncAllStMultiSelects === 'function') {
        window.syncAllStMultiSelects();
      }
      renderCurrentView();
      return;
    }

    const container = document.getElementById('ctrlMov_content');
    if (!container) return;

    showLoading(true);

    try {
      const url = 'data/control_movimientos_mb51.json' + (window.APP_CACHE_VERSION ? `?v=${window.APP_CACHE_VERSION}` : `?t=${Date.now()}`);
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      rawData = await response.json();
      window._ctrlMovData = rawData;

      populateFilterSelects();
      setupEventListeners();
      applyFilters();

      isInitialized = true;
    } catch (err) {
      console.error('[ControlMovimientos] Error al cargar los datos:', err);
      container.innerHTML = `
        <div style="padding: 40px; text-align: center; color: #b91c1c; background: #fef2f2; border: 1px solid #fecaca; border-radius: 10px; margin: 20px 0;">
          <div style="font-size: 1.1rem; font-weight: 700; margin-bottom: 8px;">Error al cargar el archivo de datos MB51</div>
          <p style="font-size: 0.85rem; color: #7f1d1d; margin: 0 0 16px 0;">No se pudo leer <code>data/control_movimientos_mb51.json</code>. Si ejecutó la actualización recientemente, verifique que el archivo exista en la carpeta data.</p>
          <button onclick="window.initControlMovimientos()" class="ctrl-mov-btn ctrl-mov-btn-primary" style="margin: 0 auto;">Reintentar</button>
        </div>
      `;
    } finally {
      showLoading(false);
    }
  };

  /**
   * Muestra/oculta estado de carga
   */
  function showLoading(show) {
    const loader = document.getElementById('ctrlMov_loader');
    const content = document.getElementById('ctrlMov_content');
    if (loader) loader.style.display = show ? 'flex' : 'none';
    if (content) content.style.opacity = show ? '0.4' : '1';
  }

  /**
   * Pobla los selects de filtros en la barra lateral con opciones para selección múltiple
   */
  function populateFilterSelects() {
    if (!rawData) return;

    // 1. Años (Multi-select)
    const selAnio = document.getElementById('ctrlMov_filterAnio');
    if (selAnio) {
      selAnio.innerHTML = '<option value="">Todos los Años</option>';
      (rawData.years || []).forEach(y => {
        const opt = document.createElement('option');
        opt.value = y;
        opt.textContent = `Año ${y}`;
        selAnio.appendChild(opt);
      });
    }

    // 2. Meses (Multi-select)
    const selMes = document.getElementById('ctrlMov_filterMes');
    if (selMes && selMes.options.length <= 1) {
      selMes.innerHTML = '<option value="">Todos los Meses</option>';
      for (let m = 1; m <= 12; m++) {
        const opt = document.createElement('option');
        opt.value = String(m);
        const pad = String(m).padStart(2, '0');
        opt.textContent = `${pad} - ${MONTH_NAMES[m - 1]}`;
        selMes.appendChild(opt);
      }
    }

    // 3. Almacenes (Multi-select)
    const selAlm = document.getElementById('ctrlMov_filterAlmacen');
    if (selAlm) {
      selAlm.innerHTML = '<option value="">Todos los Almacenes</option>';
      (rawData.almacenes || []).forEach(alm => {
        const opt = document.createElement('option');
        opt.value = alm;
        opt.textContent = alm === '(Sin Almacen)' ? '(Sin Almacén especificado)' : `Almacén ${alm}`;
        selAlm.appendChild(opt);
      });
    }

    // 4. Clase de Movimiento - CMv (Multi-select)
    const selCmv = document.getElementById('ctrlMov_filterCmv');
    if (selCmv) {
      selCmv.innerHTML = '<option value="">Todas las Clases (CMv)</option>';
      (rawData.cmvs || []).forEach(cmv => {
        const opt = document.createElement('option');
        opt.value = cmv;
        const desc = CMV_DESCRIPTIONS[cmv] || `CMv ${cmv}`;
        opt.textContent = desc;
        selCmv.appendChild(opt);
      });
    }

    // 5. Centros (Multi-select)
    const selCnt = document.getElementById('ctrlMov_filterCentro');
    if (selCnt) {
      selCnt.innerHTML = '<option value="">Todos los Centros</option>';
      (rawData.centros || []).forEach(cnt => {
        const opt = document.createElement('option');
        opt.value = cnt;
        opt.textContent = `Centro ${cnt}`;
        selCnt.appendChild(opt);
      });
    }

    // Metadata en cabecera
    const metaEl = document.getElementById('ctrlMov_metaGenerated');
    if (metaEl && rawData.generated_at) {
      metaEl.textContent = `Actualizado: ${rawData.generated_at} | ${Number(rawData.total_source_rows || 0).toLocaleString('es-AR')} movimientos procesados`;
    }

    if (typeof window.syncAllStMultiSelects === 'function') {
      setTimeout(window.syncAllStMultiSelects, 20);
    }
  }

  /**
   * Listeners de eventos de filtrado y acciones
   */
  function setupEventListeners() {
    const selAnio = document.getElementById('ctrlMov_filterAnio');
    const selMes = document.getElementById('ctrlMov_filterMes');
    const selAlm = document.getElementById('ctrlMov_filterAlmacen');
    const selCmv = document.getElementById('ctrlMov_filterCmv');
    const selCnt = document.getElementById('ctrlMov_filterCentro');
    const inputUser = document.getElementById('ctrlMov_filterUser');
    const btnReset = document.getElementById('ctrlMov_btnClearFilters');
    const btnExportTop = document.getElementById('ctrlMov_btnExport');
    const btnExportSide = document.getElementById('ctrlMov_btnExportSidebar');
    const selPageSize = document.getElementById('ctrlMov_pageSize');

    [selAnio, selMes, selAlm, selCmv, selCnt].forEach(el => {
      if (el) {
        el.addEventListener('change', () => {
          currentPage = 1;
          applyFilters();
        });
      }
    });

    if (inputUser) {
      let debounceTimer = null;
      inputUser.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
          currentPage = 1;
          applyFilters();
        }, 250);
      });
    }

    if (btnReset) {
      btnReset.addEventListener('click', window.resetControlPedidosFilters);
    }

    if (btnExportTop) btnExportTop.addEventListener('click', exportToExcel);
    if (btnExportSide) btnExportSide.addEventListener('click', exportToExcel);

    if (selPageSize) {
      selPageSize.addEventListener('change', (e) => {
        pageSize = e.target.value === '__ALL__' ? 999999 : parseInt(e.target.value, 10);
        currentPage = 1;
        renderCurrentView();
      });
    }

    const btnViewChrono = document.getElementById('ctrlMov_viewChrono');
    const btnViewMatrix = document.getElementById('ctrlMov_viewMatrix');

    if (btnViewChrono) {
      btnViewChrono.addEventListener('click', () => {
        currentView = 'chronological';
        btnViewChrono.classList.add('active');
        if (btnViewMatrix) btnViewMatrix.classList.remove('active');
        renderCurrentView();
      });
    }

    if (btnViewMatrix) {
      btnViewMatrix.addEventListener('click', () => {
        currentView = 'matrix';
        btnViewMatrix.classList.add('active');
        if (btnViewChrono) btnViewChrono.classList.remove('active');
        renderCurrentView();
      });
    }
  }

  /**
   * Resetea todos los filtros de Control de Movimientos
   */
  window.resetControlMovimientosFilters = function() {
    ['ctrlMov_filterAnio', 'ctrlMov_filterMes', 'ctrlMov_filterAlmacen', 'ctrlMov_filterCmv', 'ctrlMov_filterCentro'].forEach(id => {
      const sel = document.getElementById(id);
      if (sel) {
        for (let i = 0; i < sel.options.length; i++) {
          sel.options[i].selected = false;
        }
        sel.dispatchEvent(new Event('change', { bubbles: true }));
      }
    });

    const inputUser = document.getElementById('ctrlMov_filterUser');
    if (inputUser) {
      inputUser.value = '';
    }

    if (typeof window.syncAllStMultiSelects === 'function') {
      setTimeout(window.syncAllStMultiSelects, 30);
    }

    currentPage = 1;
    applyFilters();
  };

  /**
   * Aplica los filtros múltiples actuales sobre la colección de registros
   */
  function applyFilters() {
    if (!rawData || !rawData.records) return;

    const selAnio = document.getElementById('ctrlMov_filterAnio');
    const selMes = document.getElementById('ctrlMov_filterMes');
    const selAlm = document.getElementById('ctrlMov_filterAlmacen');
    const selCmv = document.getElementById('ctrlMov_filterCmv');
    const selCnt = document.getElementById('ctrlMov_filterCentro');
    const inputUser = document.getElementById('ctrlMov_filterUser');

    const selectedYears = getSelectedValues(selAnio);
    const selectedMeses = getSelectedValues(selMes);
    const selectedAlms = getSelectedValues(selAlm);
    const selectedCmvs = getSelectedValues(selCmv);
    const selectedCentros = getSelectedValues(selCnt);
    const filterUser = (inputUser?.value || '').trim().toUpperCase();

    filteredRecords = rawData.records.filter(r => {
      if (selectedYears.length > 0 && !selectedYears.includes(String(r.y))) {
        return false;
      }
      if (selectedMeses.length > 0 && !selectedMeses.includes(String(r.m))) {
        return false;
      }
      if (selectedAlms.length > 0 && !selectedAlms.includes(String(r.alm))) {
        return false;
      }
      if (selectedCmvs.length > 0 && !selectedCmvs.includes(String(r.cmv))) {
        return false;
      }
      if (selectedCentros.length > 0 && !selectedCentros.includes(String(r.cnt))) {
        return false;
      }
      if (filterUser) {
        const matches = (r.u || []).some(u => u.toUpperCase().includes(filterUser));
        if (!matches) return false;
      }

      return true;
    });

    renderActiveFilterChips(selectedYears, selectedMeses, selectedAlms, selectedCmvs, selectedCentros, filterUser);
    renderCurrentView();
  }

  /**
   * Renderiza chips resumen de filtros activos sobre la tabla
   */
  function renderActiveFilterChips(years, meses, alms, cmvs, centros, user) {
    const summaryEl = document.getElementById('ctrlMov_activeFiltersSummary');
    if (!summaryEl) return;

    const chips = [];

    if (years.length > 0) {
      chips.push({ lbl: 'Año', val: years.join(', ') });
    }
    if (meses.length > 0) {
      chips.push({ lbl: 'Mes', val: meses.map(m => MONTH_SHORT[parseInt(m, 10) - 1] || m).join(', ') });
    }
    if (alms.length > 0) {
      chips.push({ lbl: 'Almacén', val: alms.length <= 3 ? alms.join(', ') : `${alms.slice(0, 3).join(', ')} (+${alms.length - 3})` });
    }
    if (cmvs.length > 0) {
      chips.push({ lbl: 'CMv', val: cmvs.length <= 4 ? cmvs.join(', ') : `${cmvs.slice(0, 4).join(', ')} (+${cmvs.length - 4})` });
    }
    if (centros.length > 0) {
      chips.push({ lbl: 'Centro', val: centros.join(', ') });
    }
    if (user) {
      chips.push({ lbl: 'Usuario', val: user });
    }

    if (chips.length === 0) {
      summaryEl.innerHTML = '';
      return;
    }

    let chipsHtml = `
      <div style="display: flex; align-items: center; flex-wrap: wrap; gap: 6px; padding: 8px 12px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; margin-bottom: 12px;">
        <span style="font-size: 0.72rem; font-weight: 800; color: #15803d; text-transform: uppercase; letter-spacing: 0.04em;">Filtros activos:</span>
    `;

    chips.forEach(c => {
      chipsHtml += `
        <span style="display: inline-flex; align-items: center; gap: 4px; padding: 2px 8px; border-radius: 5px; background: #ffffff; border: 1px solid #86efac; color: #166534; font-size: 0.76rem; font-weight: 700;">
          <span style="color: #4ade80;">•</span> <strong>${escapeHtml(c.lbl)}:</strong> ${escapeHtml(c.val)}
        </span>
      `;
    });

    chipsHtml += `
        <button onclick="window.resetControlMovimientosFilters()" style="margin-left: auto; background: none; border: none; color: #b91c1c; font-size: 0.75rem; font-weight: 700; cursor: pointer; text-decoration: underline;">
          Limpiar todos
        </button>
      </div>
    `;

    summaryEl.innerHTML = chipsHtml;
  }

  /**
   * Renderiza la vista seleccionada (Cronológica o Matriz)
   */
  function renderCurrentView() {
    const tableContainer = document.getElementById('ctrlMov_tableContainer');
    const paginationContainer = document.getElementById('ctrlMov_pagination');
    if (!tableContainer) return;

    if (filteredRecords.length === 0) {
      tableContainer.innerHTML = `
        <div style="padding: 48px 20px; text-align: center; color: #64748b; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px;">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.8" style="margin-bottom: 12px;"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <div style="font-size: 1.05rem; font-weight: 700; color: #1e293b; margin-bottom: 4px;">No se encontraron registros con los filtros seleccionados</div>
          <p style="font-size: 0.85rem; color: #64748b; margin: 0 0 16px 0;">Pruebe seleccionando otros almacenes o clases de movimiento desde la barra lateral.</p>
          <button onclick="window.resetControlMovimientosFilters()" class="ctrl-mov-btn ctrl-mov-btn-secondary" style="margin: 0 auto;">Restablecer Filtros</button>
        </div>
      `;
      if (paginationContainer) paginationContainer.innerHTML = '';
      return;
    }

    if (currentView === 'chronological') {
      renderChronologicalView(tableContainer, paginationContainer);
    } else {
      renderMatrixView(tableContainer, paginationContainer);
    }
  }

  /**
   * Renderiza Vista Cronológica (Mes a mes)
   * Muestra todos los usuarios del mes tal como fue solicitado
   */
  function renderChronologicalView(container, pagContainer) {
    const totalItems = filteredRecords.length;
    const totalPages = Math.ceil(totalItems / pageSize);
    if (currentPage > totalPages) currentPage = totalPages || 1;

    const startIdx = (currentPage - 1) * pageSize;
    const pageItems = filteredRecords.slice(startIdx, startIdx + pageSize);

    let html = `
      <div style="overflow-x: auto; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
        <table class="ctrl-mov-table">
          <thead>
            <tr>
              <th style="width: 75px; text-align: center;">Año</th>
              <th style="width: 105px; text-align: center;">Mes</th>
              <th style="width: 85px; text-align: center;">Centro</th>
              <th style="width: 130px;">Almacén</th>
              <th style="width: 170px;">Clase Movimiento (CMv)</th>
              <th>Nombres de Usuarios que realizaron movimientos (Sin repetir)</th>
            </tr>
          </thead>
          <tbody>
    `;

    pageItems.forEach((r, idx) => {
      const mesName = MONTH_NAMES[r.m - 1] || `Mes ${r.m}`;
      const cmvDesc = CMV_DESCRIPTIONS[r.cmv] || `CMv ${r.cmv}`;
      // Todos los usuarios únicos de ese mes
      const userBadges = (r.u || []).map(u => `<span class="ctrl-user-badge" title="Usuario operador en SAP">${escapeHtml(u)}</span>`).join('');

      html += `
        <tr class="${idx % 2 === 0 ? 'even-row' : 'odd-row'}">
          <td style="text-align: center; font-weight: 700; color: #0f172a;">${r.y}</td>
          <td style="text-align: center;">
            <span style="display: inline-block; padding: 2px 8px; border-radius: 5px; background: #f1f5f9; color: #334155; font-weight: 700; font-size: 0.78rem;">
              ${mesName}
            </span>
          </td>
          <td style="text-align: center; font-weight: 600; color: #475569;">${escapeHtml(r.cnt)}</td>
          <td>
            <span style="font-weight: 700; color: #0284c7;">${escapeHtml(r.alm)}</span>
          </td>
          <td>
            <span style="font-weight: 600; color: #334155; font-size: 0.82rem;" title="${escapeHtml(cmvDesc)}">
              ${escapeHtml(cmvDesc)}
            </span>
          </td>
          <td>
            <div class="ctrl-users-container">
              ${userBadges || '<span style="color: #94a3b8; font-style: italic;">Sin usuarios registrados</span>'}
            </div>
          </td>
        </tr>
      `;
    });

    html += `
          </tbody>
        </table>
      </div>
    `;

    container.innerHTML = html;
    renderPaginationControls(pagContainer, totalItems, totalPages);
  }

  /**
   * Renderiza Vista Matriz Anual (12 columnas de meses)
   * Sin superposición de texto al desplazar la barra horizontal
   */
  function renderMatrixView(container, pagContainer) {
    const matrixMap = new Map();

    filteredRecords.forEach(r => {
      const key = `${r.y}|${r.cnt}|${r.alm}|${r.cmv}`;
      if (!matrixMap.has(key)) {
        matrixMap.set(key, {
          y: r.y,
          cnt: r.cnt,
          alm: r.alm,
          cmv: r.cmv,
          months: Array(12).fill(null).map(() => new Set())
        });
      }
      const entry = matrixMap.get(key);
      const mIdx = r.m - 1;
      if (mIdx >= 0 && mIdx < 12) {
        (r.u || []).forEach(u => entry.months[mIdx].add(u));
      }
    });

    const matrixRows = Array.from(matrixMap.values());
    matrixRows.sort((a, b) => {
      if (a.y !== b.y) return a.y - b.y;
      if (a.alm !== b.alm) return a.alm.localeCompare(b.alm);
      return a.cmv.localeCompare(b.cmv);
    });

    const totalItems = matrixRows.length;
    const totalPages = Math.ceil(totalItems / pageSize);
    if (currentPage > totalPages) currentPage = totalPages || 1;

    const startIdx = (currentPage - 1) * pageSize;
    const pageItems = matrixRows.slice(startIdx, startIdx + pageSize);

    let html = `
      <div style="overflow-x: auto; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
        <table class="ctrl-mov-table ctrl-mov-matrix-table">
          <thead>
            <tr>
              <th style="width: 70px; min-width: 70px; text-align: center;">Año</th>
              <th style="width: 100px; min-width: 100px;">Almacén</th>
              <th style="width: 80px; min-width: 80px; text-align: center;">CMv</th>
              ${MONTH_SHORT.map(m => `<th style="min-width: 140px; text-align: center;">${m}</th>`).join('')}
            </tr>
          </thead>
          <tbody>
    `;

    pageItems.forEach((row, idx) => {
      const cmvDesc = CMV_DESCRIPTIONS[row.cmv] || row.cmv;
      html += `
        <tr class="${idx % 2 === 0 ? 'even-row' : 'odd-row'}">
          <td style="text-align: center; font-weight: 700; color: #0f172a;">${row.y}</td>
          <td style="font-weight: 700; color: #0284c7;">${escapeHtml(row.alm)}</td>
          <td style="text-align: center; font-weight: 700; color: #334155; font-size: 0.85rem;" title="${escapeHtml(cmvDesc)}">${escapeHtml(row.cmv)}</td>
      `;

      for (let m = 0; m < 12; m++) {
        const usersSet = row.months[m];
        if (usersSet.size === 0) {
          html += `<td style="text-align: center; color: #cbd5e1; font-size: 0.8rem;">-</td>`;
        } else {
          const badges = Array.from(usersSet).sort().map(u => `<span class="ctrl-user-badge" style="font-size: 0.72rem; padding: 2px 6px;">${escapeHtml(u)}</span>`).join('');
          html += `
            <td style="vertical-align: top; padding: 6px;">
              <div class="ctrl-users-container" style="gap: 3px;">
                ${badges}
              </div>
            </td>
          `;
        }
      }

      html += `</tr>`;
    });

    html += `
          </tbody>
        </table>
      </div>
    `;

    container.innerHTML = html;
    renderPaginationControls(pagContainer, totalItems, totalPages);
  }

  /**
   * Renderiza la barra de paginación
   */
  function renderPaginationControls(container, totalItems, totalPages) {
    if (!container) return;
    if (totalPages <= 1) {
      container.innerHTML = `
        <div style="font-size: 0.8rem; color: #64748b; margin-top: 14px;">
          Mostrando todos los <strong>${totalItems.toLocaleString('es-AR')}</strong> registros filtrados
        </div>
      `;
      return;
    }

    const startIdx = (currentPage - 1) * pageSize + 1;
    const endIdx = Math.min(currentPage * pageSize, totalItems);

    let html = `
      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; width: 100%; margin-top: 14px;">
        <div style="font-size: 0.8rem; color: #64748b;">
          Mostrando <strong>${startIdx.toLocaleString('es-AR')} - ${endIdx.toLocaleString('es-AR')}</strong> de <strong>${totalItems.toLocaleString('es-AR')}</strong> registros
        </div>
        <div style="display: flex; gap: 4px; align-items: center;">
          <button class="ctrl-mov-pag-btn" ${currentPage === 1 ? 'disabled' : ''} onclick="window.ctrlMovGoPage(${currentPage - 1})">
            &laquo; Anterior
          </button>
    `;

    const maxVisible = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxVisible / 2));
    let endPage = Math.min(totalPages, startPage + maxVisible - 1);
    if (endPage - startPage + 1 < maxVisible) {
      startPage = Math.max(1, endPage - maxVisible + 1);
    }

    if (startPage > 1) {
      html += `<button class="ctrl-mov-pag-btn" onclick="window.ctrlMovGoPage(1)">1</button>`;
      if (startPage > 2) html += `<span style="padding: 0 4px; color: #94a3b8;">...</span>`;
    }

    for (let p = startPage; p <= endPage; p++) {
      html += `
        <button class="ctrl-mov-pag-btn ${p === currentPage ? 'active' : ''}" onclick="window.ctrlMovGoPage(${p})">
          ${p}
        </button>
      `;
    }

    if (endPage < totalPages) {
      if (endPage < totalPages - 1) html += `<span style="padding: 0 4px; color: #94a3b8;">...</span>`;
      html += `<button class="ctrl-mov-pag-btn" onclick="window.ctrlMovGoPage(${totalPages})">${totalPages}</button>`;
    }

    html += `
          <button class="ctrl-mov-pag-btn" ${currentPage === totalPages ? 'disabled' : ''} onclick="window.ctrlMovGoPage(${currentPage + 1})">
            Siguiente &raquo;
          </button>
        </div>
      </div>
    `;

    container.innerHTML = html;
  }

  window.ctrlMovGoPage = function(page) {
    currentPage = page;
    renderCurrentView();
    const tableContainer = document.getElementById('ctrlMov_tableContainer');
    if (tableContainer) {
      tableContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  };

  /**
   * Exporta a Excel todos los movimientos individuales según los filtros activos.
   * Descarga la lista completa con las 21 columnas originales de SAP MB51
   * (Material, Texto, Centro, Almacén, CMv, Documento Material, Fecha, Cantidad, etc.)
   */
  async function exportToExcel() {
    if (typeof ExcelJS === 'undefined') {
      alert('La biblioteca ExcelJS aún no está cargada. Por favor intente nuevamente en un instante.');
      return;
    }
    if (typeof Papa === 'undefined') {
      alert('La biblioteca PapaParse aún no está cargada. Por favor recargue la página.');
      return;
    }

    const selAnio = document.getElementById('ctrlMov_filterAnio');
    const selMes = document.getElementById('ctrlMov_filterMes');
    const selAlm = document.getElementById('ctrlMov_filterAlmacen');
    const selCmv = document.getElementById('ctrlMov_filterCmv');
    const selCnt = document.getElementById('ctrlMov_filterCentro');
    const inputUser = document.getElementById('ctrlMov_filterUser');

    const selectedYears = getSelectedValues(selAnio);
    const selectedMeses = getSelectedValues(selMes);
    const selectedAlms = getSelectedValues(selAlm);
    const selectedCmvs = getSelectedValues(selCmv);
    const selectedCentros = getSelectedValues(selCnt);
    const filterUser = (inputUser?.value || '').trim().toUpperCase();

    // Si no se seleccionó almacén, solicitar al usuario que elija al menos uno
    if (selectedAlms.length === 0) {
      alert('Para descargar el detalle completo de movimientos de SAP MB51, por favor seleccioná al menos un Almacén en los filtros de la barra lateral (ej: 0223, 0314, etc.).');
      return;
    }

    const btnExportTop = document.getElementById('ctrlMov_btnExport');
    const btnExportSide = document.getElementById('ctrlMov_btnExportSidebar');
    const originalTextTop = btnExportTop ? btnExportTop.innerHTML : '';
    const originalTextSide = btnExportSide ? btnExportSide.innerHTML : '';

    [btnExportTop, btnExportSide].forEach(b => {
      if (b) {
        b.disabled = true;
        b.innerHTML = `<svg class="ctrl-spinner" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10" stroke-opacity="0.25"/><path d="M12 2a10 10 0 0 1 10 10"/></svg> Procesando movimientos...`;
      }
    });

    try {
      // 1. Cargar los archivos CSV de detalle de cada almacén seleccionado
      const cacheBuster = window.APP_CACHE_VERSION || Date.now();
      const fetchPromises = selectedAlms.map(async (alm) => {
        const cleanName = alm === '(Sin Almacen)' ? 'SIN_ALMACEN' : alm.replace(/\//g, '_').replace(/\\/g, '_');
        const url = `data/mb51_movimientos/${encodeURIComponent(cleanName)}.csv?v=${cacheBuster}`;
        try {
          const resp = await fetch(url);
          if (!resp.ok) {
            console.warn(`[exportToExcel] No se encontró CSV para almacén ${alm} (${resp.status})`);
            return [];
          }
          const csvText = await resp.text();
          const parsed = Papa.parse(csvText, {
            header: true,
            skipEmptyLines: true
          });
          return parsed.data || [];
        } catch (e) {
          console.warn(`[exportToExcel] Error al leer almacén ${alm}:`, e);
          return [];
        }
      });

      const loadedArrays = await Promise.all(fetchPromises);
      const allRows = loadedArrays.flat();

      if (allRows.length === 0) {
        alert('No se encontraron movimientos disponibles para los almacenes seleccionados.');
        return;
      }

      // 2. Filtrar cada fila por Año, Mes, CMv, Centro y Usuario
      const filteredMovs = allRows.filter(r => {
        const feStr = r['Fe.contabilización'] || r['Fe.contabilizacion'] || '';
        const { y, m } = parseDateParts(feStr);

        if (selectedYears.length > 0 && y && !selectedYears.includes(String(y))) {
          return false;
        }
        if (selectedMeses.length > 0 && m && !selectedMeses.includes(String(m))) {
          return false;
        }
        const rowCmv = String(r['Clase de movimiento'] || '').trim();
        if (selectedCmvs.length > 0 && !selectedCmvs.includes(rowCmv)) {
          return false;
        }
        const rowCnt = String(r['Centro'] || '').trim().toUpperCase();
        if (selectedCentros.length > 0 && !selectedCentros.includes(rowCnt)) {
          return false;
        }
        if (filterUser) {
          const rowUser = String(r['Nombre del usuario'] || '').trim().toUpperCase();
          if (!rowUser.includes(filterUser)) {
            return false;
          }
        }
        return true;
      });

      if (filteredMovs.length === 0) {
        alert('No se encontraron movimientos para los filtros seleccionados (Año, Mes, CMv o Usuario).');
        return;
      }

      // 3. Generar el archivo Excel con ExcelJS
      const workbook = new ExcelJS.Workbook();
      workbook.creator = 'Abastecimiento Milicic';
      workbook.created = new Date();

      const ws = workbook.addWorksheet('Movimientos MB51 Detalle');

      const headers = [
        'Material',
        'Texto breve de material',
        'Centro',
        'Almacén',
        'Clase de movimiento',
        'Documento material',
        'Posición doc.mat.',
        'Fe.contabilización',
        'Ctd.en UM entrada',
        'Un.medida de entrada',
        'Orden',
        'Nombre del usuario',
        'Impte.mon.local',
        'Moneda',
        'Pedido',
        'Posición',
        'Centro de coste',
        'Cliente',
        'Lote',
        'Pedido de cliente',
        'Texto cab.documento'
      ];

      const headerRow = ws.addRow(headers);
      headerRow.font = { bold: true, color: { argb: 'FFFFFFFF' } };
      headerRow.alignment = { vertical: 'middle', horizontal: 'center' };
      headerRow.fill = {
        type: 'pattern',
        pattern: 'solid',
        fgColor: { argb: 'FF1E3A8A' } // Azul corporativo
      };

      filteredMovs.forEach(r => {
        const ctdNum = parseFloat(String(r['Ctd.en UM entrada'] || '').replace(',', '.'));
        const impteNum = parseFloat(String(r['Impte.mon.local'] || '').replace(',', '.'));

        const row = ws.addRow([
          r['Material'] || '',
          r['Texto breve de material'] || '',
          r['Centro'] || '',
          r['Almacén'] || '',
          r['Clase de movimiento'] || '',
          r['Documento material'] || '',
          r['Posición doc.mat.'] || '',
          r['Fe.contabilización'] || '',
          isNaN(ctdNum) ? (r['Ctd.en UM entrada'] || '') : ctdNum,
          r['Un.medida de entrada'] || '',
          r['Orden'] || '',
          r['Nombre del usuario'] || '',
          isNaN(impteNum) ? (r['Impte.mon.local'] || '') : impteNum,
          r['Moneda'] || '',
          r['Pedido'] || '',
          r['Posición'] || '',
          r['Centro de coste'] || '',
          r['Cliente'] || '',
          r['Lote'] || '',
          r['Pedido de cliente'] || '',
          r['Texto cab.documento'] || ''
        ]);

        row.alignment = { vertical: 'middle' };
      });

      // Anchos y formatos de columnas
      ws.columns = [
        { width: 14 }, // Material
        { width: 35 }, // Texto breve
        { width: 10 }, // Centro
        { width: 12 }, // Almacén
        { width: 12 }, // CMv
        { width: 18 }, // Doc Mat
        { width: 14 }, // Pos
        { width: 15 }, // Fecha
        { width: 16, numFmt: '#,##0.00' }, // Cantidad
        { width: 12 }, // UM
        { width: 14 }, // Orden
        { width: 18 }, // Usuario
        { width: 16, numFmt: '$ #,##0.00' }, // Importe
        { width: 10 }, // Moneda
        { width: 14 }, // Pedido
        { width: 10 }, // Pos
        { width: 16 }, // CeCo
        { width: 14 }, // Cliente
        { width: 12 }, // Lote
        { width: 16 }, // Pedido cliente
        { width: 25 }  // Texto cab
      ];

      // Activar autofiltro
      ws.autoFilter = {
        from: { row: 1, column: 1 },
        to: { row: filteredMovs.length + 1, column: headers.length }
      };

      const buffer = await workbook.xlsx.writeBuffer();
      const blob = new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const almLabel = selectedAlms.length <= 2 ? selectedAlms.join('_') : `${selectedAlms[0]}_y_mas`;
      const yrLabel = selectedYears.length > 0 ? selectedYears.join('_') : '2025_2026';
      a.download = `Movimientos_MB51_${almLabel}_${yrLabel}.xlsx`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);

    } catch (err) {
      console.error('[ControlMovimientos] Error al exportar Excel detallado:', err);
      alert('Ocurrió un error al generar el archivo Excel: ' + err.message);
    } finally {
      if (btnExportTop) {
        btnExportTop.disabled = false;
        btnExportTop.innerHTML = originalTextTop;
      }
      if (btnExportSide) {
        btnExportSide.disabled = false;
        btnExportSide.innerHTML = originalTextSide;
      }
    }
  }

  function escapeHtml(text) {
    if (text === null || text === undefined) return '';
    return String(text)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

})();

/**
 * Función global para alternar entre sub-pestañas de Control de Pedidos
 * Sub-tab 1: 'sello-vl' (ALM VS VL)
 * Sub-tab 2: 'movimientos' (CONTROL DE MOV)
 */
window.switchCtrlPedSubtab = function(tabKey) {
  const btnSello = document.getElementById('btnSubtabSelloVL');
  const btnMov = document.getElementById('btnSubtabMovimientos');
  const panelSello = document.getElementById('subpanel-sello-vl');
  const panelMov = document.getElementById('subpanel-movimientos');
  const sidebarMov = document.getElementById('ctrlMov_sidebarContent');
  const sidebarSello = document.getElementById('ctrlSello_sidebarContent');

  if (tabKey === 'movimientos') {
    if (btnSello) btnSello.classList.remove('active');
    if (btnMov) btnMov.classList.add('active');
    if (panelSello) panelSello.style.display = 'none';
    if (panelMov) panelMov.style.display = 'block';
    if (sidebarMov) sidebarMov.style.display = 'block';
    if (sidebarSello) sidebarSello.style.display = 'none';

    if (typeof window.initControlMovimientos === 'function') {
      window.initControlMovimientos();
    }
  } else {
    // sello-vl (default)
    if (btnMov) btnMov.classList.remove('active');
    if (btnSello) btnSello.classList.add('active');
    if (panelMov) panelMov.style.display = 'none';
    if (panelSello) panelSello.style.display = 'block';
    if (sidebarMov) sidebarMov.style.display = 'none';
    if (sidebarSello) sidebarSello.style.display = 'block';

    if (typeof window.initControlPedidos === 'function') {
      window.initControlPedidos();
    }
  }

  if (typeof window.syncAllStMultiSelects === 'function') {
    setTimeout(window.syncAllStMultiSelects, 20);
  }

  window.dispatchEvent(new Event('resize'));
};

/**
 * Función global para restablecer filtros según la sub-pestaña activa
 */
window.resetControlPedidosFilters = function() {
  const btnMov = document.getElementById('btnSubtabMovimientos');
  if (btnMov && btnMov.classList.contains('active')) {
    if (typeof window.resetControlMovimientosFilters === 'function') {
      window.resetControlMovimientosFilters();
    }
  } else {
    if (typeof window.selectCtrlPedObra === 'function') {
      window.selectCtrlPedObra('00378');
    }
    const selSidebar = document.getElementById('ctrlSello_obraSelect');
    if (selSidebar) selSidebar.value = '00378';
  }
};
