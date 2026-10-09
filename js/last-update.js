// Editá SOLO este archivo para cambiar la fecha mostrada en el header.
window.LAST_UPDATE = "09/10/2026";
// Cambia este valor para fijar el mes por defecto en los filtros (ej. "2026-08")
window.MES_POR_DEFECTO = "2026-09";

let cb = sessionStorage.getItem('mi_cache_buster');
if (!cb) {
  cb = new Date().getTime();
  sessionStorage.setItem('mi_cache_buster', cb);
}
window.CACHE_BUSTER = cb + "_v42_periodo_corto_pq_sync";

window.forceRefreshData = function() {
  sessionStorage.removeItem('mi_cache_buster');

  if (typeof window.clearDataCache === 'function') {
    window.clearDataCache().finally(() => window.location.reload());
  } else {
    window.location.reload();
  }
};



