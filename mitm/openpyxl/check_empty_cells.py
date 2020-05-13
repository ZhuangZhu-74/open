#coding=utf-8

import sys
import openpyxl

# argument 1 should be excel_file.
excel_file = sys.argv[1]

try:
    wb = openpyxl.load_workbook(excel_file)
except Exception as e:
    print(e)
    exit(2)

for ws in wb.sheetnames:
    # return sheet object.
    wx = wb[ws]

    for x,y in enumerate(wx.columns, start=1):
        if set(list(map(lambda a:a.value, y))) == set([None]):
            print('{} {} {}'.format(ws, 'empty_col', x))

    for x,y in enumerate(wx.rows, start=1):
        if set(list(map(lambda a:a.value, y))) == set([None]):
            print('{} {} {}'.format(ws, 'empty_row', x))

