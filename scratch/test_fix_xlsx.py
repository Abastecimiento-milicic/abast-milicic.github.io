# -*- coding: utf-8 -*-
import zipfile, io, openpyxl

fpath = r'C:\Users\david.benitez\Downloads\ANALISIS-MM_0365.xlsx'
with open(fpath, 'rb') as f:
    zip_bytes = f.read()

in_zip = zipfile.ZipFile(io.BytesIO(zip_bytes), 'r')
out_buf = io.BytesIO()
out_zip = zipfile.ZipFile(out_buf, 'w', zipfile.ZIP_DEFLATED)

for item in in_zip.infolist():
    data = in_zip.read(item.filename)
    if item.filename == 'xl/worksheets/sheet1.xml':
        data = data.replace(b'<c r="V175" s="8"><v>Infinity</v></c>', b'<c r="V175" s="7" t="inlineStr"><is><t>8E5529</t></is></c>')
        print('Replaced Infinity in sheet1.xml!')
    out_zip.writestr(item, data)

out_zip.close()
out_buf.seek(0)

wb = openpyxl.load_workbook(out_buf)
print('SUCCESS! Workbook loaded without any error in openpyxl! Sheet names:', wb.sheetnames)
print('Cell V175 value:', wb.active['V175'].value)
