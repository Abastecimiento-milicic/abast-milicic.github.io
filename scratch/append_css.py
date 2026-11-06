import sys
sys.stdout.reconfigure(encoding='utf-8')

css_to_append = """
/* ==========================================================================
   FILTROS INTERACTIVOS TIPO PROTOTIPO (Pills & Switch) EN PANEL RESUMEN
   ========================================================================== */
#panel-resumen .filter-search-input {
  width: 100%;
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  background: #ffffff;
  font-size: 0.78rem;
  color: #1e293b;
  outline: none;
  transition: all 0.15s ease;
  margin-bottom: 6px;
  box-sizing: border-box;
}

#panel-resumen .filter-search-input:focus {
  border-color: #0f766e;
  box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.12);
}

#panel-resumen .pills-container {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  max-height: 125px;
  overflow-y: auto;
  padding: 2px 1px;
}

#panel-resumen .filter-pill {
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  color: #475569;
  font-size: 0.72rem;
  padding: 3px 8px;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.15s ease;
  user-select: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  white-space: nowrap;
}

#panel-resumen .filter-pill:hover {
  border-color: #cbd5e1;
  color: #0f172a;
  background: #e2e8f0;
}

#panel-resumen .filter-pill.active {
  background: #0f766e;
  color: #ffffff;
  border-color: #0f766e;
  font-weight: 600;
  box-shadow: 0 1px 3px rgba(15, 118, 110, 0.25);
}

#panel-resumen .toggle-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  margin-top: 10px;
}

#panel-resumen .toggle-info {
  display: flex;
  flex-direction: column;
}

#panel-resumen .toggle-title {
  font-size: 0.78rem;
  font-weight: 700;
  color: #1e293b;
}

#panel-resumen .toggle-desc {
  font-size: 0.68rem;
  color: #64748b;
}

#panel-resumen .switch-ui {
  position: relative;
  width: 36px;
  height: 20px;
  background: #cbd5e1;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

#panel-resumen .switch-ui.active {
  background: #0f766e;
}

#panel-resumen .switch-ui::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 16px;
  height: 16px;
  background: #ffffff;
  border-radius: 50%;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 2px rgba(0,0,0,0.2);
}

#panel-resumen .switch-ui.active::after {
  transform: translateX(16px);
}

/* ==========================================================================
   REDIDENIO PANEL DE SERVICIOS (Estilo Moderno SaaS / Verde Mate)
   ========================================================================== */
#panel-servicios .serv-notice-banner {
  background: #f0fdfa;
  border: 1px solid #ccfbf1;
  border-radius: 8px;
  padding: 10px 14px;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(15, 118, 110, 0.05);
}

#panel-servicios .serv-notice-icon {
  color: #0f766e;
  flex-shrink: 0;
  margin-top: 1px;
}

#panel-servicios .serv-notice-text {
  font-size: 0.82rem;
  line-height: 1.45;
  color: #134e4a;
}

#panel-servicios .serv-notice-text strong {
  color: #0f766e;
  font-weight: 700;
}

#panel-servicios .serv-kpi-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

#panel-servicios .serv-kpi-inner {
  display: flex;
  flex-direction: column;
  gap: 2px;
  text-align: center;
}

#panel-servicios .serv-kpi-label {
  font-size: 0.68rem;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

#panel-servicios .serv-kpi-value {
  font-size: 1.4rem;
  font-weight: 800;
  color: #0f766e;
  font-family: var(--font-mono, monospace);
  line-height: 1.1;
}

#panel-servicios .btn-serv-download {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 100%;
  padding: 8px 12px;
  font-size: 0.82rem;
  font-weight: 600;
  background: #0f766e;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
  box-shadow: 0 1px 2px rgba(15, 118, 110, 0.2);
}

#panel-servicios .btn-serv-download:hover {
  background: #0d9488;
  box-shadow: 0 2px 4px rgba(15, 118, 110, 0.3);
}

#panel-servicios .serv-table-panel {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}

#panel-servicios .serv-table-panel .panel-title {
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  padding: 12px 18px;
  font-size: 0.88rem;
  font-weight: 700;
  color: #0f172a;
}

#panel-servicios .serv-resumen-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 0.82rem;
}

#panel-servicios .serv-resumen-table thead th {
  background: #f8fafc !important;
  color: #475569 !important;
  font-weight: 700 !important;
  font-size: 0.72rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.04em !important;
  padding: 10px 14px !important;
  border-bottom: 1px solid #e2e8f0 !important;
  white-space: nowrap;
}

#panel-servicios .serv-resumen-table tbody td {
  padding: 9px 14px !important;
  border-bottom: 1px solid #f1f5f9 !important;
  color: #334155 !important;
  vertical-align: middle !important;
}

#panel-servicios .serv-resumen-table tbody tr:hover {
  background-color: #f8fafc !important;
}

#panel-servicios .badge-item-status {
  display: inline-flex;
  align-items: center;
  padding: 3px 8px;
  border-radius: 9999px;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}

#panel-servicios .badge-serv-status {
  display: inline-flex;
  align-items: center;
  padding: 3px 8px;
  border-radius: 9999px;
  font-size: 0.74rem;
  font-weight: 600;
}

#panel-servicios .badge-item-verde { background-color: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }
#panel-servicios .badge-item-rojo { background-color: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
#panel-servicios .badge-item-azul { background-color: #f0fdfa; color: #0f766e; border: 1px solid #ccfbf1; }

#panel-servicios .badge-serv-verde { background-color: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }
#panel-servicios .badge-serv-amarillo { background-color: #fffbeb; color: #b45309; border: 1px solid #fde68a; }
#panel-servicios .badge-serv-naranja { background-color: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; }
#panel-servicios .badge-serv-rojo { background-color: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
#panel-servicios .badge-serv-morado { background-color: #faf5ff; color: #7e22ce; border: 1px solid #e9d5ff; }
#panel-servicios .badge-serv-gris { background-color: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }

#panel-servicios .btn-table-download {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 4px 10px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #0f766e;
  background-color: #f0fdfa;
  border: 1px solid #ccfbf1;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
}

#panel-servicios .btn-table-download:hover {
  background-color: #0f766e;
  color: #ffffff;
  border-color: #0f766e;
}
"""

with open('css/base.css', 'a', encoding='utf-8') as f:
    f.write(css_to_append)

print("CSS appended to css/base.css successfully")
