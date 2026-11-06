with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '/* =====' in l and 'STREAMLIT PILL' in l:
        print(f"Start: Line {i+1}")
    if 'window.toggleStSidebar = function()' in l:
        print(f"End: Line {i+1}")
