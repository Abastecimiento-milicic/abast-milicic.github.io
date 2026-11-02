with open('js/demoras.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace both occurrences of radius: ["60%", "86%"] with radius: ["40%", "72%"]
count = code.count('radius: ["60%", "86%"]')
print(f'Occurrences found: {count}')

code = code.replace('radius: ["60%", "86%"]', 'radius: ["40%", "72%"]')

with open('js/demoras.js', 'w', encoding='utf-8') as f:
    f.write(code)

print('Updated radius to ["40%", "72%"] successfully!')
