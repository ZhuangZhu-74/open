#coding=utf-8

import os, sys
sys.path.append(os.getcwd())

from Base.BaseRequest import BaseRequest as BR
from util.handle_json import handle_json
from util.handle_ini import handle_ini
from util.handle_excel import handle_excel
from util.handle_result import handle_result

class RunMain:
    def __init__(self):
        self.hj = handle_json()
        self.hi_case = handle_ini(r'../Config/excel_col.ini')
        self.hi_srv = handle_ini()
        self.he = handle_excel(r"C:\Users\ylliu\Desktop\API_test\test.xlsx")
        self.he.ws = self.he.sheet_by_index()
        self.br = BR()
        self.hr = handle_result()
        
    def check_case_line_valid(self):
        '''
        该函数用于校验 case_line 必填栏目是否为空
        '''
        pass
        
    
    def run_case(self):
        '''
        根据 case_line 执行BR.run_main()
        '''
        records = self.he.howmany_rows
        # skip first line
        for lineno in range(2, records+1):
            case = self.he.get_row_values(lineno)
            
            if case[self.hi_case.isrun_col] == 'yes':
                caseid = case[self.hi_case.caseid_col]
                method = case[self.hi_case.httpmethod_col]
                uri =  case[self.hi_case.uri_col]
                data =  case[self.hi_case.data_col]
                
                exp_method = case[self.hi_case.exp_method_col]
                exp_data = case[self.hi_case.exp_data_col]
                
                url = str(self.hi_srv.get_value("project", "host")) + uri
                
                res = self.br.run_main(method, url, data)
                
                if exp_method == "msg_code":
                    actual_code = res.get('errorcode')
                    actual_desc = res['errordesc']
                    expect_desc = self.hr.get_msg(uri, actual_code)
                    if expect_desc == actual_desc:
                        print("{} PASSED".format(caseid))
                        '''
                        由于在 ini 文件中我们以 python 下标计算(0-base), 但是写入表格是以 1-base， 所以加一
                        '''
                        self.he.write_cell_value(lineno, self.hi_case.run_result_col +1, "pass")
                    else:
                        error_data = "msg_code: '{}' '{}' not compared".format(expect_desc, actual_desc)
                        print("{} FAILED".format(caseid))
                        self.he.write_cell_value(lineno, self.hi_case.run_result_col +1, "fail")
                        self.he.write_cell_value(lineno, self.hi_case.error_data_col +1, error_data)
                        
                elif exp_method == "text":
                    if res == exp_data:
                        print("{} PASSED".format(caseid))
                        self.he.write_cell_value(lineno, self.hi_case.run_result_col +1, "pass")
                    else:
                        error_data = "text: '{}' '{}' not compared".format(res, exp_data)
                        print("{} FAILED".format(caseid))
                        self.he.write_cell_value(lineno, self.hi_case.run_result_col +1, "fail")
                        self.he.write_cell_value(lineno, self.hi_case.error_data_col +1, error_data)
                        
                elif exp_method == 'json':
                    actual_code = res.get('errorcode')
                    if actual_code == '10000':
                        status = "Success"
                    elif actual_code == '10001':
                        status = "UserName Error"
                    
                    except_result = self.hr.get_json(uri, status)
                    compare_result = self.hr.compare_json(except_result, res.get(status))
                    if compare_result:
                        print("{} PASSED".format(caseid))
                        self.he.write_cell_value(lineno, self.hi_case.run_result_col +1, "pass")
                    else:
                        error_data = "json: '{}' '{}' not compared".format(except_result, compare_result)
                        print("{} FAILED".format(caseid))
                        self.he.write_cell_value(lineno, self.hi_case.run_result_col +1, "fail")
                        self.he.write_cell_value(lineno, self.hi_case.error_data_col +1, error_data)
                    
                self.he.save_wb()
                        
                        

if __name__ == '__main__':
    rm = RunMain()
    rm.run_case()
        