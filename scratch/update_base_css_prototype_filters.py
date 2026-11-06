import sys
sys.stdout.reconfigure(encoding='utf-8')

css_rules = """
/* ==========================================================================
   ESTILOS UNIVERSALES DE FILTROS TIPO PROTOTIPO (Pills, Buscador, Switch, Headers)
   ========================================================================== */
.st-sidebar, .app-sidebar {
  background: #ffffff !important;
  border-right: 1px solid #e2e8f0 !important;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
}

.st-sidebar .sidebar-header,
.app-sidebar .sidebar-header {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  padding-bottom: 8px !important;
  border-bottom: 1px solid #e2e8f0 !important;
  margin-bottom: 12px !important;
}

.st-sidebar .sidebar-title,
.app-sidebar .sidebar-title {
  font-size: 0.85rem !important;
  font-weight: 700 !important;
  color: #1e293b !important;
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
}

.st-sidebar .sidebar-reset-btn,
.app-sidebar .sidebar-reset-btn {
  background: none !important;
  border: none !important;
  color: #0f766e !important;
  font-size: 0.72rem !important;
  font-weight: 700 !important;
  cursor: pointer !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 4px !important;
  padding: 2px 4px !important;
  text-decoration: none !important;
  transition: opacity 0.15s ease !important;
}

.st-sidebar .sidebar-reset-btn:hover,
.app-sidebar .sidebar-reset-btn:hover {
  text-decoration: underline !important;
  opacity: 0.85 !important;
}

.st-sidebar .filter,
.st-sidebar .filter-group,
.app-sidebar .filter,
.app-sidebar .filter-group {
  display: flex !important;
  flex-direction: column !important;
  gap: 4px !important;
  margin-bottom: 12px !important;
}

.st-sidebar .filter label,
.st-sidebar .filter-label,
.app-sidebar .filter label,
.app-sidebar .filter-label {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  font-size: 0.72rem !important;
  font-weight: 700 !important;
  color: #475569 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.03em !important;
  margin-bottom: 4px !important;
  background: transparent !important;
  padding: 0 !important;
  border-radius: 0 !important;
}

.proto-pills-filter-wrap {
  display: flex;
  flex-direction: column;
  gap: 5px;
  width: 100%;
}

.filter-search-input {
  width: 100% !important;
  padding: 6px 10px !important;
  border-radius: 6px !important;
  border: 1px solid #cbd5e1 !important;
  background: #ffffff !important;
  font-size: 0.78rem !important;
  color: #1e293b !important;
  outline: none !important;
  transition: all 0.15s ease !important;
  margin-bottom: 4px !important;
  box-sizing: border-box !important;
}

.filter-search-input:focus {
  border-color: #0f766e !important;
  box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.12) !important;
}

.pills-container {
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 4px !important;
  max-height: 125px !important;
  overflow-y: auto !important;
  padding: 2px 1px !important;
  width: 100% !important;
}

.filter-pill {
  background: #f1f5f9 !important;
  border: 1px solid #e2e8f0 !important;
  color: #475569 !important;
  font-size: 0.72rem !important;
  padding: 3px 8px !important;
  border-radius: 9999px !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
  user-select: none !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 4px !important;
  white-space: nowrap !important;
  line-height: 1.3 !important;
  font-family: inherit !important;
}

.filter-pill:hover {
  border-color: #cbd5e1 !important;
  color: #0f172a !important;
  background: #e2e8f0 !important;
}

.filter-pill.active {
  background: #0f766e !important;
  color: #ffffff !important;
  border-color: #0f766e !important;
  font-weight: 600 !important;
  box-shadow: 0 1px 3px rgba(15, 118, 110, 0.25) !important;
}

.proto-select-hidden {
  display: none !important;
}

.st-sidebar .toggle-row,
.app-sidebar .toggle-row {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  padding: 8px 10px !important;
  background: #f8fafc !important;
  border-radius: 8px !important;
  border: 1px solid #e2e8f0 !important;
  margin-top: 8px !important;
  width: 100% !important;
  box-sizing: border-box !important;
}

.st-sidebar .toggle-info,
.app-sidebar .toggle-info {
  display: flex !important;
  flex-direction: column !important;
}

.st-sidebar .toggle-title,
.app-sidebar .toggle-title {
  font-size: 0.78rem !important;
  font-weight: 700 !important;
  color: #1e293b !important;
}

.st-sidebar .toggle-desc,
.app-sidebar .toggle-desc {
  font-size: 0.68rem !important;
  color: #64748b !important;
}

.st-sidebar .switch-ui,
.app-sidebar .switch-ui {
  position: relative !important;
  width: 36px !important;
  height: 20px !important;
  background: #cbd5e1 !important;
  border-radius: 9999px !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
  flex-shrink: 0 !important;
}

.st-sidebar .switch-ui.active,
.app-sidebar .switch-ui.active {
  background: #0f766e !important;
}

.st-sidebar .switch-ui::after,
.app-sidebar .switch-ui::after {
  content: '' !important;
  position: absolute !important;
  top: 2px !important;
  left: 2px !important;
  width: 16px !important;
  height: 16px !important;
  background: #ffffff !important;
  border-radius: 50% !important;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
  box-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
}

.st-sidebar .switch-ui.active::after,
.app-sidebar .switch-ui.active::after {
  transform: translateX(16px) !important;
}

/* Ocultar el dropdown antiguo para dar paso a las pastillas del prototipo */
.st-ms-container {
  display: none !important;
}
"""

with open('css/base.css', 'a', encoding='utf-8') as f:
    f.write(css_rules)

print("Appended universal prototype filter styles to css/base.css")
