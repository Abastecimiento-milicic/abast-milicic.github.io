# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('id="panel-resumen"')
end = text.find('</section>\n\n  </main>', start)
if end == -1:
    end = text.find('</section>\r\n\r\n  </main>', start)
if end == -1:
    end = text.find('</main>', start)

print("Panel resumen length:", end - start)
with open('scratch/panel_resumen_dump.html', 'w', encoding='utf-8') as f_out:
    f_out.write(text[start:end])
print("Saved to scratch/panel_resumen_dump.html")
