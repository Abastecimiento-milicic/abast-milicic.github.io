document.addEventListener('DOMContentLoaded', () => {
    const btnExport = document.getElementById('cumpl_btnExportPPTX');
    if (!btnExport) return;

    btnExport.addEventListener('click', async () => {
        try {
            const originalText = btnExport.innerHTML;
            btnExport.innerHTML = '⏳ Generando Canvas...';
            btnExport.disabled = true;

            // 1. Inicializar PptxGenJS en formato Vertical (A4/Letter) para estilo Canvas/Infografía
            let pres = new PptxGenJS();
            // Tamaño personalizado tipo póster vertical (8.5 x 11 pulgadas)
            pres.layout = { name: 'CANVAS_PORTRAIT', width: 8.5, height: 11 };

            // 2. Extraer Textos del DOM
            const getSelectedText = (id) => {
                const sel = document.getElementById(id);
                if (!sel) return 'Todos';
                const vals = Array.from(sel.selectedOptions).map(o => o.text).filter(t => t !== 'Todos' && t !== '__ALL__');
                return vals.length > 0 ? vals.join(', ') : 'Todos';
            };
            const getElText = (id) => document.getElementById(id) ? document.getElementById(id).innerText.replace(/\n/g, ' ') : '-';

            const filtros = [
                { nombre: 'Cliente/Obra', valor: getSelectedText('cumpl_clienteSelect') },
                { nombre: 'Clasificación', valor: getSelectedText('cumpl_clasif2Select') },
                { nombre: 'Mes', valor: getSelectedText('cumpl_mesSelect') },
                { nombre: 'Centro', valor: getSelectedText('centroSelect') } 
            ];

            // 3. Crear el único Slide (El Canvas)
            let slide = pres.addSlide();
            
            // ================= HEADER =================
            // Fondo azul oscuro
            slide.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: '100%', h: 1.2, fill: { color: '0f172a' } });
            // Título Principal
            slide.addText('TABLERO DE INDICADORES', { x: 0.5, y: 0.2, w: 7.5, h: 0.4, fontSize: 24, bold: true, color: 'FFFFFF', align: 'center' });
            slide.addText('CUMPLIMIENTO DE ABASTECIMIENTO', { x: 0.5, y: 0.6, w: 7.5, h: 0.3, fontSize: 16, bold: true, color: 'fde047', align: 'center' });
            // Línea separadora
            slide.addShape(pres.ShapeType.line, { x: 1.0, y: 1.0, w: 6.5, h: 0, line: { color: 'fde047', width: 1 } });

            // ================= FILTROS =================
            let filterText = filtros.map(f => `${f.nombre.toUpperCase()}: ${f.valor}`).join('   |   ');
            slide.addText(filterText, { x: 0.25, y: 1.3, w: 8.0, h: 0.3, fontSize: 9, color: '475569', fill: { color: 'f8fafc' }, align: 'center', bold: true });

            // ================= FUNCIÓN HELPER PARA TARJETAS KPI =================
            function addKpiCard(x, y, title, value, subValue, colorHex) {
                if (!value || value === '-') return; // No agregar si no hay datos
                
                // Sombra / Borde
                slide.addShape(pres.ShapeType.rect, { x: x, y: y, w: 1.5, h: 1.0, fill: { color: 'FFFFFF' }, line: { color: colorHex, width: 1.5 }, rectRadius: 0.1 });
                // Cabecera de la tarjeta
                slide.addShape(pres.ShapeType.rect, { x: x, y: y, w: 1.5, h: 0.25, fill: { color: colorHex }, rectRadius: 0.1 });
                // Título
                slide.addText(title, { x: x, y: y, w: 1.5, h: 0.25, fontSize: 8, color: 'FFFFFF', bold: true, align: 'center', valign: 'middle' });
                // Valor Principal
                slide.addText(value, { x: x, y: y + 0.3, w: 1.5, h: 0.4, fontSize: 18, color: colorHex, bold: true, align: 'center', valign: 'middle' });
                // Sub Valor
                if (subValue) {
                    slide.addText(subValue, { x: x, y: y + 0.7, w: 1.5, h: 0.2, fontSize: 8, color: '64748b', align: 'center', valign: 'middle' });
                }
            }

            // ================= SECCIÓN: ACUMULADO =================
            slide.addText('RESUMEN ACUMULADO (Últimos 12 meses)', { x: 0.25, y: 1.8, w: 8.0, h: 0.3, fontSize: 11, bold: true, color: '0f172a', fill: { color: 'e2e8f0' }, align: 'center' });
            
            let startY1 = 2.2;
            let startX = 0.25;
            let stepX = 1.625; // 1.5 ancho + 0.125 espacio

            addKpiCard(startX + stepX*0, startY1, 'COMPROMETIDOS', getElText('cumpl_kpiComprometidos'), 'Total del período', '334155');
            addKpiCard(startX + stepX*1, startY1, 'A TIEMPO (AT)', getElText('cumpl_kpiATpct'), getElText('cumpl_kpiATqty'), '10b981');
            addKpiCard(startX + stepX*2, startY1, 'FUERA DE TIEMPO', getElText('cumpl_kpiFTpct'), 'Entregados tarde', 'f59e0b');
            addKpiCard(startX + stepX*3, startY1, 'NO ENTREGADOS', getElText('cumpl_kpiNOpct'), 'Pendientes', 'ef4444');
            addKpiCard(startX + stepX*4, startY1, 'DEMORA PROMEDIO', getElText('cumpl_kpiDemoraPromedio'), 'Días promedio', '64748b');

            // ================= SECCIÓN: MES SELECCIONADO =================
            slide.addText(`MES SELECCIONADO: ${filtros[2].valor.toUpperCase()}`, { x: 0.25, y: 3.4, w: 8.0, h: 0.3, fontSize: 11, bold: true, color: '0f172a', fill: { color: 'e2e8f0' }, align: 'center' });
            
            let startY2 = 3.8;
            addKpiCard(startX + stepX*0, startY2, 'COMPROMETIDOS', getElText('cumpl_kpiComprometidosMes'), 'Total del mes', '334155');
            addKpiCard(startX + stepX*1, startY2, 'A TIEMPO (AT)', getElText('cumpl_kpiATmes'), getElText('cumpl_kpiATmesSub'), '10b981');
            addKpiCard(startX + stepX*2, startY2, 'FUERA DE TIEMPO', getElText('cumpl_kpiFTmes'), 'Entregados tarde', 'f59e0b');
            addKpiCard(startX + stepX*3, startY2, 'NO ENTREGADOS', getElText('cumpl_kpiNOmes'), 'Pendientes', 'ef4444');
            addKpiCard(startX + stepX*4, startY2, 'DEMORA PROMEDIO', getElText('cumpl_kpiDemoraMes'), 'Días promedio', '64748b');

            // ================= GRÁFICOS (ECHARTS) =================
            if (window.echarts) {
                const getChartBase64 = (domId) => {
                    const dom = document.getElementById(domId);
                    if (!dom) return null;
                    const instance = echarts.getInstanceByDom(dom);
                    if (!instance) return null;
                    return instance.getDataURL({ type: 'png', pixelRatio: 2, backgroundColor: '#ffffff' });
                };

                const chartMesBase64 = getChartBase64('cumpl_chartMes');
                if (chartMesBase64) {
                    slide.addText('1. CUMPLIMIENTO POR MES', { x: 0.25, y: 5.1, w: 8.0, h: 0.25, fontSize: 10, bold: true, color: '0f172a' });
                    slide.addShape(pres.ShapeType.rect, { x: 0.25, y: 5.4, w: 8.0, h: 2.6, line: { color: 'e2e8f0', width: 1 } });
                    slide.addImage({ data: chartMesBase64, x: 0.3, y: 5.45, w: 7.9, h: 2.5 });
                }

                const chartTendenciaBase64 = getChartBase64('cumpl_chartTendencia');
                if (chartTendenciaBase64) {
                    slide.addText('2. TENDENCIA DE CUMPLIMIENTO', { x: 0.25, y: 8.1, w: 8.0, h: 0.25, fontSize: 10, bold: true, color: '0f172a' });
                    slide.addShape(pres.ShapeType.rect, { x: 0.25, y: 8.4, w: 8.0, h: 2.2, line: { color: 'e2e8f0', width: 1 } });
                    // El de tendencia suele ser más bajo
                    slide.addImage({ data: chartTendenciaBase64, x: 0.3, y: 8.45, w: 7.9, h: 2.1 });
                }
            }

            // Pie de página
            slide.addText('Documento generado automáticamente desde el Tablero de Abastecimiento.', { x: 0.25, y: 10.7, w: 8.0, fontSize: 8, color: '94a3b8', align: 'center' });

            // 4. Descargar archivo
            await pres.writeFile({ fileName: `Tablero_Cumplimiento_${new Date().toISOString().slice(0,10)}.pptx` });

        } catch (error) {
            console.error('Error generando PPTX:', error);
            alert('Hubo un error al generar el archivo de PowerPoint.');
        } finally {
            btnExport.innerHTML = '📊 Exportar PPTX';
            btnExport.disabled = false;
        }
    });
});
