import json

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
  <style>
    body { font-family: system-ui, sans-serif; background: #f1f5f9; padding: 20px; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 1200px; margin: 0 auto; }
    .card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px 16px; }
    .title { font-size: 13.5px; font-weight: 800; text-transform: uppercase; color: #1e293b; margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1.5px solid #e2e8f0; }
    .chart { width: 100%; height: 410px; }
  </style>
</head>
<body>
  <div class="grid">
    <div class="card">
      <div class="title">Demora por Área</div>
      <div id="chartAreas" class="chart"></div>
    </div>
    <div class="card">
      <div class="title">Demoras Proyecto (Motivos)</div>
      <div id="chartMotivos" class="chart"></div>
    </div>
  </div>

  <script>
    const palette = ["#0d6efd", "#20c997", "#ffc107", "#6f42c1", "#fd7e14", "#198754", "#0dcaf0", "#6c757d"];

    // Areas
    const areasData = [
      { name: "PROYECTO", value: 45 },
      { name: "ALMACÉN", value: 28 },
      { name: "TRASLADO", value: 18 },
      { name: "COMPRAS", value: 12 },
      { name: "EXPEDICION", value: 7 },
      { name: "PERIODO CORTO", value: 5 }
    ];
    const totalAreas = areasData.reduce((a, b) => a + b.value, 0);

    const chartA = echarts.init(document.getElementById("chartAreas"));
    chartA.setOption({
      tooltip: {
        trigger: "item",
        formatter: (p) => `${p.name}: <b>${p.value}</b> (${p.percent.toFixed(1)}%)`
      },
      legend: {
        orient: "horizontal",
        bottom: 6,
        left: "center",
        type: "scroll",
        itemWidth: 12,
        itemHeight: 9,
        itemGap: 10,
        textStyle: { fontSize: 10.5, color: "#334155" },
        formatter: (name) => {
          const it = areasData.find(x => x.name === name);
          const pct = ((it.value / totalAreas) * 100).toFixed(1);
          return `${name} (${pct}%)`;
        }
      },
      series: [{
        type: "pie",
        radius: ["34%", "62%"],
        center: ["50%", "36%"],
        itemStyle: { borderColor: "#fff", borderWidth: 2 },
        label: {
          show: true,
          position: "inner",
          fontSize: 10.5,
          fontWeight: "bold",
          color: "#fff",
          formatter: (p) => p.percent >= 4 ? `${Math.round(p.percent)}%` : ""
        },
        emphasis: {
          scale: true,
          scaleSize: 5,
          label: { show: true, fontSize: 12, fontWeight: "bold" }
        },
        data: areasData.map((d, i) => ({
          ...d,
          itemStyle: { color: i === 0 ? "#dc3545" : palette[i % palette.length] }
        }))
      }]
    });

    // Motivos
    const motivosData = [
      { name: "FEMC (CON PRIORIDAD)", value: 34 },
      { name: "FEMC (SIN PRIORIDAD)", value: 22 },
      { name: "PLAZO DE ENTREGA EXCEDIDO CS", value: 19 },
      { name: "ENTREGA DEL PROVEEDOR CS", value: 14 },
      { name: "LIBERACION SOLPED CS", value: 8 },
      { name: "COLOCACION OC CS", value: 5 }
    ];
    const totalMotivos = motivosData.reduce((a, b) => a + b.value, 0);

    const chartM = echarts.init(document.getElementById("chartMotivos"));
    chartM.setOption({
      tooltip: {
        trigger: "item",
        formatter: (p) => `${p.name}: <b>${p.value}</b> (${p.percent.toFixed(1)}%)`
      },
      legend: {
        orient: "horizontal",
        bottom: 6,
        left: "center",
        type: "scroll",
        itemWidth: 12,
        itemHeight: 9,
        itemGap: 10,
        textStyle: { fontSize: 10.5, color: "#334155" },
        formatter: (name) => {
          const it = motivosData.find(x => x.name === name);
          const pct = ((it.value / totalMotivos) * 100).toFixed(1);
          return `${name} (${pct}%)`;
        }
      },
      series: [{
        type: "pie",
        radius: ["34%", "62%"],
        center: ["50%", "36%"],
        itemStyle: { borderColor: "#fff", borderWidth: 2 },
        label: {
          show: true,
          position: "inner",
          fontSize: 10.5,
          fontWeight: "bold",
          color: "#fff",
          formatter: (p) => p.percent >= 4 ? `${Math.round(p.percent)}%` : ""
        },
        emphasis: {
          scale: true,
          scaleSize: 5,
          label: { show: true, fontSize: 12, fontWeight: "bold" }
        },
        data: motivosData.map((d, i) => {
          let c = palette[i % palette.length];
          if (d.name.includes("CON PRIORIDAD")) c = "#dc3545";
          else if (d.name.includes("SIN PRIORIDAD")) c = "#e4606d";
          return { ...d, itemStyle: { color: c } };
        })
      }]
    });
  </script>
</body>
</html>
"""

with open('scratch/test_legend_bottom.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Saved test_legend_bottom.html")
