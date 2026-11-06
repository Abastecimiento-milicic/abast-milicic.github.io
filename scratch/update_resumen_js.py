import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('js/resumen.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update renderObrasSelect
old_render_obras = '''    sel.onchange = () => updateResumen();

    if (typeof window.syncAllStMultiSelects === "function") {
      window.syncAllStMultiSelects();
    }
  }'''

new_render_obras = '''    sel.onchange = () => updateResumen();

    const pillsCont = document.getElementById("obraPillsContainer");
    if (pillsCont) {
      const isAllSelected = !prevSelected.length || prevSelected.includes("__ALL__");
      let pillsHtml = `<span class="filter-pill ${isAllSelected ? 'active' : ''}" data-val="__ALL__" onclick="window.selectResumenObraPill(this, '__ALL__')">Todas las Obras</span>`;
      sortedCodes.forEach(code => {
        const isSel = prevSelected.includes(code);
        const label = OBRA_MAP[code] || `Obra ${code}`;
        pillsHtml += `<span class="filter-pill ${isSel ? 'active' : ''}" data-val="${code}" onclick="window.selectResumenObraPill(this, '${code}')">${label}</span>`;
      });
      pillsCont.innerHTML = pillsHtml;
    }

    if (typeof window.syncAllStMultiSelects === "function") {
      window.syncAllStMultiSelects();
    }
  }'''

# 2. Update renderAniosSelect
old_render_anios = '''    sel.onchange = () => {
      renderMesesCumplSelect(true);
      updateCumplimientoBlock();
      updateDemorasBlock();
      updateTiemposBlock();
    };

    if (typeof window.syncAllStMultiSelects === "function") {
      window.syncAllStMultiSelects();
    }
  }'''

new_render_anios = '''    sel.onchange = () => {
      renderMesesCumplSelect(true);
      updateCumplimientoBlock();
      updateDemorasBlock();
      updateTiemposBlock();
    };

    const pillsCont = document.getElementById("anioPillsContainer");
    if (pillsCont) {
      const isAllSelected = !prevSelected.length || prevSelected.includes("__ALL__");
      let pillsHtml = `<span class="filter-pill ${isAllSelected ? 'active' : ''}" data-val="__ALL__" onclick="window.selectResumenAnioPill(this, '__ALL__')">Todos</span>`;
      sortedYears.forEach(year => {
        const isSel = prevSelected.includes(year);
        pillsHtml += `<span class="filter-pill ${isSel ? 'active' : ''}" data-val="${year}" onclick="window.selectResumenAnioPill(this, '${year}')">${year}</span>`;
      });
      pillsCont.innerHTML = pillsHtml;
    }

    if (typeof window.syncAllStMultiSelects === "function") {
      window.syncAllStMultiSelects();
    }
  }'''

# 3. Update renderMesesCumplSelect
old_render_meses = '''    sel.onchange = () => { updateCumplimientoBlock(); updateDemorasBlock(); updateTiemposBlock(); };

    if (typeof window.syncAllStMultiSelects === "function") {
      window.syncAllStMultiSelects();
    }
  }'''

new_render_meses = '''    sel.onchange = () => { updateCumplimientoBlock(); updateDemorasBlock(); updateTiemposBlock(); };

    const pillsCont = document.getElementById("mesPillsContainer");
    if (pillsCont) {
      const isAllSelected = !hasSelection;
      let pillsHtml = `<span class="filter-pill ${isAllSelected ? 'active' : ''}" data-val="__ALL__" onclick="window.selectResumenMesPill(this, '__ALL__')">Todos</span>`;
      [...sortedYM].reverse().forEach(ym => {
        const [year, month] = ym.split("-");
        const nombreMes = MES_NOMBRES[month] || month;
        const isSel = prevSelected.includes(ym);
        pillsHtml += `<span class="filter-pill ${isSel ? 'active' : ''}" data-val="${ym}" onclick="window.selectResumenMesPill(this, '${ym}')">${nombreMes} ${year}</span>`;
      });
      pillsCont.innerHTML = pillsHtml;
    }

    if (typeof window.syncAllStMultiSelects === "function") {
      window.syncAllStMultiSelects();
    }
  }'''

# 4. Update renderGcEmrfSelect
old_render_gc = '''    sel.onchange = () => {
      updateEmrfBlock();
    };

    if (typeof window.syncAllStMultiSelects === "function") {
      window.syncAllStMultiSelects();
    }
  }'''

new_render_gc = '''    sel.onchange = () => {
      updateEmrfBlock();
    };

    const pillsCont = document.getElementById("gcEmrfPillsContainer");
    if (pillsCont) {
      let pillsHtml = `<span class="filter-pill ${hadAllSelected ? 'active' : ''}" data-val="__ALL__" onclick="window.selectResumenGcPill(this, '__ALL__')">Todos</span>`;
      orderedGcs.forEach(gc => {
        const isSel = !hadAllSelected && prevSelected.includes(gc);
        pillsHtml += `<span class="filter-pill ${isSel ? 'active' : ''}" data-val="${gc}" onclick="window.selectResumenGcPill(this, '${gc}')">${gc}</span>`;
      });
      pillsCont.innerHTML = pillsHtml;
    }

    if (typeof window.syncAllStMultiSelects === "function") {
      window.syncAllStMultiSelects();
    }
  }'''

# 5. Update setResumenArribaMode & hookClearButton
old_arriba_block = '''  function setResumenArribaMode(active) {
    isResumenArribaActive = !!active;
    const btn = document.getElementById("resumen_btnArriba");
    if (btn) {
      if (isResumenArribaActive) {
        btn.classList.add("btn-active");
        btn.innerHTML = "↩ Volver a cumplimiento estándar";
      } else {
        btn.classList.remove("btn-active");
        btn.innerHTML = "🏔️ Medir cumplimiento arriba";
      }
    }

    updateCumplimientoBlock();
    updateTiemposBlock();
  }'''

new_arriba_block = '''  function setResumenArribaMode(active) {
    isResumenArribaActive = !!active;
    const btn = document.getElementById("resumen_btnArriba");
    if (btn) {
      if (isResumenArribaActive) {
        btn.classList.add("btn-active");
        btn.innerHTML = "↩ Volver a cumplimiento estándar";
      } else {
        btn.classList.remove("btn-active");
        btn.innerHTML = "🏔️ Medir cumplimiento arriba";
      }
    }
    const sw = document.getElementById("switchArriba");
    if (sw) {
      sw.classList.toggle("active", isResumenArribaActive);
    }

    updateCumplimientoBlock();
    updateTiemposBlock();
  }

  /* ==========================================================================
     MÉTODOS PÚBLICOS DE PASTILLAS Y FILTROS INTERACTIVOS TIPO PROTOTIPO
     ========================================================================== */
  window.selectResumenObraPill = function(el, code) {
    const sel = document.getElementById("resumen_obraSelect");
    if (!sel) return;
    const pillsCont = document.getElementById("obraPillsContainer");

    if (code === "__ALL__") {
      if (pillsCont) {
        pillsCont.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("active"));
      }
      el.classList.add("active");
      [...sel.options].forEach((o, idx) => {
        o.selected = (o.value === "__ALL__" || idx === 0);
      });
    } else {
      const allPill = pillsCont ? pillsCont.querySelector('[data-val="__ALL__"]') : null;
      if (allPill) allPill.classList.remove("active");

      if (pillsCont) {
        pillsCont.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("active"));
      }
      el.classList.add("active");

      [...sel.options].forEach(o => {
        o.selected = (o.value === code);
      });
    }
    updateResumen();
  };

  window.filterResumenObraPills = function(query) {
    const text = (query || "").toLowerCase().trim();
    const pills = document.querySelectorAll("#obraPillsContainer .filter-pill");
    pills.forEach(pill => {
      const val = pill.getAttribute("data-val");
      if (val === "__ALL__" || pill.textContent.toLowerCase().includes(text)) {
        pill.style.display = "inline-flex";
      } else {
        pill.style.display = "none";
      }
    });
  };

  window.selectResumenAnioPill = function(el, year) {
    const sel = document.getElementById("resumen_anioSelect");
    if (!sel) return;
    const pillsCont = document.getElementById("anioPillsContainer");
    if (pillsCont) {
      pillsCont.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("active"));
    }
    el.classList.add("active");
    [...sel.options].forEach(o => {
      o.selected = (year === "__ALL__" ? (o.value === "__ALL__") : (o.value === year));
    });
    renderMesesCumplSelect(true);
    updateCumplimientoBlock();
    updateDemorasBlock();
    updateTiemposBlock();
  };

  window.selectResumenMesPill = function(el, ym) {
    const sel = document.getElementById("resumen_mesCumplSelect");
    if (!sel) return;
    const pillsCont = document.getElementById("mesPillsContainer");
    if (pillsCont) {
      pillsCont.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("active"));
    }
    el.classList.add("active");
    [...sel.options].forEach(o => {
      o.selected = (ym === "__ALL__" ? (o.value === "__ALL__") : (o.value === ym));
    });
    updateCumplimientoBlock();
    updateDemorasBlock();
    updateTiemposBlock();
  };

  window.selectResumenGcPill = function(el, gc) {
    const sel = document.getElementById("resumen_gcEmrfSelect");
    if (!sel) return;
    const pillsCont = document.getElementById("gcEmrfPillsContainer");
    if (gc === "__ALL__") {
      if (pillsCont) {
        pillsCont.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("active"));
      }
      el.classList.add("active");
      [...sel.options].forEach((o, i) => o.selected = (i === 0 || o.value === "__ALL__"));
    } else {
      const allPill = pillsCont ? pillsCont.querySelector('[data-val="__ALL__"]') : null;
      if (allPill) allPill.classList.remove("active");
      el.classList.toggle("active");
      const activeVals = Array.from(pillsCont.querySelectorAll(".filter-pill.active")).map(p => p.getAttribute("data-val"));
      if (!activeVals.length) {
        if (allPill) allPill.classList.add("active");
        [...sel.options].forEach((o, i) => o.selected = (i === 0));
      } else {
        [...sel.options].forEach(o => {
          o.selected = activeVals.includes(o.value);
        });
      }
    }
    updateEmrfBlock();
  };

  window.toggleResumenArribaSwitch = function() {
    setResumenArribaMode(!isResumenArribaActive);
  };

  window.toggleResumenExcludeObra = function() {
    setObraExcludeMode(!isObraExcludeMode);
    updateResumen();
  };'''

# 6. Update hookClearButton to also reset pill classes
old_clear_btn = '''      if (typeof window.syncAllStMultiSelects === "function") {
        setTimeout(() => window.syncAllStMultiSelects(), 30);
      }
    };
  }'''

new_clear_btn = '''      // Resetear clases activas de las pastillas interactivas
      const obraPills = document.querySelectorAll("#obraPillsContainer .filter-pill");
      obraPills.forEach((p, idx) => {
        if (p.getAttribute("data-val") === "__ALL__" || idx === 0) p.classList.add("active");
        else p.classList.remove("active");
        p.style.display = "inline-flex";
      });
      const qInput = document.getElementById("resumen_obraQuickSearch");
      if (qInput) qInput.value = "";

      const anioPills = document.querySelectorAll("#anioPillsContainer .filter-pill");
      anioPills.forEach((p, idx) => {
        if (p.getAttribute("data-val") === "__ALL__" || idx === 0) p.classList.add("active");
        else p.classList.remove("active");
      });

      const mesPills = document.querySelectorAll("#mesPillsContainer .filter-pill");
      mesPills.forEach((p, idx) => {
        if (p.getAttribute("data-val") === "__ALL__" || idx === 0) p.classList.add("active");
        else p.classList.remove("active");
      });

      const gcPills = document.querySelectorAll("#gcEmrfPillsContainer .filter-pill");
      gcPills.forEach(p => {
        const v = p.getAttribute("data-val");
        p.classList.toggle("active", DEFAULT_EMRF_GCS.includes(v));
      });

      const sw = document.getElementById("switchArriba");
      if (sw) sw.classList.remove("active");

      if (typeof window.syncAllStMultiSelects === "function") {
        setTimeout(() => window.syncAllStMultiSelects(), 30);
      }
    };
  }'''

def norm(t): return t.replace('\r\n', '\n')

code_norm = norm(code)
items = [
    ("renderObrasSelect", norm(old_render_obras), norm(new_render_obras)),
    ("renderAniosSelect", norm(old_render_anios), norm(new_render_anios)),
    ("renderMesesCumplSelect", norm(old_render_meses), norm(new_render_meses)),
    ("renderGcEmrfSelect", norm(old_render_gc), norm(new_render_gc)),
    ("arribaBlock", norm(old_arriba_block), norm(new_arriba_block)),
    ("clearButton", norm(old_clear_btn), norm(new_clear_btn))
]

for name, o, n in items:
    if o in code_norm:
        code_norm = code_norm.replace(o, n, 1)
        print(f"Updated {name} successfully")
    else:
        print(f"FAILED to find {name}!")

with open('js/resumen.js', 'w', encoding='utf-8') as f:
    f.write(code_norm)

print("js/resumen.js updated successfully")
