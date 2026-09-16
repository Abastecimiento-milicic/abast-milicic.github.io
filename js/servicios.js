(function() {
  const csvUrl = "data/SERVICIOS OBRA.csv";
  const DELIM = ";";

  const CLIENT_COL_NAME = "CLIENTE";
  const PERIODO_COL_NAME = "Período de certificación";
  const ESTADO_COL_NAME = "Estado Servicio";
  const G_COMPRA_COL_NAME = "Grupo de Compra Definitivo";
  const ESTADO_ITEM_COL = "ESTADO ITEM";

  let data = [];
  let headers = [];
  let currentSort = { col: 'count', dir: 'desc' };

  const clean = (v) => (v ?? "").toString().trim();
  function setText(id, txt) { const el = document.getElementById(id); if (el) el.textContent = txt ?? ""; }
  function fmtInt(n) { return Number(n || 0).toLocaleString("es-AR"); }
  function safeFileName(str) {
      return (str || "").toString().replace(/[^\w\-]+/g, "_").replace(/^_+|_+$/g, "") || "Item";
  }

  function parseCSV(text) {
      const result = Papa.parse(text, { delimiter: DELIM, skipEmptyLines: true });
      return result.data;
  }

  function getSelValues(id) {
      const sel = document.getElementById(id) || document.getElementById(id.replace('serv_', ''));
      if (!sel) return [];
      return [...sel.selectedOptions].map(o => o.value).filter(v => v !== "__ALL__");
  }

  async function downloadExcel(rows, filename = "Seleccion_Servicios.xlsx") {
      if (!rows || !rows.length) return alert("No hay datos seleccionados para descargar.");
      await window.saveAsExcel(filename, "Servicios", headers, rows, headers);
  }

  function getItemBadgeClass(estadoItem) {
      const val = clean(estadoItem).toUpperCase();
      const rojos = ["ADJUDICADO", "ADJUDICADO PARCIAL", "RESPONDIDO", "INCOMPLETO", "SIN TRATAMIENTO"];
      const verdes = ["CUMPLIDO", "ALMACENADO", "CONSUMIDO PARCIAL"];
      if (verdes.includes(val)) return "badge-item-verde";
      if (rojos.includes(val)) return "badge-item-rojo";
      return "badge-item-azul";
  }

  function getServicioBadgeClass(estadoServicio) {
      const val = clean(estadoServicio);
      if (val === "En curso") return "badge-serv-verde";
      if (val === "En curso - Próximo a vencer") return "badge-serv-amarillo";
      if (val === "En curso - Total recepcionado") return "badge-serv-naranja";
      if (val === "Vencido con cant pendiente a recep") return "badge-serv-rojo";
      if (val === "Pedido de Info") return "badge-serv-morado";
      return "badge-serv-gris";
  }

  function renderResumenTable(filtered) {
      const resumenTbody = document.getElementById("serv_resumenBody") || document.getElementById("resumenBody");

      if (!resumenTbody) return;
      resumenTbody.innerHTML = "";

      if (!filtered || filtered.length === 0) {
          resumenTbody.innerHTML = `<tr><td colspan="4" style="text-align: center; color: #64748b; padding: 25px; font-style: italic;">No hay pedidos para los filtros seleccionados</td></tr>`;
          return;
      }

      // Agrupar por ESTADO ITEM y Estado Servicio guardando las filas asociadas
      const summaryMap = new Map();
      filtered.forEach(r => {
          const estadoItem = clean(r[ESTADO_ITEM_COL]) || "(Sin Estado Item)";
          const estadoServicio = clean(r[ESTADO_COL_NAME]) || "(Sin Estado Servicio)";
          const key = `${estadoItem}___${estadoServicio}`;

          if (!summaryMap.has(key)) {
              summaryMap.set(key, { estadoItem, estadoServicio, count: 0, rows: [] });
          }
          const grp = summaryMap.get(key);
          grp.count += 1;
          grp.rows.push(r);
      });

      const summaryList = Array.from(summaryMap.values());

      // Ordenamiento dinámico
      summaryList.sort((a, b) => {
          let res = 0;
          if (currentSort.col === 'count') {
              res = a.count - b.count;
              if (res === 0) res = a.estadoItem.localeCompare(b.estadoItem);
          } else if (currentSort.col === 'estadoItem') {
              res = a.estadoItem.localeCompare(b.estadoItem);
              if (res === 0) res = b.count - a.count;
          } else if (currentSort.col === 'estadoServicio') {
              res = a.estadoServicio.localeCompare(b.estadoServicio);
              if (res === 0) res = b.count - a.count;
          }
          return currentSort.dir === 'desc' ? -res : res;
      });

      // Actualizar íconos indicadores de orden en encabezados
      ['estadoItem', 'estadoServicio', 'count'].forEach(col => {
          const icon = document.getElementById(`serv_sort_${col}`);
          if (icon) {
              if (currentSort.col === col) {
                  icon.textContent = currentSort.dir === 'asc' ? '▲' : '▼';
                  icon.style.color = '#2563eb';
              } else {
                  icon.textContent = '↕';
                  icon.style.color = '#94a3b8';
              }
          }
      });

      // Renderizar filas de la tabla con botón de descarga individual
      summaryList.forEach((item, index) => {
          const tr = document.createElement("tr");
          const itemBadge = getItemBadgeClass(item.estadoItem);
          const servBadge = getServicioBadgeClass(item.estadoServicio);

          tr.innerHTML = `
              <td><span class="badge-item-status ${itemBadge}">${item.estadoItem}</span></td>
              <td><span class="badge-serv-status ${servBadge}">${item.estadoServicio}</span></td>
              <td style="text-align: right;"><span style="font-weight: 700; font-size: 0.95rem; color: #1e293b;">${fmtInt(item.count)}</span></td>
              <td style="text-align: center;">
                  <button class="btn-table-download" data-idx="${index}" title="Descargar ${item.count} items en Excel">⬇ Descargar</button>
              </td>
          `;
          resumenTbody.appendChild(tr);
      });

      // Listener para cada botón de descarga por fila
      resumenTbody.querySelectorAll(".btn-table-download").forEach(btn => {
          btn.addEventListener("click", (e) => {
              e.stopPropagation();
              const idx = parseInt(btn.getAttribute("data-idx"), 10);
              const targetItem = summaryList[idx];
              if (targetItem && targetItem.rows && targetItem.rows.length) {
                  const fname = `Servicios_${safeFileName(targetItem.estadoItem)}_${safeFileName(targetItem.estadoServicio)}.xlsx`;
                  downloadExcel(targetItem.rows, fname);
              }
          });
      });
  }

  function setupSortListeners() {
      document.querySelectorAll('#panel-servicios th.sortable, .serv-resumen-table th.sortable').forEach(th => {
          th.addEventListener('click', () => {
              const col = th.getAttribute('data-sort');
              if (!col) return;
              if (currentSort.col === col) {
                  currentSort.dir = currentSort.dir === 'asc' ? 'desc' : 'asc';
              } else {
                  currentSort.col = col;
                  currentSort.dir = col === 'count' ? 'desc' : 'asc';
              }
              applyAll();
          });
      });
  }

  function applyAll() {
      const selClientes = getSelValues("serv_clienteSelect");
      const selPeriodos = getSelValues("serv_clasif2Select");
      const selEstados = getSelValues("serv_gcocSelect");
      const selGrupos = getSelValues("serv_grupoCompraSelect");
      const selItemEst = getSelValues("serv_estadoItemSelect"); 
      
      const filtered = data.filter(r => {
          const matchClie = !selClientes.length || selClientes.includes(r[CLIENT_COL_NAME]);
          const matchPeri = !selPeriodos.length || selPeriodos.includes(r[PERIODO_COL_NAME]);
          const matchEsta = !selEstados.length || selEstados.includes(r[ESTADO_COL_NAME]);
          const matchGrup = !selGrupos.length || selGrupos.includes(r[G_COMPRA_COL_NAME]);
          const matchItem = !selItemEst.length || selItemEst.includes(r[ESTADO_ITEM_COL]);
          return matchClie && matchPeri && matchEsta && matchGrup && matchItem;
      });

      setText("serv_kpiTotal", fmtInt(filtered.length));
      setText("kpiTotal", fmtInt(filtered.length));

      renderResumenTable(filtered);

      return filtered;
  }

  function fill(id, col) {
      const values = [...new Set(data.map(r => r[col]).filter(Boolean))].sort();
      const sel = document.getElementById(id) || document.getElementById(id.replace('serv_', ''));
      if (!sel) return;
      sel.innerHTML = '<option value="__ALL__">Todos</option>';
      values.forEach(v => {
          const opt = document.createElement("option");
          opt.value = v; opt.textContent = v;
          sel.appendChild(opt);
      });
  }

  /* ============================
     EXPOSE DEFERRED INITIALIZATION LIFE CYCLE HOOK
  =========================== */
  window.initServicios = function() {
      if (window.serviciosInitialized) return;
      window.serviciosInitialized = true;

      // fetch with cache optimized
      fetchWithCache(csvUrl + "?t=" + window.CACHE_BUSTER)
      .then(text => {
          const rows = parseCSV(text);
          if (rows.length < 2) return;
          headers = rows[0].map(clean);
          data = rows.slice(1).map(row => {
              let o = {};
              headers.forEach((h, i) => o[h] = clean(row[i]));
              return o;
          });

          fill("serv_clienteSelect", CLIENT_COL_NAME);
          fill("serv_clasif2Select", PERIODO_COL_NAME);
          fill("serv_gcocSelect", ESTADO_COL_NAME);
          fill("serv_grupoCompraSelect", G_COMPRA_COL_NAME);
          fill("serv_estadoItemSelect", ESTADO_ITEM_COL);

          ["serv_clienteSelect", "serv_clasif2Select", "serv_gcocSelect", "serv_grupoCompraSelect", "serv_estadoItemSelect"].forEach(id => {
              const el = document.getElementById(id) || document.getElementById(id.replace('serv_', ''));
              el?.addEventListener("change", () => {
                  applyAll();
              });
          });

          const btnDl = document.getElementById("serv_btnDownloadSelection") || document.getElementById("btnDownloadSelection");
          btnDl?.addEventListener("click", () => {
              const currentFiltered = applyAll();
              downloadExcel(currentFiltered);
          });

          setupSortListeners();
          applyAll();

          const loader = document.getElementById("serv_loader") || document.getElementById("loader");
          if (loader) loader.style.display = "none";
      });
  };

  // Auto-init if running on standalone servicios.html
  if (document.getElementById('panel-servicios') === null && (document.getElementById('serv_clienteSelect') || document.getElementById('clienteSelect'))) {
      if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', () => window.initServicios());
      } else {
          window.initServicios();
      }
  }

})();
