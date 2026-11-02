import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('height: 410px; min-height: 410px;', 'height: 470px; min-height: 470px;')
html = html.replace('?v=20261030_160000', '?v=20261030_163500')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html container height to 470px and bumped cache buster!")

# 2. Update js/demoras.js
with open('js/demoras.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 2.1 Update buildChartAreas
old_b_areas = """          legend: {
              orient: "horizontal",
              bottom: 4,
              left: "center",
              type: "scroll",
              itemWidth: 12,
              itemHeight: 9,
              itemGap: 10,
              textStyle: { fontSize: 10.5, color: "#334155" },
              formatter: (name) => {
                  const it = items.find(x => x.name === name);
                  const v = it ? it.value : 0;
                  const pct = (v / total) * 100;
                  return `${getDisplayName(name)} (${pct.toFixed(1).replace(".", ",")}%)`;
              }
          },
          series: [
              {
                  name: "% demoras por área",
                  type: "pie",
                  radius: ["34%", "62%"],
                  center: ["50%", "36%"],
                  avoidLabelOverlap: true,
                  itemStyle: {
                      borderColor: "#fff",
                      borderWidth: 2
                  },
                  label: {
                      show: true,
                      position: "inner",
                      fontSize: 10.5,
                      fontWeight: "bold",
                      color: "#fff",
                      formatter: (p) => p.percent >= 4 ? `${Math.round(p.percent)}%` : ""
                  },"""

new_b_areas = """          legend: {
              type: "plain",
              orient: "horizontal",
              bottom: 4,
              left: "center",
              width: "95%",
              itemWidth: 11,
              itemHeight: 8,
              itemGap: 8,
              textStyle: { fontSize: 10, color: "#334155" },
              formatter: (name) => {
                  const it = items.find(x => x.name === name);
                  const v = it ? it.value : 0;
                  const pct = (v / total) * 100;
                  return `${getDisplayName(name)} (${pct.toFixed(1).replace(".", ",")}%)`;
              }
          },
          series: [
              {
                  name: "% demoras por área",
                  type: "pie",
                  radius: ["28%", "48%"],
                  center: ["50%", "35%"],
                  avoidLabelOverlap: true,
                  itemStyle: {
                      borderColor: "#fff",
                      borderWidth: 2
                  },
                  label: {
                      show: true,
                      position: "outside",
                      fontSize: 10,
                      fontWeight: "600",
                      color: "#1e293b",
                      formatter: (p) => `${getDisplayName(p.name)}\\n${p.percent.toFixed(1).replace(".", ",")}%`
                  },
                  labelLine: {
                      show: true,
                      length: 10,
                      length2: 8,
                      smooth: true
                  },"""

if old_b_areas in js:
    js = js.replace(old_b_areas, new_b_areas, 1)
    print("Updated buildChartAreas in demoras.js!")
else:
    print("WARNING: old_b_areas not found in demoras.js")

# 2.2 Update buildChartMotivos
old_b_motivos = """          legend: {
              orient: "horizontal",
              bottom: 4,
              left: "center",
              type: "scroll",
              itemWidth: 12,
              itemHeight: 9,
              itemGap: 10,
              textStyle: { fontSize: 10.5, color: "#334155" },
              formatter: (name) => {
                  const it = sums.find(x => x.name === name);
                  const v = it ? it.value : 0;
                  const pct = (v / total) * 100;
                  return `${getDisplayName(name)} (${pct.toFixed(1).replace(".", ",")}%)`;
              }
          },
          series: [{
              name: "Demoras proyecto",
              type: "pie",
              radius: ["34%", "62%"],
              center: ["50%", "36%"],
              avoidLabelOverlap: true,
              itemStyle: {
                  borderColor: "#ffffff",
                  borderWidth: 2
              },
              emphasis: {
                  scale: true,
                  scaleSize: 6,
                  label: {
                      show: true,
                      fontSize: 12,
                      fontWeight: "bold",
                      color: "#fff",
                      formatter: (p) => `${p.percent.toFixed(1).replace(".", ",")}%`
                  }
              },
              label: {
                  show: true,
                  position: "inner",
                  fontSize: 10.5,
                  fontWeight: "bold",
                  color: "#fff",
                  formatter: (p) => p.percent >= 4 ? `${Math.round(p.percent)}%` : ""
              },"""

new_b_motivos = """          legend: {
              type: "plain",
              orient: "horizontal",
              bottom: 4,
              left: "center",
              width: "95%",
              itemWidth: 11,
              itemHeight: 8,
              itemGap: 8,
              textStyle: { fontSize: 10, color: "#334155" },
              formatter: (name) => {
                  const it = sums.find(x => x.name === name);
                  const v = it ? it.value : 0;
                  const pct = (v / total) * 100;
                  return `${getDisplayName(name)} (${pct.toFixed(1).replace(".", ",")}%)`;
              }
          },
          series: [{
              name: "Demoras proyecto",
              type: "pie",
              radius: ["28%", "48%"],
              center: ["50%", "35%"],
              avoidLabelOverlap: true,
              itemStyle: {
                  borderColor: "#ffffff",
                  borderWidth: 2
              },
              emphasis: {
                  scale: true,
                  scaleSize: 6,
                  label: {
                      show: true,
                      fontSize: 11,
                      fontWeight: "bold"
                  }
              },
              label: {
                  show: true,
                  position: "outside",
                  fontSize: 10,
                  fontWeight: "600",
                  color: "#1e293b",
                  formatter: (p) => `${getDisplayName(p.name)}\\n${p.percent.toFixed(1).replace(".", ",")}%`
              },
              labelLine: {
                  show: true,
                  length: 10,
                  length2: 8,
                  smooth: true
              },"""

if old_b_motivos in js:
    js = js.replace(old_b_motivos, new_b_motivos, 1)
    print("Updated buildChartMotivos in demoras.js!")
else:
    print("WARNING: old_b_motivos not found in demoras.js")

# 2.3 Update renderResumenDemoras (Areas)
old_res_areas = """                  legend: {
                      orient: "horizontal",
                      bottom: 4,
                      left: "center",
                      type: "scroll",
                      itemWidth: 12,
                      itemHeight: 9,
                      itemGap: 10,
                      textStyle: { fontSize: 10.5, color: "#334155" },
                      formatter: (name) => {
                          const it = areaItems.find(x => x.name === name);
                          const v = it ? it.value : 0;
                          const pct = (v / totalAreas) * 100;
                          return `${getDisplayName(name)} (${pct.toFixed(1).replace(".", ",")}%)`;
                      }
                  },
                  series: [
                      {
                          name: "% demoras por área",
                          type: "pie",
                          radius: ["34%", "62%"],
                          center: ["50%", "36%"],
                          avoidLabelOverlap: true,
                          itemStyle: {
                              borderColor: "#fff",
                              borderWidth: 2
                          },
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
                              label: {
                                  show: true,
                                  fontSize: 12,
                                  fontWeight: "bold",
                                  color: "#fff",
                                  formatter: (p) => `${p.percent.toFixed(1).replace(".", ",")}%`
                              }
                          },
                          data: dataWithColors
                      }
                  ]"""

new_res_areas = """                  legend: {
                      type: "plain",
                      orient: "horizontal",
                      bottom: 4,
                      left: "center",
                      width: "95%",
                      itemWidth: 11,
                      itemHeight: 8,
                      itemGap: 8,
                      textStyle: { fontSize: 10, color: "#334155" },
                      formatter: (name) => {
                          const it = areaItems.find(x => x.name === name);
                          const v = it ? it.value : 0;
                          const pct = (v / totalAreas) * 100;
                          return `${getDisplayName(name)} (${pct.toFixed(1).replace(".", ",")}%)`;
                      }
                  },
                  series: [
                      {
                          name: "% demoras por área",
                          type: "pie",
                          radius: ["28%", "48%"],
                          center: ["50%", "35%"],
                          avoidLabelOverlap: true,
                          itemStyle: {
                              borderColor: "#fff",
                              borderWidth: 2
                          },
                          label: {
                              show: true,
                              position: "outside",
                              fontSize: 10,
                              fontWeight: "600",
                              color: "#1e293b",
                              formatter: (p) => `${getDisplayName(p.name)}\\n${p.percent.toFixed(1).replace(".", ",")}%`
                          },
                          labelLine: {
                              show: true,
                              length: 10,
                              length2: 8,
                              smooth: true
                          },
                          emphasis: {
                              scale: true,
                              scaleSize: 5,
                              label: {
                                  show: true,
                                  fontSize: 11,
                                  fontWeight: "bold"
                              }
                          },
                          data: dataWithColors
                      }
                  ]"""

assert old_res_areas in js, "old_res_areas not found in demoras.js"
js = js.replace(old_res_areas, new_res_areas, 1)

# 2.4 Update renderResumenDemoras (Motivos)
old_res_motivos = """                  legend: {
                      orient: "horizontal",
                      bottom: 4,
                      left: "center",
                      type: "scroll",
                      itemWidth: 12,
                      itemHeight: 9,
                      itemGap: 10,
                      textStyle: { fontSize: 10.5, color: "#334155" },
                      formatter: (name) => {
                          const it = motivosItems.find(x => x.name === name);
                          const v = it ? it.value : 0;
                          const pct = (v / totalMotivos) * 100;
                          return `${getDisplayName(name)} (${pct.toFixed(1).replace(".", ",")}%)`;
                      }
                  },
                  series: [
                      {
                          name: "Demoras proyecto",
                          type: "pie",
                          radius: ["34%", "62%"],
                          center: ["50%", "36%"],
                          avoidLabelOverlap: true,
                          itemStyle: {
                              borderColor: "#ffffff",
                              borderWidth: 2
                          },
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
                              label: {
                                  show: true,
                                  fontSize: 12,
                                  fontWeight: "bold",
                                  color: "#fff",
                                  formatter: (p) => `${p.percent.toFixed(1).replace(".", ",")}%`
                              }
                          },
                          data: dataPie
                      }
                  ]"""

new_res_motivos = """                  legend: {
                      type: "plain",
                      orient: "horizontal",
                      bottom: 4,
                      left: "center",
                      width: "95%",
                      itemWidth: 11,
                      itemHeight: 8,
                      itemGap: 8,
                      textStyle: { fontSize: 10, color: "#334155" },
                      formatter: (name) => {
                          const it = motivosItems.find(x => x.name === name);
                          const v = it ? it.value : 0;
                          const pct = (v / totalMotivos) * 100;
                          return `${getDisplayName(name)} (${pct.toFixed(1).replace(".", ",")}%)`;
                      }
                  },
                  series: [
                      {
                          name: "Demoras proyecto",
                          type: "pie",
                          radius: ["28%", "48%"],
                          center: ["50%", "35%"],
                          avoidLabelOverlap: true,
                          itemStyle: {
                              borderColor: "#ffffff",
                              borderWidth: 2
                          },
                          label: {
                              show: true,
                              position: "outside",
                              fontSize: 10,
                              fontWeight: "600",
                              color: "#1e293b",
                              formatter: (p) => `${getDisplayName(p.name)}\\n${p.percent.toFixed(1).replace(".", ",")}%`
                          },
                          labelLine: {
                              show: true,
                              length: 10,
                              length2: 8,
                              smooth: true
                          },
                          emphasis: {
                              scale: true,
                              scaleSize: 5,
                              label: {
                                  show: true,
                                  fontSize: 11,
                                  fontWeight: "bold"
                              }
                          },
                          data: dataPie
                      }
                  ]"""

assert old_res_motivos in js, "old_res_motivos not found in demoras.js"
js = js.replace(old_res_motivos, new_res_motivos, 1)

with open('js/demoras.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated js/demoras.js successfully!")
