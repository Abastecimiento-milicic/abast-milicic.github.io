import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("js/resumen.js", "r", encoding="utf-8") as f:
    code = f.read()

old_parse_csv = """  function parseCSV(text) {
    const lines = text.split(/\\r?\\n/).map(l => l.trim()).filter(Boolean);
    if (!lines.length) return { headers: [], rows: [] };
    const headers = lines[0].split(DELIM).map(clean);
    const rows = [];
    for (let i = 1; i < lines.length; i++) {
      const parts = lines[i].split(DELIM);
      const row = {};
      for (let j = 0; j < headers.length; j++) {
        row[headers[j]] = clean(parts[j]);
      }
      rows.push(row);
    }
    return { headers, rows };
  }"""

new_parse_csv = """  function parseCSV(text) {
    if (typeof Papa !== "undefined" && typeof Papa.parse === "function") {
      const res = Papa.parse(text, {
        delimiter: DELIM,
        skipEmptyLines: true
      });
      const data = res.data || [];
      if (!data.length) return { headers: [], rows: [] };
      const headers = data[0].map(clean);
      const rows = [];
      for (let i = 1; i < data.length; i++) {
        const parts = data[i];
        if (!parts || !parts.length || (parts.length === 1 && !parts[0])) continue;
        const row = {};
        for (let j = 0; j < headers.length; j++) {
          row[headers[j]] = clean(parts[j]);
        }
        rows.push(row);
      }
      return { headers, rows };
    }

    const lines = text.split(/\\r?\\n/).map(l => l.trim()).filter(Boolean);
    if (!lines.length) return { headers: [], rows: [] };
    const headers = lines[0].split(DELIM).map(clean);
    const rows = [];
    for (let i = 1; i < lines.length; i++) {
      const parts = lines[i].split(DELIM);
      const row = {};
      for (let j = 0; j < headers.length; j++) {
        row[headers[j]] = clean(parts[j]);
      }
      rows.push(row);
    }
    return { headers, rows };
  }"""

assert old_parse_csv in code, "old_parse_csv not found!"
code = code.replace(old_parse_csv, new_parse_csv)

# Also ensure renderObrasSelect excludes 1 and 1500
code = code.replace('if (c && c !== "0") codes.add(c);', 'if (c && c !== "0" && c !== "1" && c !== "1500") codes.add(c);')

with open("js/resumen.js", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated parseCSV in js/resumen.js")

# Bump cache buster to v81
with open("js/last-update.js", "r", encoding="utf-8") as f:
    lu = f.read()
lu = lu.replace("_v80_20261102_155200", "_v81_20261102_164500")
with open("js/last-update.js", "w", encoding="utf-8") as f:
    f.write(lu)

with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()
idx = idx.replace("js/demoras.js?v=20261102_155200", "js/demoras.js?v=20261102_164500")
idx = idx.replace("js/resumen.js?v=20261102_155200", "js/resumen.js?v=20261102_164500")
with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx)

print("Bumped cache buster to v81")
