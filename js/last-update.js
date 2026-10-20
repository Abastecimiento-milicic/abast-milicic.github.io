// Inicialización global de fechas por sector (OBRAS, SEDE, COMPRAS, ALMACEN)
window.LAST_UPDATE = window.LAST_UPDATE_OBRAS || "19/10/2026";
window.MES_POR_DEFECTO = window.MES_POR_DEFECTO_OBRAS || "2026-09";

window.syncSectorLastUpdate = function(sector) {
  const sec = (sector || window.currentAppSector || "abastecimiento").toLowerCase();
  if (sec === "sede" || sec.startsWith("sede_")) {
    window.LAST_UPDATE = window.LAST_UPDATE_SEDE || window.LAST_UPDATE_OBRAS || "19/10/2026";
    window.MES_POR_DEFECTO = window.MES_POR_DEFECTO_SEDE || window.MES_POR_DEFECTO_OBRAS || "2026-09";
  } else if (sec === "compras") {
    window.LAST_UPDATE = window.LAST_UPDATE_COMPRAS || window.LAST_UPDATE_OBRAS || "19/10/2026";
    window.MES_POR_DEFECTO = window.MES_POR_DEFECTO_COMPRAS || window.MES_POR_DEFECTO_OBRAS || "2026-09";
  } else if (sec === "almacen") {
    window.LAST_UPDATE = window.LAST_UPDATE_ALMACEN || window.LAST_UPDATE_OBRAS || "19/10/2026";
    window.MES_POR_DEFECTO = window.MES_POR_DEFECTO_ALMACEN || window.MES_POR_DEFECTO_OBRAS || "2026-09";
  } else {
    window.LAST_UPDATE = window.LAST_UPDATE_OBRAS || "19/10/2026";
    window.MES_POR_DEFECTO = window.MES_POR_DEFECTO_OBRAS || "2026-09";
  }

  const el = document.getElementById("lastUpdate");
  if (el) el.textContent = window.LAST_UPDATE;
};

let cb = sessionStorage.getItem('mi_cache_buster');
if (!cb) {
  cb = new Date().getTime();
  sessionStorage.setItem('mi_cache_buster', cb);
}
window.CACHE_BUSTER = cb + "_v64_multi_sector_20261020";

window.forceRefreshData = function() {
  sessionStorage.removeItem('mi_cache_buster');

  if (typeof window.clearDataCache === 'function') {
    window.clearDataCache().finally(() => window.location.reload());
  } else {
    window.location.reload();
  }
};
