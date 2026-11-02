with open('js/demoras.js', encoding='utf-8') as f:
    js = f.read()

assert 'radius: ["60%", "86%"]' not in js, 'Still has 60%, 86%'
assert js.count('radius: ["40%", "72%"]') >= 2, 'Must have 40%, 72%'
print('Verification successful: Both charts now use the exact same dimensions!')
