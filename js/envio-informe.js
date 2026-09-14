document.addEventListener('DOMContentLoaded', () => {
    const tabEnvio = document.getElementById('tab-envio');
    
    // Mapeo de selectores entre la pestaña de envío y la de cumplimiento
    const selectIds = [
        { envio: 'envio_clienteSelect', cumpl: 'cumpl_clienteSelect' },
        { envio: 'envio_clasif2Select', cumpl: 'cumpl_clasif2Select' },
        { envio: 'envio_gcocSelect', cumpl: 'cumpl_gcocSelect' },
        { envio: 'envio_mesSelect', cumpl: 'cumpl_mesSelect' },
        { envio: 'envio_centroSelect', cumpl: 'centroSelect' }
    ];

    // Sincronizar opciones cuando se cambia a la pestaña de envío
    document.addEventListener('click', (e) => {
        if (e.target.id === 'tab-envio') {
            selectIds.forEach(pair => {
                const elEnvio = document.getElementById(pair.envio);
                const elCumpl = document.getElementById(pair.cumpl);
                
                if (elEnvio && elCumpl) {
                    // Limpiar y clonar opciones
                    elEnvio.innerHTML = '';
                    Array.from(elCumpl.options).forEach(opt => {
                        const newOpt = document.createElement('option');
                        newOpt.value = opt.value;
                        newOpt.textContent = opt.textContent;
                        newOpt.selected = opt.selected;
                        elEnvio.appendChild(newOpt);
                    });
                }
            });
        }
    });

    // También sincronizar si el usuario cambia el filtro aquí, pero al revés: aplicar a cumplimiento
    function applyFiltersToCumplimiento() {
        selectIds.forEach(pair => {
            const elEnvio = document.getElementById(pair.envio);
            const elCumpl = document.getElementById(pair.cumpl);
            
            if (elEnvio && elCumpl) {
                const selectedValues = Array.from(elEnvio.selectedOptions).map(o => o.value);
                Array.from(elCumpl.options).forEach(opt => {
                    opt.selected = selectedValues.includes(opt.value);
                });
                
                // Disparar evento change para que se actualicen los gráficos de Cumplimiento
                const event = new Event('change', { bubbles: true });
                elCumpl.dispatchEvent(event);
            }
        });
    }

    const btnPreview = document.getElementById('envio_btnPreview');
    if (btnPreview) {
        btnPreview.addEventListener('click', () => {
            applyFiltersToCumplimiento();
            // Cambiar a la pestaña de cumplimiento
            if (window.switchTab) window.switchTab('cumplimiento');
        });
    }

    const btnGenerate = document.getElementById('envio_btnGenerate');
    if (btnGenerate) {
        btnGenerate.addEventListener('click', async () => {
            applyFiltersToCumplimiento();
            
            // Cambiar a la pestaña de cumplimiento para que html2pdf la pueda capturar
            if (window.switchTab) window.switchTab('cumplimiento');
            
            // Esperar a que se actualicen los gráficos e interfaz
            await new Promise(resolve => setTimeout(resolve, 800));
            
            const element = document.getElementById('panel-cumplimiento');
            const emailTo = document.getElementById('envio_emailTo').value || 'ventas@milicic.com';
            
            // Configurar html2pdf
            // Formato A3 Vertical (Portrait)
            const opt = {
                margin:       [15, 10, 15, 10], // Margen arriba, derecha, abajo, izquierda
                filename:     'Informe_Cumplimiento.pdf',
                image:        { type: 'jpeg', quality: 0.98 },
                html2canvas:  { scale: 2, useCORS: true },
                jsPDF:        { unit: 'mm', format: 'a3', orientation: 'portrait' }
            };

            const originalBtnText = btnGenerate.innerHTML;
            btnGenerate.innerHTML = '⏳ Generando PDF...';
            btnGenerate.disabled = true;

            // Elementos a ocultar/modificar temporalmente
            const loader = document.getElementById('cumpl_loader');
            const panelFiltrosBody = element.querySelector('.panel-body.filters');
            const btnClear = document.getElementById('cumpl_btnClearFilters');
            const helpBtns = element.querySelectorAll('.help-btn');
            
            // Forzar un ancho fijo de 1000px. Al ser Portrait, html2pdf escalará estos 1000px 
            // al ancho del A3, reduciendo proporcionalmente la altura, logrando que entre en 1 hoja.
            const originalWidth = element.style.width;
            const originalMaxWidth = element.style.maxWidth;
            element.style.width = '1000px';
            element.style.maxWidth = '1000px';
            
            let summaryDiv = null;

            try {
                // Forzar un estilo temporal para la impresión
                if (loader) loader.style.display = 'none';
                if (panelFiltrosBody) panelFiltrosBody.style.display = 'none';
                if (btnClear) btnClear.style.display = 'none';
                helpBtns.forEach(btn => btn.style.display = 'none');

                // Crear un resumen de los filtros aplicados
                const panelFiltrosTitle = element.querySelector('.panel-title');
                if (panelFiltrosTitle) {
                    const getSelectedText = (id) => {
                        const sel = document.getElementById(id);
                        if (!sel) return 'Todos';
                        const vals = Array.from(sel.selectedOptions).map(o => o.text).filter(t => t !== 'Todos' && t !== '__ALL__');
                        return vals.length > 0 ? vals.join(', ') : 'Todos';
                    };

                    const cliente = getSelectedText('envio_clienteSelect');
                    const clasif = getSelectedText('envio_clasif2Select');
                    const mes = getSelectedText('envio_mesSelect');
                    const centro = getSelectedText('envio_centroSelect');

                    summaryDiv = document.createElement('div');
                    summaryDiv.style.padding = '8px 15px';
                    summaryDiv.style.backgroundColor = '#f8fafc';
                    summaryDiv.style.borderBottom = '1px solid #cbd5e1';
                    summaryDiv.style.fontSize = '0.85rem';
                    summaryDiv.style.fontWeight = '600';
                    summaryDiv.style.color = '#334155';
                    summaryDiv.style.display = 'flex';
                    summaryDiv.style.flexWrap = 'wrap';
                    summaryDiv.style.gap = '15px';
                    summaryDiv.innerHTML = `
                        <span><b>Cliente/Obra:</b> <span style="color:#0d9488">${cliente}</span></span>
                        <span><b>Clasif:</b> <span style="color:#0d9488">${clasif}</span></span>
                        <span><b>Mes:</b> <span style="color:#0d9488">${mes}</span></span>
                        <span><b>Centro:</b> <span style="color:#0d9488">${centro}</span></span>
                    `;
                    panelFiltrosTitle.parentNode.insertBefore(summaryDiv, panelFiltrosTitle.nextSibling);
                }

                // Re-renderizar gráficos de ECharts para ajustarse al nuevo ancho de 1000px
                if (window.echarts) {
                    const echartsInstances = document.querySelectorAll('.chart-box');
                    echartsInstances.forEach(dom => {
                        const instance = echarts.getInstanceByDom(dom);
                        if (instance) instance.resize();
                    });
                }
                
                // Esperar un momento a que terminen los resizes
                await new Promise(resolve => setTimeout(resolve, 300));

                // Generar y descargar el PDF
                await html2pdf().set(opt).from(element).save();
                
                // Preparar URL mailto:
                const subject = encodeURIComponent("Informe de Cumplimiento");
                const body = encodeURIComponent("Adjunto el informe de cumplimiento en formato PDF generado desde el portal.\n\nSaludos.");
                
                // Abrir el cliente de correo por defecto
                window.location.href = `mailto:${emailTo}?subject=${subject}&body=${body}`;
            } catch (err) {
                console.error("Error al generar PDF:", err);
                alert("Ocurrió un error al generar el PDF. Verifica la consola para más detalles.");
            } finally {
                // Restaurar vista original
                element.style.width = originalWidth;
                element.style.maxWidth = originalMaxWidth;

                // Re-renderizar gráficos a tamaño original
                if (window.echarts) {
                    const echartsInstances = document.querySelectorAll('.chart-box');
                    echartsInstances.forEach(dom => {
                        const instance = echarts.getInstanceByDom(dom);
                        if (instance) instance.resize();
                    });
                }

                if (panelFiltrosBody) panelFiltrosBody.style.display = '';
                if (btnClear) btnClear.style.display = '';
                helpBtns.forEach(btn => btn.style.display = '');
                if (summaryDiv) summaryDiv.remove();

                btnGenerate.innerHTML = originalBtnText;
                btnGenerate.disabled = false;
                // Volver a la pestaña de envío
                if (window.switchTab) window.switchTab('envio');
            }
        });
    }
});
