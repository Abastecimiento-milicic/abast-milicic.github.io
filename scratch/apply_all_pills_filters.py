import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

def norm(t): return t.replace('\r\n', '\n')

content_norm = norm(content)

# 1. Panel Cumplimiento header
old_cumpl_header = norm('''        <h3 class="st-ctrl-title">Panel de Control</h3>

        <div class="st-filters-header">
          <h4 class="st-filters-title">Filtros de Búsqueda</h4>
          <div class="st-filters-actions">
            <button id="cumpl_btnClearFilters" class="btn-clear" title="Restablecer todos los filtros">🧹 Limpiar</button>''')

new_cumpl_header = norm('''        <div class="sidebar-header">
          <div class="sidebar-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
            <span>Filtros de Control</span>
          </div>
          <div style="display: flex; align-items: center; gap: 4px;">
            <button id="cumpl_btnClearFilters" class="sidebar-reset-btn" title="Restablecer todos los filtros">Restablecer</button>''')

# 2. Panel Cumplimiento Medición Arriba
old_cumpl_arriba = norm('''          <!-- Botón Medir Cumplimiento Arriba -->
          <div id="cumpl_arribaWrap" style="width: 100%; display: flex; flex-direction: column; gap: 3px;">
            <button id="cumpl_btnArriba" class="btn btn-arriba" type="button" style="width: 100%;" title="Alternar entre medición en Base y medición en Mina (Arriba)">
              🏔️ Medir cumplimiento arriba
            </button>
            <div class="hint" style="color: #475569; font-size: 0.68rem; font-weight: 600; text-align: center; line-height: 1.2;">
              Obras 365 y 372 (año 2026)
            </div>
          </div>''')

new_cumpl_arriba = norm('''          <!-- Interruptor Toggle: Medir Cumplimiento Arriba -->
          <div id="cumpl_arribaWrap" style="width: 100%;">
            <div class="toggle-row">
              <div class="toggle-info">
                <span class="toggle-title">Medición Arriba</span>
                <span class="toggle-desc">Mina Obras 365 y 372 (2026)</span>
              </div>
              <div class="switch-ui" id="cumpl_switchArriba" onclick="window.toggleCumplArribaSwitch()" title="Alternar entre Base y Mina"></div>
            </div>
            <button id="cumpl_btnArriba" class="btn btn-arriba" type="button" style="display: none;" title="Alternar entre Base y Mina"></button>
          </div>''')

# 3. Panel MM header
old_mm_header = norm('''        <h3 class="st-ctrl-title">Panel de Control</h3>

        <div class="st-filters-header">
          <h4 class="st-filters-title">Filtros de Búsqueda</h4>
          <div class="st-filters-actions">
            <button class="help-btn" onclick="openHelp('Filtros y Disponibilidad — Análisis MM',''')

new_mm_header = norm('''        <div class="sidebar-header">
          <div class="sidebar-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
            <span>Filtros de Control</span>
          </div>
          <div style="display: flex; align-items: center; gap: 4px;">
            <button id="mm_btnClearFilters" class="sidebar-reset-btn" onclick="window.resetMMFilters()" title="Restablecer filtros">Restablecer</button>
            <button class="help-btn" onclick="openHelp('Filtros y Disponibilidad — Análisis MM',''')

# 4. Panel Demoras header
old_dem_header = norm('''        <h3 class="st-ctrl-title">Panel de Control</h3>

        <div class="st-filters-header">
          <h4 class="st-filters-title">Filtros de Búsqueda</h4>
        </div>''')

new_dem_header = norm('''        <div class="sidebar-header">
          <div class="sidebar-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
            <span>Filtros de Control</span>
          </div>
          <button id="dem_btnClearFilters" class="sidebar-reset-btn" onclick="window.resetDemorasFilters()" title="Restablecer filtros">Restablecer</button>
        </div>''')

# 5. Panel Tiempos header
old_tiempos_header = norm('''        <h3 class="st-ctrl-title">Panel de Control</h3>

        <div class="st-filters-header">
          <h4 class="st-filters-title">Filtros de Búsqueda</h4>
        </div>''')

# Note: old_tiempos_header is identical to old_dem_header text, but occurs after panel-tiempos
# Let's handle it carefully in sequential replacement.

# 6. Panel EMRF header
old_emrf_header = norm('''        <h3 class="st-ctrl-title">Panel de Control</h3>

        <!-- 1. Base de Datos / Sociedad (como en Streamlit) -->''')

new_emrf_header = norm('''        <div class="sidebar-header">
          <div class="sidebar-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
            <span>Filtros de Control</span>
          </div>
          <div style="display: flex; align-items: center; gap: 4px;">
            <button id="emrf_btnClearFilters" class="sidebar-reset-btn" title="Restablecer todos los filtros">Restablecer</button>
            <button id="emrf_btnHelp" class="help-btn" title="Ayuda y Guía Operativa de la Cuenta EM/RF">ℹ</button>
          </div>
        </div>

        <!-- 1. Base de Datos / Sociedad (como en Streamlit) -->''')

old_emrf_subhead = norm('''        <div class="st-filters-header">
          <h4 class="st-filters-title">Filtros de Búsqueda</h4>
          <div class="st-filters-actions">
            <button id="emrf_btnClearFilters" class="btn-clear" title="Restablecer todos los filtros">🧹 Limpiar</button>
            <button id="emrf_btnHelp" class="help-btn" title="Ayuda y Guía Operativa de la Cuenta EM/RF">ℹ</button>
          </div>
        </div>''')

new_emrf_subhead = '' # remove redundant subhead

print("1. old_cumpl_header found:", old_cumpl_header in content_norm)
print("2. old_cumpl_arriba found:", old_cumpl_arriba in content_norm)
print("3. old_mm_header found:", old_mm_header in content_norm)
print("4. old_dem_header found:", old_dem_header in content_norm)
print("5. old_emrf_header found:", old_emrf_header in content_norm)
print("6. old_emrf_subhead found:", old_emrf_subhead in content_norm)
