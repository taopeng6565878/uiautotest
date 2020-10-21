import pytest
from tool.logging import *

class verifydata:
    def verifycase(self,rownum, Handle, Name, Param, Expect, Variable, Function):
        if Handle =='':
            logging.error('行号:' + str(rownum) +' 操作列不能为空! ')
            pytest.fail()
        if Handle in ('点击','输入','获取文本','切换Iframe','双击','清空','上传','鼠标移至','执行用例','文本下拉选择','序号下拉选择'):
            if Name == '':
                logging.error('行号:' + str(rownum) +'节点名称不能为空！')
                pytest.fail()
        if Handle in ('输入', '上传', '打开网址','存入Cookie','加载Cookie','文本下拉选择', '序号下拉选择'):
            if Param == '':
                logging.error('行号:' + str(rownum) + '输入参数不能为空！')
                pytest.fail()
        if Handle in ('获取文本'):
            if Variable == '':
                logging.warning('行号:' + str(rownum) + '参数名称为空，文本未赋值给参数！')
        if Handle in ('参数赋值'):
            if Variable == '':
                logging.error('行号:' + str(rownum) + '参数名称不能为空! ')
                pytest.fail()

    def verifyelement(self,elementname, bytype, param):
        if bytype == '':
            logging.error('页面元素:' + elementname + '定位方式不能为空! ')
            pytest.fail()
        if param == '':
            logging.error('页面元素:' + elementname + '定位元素不能为空! ')
            pytest.fail()