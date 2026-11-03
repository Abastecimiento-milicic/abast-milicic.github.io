with open('js/demoras.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """  function getDisplayName(name) {
      if (name === "FECHAENTREGAMUYCERCANA CON PRIORIDAD" || name === "FECHA ENTREGA MUY CERCANA (CON PRIORIDAD)" || name === "FECHA DE ENTREGA MUY CERCANA (CON PRIORIDAD)") {
          return "FEMC (CON PRIORIDAD)";
      }
      if (name === "FECHAENTREGAMUYCERCANA SIN PRIORIDAD" || name === "FECHA ENTREGA MUY CERCANA (SIN PRIORIDAD)" || name === "FECHA DE ENTREGA MUY CERCANA (SIN PRIORIDAD)") {
          return "FEMC (SIN PRIORIDAD)";
      }
      const normalized = norm(name);
      if (normalized.includes("FECHA") && (normalized.includes("CERCANA") || normalized.includes("MUYCERCANA"))) {
          if (normalized.includes("CON PRIORIDAD") || normalized.includes("CONPRIORIDAD")) return "FEMC (CON PRIORIDAD)";
          if (normalized.includes("SIN PRIORIDAD") || normalized.includes("SINPRIORIDAD")) return "FEMC (SIN PRIORIDAD)";
          return "FEMC";
      }
      if (normalized === norm("CADENA DE SUMINISTRO") || normalized === norm("CADENA DE SUMINISTROS")) {
          return "PROYECTO";
      }
      if (normalized === norm("BLEN")) {
          return "BLEND";
      }
      return name;
  }"""

repl = """  function getDisplayName(name) {
      if (name === "FECHAENTREGAMUYCERCANA CON PRIORIDAD" || 
          name === "FECHA ENTREGA MUY CERCANA (CON PRIORIDAD)" || 
          name === "FECHA DE ENTREGA MUY CERCANA (CON PRIORIDAD)" ||
          name === "FEMC (CON PRIORIDAD)" ||
          name === "PERIODO CORTO CON PRIORIDAD") {
          return "PERIODO CORTO (CON PRIORIDAD)";
      }
      if (name === "FECHAENTREGAMUYCERCANA SIN PRIORIDAD" || 
          name === "FECHA ENTREGA MUY CERCANA (SIN PRIORIDAD)" || 
          name === "FECHA DE ENTREGA MUY CERCANA (SIN PRIORIDAD)" ||
          name === "FEMC (SIN PRIORIDAD)" ||
          name === "PERIODO CORTO SIN PRIORIDAD") {
          return "PERIODO CORTO (SIN PRIORIDAD)";
      }
      const normalized = norm(name);
      if (normalized.includes("FECHA") && (normalized.includes("CERCANA") || normalized.includes("MUYCERCANA"))) {
          if (normalized.includes("CON PRIORIDAD") || normalized.includes("CONPRIORIDAD")) return "PERIODO CORTO (CON PRIORIDAD)";
          if (normalized.includes("SIN PRIORIDAD") || normalized.includes("SINPRIORIDAD")) return "PERIODO CORTO (SIN PRIORIDAD)";
          return "PERIODO CORTO";
      }
      if (normalized.startsWith("FEMC") || normalized.startsWith("PERIODO CORTO")) {
          if (normalized.includes("CON PRIORIDAD") || normalized.includes("CONPRIORIDAD")) return "PERIODO CORTO (CON PRIORIDAD)";
          if (normalized.includes("SIN PRIORIDAD") || normalized.includes("SINPRIORIDAD")) return "PERIODO CORTO (SIN PRIORIDAD)";
          return "PERIODO CORTO";
      }
      if (normalized === norm("CADENA DE SUMINISTRO") || normalized === norm("CADENA DE SUMINISTROS")) {
          return "PROYECTO";
      }
      if (normalized === norm("BLEN")) {
          return "BLEND";
      }
      return name;
  }"""

assert target in js, "Target getDisplayName not found in js/demoras.js"
js = js.replace(target, repl, 1)

with open('js/demoras.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated getDisplayName in js/demoras.js to PERIODO CORTO successfully!")

# Bump cache buster in index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('?v=20261030_163500', '?v=20261102_144500')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Bumped cache buster in index.html to 20261102_144500!")
