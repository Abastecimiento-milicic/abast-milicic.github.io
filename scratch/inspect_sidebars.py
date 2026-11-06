import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's inspect each tab-panel and its sidebar
panel_splits = html.split('<section id="panel-')

for part in panel_splits[1:]:
    panel_id = "panel-" + part.split('"')[0]
    # find sidebar
    if '<aside class="st-sidebar' in part:
        sb = part.split('<aside class="st-sidebar')[1].split('</aside>')[0]
        selects = re.findall(r'<select[^>]*id="([^"]*)"[^>]*>', sb)
        buttons = re.findall(r'<button[^>]*id="([^"]*)"[^>]*>', sb)
        print(f"Panel: {panel_id}")
        print(f"  Selects: {selects}")
        print(f"  Buttons: {buttons}")
    else:
        print(f"Panel: {panel_id} (No sidebar)")
