#coding=utf-8

import os, sys
sys.path.append(os.getcwd())

prj_path = os.path.dirname(os.getcwd())

import ddt
import unittest
from Base.BaseRequest import BaseRequest as BR
from util.handle_json import handle_json
from util.handle_ini import handle_ini
from util.handle_excel import handle_excel
from util.handle_result import handle_result
import HTMLTestRunner_cn

hd_xlsx = handle_excel(prj_path + r"\Case\test.xlsx")
hd_xlsx.ws = hd_xlsx.sheet_by_index()
data = list(hd_xlsx.get_all_values_by_rows(exclude_firstline=True))


@ddt.ddt
class RunMainDdt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hj = handle_json()
        cls.hi_case = handle_ini(r'../Config/excel_col.ini')
        cls.hi_srv = handle_ini()
        cls.br = BR()
        cls.hr = handle_result()
        
    
    @ddt.data(*data)
    def test_RunMain(self, data):
        if data[self.hi_case.isrun_col] == 'yes':
            caseid = data[self.hi_case.caseid_col]
            lineno = hd_xlsx.get_lineno_by_caseid(caseid)
            
            method = data[self.hi_case.httpmethod_col]
            uri =  data[self.hi_case.uri_col]
            req_data =  data[self.hi_case.data_col]
            
            exp_method = data[self.hi_case.exp_method_col]
            exp_data = data[self.hi_case.exp_data_col]
            
            url = str(self.hi_srv.get_value("project", "host")) + uri
            
            res = self.br.run_main(method, url, req_data)
            
                
            try:
                if exp_method == "msg_code":
                    
                    actual_code = res.get('errorcode')
                    actual_desc = res['errordesc']
                    expect_desc = self.hr.get_msg(uri, actual_code)
                    
                    try:
                        self.assertEqual(expect_desc, actual_desc)
                        hd_xlsx.write_cell_value(lineno, self.hi_case.run_result_col +1, "pass")
                    except Exception as e:
                        hd_xlsx.write_cell_value(lineno, self.hi_case.run_result_col +1, "fail")
                        raise e
                    
                elif exp_method == "text":
                    try:
                        self.assertEqual(res, exp_data)
                        hd_xlsx.write_cell_value(lineno, self.hi_case.run_result_col +1, "pass")
                    except Exception as e:
                        hd_xlsx.write_cell_value(lineno, self.hi_case.run_result_col +1, "fail")
                        raise e
                    
                elif exp_method == 'json':
                    actual_code = res.get('errorcode')
                    if actual_code == '10000':
                        status = "Success"
                    elif actual_code == '10001':
                        status = "UserName Error"
                    
                    except_result = self.hr.get_json(uri, status)
                    compare_result = self.hr.compare_json(except_result, res.get(status))
                    try:
                        self.assertTrue(compare_result)
                        hd_xlsx.write_cell_value(lineno, self.hi_case.run_result_col +1, "pass")
                    except Exception as e:
                        hd_xlsx.write_cell_value(lineno, self.hi_case.run_result_col +1, "fail")
                        raise e
                        
            except Exception as e:
                hd_xlsx.write_cell_value(lineno, self.hi_case.run_result_col +1, "fail")
                raise e
            finally:
                hd_xlsx.save_wb()
                        
                        

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(RunMainDdt)
    file_path = os.path.join(prj_path, "Report", "report.html")

    with open(file_path, 'wb') as f:
        runner = HTMLTestRunner_cn.HTMLTestRunner(stream=f,title="接口测试",description=u"测试报告",verbosity=2)
        runner.run(suite)
        
        
        
        
        
        
    