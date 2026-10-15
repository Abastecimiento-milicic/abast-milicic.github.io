/**
 * cache-utils.js — Shared IndexedDB caching utility.
 * 
 * Stores fetched text responses in IndexedDB so that navigating
 * between tabs (separate HTML pages) does not re-download the same
 * CSV/JSON data files.
 * 
 * The cache key is the full URL (including the CACHE_BUSTER query param
 * generated per session in last-update.js).  A new browser session
 * produces a new CACHE_BUSTER → old entries are ignored automatically.
 *
 * Usage:
 *   fetchWithCache(url)          → Promise<string>  (response text)
 *   clearDataCache()             → Promise<void>    (wipe all entries)
 */

(function () {
  const DB_NAME = "appDataCache";
  const DB_VERSION = 1;
  const STORE_NAME = "responses";

  /** Open (or create) the database once and reuse the handle. */
  let _dbPromise = null;
  function openDB() {
    if (_dbPromise) return _dbPromise;
    _dbPromise = new Promise((resolve, reject) => {
      const req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onupgradeneeded = (e) => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains(STORE_NAME)) {
          db.createObjectStore(STORE_NAME, { keyPath: "url" });
        }
      };
      req.onsuccess = (e) => resolve(e.target.result);
      req.onerror = (e) => {
        console.warn("[cache-utils] IndexedDB open failed, caching disabled.", e.target.error);
        _dbPromise = null;
        reject(e.target.error);
      };
    });
    return _dbPromise;
  }

  /**
   * Fetch a URL with IndexedDB caching.
   * Returns a Promise that resolves to the response **text**.
   * On cache hit the network is skipped entirely.
   */
  window.fetchWithCache = async function fetchWithCache(url) {
    try {
      const db = await openDB();
      const tx = db.transaction(STORE_NAME, "readonly");
      const store = tx.objectStore(STORE_NAME);

      const cached = await new Promise((resolve) => {
        const getReq = store.get(url);
        getReq.onsuccess = (e) => resolve(e.target.result);
        getReq.onerror = () => resolve(null);
      });

      if (cached && cached.data) {
        return cached.data;
      }
    } catch (_) {
      // IndexedDB unavailable — fall through to network
    }

    // Network fetch
    const resp = await fetch(url);
    if (!resp.ok) throw new Error(`No pude abrir ${url} (HTTP ${resp.status})`);
    const data = await resp.text();

    // Store in cache (fire-and-forget)
    try {
      const db = await openDB();
      const tx = db.transaction(STORE_NAME, "readwrite");
      const store = tx.objectStore(STORE_NAME);
      store.put({ url, data });
    } catch (_) {
      // silently ignore cache-write errors
    }

    return data;
  };

  /** Get raw or structured data by key */
  window.getCachedData = async function getCachedData(key) {
    try {
      const db = await openDB();
      const tx = db.transaction(STORE_NAME, "readonly");
      const store = tx.objectStore(STORE_NAME);
      const cached = await new Promise((resolve) => {
        const getReq = store.get(key);
        getReq.onsuccess = (e) => resolve(e.target.result);
        getReq.onerror = () => resolve(null);
      });
      return cached ? cached.data : null;
    } catch (_) {
      return null;
    }
  };

  /** Set raw or structured data by key */
  window.setCachedData = async function setCachedData(key, data) {
    try {
      const db = await openDB();
      const tx = db.transaction(STORE_NAME, "readwrite");
      const store = tx.objectStore(STORE_NAME);
      store.put({ url: key, data: data });
    } catch (_) {
      // ignore
    }
  };

  /**
   * Wipe all cached entries.  Called by forceRefreshData() in last-update.js.
   */
  window.clearDataCache = async function clearDataCache() {
    try {
      const db = await openDB();
      const tx = db.transaction(STORE_NAME, "readwrite");
      tx.objectStore(STORE_NAME).clear();
    } catch (_) {
      // ignore
    }
  };

  /**
   * Universal ExcelJS download helper.
   */
  window.saveAsExcel = async function(filename, sheetName, headers, rows, colKeys = null) {
    if (typeof ExcelJS === 'undefined') {
      alert("Error: No se pudo cargar la librería ExcelJS. Por favor refresque la página.");
      return;
    }
    try {
      const workbook = new ExcelJS.Workbook();
      const safeSheetName = sheetName.replace(/[^a-zA-Z0-9 ]/g, '').substring(0, 31) || "Datos";
      const worksheet = workbook.addWorksheet(safeSheetName);

      const caractIdx = headers.findIndex(h => /Caract\.planif\.nec/i.test(h || ''));
      const planifIdx = headers.findIndex(h => /^Planificado$/i.test(h || ''));

      const defaultHeaderFill = {
        type: 'pattern',
        pattern: 'solid',
        fgColor: { argb: 'FF1B365D' } // Navy corporativo
      };
      const caractHeaderFill = {
        type: 'pattern',
        pattern: 'solid',
        fgColor: { argb: 'FF0284C7' } // Azul cielo destacado
      };
      const planifHeaderFill = {
        type: 'pattern',
        pattern: 'solid',
        fgColor: { argb: 'FF047857' } // Verde esmeralda
      };
      const headerFont = {
        name: 'Segoe UI',
        size: 11,
        bold: true,
        color: { argb: 'FFFFFFFF' }
      };

      const headerRowObj = worksheet.addRow(headers);
      headerRowObj.height = 28;
      
      for (let colIdx = 1; colIdx <= headers.length; colIdx++) {
        const cell = headerRowObj.getCell(colIdx);
        if (colIdx - 1 === caractIdx) {
          cell.fill = caractHeaderFill;
        } else if (colIdx - 1 === planifIdx) {
          cell.fill = planifHeaderFill;
        } else {
          cell.fill = defaultHeaderFill;
        }
        cell.font = headerFont;
        cell.alignment = { vertical: 'middle', horizontal: 'center', wrapText: true };
        cell.border = {
          left: { style: 'thin', color: { argb: 'FFCBD5E1' } },
          right: { style: 'thin', color: { argb: 'FFCBD5E1' } },
          top: { style: 'medium', color: { argb: 'FF0F172A' } },
          bottom: { style: 'medium', color: { argb: 'FF0F172A' } }
        };
      }

      rows.forEach((r, rowIdx) => {
        let rowData;
        if (colKeys && Array.isArray(colKeys)) {
          rowData = colKeys.map(k => {
            const v = r[k];
            return (v === null || v === undefined) ? "" : v;
          });
        } else if (Array.isArray(r)) {
          rowData = r.map(v => (v === null || v === undefined) ? "" : v);
        } else {
          rowData = headers.map(h => {
            const v = r[h];
            return (v === null || v === undefined) ? "" : v;
          });
        }
        
        const rowObj = worksheet.addRow(rowData);
        rowObj.height = 20;
        const isOdd = rowIdx % 2 === 1;
        const baseRowBg = isOdd ? 'FFF8FAFC' : 'FFFFFFFF';
        
        for (let colIdx = 1; colIdx <= headers.length; colIdx++) {
          const cell = rowObj.getCell(colIdx);
          cell.font = { name: 'Segoe UI', size: 10, color: { argb: 'FF1F2937' } };
          cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: baseRowBg } };
          cell.border = {
            left: { style: 'thin', color: { argb: 'FFE2E8F0' } },
            right: { style: 'thin', color: { argb: 'FFE2E8F0' } },
            top: { style: 'thin', color: { argb: 'FFE2E8F0' } },
            bottom: { style: 'thin', color: { argb: 'FFE2E8F0' } }
          };
          cell.alignment = { vertical: 'middle', horizontal: 'left' };
          const hName = headers[colIdx - 1] || "";
          if (/^(Centro|Almacén|Planificado|Caract\.planif\.nec|Unidad medida base|Moneda|Tipo material)$/i.test(hName.trim())) {
            cell.alignment = { vertical: 'middle', horizontal: 'center' };
          }
          
          const rawVal = rowData[colIdx - 1];
          if (rawVal !== "" && !isNaN(rawVal) && typeof rawVal !== 'boolean') {
            const num = Number(rawVal);
            cell.value = num;
            cell.alignment = { vertical: 'middle', horizontal: 'right' };
            if (Number.isInteger(num)) {
              cell.numFmt = '#,##0';
            } else {
              cell.numFmt = '#,##0.00';
            }
          }

          // Resaltado de color en Caract.planif.nec.
          if (colIdx - 1 === caractIdx) {
            const vStr = String(rawVal || '').trim().toUpperCase();
            if (vStr && !['NO PLANIFICADO', 'ND', '-', 'SIN PLANIFICAR'].includes(vStr)) {
              cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFDCFCE7' } };
              cell.font = { name: 'Segoe UI', size: 10, bold: true, color: { argb: 'FF166534' } };
            } else {
              cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFFEE2E2' } };
              cell.font = { name: 'Segoe UI', size: 10, bold: true, color: { argb: 'FF991B1B' } };
            }
            cell.alignment = { vertical: 'middle', horizontal: 'center' };
          }
          // Resaltado de color en Planificado
          else if (colIdx - 1 === planifIdx) {
            const vStr = String(rawVal || '').trim().toUpperCase();
            if (['SÍ', 'SI', 'YES', '1'].includes(vStr)) {
              cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFDCFCE7' } };
              cell.font = { name: 'Segoe UI', size: 10, bold: true, color: { argb: 'FF166534' } };
            } else {
              cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFFEE2E2' } };
              cell.font = { name: 'Segoe UI', size: 10, bold: true, color: { argb: 'FF991B1B' } };
            }
            cell.alignment = { vertical: 'middle', horizontal: 'center' };
          }
        }
      });

      worksheet.views = [{ state: 'frozen', ySplit: 1 }];
      if (rows.length > 0) {
        worksheet.autoFilter = { from: { row: 1, column: 1 }, to: { row: rows.length + 1, column: headers.length } };
      }

      worksheet.columns.forEach(col => {
        let maxLen = 10;
        col.eachCell({ includeHeader: true }, cell => {
          const val = cell.value;
          if (val) {
            const len = val.toString().length;
            if (len > maxLen) maxLen = len;
          }
        });
        col.width = Math.min(maxLen + 4, 45);
      });

      const buffer = await workbook.xlsx.writeBuffer();
      const blob = new Blob([buffer], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
      const link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);
      const outputName = filename.endsWith('.xlsx') ? filename : filename.replace(/\.[^/.]+$/, "") + ".xlsx";
      link.download = outputName;
      link.click();
    } catch (err) {
      console.error("[saveAsExcel] Error generating excel file:", err);
      alert("Error al generar el archivo Excel: " + err.message);
    }
  };
})();
