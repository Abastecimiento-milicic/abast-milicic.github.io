import os

c_path = r"c:\Users\david.benitez\Documents\GitHub\abast-milicic.github.io\js\cumplimiento.js"
with open(c_path, "r", encoding="utf-8") as f:
    text = f.read()

# Fix target 1 in cumplimiento.js
old1 = """    if (months.length === 0) {
      chartMes.setOption({
        title: {
          show: true,
          text: "No hay meses seleccionados para mostrar",
          left: "center",
          top: "middle",
          textStyle: { color: "#64748b", fontSize: 13, fontWeight: "normal" }
        },
        xAxis: { data: [] },
        series: []
      }, true);
      return;
    }"""

new1 = """    if (months.length === 0) {
      chartMes.clear();
      chartMes.setOption({
        title: {
          show: true,
          text: "No hay meses seleccionados para mostrar",
          left: "center",
          top: "middle",
          textStyle: { color: "#64748b", fontSize: 13, fontWeight: "normal" }
        },
        xAxis: { show: false, type: "category", data: [] },
        yAxis: { show: false, type: "value" },
        series: []
      }, true);
      return;
    }"""

# Fix target 2 in cumplimiento.js
old2 = """    if (months.length === 0) {
      chartTendencia.setOption({
        title: {
          show: true,
          text: "No hay meses seleccionados para mostrar",
          left: "center",
          top: "middle",
          textStyle: { color: "#64748b", fontSize: 13, fontWeight: "normal" }
        },
        xAxis: { data: [] },
        series: []
      }, true);
      return;
    }"""

new2 = """    if (months.length === 0) {
      chartTendencia.clear();
      chartTendencia.setOption({
        title: {
          show: true,
          text: "No hay meses seleccionados para mostrar",
          left: "center",
          top: "middle",
          textStyle: { color: "#64748b", fontSize: 13, fontWeight: "normal" }
        },
        xAxis: { show: false, type: "category", data: [] },
        yAxis: { show: false, type: "value" },
        series: []
      }, true);
      return;
    }"""

assert old1 in text, "old1 not found"
text = text.replace(old1, new1)

assert old2 in text, "old2 not found"
text = text.replace(old2, new2)

with open(c_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated cumplimiento.js successfully!")

# Now fix cumplimiento-arriba.js
ca_path = r"c:\Users\david.benitez\Documents\GitHub\abast-milicic.github.io\js\cumplimiento-arriba.js"
with open(ca_path, "r", encoding="utf-8") as f:
    text_ca = f.read()

old_ca = """    if (months.length === 0) {
      if (chartMes) {
        chartMes.setOption({
          title: {
            show: true,
            text: "No hay meses seleccionados para mostrar",
            left: "center",
            top: "middle",
            textStyle: { color: "#64748b", fontSize: 13, fontWeight: "normal" }
          },
          xAxis: { data: [] },
          series: []
        }, true);
      }
      if (chartTendencia) {
        chartTendencia.setOption({
          title: {
            show: true,
            text: "No hay meses seleccionados para mostrar",
            left: "center",
            top: "middle",
            textStyle: { color: "#64748b", fontSize: 13, fontWeight: "normal" }
          },
          xAxis: { data: [] },
          series: []
        }, true);
      }
      return;
    }"""

new_ca = """    if (months.length === 0) {
      if (chartMes) {
        chartMes.clear();
        chartMes.setOption({
          title: {
            show: true,
            text: "No hay meses seleccionados para mostrar",
            left: "center",
            top: "middle",
            textStyle: { color: "#64748b", fontSize: 13, fontWeight: "normal" }
          },
          xAxis: { show: false, type: "category", data: [] },
          yAxis: { show: false, type: "value" },
          series: []
        }, true);
      }
      if (chartTendencia) {
        chartTendencia.clear();
        chartTendencia.setOption({
          title: {
            show: true,
            text: "No hay meses seleccionados para mostrar",
            left: "center",
            top: "middle",
            textStyle: { color: "#64748b", fontSize: 13, fontWeight: "normal" }
          },
          xAxis: { show: false, type: "category", data: [] },
          yAxis: { show: false, type: "value" },
          series: []
        }, true);
      }
      return;
    }"""

assert old_ca in text_ca, "old_ca not found"
text_ca = text_ca.replace(old_ca, new_ca)

with open(ca_path, "w", encoding="utf-8") as f:
    f.write(text_ca)

print("Updated cumplimiento-arriba.js successfully!")
