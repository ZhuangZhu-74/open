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

base_path = os.getcwd()
sys.path.append(base_path)


class handle_excel():
    def __init__(self, xlsx_file):
        try:
            self.file = xlsx_file
            self.wb = self.load_excel()
            self.ws = None
            
        except Exception as e:
            print('init error: ')
            print(e)
            
    @staticmethod
    def use_backup(newname, old_file=None):
        '''
        backup file
        '''
        if old_file == None:
            old_file = "c:\test.xlsx"
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
    
    
    def load_excel(self):
        """
        load excel file
        """
        try:
            wb = openpyxl.load_workbook(self.file)
        except Exception as e:
            print(self.file)
            print(e)
            return None
        return wb
            
    def sheet_by_name(self, name=None):
        '''
        same method name like 'xlrd'
        '''
        
        all_sheet_names = self.wb.sheetnames
        if name != None:
            if name in all_sheet_names:
                self.ws = self.wb[name]
            else:
                print("No such name {}".format(name))
                return None
        else:
            self.ws = self.wb.active
        return self.ws
    
    def sheet_by_index(self, index=None):
        '''
        same method name like 'xlrd'
        index >= 0
        '''
        
        all_sheet_names = self.wb.sheetnames
        if index in range(len(all_sheet_names)):
            self.ws = self.wb[all_sheet_names[index]]
        elif index == None:
            self.ws = self.wb.active
        else:
            print("index illegal")
            return None
        return self.ws

    def save_wb(self, excel_file=None):
        if excel_file == None:
            excel_file = self.file
        else:
            excel_file = excel_file
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
    
    @property
    def howmany_rows(self):
        return self.ws.max_row - self.ws.min_row + 1
    
    @property
    def howmany_cols(self):
        return self.ws.max_column - self.ws.min_column + 1
        
        
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
    test_path = r'.'
    excel_file = os.path.join(test_path, 'test.xlsx')
    handle = handle_excel(excel_file)
    print(handle.ws)
    ws2 = handle.sheet_by_index()
    print(handle.ws)
    print(ws2)
    print(handle.get_row_values(1))
    
    
