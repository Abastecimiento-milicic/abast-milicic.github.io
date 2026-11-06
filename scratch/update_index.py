import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update panel-servicios
old_serv = '''    <section id="panel-servicios" class="tab-panel" style="display: none;">
      <div id="serv_loader" class="loader-overlay">
        <div class="spinner-bars"><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div></div>
        <div class="loading-text">Cargando servicios...</div>
      </div>

      <div class="topbar-badge" style="margin-bottom: 14px; font-size: 0.82rem; font-weight: 500; line-height: 1.45; display: block; padding: 8px 14px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); background-color: #ea580c; color: #fff;">
        ℹ️ Este reporte contempla las VA tipo <strong>ZPAN</strong> y <strong>ZPAI</strong> de clientes (obras) cuyo GC es <strong>24, 25, 26, 16 ó 04</strong>, y posiciones con Tipo de Ítem <strong>"SERVICIOS"</strong> (aun si pertenecen a otro GC). No se muestran los servicios ya finalizados (sin cantidades pendientes de recepción y con fecha vencida).
      </div>

      <aside class="st-sidebar">
        <div class="st-sidebar-toprow">
          <div class="st-sector-switcher">
            <select class="st-sector-select" onchange="window.switchSector(this.value)" aria-label="Seleccionar sector">
              <option value="abastecimiento">🏗️ OBRAS</option>
              <option value="sede">🏢 SEDE</option><option value="compras">🛒 COMPRAS</option><option value="almacen">🏭 ALMACEN</option>
            </select>
          </div>
          <button type="button" class="st-collapse-btn" onclick="window.toggleStSidebar()" title="Ocultar barra lateral">«</button>
        </div>
        <h3 class="st-ctrl-title">Panel de Control</h3>

        <div class="st-filters-header">
          <h4 class="st-filters-title">Filtros de Búsqueda</h4>
        </div>

        <div class="st-filters-stack">
          <div class="filter"><label>Cliente:</label><select id="serv_clienteSelect" multiple class="multi-select"></select></div>
          <div class="filter"><label>Período:</label><select id="serv_clasif2Select" multiple class="multi-select"></select></div>
          <div class="filter"><label>Estado:</label><select id="serv_gcocSelect" multiple class="multi-select"></select></div>
          <div class="filter"><label>Grupo de Compra:</label><select id="serv_grupoCompraSelect" multiple class="multi-select"></select></div>
          <div class="filter"><label>Estado del Ítem:</label><select id="serv_estadoItemSelect" multiple class="multi-select"></select></div>

          <hr class="st-divider" />

          <div class="filter-kpi" style="display: flex; flex-direction: column; gap: 8px;">
            <div class="kpi-mini-box">
              <span id="serv_kpiTotal" class="kpi-mini-value">0</span>
              <span class="kpi-mini-label">Servicios Seleccionados</span>
            </div>
            <button id="serv_btnDownloadSelection" class="btn" style="width: 100%;">⬇ Descargar Selección</button>
          </div>
        </div>
      </aside>

      <section class="panel">
        <div class="panel-title">RESUMEN DE PEDIDOS POR ESTADO<span id="serv_activeFiltersSummary" class="st-active-filters-summary"></span></div>
        <div class="panel-body" style="padding: 20px; overflow-x: auto;">
          <table id="serv_tablaResumen" class="serv-resumen-table">
            <thead>
              <tr>
                <th class="sortable" data-sort="estadoItem" title="Ordenar por Estado Item">ESTADO ITEM <span id="serv_sort_estadoItem">↕</span></th>
                <th class="sortable" data-sort="estadoServicio" title="Ordenar por Estado Servicio">Estado Servicio <span id="serv_sort_estadoServicio">↕</span></th>
                <th class="sortable" data-sort="count" title="Ordenar por Cantidad" style="text-align: right;">CANTIDAD DE PEDIDOS <span id="serv_sort_count">▼</span></th>
                <th style="text-align: center; width: 130px;">ACCIONES</th>
              </tr>
            </thead>
            <tbody id="serv_resumenBody"></tbody>
          </table>
        </div>
      </section>
    </section>'''

new_serv = '''    <section id="panel-servicios" class="tab-panel" style="display: none;">
      <div id="serv_loader" class="loader-overlay">
        <div class="spinner-bars"><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div></div>
        <div class="loading-text">Cargando servicios...</div>
      </div>

      <!-- Banner Informativo Estilo SaaS -->
      <div class="serv-notice-banner">
        <div class="serv-notice-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
          </svg>
        </div>
        <div class="serv-notice-text">
          Este reporte contempla las VA tipo <strong>ZPAN</strong> y <strong>ZPAI</strong> de clientes (obras) cuyo GC es <strong>24, 25, 26, 16 ó 04</strong>, y posiciones con Tipo de Ítem <strong>"SERVICIOS"</strong> (aun si pertenecen a otro GC). No se muestran los servicios ya finalizados (sin cantidades pendientes de recepción y con fecha vencida).
        </div>
      </div>

      <aside class="st-sidebar app-sidebar">
        <div class="st-sidebar-toprow">
          <div class="st-sector-switcher">
            <select class="st-sector-select" onchange="window.switchSector(this.value)" aria-label="Seleccionar sector">
              <option value="abastecimiento">🏗️ OBRAS</option>
              <option value="sede">🏢 SEDE</option>
              <option value="compras">🛒 COMPRAS</option>
              <option value="almacen">🏭 ALMACEN</option>
            </select>
          </div>
          <button type="button" class="st-collapse-btn" onclick="window.toggleStSidebar()" title="Ocultar barra lateral">«</button>
        </div>

        <div class="sidebar-header">
          <div class="sidebar-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
            <span>Filtros de Control</span>
          </div>
          <button type="button" class="sidebar-reset-btn" onclick="window.resetServiciosFilters()" title="Restablecer filtros">Restablecer</button>
        </div>

        <div class="st-filters-stack" style="margin-top: 10px;">
          <div class="filter"><label>Cliente / Obra:</label><select id="serv_clienteSelect" multiple class="multi-select" size="5"></select></div>
          <div class="filter"><label>Período de Certificación:</label><select id="serv_clasif2Select" multiple class="multi-select" size="4"></select></div>
          <div class="filter"><label>Estado del Servicio:</label><select id="serv_gcocSelect" multiple class="multi-select" size="4"></select></div>
          <div class="filter"><label>Grupo de Compra:</label><select id="serv_grupoCompraSelect" multiple class="multi-select" size="4"></select></div>
          <div class="filter"><label>Estado del Ítem:</label><select id="serv_estadoItemSelect" multiple class="multi-select" size="4"></select></div>

          <hr class="st-divider" />

          <div class="serv-kpi-card">
            <div class="serv-kpi-inner">
              <span class="serv-kpi-label">SERVICIOS SELECCIONADOS</span>
              <span id="serv_kpiTotal" class="serv-kpi-value">0</span>
            </div>
            <button id="serv_btnDownloadSelection" class="btn btn-serv-download" type="button">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              <span>Descargar Selección</span>
            </button>
          </div>
        </div>
      </aside>

      <section class="panel serv-table-panel">
        <div class="panel-title" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
          <div style="display: flex; align-items: center; gap: 8px;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0f766e" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
              <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
            </svg>
            <span>RESUMEN DE PEDIDOS POR ESTADO</span>
            <span id="serv_activeFiltersSummary" class="st-active-filters-summary"></span>
          </div>
        </div>
        <div class="panel-body" style="padding: 18px; overflow-x: auto;">
          <table id="serv_tablaResumen" class="serv-resumen-table">
            <thead>
              <tr>
                <th class="sortable" data-sort="estadoItem" title="Ordenar por Estado Item">ESTADO ITEM <span id="serv_sort_estadoItem">↕</span></th>
                <th class="sortable" data-sort="estadoServicio" title="Ordenar por Estado Servicio">ESTADO SERVICIO <span id="serv_sort_estadoServicio">↕</span></th>
                <th class="sortable" data-sort="count" title="Ordenar por Cantidad" style="text-align: right;">CANTIDAD DE PEDIDOS <span id="serv_sort_count">▼</span></th>
                <th style="text-align: center; width: 140px;">ACCIONES</th>
              </tr>
            </thead>
            <tbody id="serv_resumenBody"></tbody>
          </table>
        </div>
      </section>
    </section>'''

# 2. Update panel-resumen
old_resumen_sidebar = '''      <!-- Barra Lateral Izquierda (Panel de Control) -->
      <aside class="st-sidebar app-sidebar">
        <div class="st-sidebar-toprow">
          <div class="st-sector-switcher">
            <select class="st-sector-select" onchange="window.switchSector(this.value)" aria-label="Seleccionar sector">
              <option value="abastecimiento">🏗️ OBRAS</option>
              <option value="sede">🏢 SEDE</option>
              <option value="compras">🛒 COMPRAS</option>
              <option value="almacen">🏭 ALMACEN</option>
            </select>
          </div>
          <button type="button" class="st-collapse-btn" onclick="window.toggleStSidebar()" title="Ocultar barra lateral">«</button>
        </div>

        <div class="sidebar-header">
          <div class="sidebar-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
            <span>Filtros de Control</span>
          </div>
          <div style="display: flex; align-items: center; gap: 4px;">
            <button id="resumen_btnClearFilters" class="sidebar-reset-btn" title="Restablecer todos los filtros">Restablecer</button>
            <button class="help-btn" onclick="openHelp('Filtros — Resumen Ejecutivo', `
              <h4>Cliente / Obra</h4>
              <p>Filtrá el resumen por obra o almacén para visualizar el estado de stock y el cumplimiento de pedidos correspondiente.</p>
              <h4>Mes Evaluado</h4>
              <p>Seleccioná el mes a evaluar en el bloque de rendimiento mensual de cumplimiento.</p>
              <div class=&quot;hm-tip&quot;>💡 Podés restablecer a todas las obras con el botón Limpiar.</div>
            `)" title="Ayuda sobre los filtros">ℹ</button>
          </div>
        </div>

        <div class="filter-group" id="resumen_obraFilterWrap">
          <div class="filter-label">
            <span>Cliente / Obra:</span>
            <button type="button" id="resumen_btnExcludeObra" class="res-exclude-toggle-btn" title="Activar para EXCLUIR obras">🚫 Excluir: OFF</button>
          </div>
          <input type="text" id="resumen_obraQuickSearch" class="filter-search-input" placeholder="🔍 Filtrar o buscar obra..." oninput="window.filterResumenObraSelect(this.value)" autocomplete="off">
          <select id="resumen_obraSelect" multiple size="6" class="multi-select">
            <option value="__ALL__">Todas las Obras</option>
          </select>
          <div id="resumen_obraHint" class="hint">Elegí obras o activá «Excluir» para omitir</div>
        </div>

        <div class="filter-group">
          <div class="filter-label">
            <span>Año Evaluado:</span>
          </div>
          <select id="resumen_anioSelect" multiple size="3" class="multi-select">
            <option value="__ALL__">Todos los Años</option>
          </select>
        </div>

        <div class="filter-group">
          <div class="filter-label">
            <span>Mes Evaluado:</span>
          </div>
          <select id="resumen_mesCumplSelect" multiple size="4" class="multi-select">
            <option value="__ALL__">Todos los Meses</option>
          </select>
        </div>

        <div class="filter-group">
          <div class="filter-label">
            <span>Grupo de Compras (Partidas):</span>
          </div>
          <select id="resumen_gcEmrfSelect" multiple size="4" class="multi-select">
            <option value="__ALL__">Todos los Grupos</option>
            <option value="C01" selected>C01</option>
            <option value="C07" selected>C07</option>
            <option value="C02" selected>C02</option>
          </select>
        </div>

        <div id="resumen_arribaWrap" style="width: 100%; margin-top: 6px;">
          <button id="resumen_btnArriba" class="btn btn-arriba" type="button" style="width: 100%;" title="Alternar entre Base y Mina">
            🏔️ Medir cumplimiento arriba
          </button>
          <div class="hint" style="color: #64748b; font-size: 0.65rem; text-align: center; margin-top: 2px;">
            Obras 365 y 372 (año 2026)
          </div>
        </div>
      </aside>

      <!-- ÁREA DE TRABAJO BENTO GRID (Basado 100% en Prototipo) -->
      <div class="main-workspace">
        
        <!-- Context Bar -->
        <div class="executive-context-bar">
          <div class="ctx-left">
            <span class="ctx-badge">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              <span id="resumen_lblObra">Todas las Obras</span>
            </span>
            <span class="ctx-desc">Estado consolidado de inventario, logística y cumplimiento de pedidos.</span>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 0.75rem; color: var(--text-muted);">Meta Corporativa AT: <strong style="color: #0f766e;">78%</strong></span>
          </div>
        </div>

        <!-- BENTO MASTER GRID -->'''

new_resumen_sidebar = '''      <!-- Barra Lateral Izquierda (Panel de Control - Estilo Prototipo) -->
      <aside class="st-sidebar app-sidebar" id="smartSidebar">
        <div class="st-sidebar-toprow">
          <div class="st-sector-switcher">
            <select class="st-sector-select" onchange="window.switchSector(this.value)" aria-label="Seleccionar sector">
              <option value="abastecimiento">🏗️ OBRAS</option>
              <option value="sede">🏢 SEDE</option>
              <option value="compras">🛒 COMPRAS</option>
              <option value="almacen">🏭 ALMACEN</option>
            </select>
          </div>
          <button type="button" class="st-collapse-btn" onclick="window.toggleStSidebar()" title="Ocultar barra lateral">«</button>
        </div>

        <div class="sidebar-header">
          <div class="sidebar-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
            <span>Filtros de Control</span>
          </div>
          <div style="display: flex; align-items: center; gap: 4px;">
            <button id="resumen_btnClearFilters" class="sidebar-reset-btn" title="Restablecer todos los filtros">Restablecer</button>
            <button class="help-btn" onclick="openHelp('Filtros — Resumen Ejecutivo', `
              <h4>Cliente / Obra</h4>
              <p>Filtrá el resumen por obra o almacén seleccionando las pastillas de obras.</p>
              <h4>Año y Mes Evaluado</h4>
              <p>Seleccioná el período para analizar el rendimiento de cumplimiento.</p>
              <div class=&quot;hm-tip&quot;>💡 Podés restablecer con el botón Restablecer.</div>
            `)" title="Ayuda sobre los filtros">ℹ</button>
          </div>
        </div>

        <!-- Buscador y Pastillas de Obra -->
        <div class="filter-group" id="resumen_obraFilterWrap">
          <div class="filter-label">
            <span>Cliente / Obra:</span>
            <span style="font-size: 0.68rem; color: #0f766e; cursor: pointer; font-weight: 700;" onclick="window.toggleResumenExcludeObra()" id="resumen_btnExcludeObra">Excluir: OFF</span>
          </div>
          <input type="text" id="resumen_obraQuickSearch" class="filter-search-input" placeholder="🔍 Filtrar o buscar obra..." oninput="window.filterResumenObraPills(this.value)" autocomplete="off">
          
          <div class="pills-container" id="obraPillsContainer">
            <span class="filter-pill active" data-val="__ALL__" onclick="window.selectResumenObraPill(this, '__ALL__')">Todas las Obras</span>
          </div>
          <!-- Select oculto para sincronización con lógica existente -->
          <select id="resumen_obraSelect" multiple style="display: none;">
            <option value="__ALL__" selected>Todas las Obras</option>
          </select>
          <div id="resumen_obraHint" class="hint" style="display: none;">Elegí obras o activá «Excluir» para omitir</div>
        </div>

        <!-- Filtro de Año con Pastillas -->
        <div class="filter-group">
          <div class="filter-label">
            <span>Año Evaluado:</span>
          </div>
          <div class="pills-container" id="anioPillsContainer">
            <span class="filter-pill active" data-val="__ALL__" onclick="window.selectResumenAnioPill(this, '__ALL__')">Todos</span>
          </div>
          <select id="resumen_anioSelect" multiple style="display: none;">
            <option value="__ALL__" selected>Todos los Años</option>
          </select>
        </div>

        <!-- Filtro Mes Evaluado con Pastillas -->
        <div class="filter-group">
          <div class="filter-label">
            <span>Mes Evaluado:</span>
          </div>
          <div class="pills-container" id="mesPillsContainer">
            <span class="filter-pill active" data-val="__ALL__" onclick="window.selectResumenMesPill(this, '__ALL__')">Todos</span>
          </div>
          <select id="resumen_mesCumplSelect" multiple style="display: none;">
            <option value="__ALL__" selected>Todos los Meses</option>
          </select>
        </div>

        <!-- Grupo de Compras (Partidas) con Pastillas -->
        <div class="filter-group">
          <div class="filter-label">
            <span>Grupo de Compras (Partidas):</span>
          </div>
          <div class="pills-container" id="gcEmrfPillsContainer">
            <span class="filter-pill" data-val="__ALL__" onclick="window.selectResumenGcPill(this, '__ALL__')">Todos</span>
            <span class="filter-pill active" data-val="C01" onclick="window.selectResumenGcPill(this, 'C01')">C01</span>
            <span class="filter-pill active" data-val="C07" onclick="window.selectResumenGcPill(this, 'C07')">C07</span>
            <span class="filter-pill active" data-val="C02" onclick="window.selectResumenGcPill(this, 'C02')">C02</span>
          </div>
          <select id="resumen_gcEmrfSelect" multiple style="display: none;">
            <option value="__ALL__">Todos los Grupos</option>
            <option value="C01" selected>C01</option>
            <option value="C07" selected>C07</option>
            <option value="C02" selected>C02</option>
          </select>
        </div>

        <!-- Interruptor Toggle: Medir Cumplimiento Arriba -->
        <div class="toggle-row">
          <div class="toggle-info">
            <span class="toggle-title">Medición Arriba</span>
            <span class="toggle-desc">Mina Obras 365 y 372</span>
          </div>
          <div class="switch-ui" id="switchArriba" onclick="window.toggleResumenArribaSwitch()" title="Alternar entre Base y Mina"></div>
        </div>
        <button id="resumen_btnArriba" style="display: none;" type="button"></button>
      </aside>

      <!-- ÁREA DE TRABAJO BENTO GRID (Basado 100% en Prototipo) -->
      <div class="main-workspace">
        <!-- Span oculto para compatibilidad con scripts existentes -->
        <span id="resumen_lblObra" style="display: none;">Todas las Obras</span>

        <!-- BENTO MASTER GRID -->'''

# Normalize newlines
def norm(t):
    return t.replace('\r\n', '\n')

content_norm = norm(content)
old_serv_norm = norm(old_serv)
new_serv_norm = norm(new_serv)
old_resumen_sidebar_norm = norm(old_resumen_sidebar)
new_resumen_sidebar_norm = norm(new_resumen_sidebar)

if old_serv_norm in content_norm:
    content_norm = content_norm.replace(old_serv_norm, new_serv_norm, 1)
    print("Replaced old_serv successfully")
else:
    print("Could not find old_serv!")

if old_resumen_sidebar_norm in content_norm:
    content_norm = content_norm.replace(old_resumen_sidebar_norm, new_resumen_sidebar_norm, 1)
    print("Replaced old_resumen_sidebar successfully")
else:
    print("Could not find old_resumen_sidebar!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content_norm)

print("index.html updated successfully")
