import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Update index.html - change chart height to 410px for better vertical separation
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('height: 380px; min-height: 380px;', 'height: 410px; min-height: 410px;')
html = html.replace('?v=20261030_154000', '?v=20261030_160000')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html chart heights to 410px and bumped cache buster!")

# 2. Update js/demoras.js
with open('js/demoras.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 2.1 Update buildChartAreas
old_areas_legend = """          legend: {
              orient: "vertical",
              right: 10,
              top: "middle",
              itemWidth: 18,
              itemHeight: 10,
              formatter: (name) => {
                  const it = items.find(x => x.name === name);
                  const v = it ? it.value : 0;
                  const pct = (v / total) * 100;
                  return `${getDisplayName(name)} - ${pct.toFixed(1).replace(".", ",")}%`;
              }
          },
          series: [
              {
                  name: "% demoras por área",
                  type: "pie",
                  radius: ["40%", "72%"],
                  center: ["40%", "50%"],
                  avoidLabelOverlap: true,
                  itemStyle: {
                      borderColor: "#fff",
                      borderWidth: 2
                  },
                  label: {
                      show: true,
                      position: "outside",
                      fontSize: 12,
                      fontWeight: "bold",
                      formatter: (p) => `${getDisplayName(p.name)}\\n${p.value} (${p.percent.toFixed(1).replace(".", ",")}%)`
                  },"""

new_areas_legend = """          legend: {
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

if old_areas_legend in js:
    js = js.replace(old_areas_legend, new_areas_legend, 1)
    print("Updated buildChartAreas in demoras.js!")
else:
    print("WARNING: old_areas_legend not found in demoras.js")

# 2.2 Update buildChartMotivos
old_motivos_legend = """          legend: {
              orient: "vertical",
              right: 10,
              top: "middle",
              itemWidth: 18,
              itemHeight: 10,
              formatter: (name) => {
                  const it = sums.find(x => x.name === name);
                  const v = it ? it.value : 0;
                  const pct = (v / total) * 100;
                  return `${getDisplayName(name)} - ${pct.toFixed(1).replace(".", ",")}%`;
              },
              textStyle: { fontSize: 12 }
          },
          series: [{
              name: "Demoras proyecto",
              type: "pie",
              radius: ["40%", "72%"],
              center: ["40%", "50%"],
              avoidLabelOverlap: true,
              itemStyle: {
                  borderColor: "#ffffff",
                  borderWidth: 2
              },
              emphasis: {
                  scale: true,
                  scaleSize: 10,
                  itemStyle: {
                      shadowBlur: 18,
                      shadowColor: "rgba(0,0,0,0.35)"
                  }
              },
              label: {
                  show: true,
                  backgroundColor: "rgba(255,255,255,0.85)",
                  borderRadius: 4,
                  padding: [4, 6],
                  fontSize: 13,
                  fontWeight: "bold",
                  color: "#0b1220",
                  formatter: (p) =>
                      `${getDisplayName(p.name)}\\n${fmtInt(p.value)} (${String(p.percent).replace(".", ",")}%)`
              },"""

new_motivos_legend = """          legend: {
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

if old_motivos_legend in js:
    js = js.replace(old_motivos_legend, new_motivos_legend, 1)
    print("Updated buildChartMotivos in demoras.js!")
else:
    print("WARNING: old_motivos_legend not found in demoras.js")

# 2.3 Update renderResumenDemoras
old_res_areas_block = """              const areasOption = {
                  tooltip: {
                      trigger: "item",
                      formatter: (p) => {
                          const pct = (p.value / totalAreas) * 100;
                          return `${getDisplayName(p.name)}: <b>${fmtInt(p.value)}</b> (${pct.toFixed(1).replace(".", ",")}%)`;
                      }
                  },
                  legend: {
                      orient: "vertical",
                      right: 10,
                      top: "middle",
                      type: "scroll",
                      itemWidth: 18,
                      itemHeight: 10,
                      formatter: (name) => {
                          const it = areaItems.find(x => x.name === name);
                          const v = it ? it.value : 0;
                          const pct = (v / totalAreas) * 100;
                          return `${getDisplayName(name)} - ${pct.toFixed(1).replace(".", ",")}%`;
                      },
                      textStyle: { fontSize: 12 }
                  },
                  series: [
                      {
                          name: "% demoras por área",
                          type: "pie",
                          radius: ["40%", "72%"],
                          center: ["35%", "50%"],
                          avoidLabelOverlap: true,
                          itemStyle: {
                              borderColor: "#fff",
                              borderWidth: 2
                          },
                          label: {
                              show: false
                          },
                          emphasis: {
                              scale: true,
                              scaleSize: 6,
                              label: {
                                  show: true,
                                  fontSize: 12,
                                  fontWeight: "bold",
                                  formatter: (p) => `${p.percent.toFixed(0)}%`
                              }
                          },
                          data: dataWithColors
                      }
                  ]
              };"""

new_res_areas_block = """              const areasOption = {
                  tooltip: {
                      trigger: "item",
                      formatter: (p) => {
                          const pct = (p.value / totalAreas) * 100;
                          return `${getDisplayName(p.name)}: <b>${fmtInt(p.value)}</b> (${pct.toFixed(1).replace(".", ",")}%)`;
                      }
                  },
                  legend: {
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
                  ]
              };"""

assert old_res_areas_block in js, "old_res_areas_block not found in demoras.js"
js = js.replace(old_res_areas_block, new_res_areas_block, 1)

old_res_motivos_block = """              const motivosOption = {
                  tooltip: {
                      trigger: "item",
                      formatter: (p) => {
                          const pct = (p.value / totalMotivos) * 100;
                          return `${getDisplayName(p.name)}: <b>${fmtInt(p.value)}</b> (${pct.toFixed(1).replace(".", ",")}%)`;
                      }
                  },
                  legend: {
                      orient: "vertical",
                      right: 10,
                      top: "middle",
                      type: "scroll",
                      itemWidth: 18,
                      itemHeight: 10,
                      formatter: (name) => {
                          const it = motivosItems.find(x => x.name === name);
                          const v = it ? it.value : 0;
                          const pct = (v / totalMotivos) * 100;
                          return `${getDisplayName(name)} - ${pct.toFixed(1).replace(".", ",")}%`;
                      },
                      textStyle: { fontSize: 12 }
                  },
                  series: [
                      {
                          name: "Demoras proyecto",
                          type: "pie",
                          radius: ["40%", "72%"],
                          center: ["35%", "50%"],
                          avoidLabelOverlap: true,
                          itemStyle: {
                              borderColor: "#ffffff",
                              borderWidth: 2
                          },
                          label: {
                              show: false
                          },
                          emphasis: {
                              scale: true,
                              scaleSize: 6,
                              label: {
                                  show: true,
                                  fontSize: 12,
                                  fontWeight: "bold",
                                  formatter: (p) => `${p.percent.toFixed(0)}%`
                              }
                          },
                          data: dataPie
                      }
                  ]
              };"""

new_res_motivos_block = """              const motivosOption = {
                  tooltip: {
                      trigger: "item",
                      formatter: (p) => {
                          const pct = (p.value / totalMotivos) * 100;
                          return `${getDisplayName(p.name)}: <b>${fmtInt(p.value)}</b> (${pct.toFixed(1).replace(".", ",")}%)`;
                      }
                  },
                  legend: {
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
                  ]
              };"""

assert old_res_motivos_block in js, "old_res_motivos_block not found in demoras.js"
js = js.replace(old_res_motivos_block, new_res_motivos_block, 1)

with open('js/demoras.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Successfully updated js/demoras.js with horizontal bottom legend and inner slice labels!")
