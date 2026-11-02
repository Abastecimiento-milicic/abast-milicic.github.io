# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import zipfile

fpath = r'C:\Users\david.benitez\Downloads\ANALISIS-MM_0365.xlsx'
with zipfile.ZipFile(fpath, 'r') as z:
    with z.open('xl/worksheets/sheet1.xml') as f:
        sheet_tree = ET.parse(f)
        sheet_root = sheet_tree.getroot()

ns = {'x': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
af = sheet_root.find('x:autoFilter', ns)
if af is not None:
    print("AutoFilter tag found! Attributes:", af.attrib)
else:
    print("No AutoFilter tag found!")

# Check dimension
dim = sheet_root.find('x:dimension', ns)
if dim is not None:
    print("Dimension:", dim.attrib)
