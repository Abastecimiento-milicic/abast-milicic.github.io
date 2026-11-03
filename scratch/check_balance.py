import sys
sys.stdout.reconfigure(encoding='utf-8')

for f in ['js/resumen.js', 'js/demoras.js', 'js/last-update.js']:
    with open(f, 'r', encoding='utf-8') as fh:
        c = fh.read()
    counts = {ch: c.count(ch) for ch in '{}()[]'}
    print(f, 'Brackets balance:')
    print('  {}:', counts['{'] == counts['}'], str(counts['{']) + ' vs ' + str(counts['}']))
    print('  ():', counts['('] == counts[')'], str(counts['(']) + ' vs ' + str(counts[')']))
    print('  []:', counts['['] == counts[']'], str(counts['[']) + ' vs ' + str(counts[']']))
