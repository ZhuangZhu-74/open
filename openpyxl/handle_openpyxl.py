#coding=utf-8

'''
关于函数内变量的说明：
row：行的标签或行的数字下标，比如单元格C4 -> 4
col_tag：列的标签，比如单元格C4 -> C
col_index：列的数字下标，比如单元格C4 -> 3

使用 1-based；
行列必须是拆开的；
行你只可能传数字，列你传进来(必须大写字母)，有需要我再转就完了。

转换使用 openpyxl/utils/cell.py 中的 
  get_column_letter(x): 3 -> "C"
  column_index_from_string(str_col): ('A' -> 1)

'''

import sys, os, shutil
import openpyxl
from openpyxl.utils.cell import get_column_letter, column_index_from_string

from openpyxl.worksheet.worksheet import Worksheet

base_path = os.getcwd()
sys.path.append(base_path)

test_path = r'.'
excel_file = os.path.join(test_path, 'test.xlsx')


def use_backup(newname, old_file=excel_file):
    '''
    backup file
    '''
    
    if os.path.isfile(newname) and os.path.getsize(newname):
        pass
    else:
        os.path.isfile(old_file)
        shutil.copy(old_file, newname)
        '''
        global 分开写，不然会报错
        '''
        
    global excel_file
    excel_file = newname
    return excel_file
    
    
def load_excel():
    """
    load excel file
    """
    try:
        wb = openpyxl.load_workbook(excel_file)
    except Exception as e:
        print(excel_file)
        print(e)
        return None
    return wb

        
def sheet_by_name(wb, name=None):
    '''
    same method name like 'xlrd'
    '''
    
    all_sheet_names = wb.sheetnames
    if name != None:
        if name in all_sheet_names:
            ws = wb[name]
        else:
            print("No such name {}".format(name))
            return None
    else:
        ws = wb.active
    return ws

def sheet_by_index(wb, index=None):
    '''
    same method name like 'xlrd'
    index >= 0
    '''
    
    all_sheet_names = wb.sheetnames
    if index in range(len(all_sheet_names)):
        ws = wb[all_sheet_names[index]]
    elif index == None:
        ws = wb.active
    else:
        print("index illegal")
        return None
    return ws


class test_raw():
    def __init__(self, wb, ws):
        try:
            if isinstance(ws, Worksheet):
                self.ws = ws
            if isinstance(wb, openpyxl.Workbook):
                self.wb = wb
        except Exception as e:
            print('init error: ')
            print(e)

    def save_wb(self):
        self.wb.save(excel_file)
        
    @staticmethod
    def col_conv(col):
        '''
        give str or int of a sheet col
        return (col_index, col_tag) 
        '''
        if isinstance(col, str):
            col_tag = col
            col_index = column_index_from_string(col)
        elif isinstance(col, int):
            col_index = col
            col_tag = get_column_letter(col)
        return col_index, col_tag
        
        
    def get_all_values_by_rows(self):
        """
        get all data by list of rows in sheet.
        
        ws.values
        return a generator
        """
        
        return self.ws.values
        
    def get_all_values_by_cols(self):
        """
        get all data by list of cols in sheet.
        
        return a generator
        """
        
        for col in self.ws.iter_cols(values_only=True):
            yield col
    
    def get_row_values(self, row):
        """
        get one-row value, return a list
        row should start from 1
        """

        if row in range(self.ws.min_row, self.ws.max_row+1):
            return list(map(lambda i:i.value, self.ws[row]))
        else:
            return None
    
    def get_col_values(self, col):
        """
        get one-col value, return a list.
        
        if you want to get col B
        write get_col_values('B') or get_col_values(2)
        """
        
        col_index, col_tag = self.col_conv(col)
        
        if col_index in range(self.ws.min_column, self.ws.max_column+1):
            return list(map(lambda i:i.value, self.ws[col_tag]))
        else:
            return None
    
    def get_cell_value(self, row, col):
        """
        get cell value
        """
        
        col_index = self.col_conv(col)[0]
        
        if row in range(self.ws.min_row, self.ws.max_row+1):
            if col_index in range(self.ws.min_column, self.ws.max_column+1):
                return self.ws.cell(row, col_index).value
    
    def write_cell_value(self, row, col, value):
        """
        write a cell. but not save.
        """
        
        col_index = self.col_conv(col)[0]
        
        self.ws.cell(row, col_index, value)
        #self.wb.save(excel_file)

            
    def write_col_values(self, data, col, row_start=1):
        '''
        data: tuple or list for write, 
        col_tag: 
        row_start: start index of row, default is 1
        '''

        col_index = self.col_conv(col)[0]

        for i in range(len(data)):
            self.ws.cell(row_start+i, col_index, data[i])
    
    def write_row_values(self, data, row, col_start=1):
        '''
        data: tuple or list for write, 
        col_tag: 
        row_start: start index of row, default is 1
        '''
        
        col_index = col_start

        for i in range(len(data)):
            self.ws.cell(row, col_index+i, data[i])
            


if __name__ == '__main__':
    use_backup(r'.\test_backup.xlsx')
    wb = load_excel()
    ws = sheet_by_index(wb, 1)
    handle = test_raw(wb, ws)
    
    handle.write_cell_value(6, 6, "newtest")
    print(handle.get_cell_value(row=6, col=6))
    
    handle.write_col_values(['a','b','c'], 8, 3)
    print(handle.get_col_values(8))
    
    handle.write_row_values(['a','b','c'], 8, 3)
    print(handle.get_row_values(8))
    
    handle.save_wb()
    
    
