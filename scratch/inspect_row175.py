# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import zipfile

fpath = r'C:\Users\david.benitez\Downloads\ANALISIS-MM_0365.xlsx'
with zipfile.ZipFile(fpath, 'r') as z:
    with z.open('xl/sharedStrings.xml') as f:
        sst_tree = ET.parse(f)
        sst_root = sst_tree.getroot()
        shared_strings = [elem.text for elem in sst_root.iter('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')]

    with z.open('xl/worksheets/sheet1.xml') as f:
        sheet_tree = ET.parse(f)
        sheet_root = sheet_tree.getroot()

ns = {'x': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
row175 = sheet_root.find('.//x:row[@r="175"]', ns)
headers_row = sheet_root.find('.//x:row[@r="1"]', ns)

if row175 is not None:
    for c in row175.findall('x:c', ns):
        ref = c.get('r')
        t = c.get('t')
        v = c.find('x:v', ns)
        val = v.text if v is not None else ""
        if t == 's':
            val = shared_strings[int(val)]
        print(f"{ref}: {repr(val)}")
