with open('index.html', encoding='utf-8') as f:
    html = f.read()

import re
iframes = re.findall(r'<iframe[^>]*>', html, re.IGNORECASE)
print('iframes in index.html:', iframes)
