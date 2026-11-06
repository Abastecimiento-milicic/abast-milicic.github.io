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
        </div>

        <div class="st-filters-stack">
          <div class="filter">
            <label>Cliente:</label>''')

new_dem_header = norm('''        <div class="sidebar-header">
          <div class="sidebar-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
            <span>Filtros de Control</span>
          </div>
          <button id="dem_btnClearFilters" class="sidebar-reset-btn" onclick="window.resetDemorasFilters()" title="Restablecer filtros">Restablecer</button>
        </div>

        <div class="st-filters-stack">
          <div class="filter">
            <label>Cliente:</label>''')

# 5. Panel Tiempos header
old_tiempos_header = norm('''        <div class="st-sidebar-toprow">
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
        </div>''')

new_tiempos_header = norm('''        <div class="st-sidebar-toprow">
          <div class="st-sector-switcher">
            <select class="st-sector-select" onchange="window.switchSector(this.value)" aria-label="Seleccionar sector">
              <option value="abastecimiento">🏗️ OBRAS</option>
              <option value="sede">🏢 SEDE</option><option value="compras">🛒 COMPRAS</option><option value="almacen">🏭 ALMACEN</option>
            </select>
          </div>
          <button type="button" class="st-collapse-btn" onclick="window.toggleStSidebar()" title="Ocultar barra lateral">«</button>
        </div>

        <div class="sidebar-header">
          <div class="sidebar-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
            <span>Filtros de Control</span>
          </div>
          <button id="tiempos_btnReset" class="sidebar-reset-btn" onclick="window.resetTiemposFilters()" title="Restablecer filtros">Restablecer</button>
        </div>''')

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

new_emrf_subhead = ''

# Check presence
replacements = [
    ("cumpl_header", old_cumpl_header, new_cumpl_header),
    ("cumpl_arriba", old_cumpl_arriba, new_cumpl_arriba),
    ("mm_header", old_mm_header, new_mm_header),
    ("dem_header", old_dem_header, new_dem_header),
    ("tiempos_header", old_tiempos_header, new_tiempos_header),
    ("emrf_header", old_emrf_header, new_emrf_header),
    ("emrf_subhead", old_emrf_subhead, new_emrf_subhead),
]

for name, o, n in replacements:
    if o in content_norm:
        content_norm = content_norm.replace(o, n, 1)
        print(f"Applied {name} replacement successfully")
    else:
        print(f"FAILED to find {name}!")

# Now replace the JS controller (createStMultiSelect -> createPrototypePillsFilter)
js_start_marker = norm('/* ==========================================================================\n       STREAMLIT PILL MULTISELECT CONTROLLER')
js_end_marker = norm('window.toggleStSidebar = function()')

new_js_controller = norm('''/* ==========================================================================
       PROTOTYPE PILLS FILTER CONTROLLER (Universal en todas las pestañas)
       ========================================================================== */
    (function() {
      const instances = new Map();

      function isAllOption(opt) {
        if (!opt) return false;
        const val = (opt.value || '').trim();
        const txt = (opt.textContent || '').trim().toLowerCase();
        return val === '' || val === '__ALL__' || val.toUpperCase() === 'TODAS' || val.toUpperCase() === 'TODOS' || txt === 'todos' || txt === 'todas' || txt.startsWith('todo ') || txt.startsWith('toda ') || txt.startsWith('todas las') || txt.startsWith('todos los');
      }

      function createPrototypePillsFilter(sel) {
        if (instances.has(sel)) return instances.get(sel);

        // Ocultar select original pero mantenerlo plenamente funcional en el DOM
        sel.style.setProperty('display', 'none', 'important');
        sel.classList.add('proto-select-hidden');

        const wrapper = document.createElement('div');
        wrapper.className = 'proto-pills-filter-wrap';

        let searchInput = null;

        const pillsContainer = document.createElement('div');
        pillsContainer.className = 'pills-container';

        wrapper.appendChild(pillsContainer);
        sel.parentNode.insertBefore(wrapper, sel.nextSibling);

        let lastSig = '';
        let isUpdating = false;

        function triggerSelectChange() {
          isUpdating = true;
          sel.dispatchEvent(new Event('change', { bubbles: true }));
          setTimeout(() => {
            isUpdating = false;
            render();
            if (typeof window.updateCumplFiltersSummary === 'function') window.updateCumplFiltersSummary();
          }, 0);
        }

        function render(force = false) {
          const opts = Array.from(sel.options).filter(o => o.value !== undefined);
          if (!opts.length) {
            wrapper.style.display = 'none';
            return;
          }
          wrapper.style.display = '';

          // Si tiene más de 6 opciones, agregar buscador interactivo en la parte superior
          if (opts.length > 6 && !searchInput) {
            searchInput = document.createElement('input');
            searchInput.type = 'text';
            searchInput.className = 'filter-search-input';
            searchInput.placeholder = '🔍 Filtrar opciones...';
            searchInput.autocomplete = 'off';
            searchInput.addEventListener('input', () => {
              const q = searchInput.value.toLowerCase().trim();
              pillsContainer.querySelectorAll('.filter-pill').forEach(pill => {
                const isAll = pill.getAttribute('data-is-all') === 'true';
                if (isAll || pill.textContent.toLowerCase().includes(q)) {
                  pill.style.display = 'inline-flex';
                } else {
                  pill.style.display = 'none';
                }
              });
            });
            wrapper.insertBefore(searchInput, pillsContainer);
          } else if (opts.length <= 6 && searchInput) {
            searchInput.remove();
            searchInput = null;
          }

          const sig = opts.map(o => o.value + ':' + (o.selected ? '1' : '0') + ':' + o.textContent).join('|');
          if (!force && sig === lastSig) return;
          lastSig = sig;

          pillsContainer.innerHTML = '';

          const allOpt = opts.find(isAllOption);
          const specificOpts = opts.filter(o => !isAllOption(o));
          const hasSelectedSpecific = specificOpts.some(o => o.selected);

          opts.forEach(opt => {
            const isAll = isAllOption(opt);
            const isSelected = isAll ? !hasSelectedSpecific : opt.selected;

            const pill = document.createElement('span');
            pill.className = 'filter-pill' + (isSelected ? ' active' : '');
            pill.setAttribute('data-val', opt.value);
            pill.setAttribute('data-is-all', isAll ? 'true' : 'false');
            pill.textContent = opt.textContent.trim() || (isAll ? 'Todos' : opt.value);

            pill.addEventListener('click', (e) => {
              const isMulti = e.ctrlKey || e.metaKey || e.shiftKey;

              if (isAll) {
                // Seleccionar Todos y deseleccionar opciones específicas
                opts.forEach(o => {
                  o.selected = isAllOption(o);
                });
              } else {
                if (isMulti) {
                  // Modo multiselección con Ctrl / Shift
                  opt.selected = !opt.selected;
                  if (allOpt) allOpt.selected = false;
                } else {
                  // Clic normal: foco en esta opción específica (o toggle si ya era la única seleccionada)
                  if (opt.selected && specificOpts.filter(o => o.selected).length === 1) {
                    opts.forEach(o => {
                      o.selected = isAllOption(o);
                    });
                  } else {
                    opts.forEach(o => {
                      o.selected = (o === opt);
                    });
                  }
                }
              }

              // Si ninguna específica quedó seleccionada, marcar Todos
              const anySpecific = specificOpts.some(o => o.selected);
              if (!anySpecific && allOpt) {
                allOpt.selected = true;
              }

              triggerSelectChange();
            });

            pillsContainer.appendChild(pill);
          });
        }

        // Observar cambios en las opciones del <select> subyacente
        const observer = new MutationObserver(() => {
          if (!isUpdating) render();
        });
        observer.observe(sel, { childList: true, subtree: true, attributes: true });

        sel.addEventListener('change', () => {
          setTimeout(() => render(), 10);
        });

        render();
        const inst = { render, wrapper, pillsContainer, sel };
        instances.set(sel, inst);
        return inst;
      }

      window.updateCumplFiltersSummary = function() {
        const renderChips = (elId, defs) => {
          const el = document.getElementById(elId);
          if (!el) return;
          el.innerHTML = '<span class="st-af-title">FILTROS:</span>' + defs.map(d => {
            if (d.custom) {
              const res = d.custom();
              return `<span class="st-af-chip ${res.active ? 'is-active' : ''}"><span class="st-af-k">${d.lbl}:</span> <span class="st-af-v">${res.txt}</span></span>`;
            }
            const s = document.getElementById(d.id);
            const selOpts = s ? [...s.options].filter(o => o.selected && !isAllOption(o)) : [];
            const active = selOpts.length > 0;
            const valTxt = active ? selOpts.map(o => (o.textContent || o.value || '').trim()).join(', ') : 'Todos';
            return `<span class="st-af-chip ${active ? 'is-active' : ''}"><span class="st-af-k">${d.lbl}:</span> <span class="st-af-v">${valTxt}</span></span>`;
          }).join('');
        };
        const isCompras = window.currentAppSector === 'compras';
        renderChips('cumpl_activeFiltersSummary', isCompras ? [
          { id: 'cumpl_clienteSelect', lbl: 'Cliente' },
          { id: 'cumpl_operadorSelect', lbl: 'Comprador' },
          { id: 'cumpl_clasif2Select', lbl: 'Clasif.' },
          { id: 'cumpl_gcocSelect', lbl: 'GC' },
          { id: 'cumpl_mesSelect', lbl: 'Mes' },
          { id: 'centroSelect', lbl: 'Centro' },
          { id: 'cumpl_proveedorSelect', lbl: 'Proveedor' },
          { id: 'cumpl_soloAbastSelect', lbl: 'Compras / Abast. / Equipos' }
        ] : [
          { id: 'cumpl_clienteSelect', lbl: 'Obra' },
          { id: 'cumpl_clasif2Select', lbl: 'Clasif.' },
          { id: 'cumpl_gcocSelect', lbl: 'GC' },
          { id: 'cumpl_mesSelect', lbl: 'Mes' },
          { id: 'centroSelect', lbl: 'Centro' }
        ]);
        renderChips('mm_activeFiltersSummary', [{ id: 'mm_clienteSelect', lbl: 'Almacén' }]);
        renderChips('dem_activeFiltersSummary', [
          { id: 'dem_clienteSelect', lbl: 'Cliente' },
          { id: 'dem_clasifSelect', lbl: 'Clasif.' },
          { id: 'dem_mesSelect', lbl: 'Mes' }
        ]);
        renderChips('serv_activeFiltersSummary', [
          { id: 'serv_clienteSelect', lbl: 'Cliente' },
          { id: 'serv_clasif2Select', lbl: 'Período' },
          { id: 'serv_gcocSelect', lbl: 'Estado' },
          { id: 'serv_grupoCompraSelect', lbl: 'GC' },
          { id: 'serv_estadoItemSelect', lbl: 'Estado Ítem' }
        ]);
        renderChips('tiempos_activeFiltersSummary', [
          {
            lbl: 'Obra',
            custom: () => {
              const s = document.getElementById('tiempos_obraSelect');
              const o = s && s.selectedOptions[0];
              const txt = o ? (o.textContent || o.value || '').trim() : 'Todos';
              return { active: !!(txt && txt.toLowerCase() !== 'todos' && txt.toLowerCase() !== 'todas'), txt: txt || 'Todos' };
            }
          },
          {
            lbl: 'Mes',
            custom: () => {
              const list = document.getElementById('tiempos_slicer_list');
              if (!list) return { active: false, txt: 'Todos' };
              const all = list.querySelectorAll('.tiempos-slicer-item');
              const act = list.querySelectorAll('.tiempos-slicer-item.active');
              if (!act.length || act.length === all.length) return { active: false, txt: 'Todos' };
              const names = [...act].map(i => (i.querySelector('span')?.textContent || '').trim()).filter(Boolean);
              return { active: true, txt: names.join(', ') };
            }
          }
        ]);
        renderChips('emrf_activeFiltersSummary', [
          {
            lbl: 'Sociedad',
            custom: () => {
              const s = document.getElementById('emrf_sociedadSelect');
              const v = s ? s.value : 'TODAS';
              const o = s && s.selectedOptions[0];
              return { active: v !== 'TODAS', txt: (v === 'TODAS' || !o) ? 'Todas' : o.textContent.trim() };
            }
          },
          {
            lbl: 'Búsqueda',
            custom: () => {
              const inp = document.getElementById('emrf_searchInput');
              const v = inp ? inp.value.trim() : '';
              return { active: !!v, txt: v || 'Todos' };
            }
          },
          { id: 'emrf_estadoSelect', lbl: 'Estado' },
          { id: 'emrf_gcSelect', lbl: 'GC' },
          { id: 'emrf_vencSelect', lbl: 'Venc.' },
          { id: 'emrf_operOcSelect', lbl: 'Operador' }
        ]);
      };

      window.syncAllStMultiSelects = function() {
        // Encontrar todos los selects en barras laterales (excepto el de sector y los que tienen contenedores HTML dedicados)
        document.querySelectorAll('.st-sidebar select:not(.st-sector-select):not([data-skip-pills])').forEach(sel => {
          if (sel.id === 'resumen_obraSelect' || sel.id === 'resumen_anioSelect' || sel.id === 'resumen_mesCumplSelect' || sel.id === 'resumen_gcEmrfSelect') {
            return;
          }
          const inst = createPrototypePillsFilter(sel);
          inst.render();
        });
        if (typeof window.updateCumplFiltersSummary === 'function') window.updateCumplFiltersSummary();
      };

      // Helper global para alternar Medición Arriba con switch UI en Cumplimiento
      window.toggleCumplArribaSwitch = function() {
        const btn = document.getElementById("cumpl_btnArriba");
        if (btn) btn.click();
        const sw = document.getElementById("cumpl_switchArriba");
        if (sw && btn) {
          setTimeout(() => {
            sw.classList.toggle("active", btn.classList.contains("btn-active"));
          }, 20);
        }
      };

      window.resetMMFilters = function() {
        const sel = document.getElementById("mm_clienteSelect");
        if (sel) {
          [...sel.options].forEach((o, i) => o.selected = (i === 0 || o.value === "" || o.value === "__ALL__"));
          sel.dispatchEvent(new Event('change', { bubbles: true }));
        }
        if (typeof window.syncAllStMultiSelects === 'function') window.syncAllStMultiSelects();
      };

      window.resetDemorasFilters = function() {
        ['dem_clienteSelect', 'dem_clasifSelect', 'dem_mesSelect'].forEach(id => {
          const sel = document.getElementById(id);
          if (sel) {
            [...sel.options].forEach((o, i) => o.selected = (i === 0 || o.value === "" || o.value === "__ALL__"));
            sel.dispatchEvent(new Event('change', { bubbles: true }));
          }
        });
        if (typeof window.syncAllStMultiSelects === 'function') window.syncAllStMultiSelects();
      };

      window.resetTiemposFilters = function() {
        const sel = document.getElementById("tiempos_obraSelect");
        if (sel) {
          [...sel.options].forEach((o, i) => o.selected = (i === 0 || o.value === "" || o.value === "__ALL__"));
          sel.dispatchEvent(new Event('change', { bubbles: true }));
        }
        const btnAll = document.getElementById("tiempos_btn_select_all");
        if (btnAll) btnAll.click();
        if (typeof window.syncAllStMultiSelects === 'function') window.syncAllStMultiSelects();
      };

      // Sincronizar al hacer clic en botones de restablecer o cambiar pestañas
      document.addEventListener('click', (e) => {
        if (e.target.closest('.sidebar-reset-btn') || e.target.closest('.btn-clear') || e.target.closest('#cumpl_btnArriba') || e.target.closest('.st-sidebar')) {
          setTimeout(() => {
            if (typeof window.updateCumplFiltersSummary === 'function') window.updateCumplFiltersSummary();
            if (typeof window.syncAllStMultiSelects === 'function') window.syncAllStMultiSelects();
          }, 40);
        }
      });

      window.addEventListener('DOMContentLoaded', () => {
        window.syncAllStMultiSelects();
        setInterval(() => window.syncAllStMultiSelects(), 500);
        document.addEventListener('input', (e) => {
          if (e.target.closest('.st-sidebar') && typeof window.updateCumplFiltersSummary === 'function') window.updateCumplFiltersSummary();
        });
        document.addEventListener('change', (e) => {
          if (e.target.closest('.st-sidebar') && typeof window.updateCumplFiltersSummary === 'function') setTimeout(() => window.updateCumplFiltersSummary(), 15);
        });
      });
    })();\n\n    ''')

if js_start_marker in content_norm and js_end_marker in content_norm:
    pre = content_norm.split(js_start_marker)[0]
    post = content_norm.split(js_end_marker)[1]
    content_norm = pre + new_js_controller + js_end_marker + post
    print("Replaced JS controller with createPrototypePillsFilter successfully")
else:
    print("FAILED to find JS controller range!")

# Bump cache buster
content_norm = content_norm.replace('20261106_114900', '20261106_121500')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content_norm)

print("index.html updated successfully")
