from business.reflectrun import *
from base.assertion import assertion
from business.assignvar import assignvar
from business.replacevar import replacevar
from tool.verifydata import verifydata
from base.element import *


class runcase:
    rrun = reflectrun()
    replace = replacevar()
    ass = assertion()
    assign = assignvar()
    verify = verifydata()
    casedict = readcase.get_datadict()
    rel = element()
    elementdict = readelement.get_datadict()
    errorlist = []

    def run(self, casename):
        logging.info('Start Case:' + casename)
        self.errorlist = []
        self.runcase(casename)
        if len(self.errorlist) > 0:  # 判断错误列表，数量大于0则本条用例fail
            pytest.fail()

    # 遍历casedict，按顺序执行用例
    def runcase(self, casename):
        casestep = self.casedict.get(casename)
        if casestep == None:
            logging.error('Can not find case:' + casename)
            pytest.fail()
        for step in casestep:
            valve = step.get('开关')
            RowNum = step.get('行号')
            if valve == 'ON':  # 判断开关，步骤是否执行
                Handle = step.get('操作')
                Name = step.get('元素名称')
                NameParam = step.get('元素参数')
                #if NameParam != '':
                overalldict['EleParam'] = NameParam
                Param = self.replace.replacevar(step.get('输入参数'))
                Expect = str(step.get('验证点'))
                Variable = str(step.get('参数名称'))
                Function = str(step.get('参数'))
                self.verify.verifycase(RowNum, Handle, Name, Param, Expect, Variable, Function)
                try:
                    self.DealHandle(RowNum, Handle, Name, Param, Expect, Variable, Function)
                except Exception as e:
                    logging.error('行号:' + str(RowNum) + 'Error: ' + repr(e))
                    raise e
            else:
                logging.debug('行号:' + str(RowNum) + ' Step is not running!')

    # 处理用例中的操作列
    def DealHandle(self, rownum, handle, name, param, expect, variable, function):
        handledict = {'点击': 'click', '输入': 'sendKeys', '获取文本': 'gettext', '打开网址': 'geturl', '存入Cookie': 'getcookies',
                      '加载Cookie': 'addcookie', '文本下拉选择': 'selectbytext', '序号下拉选择': 'selectbyindex',
                      '双击': 'doubleclick', '清空': 'clear', '鼠标移至': 'movetoelement', '刷新': 'refresh',
                      '切换Iframe': 'switchtoframe', '切换到窗口': 'switchtowindow', '上传文件': 'upload'}
        result = ''
        dr = rdr.getdriver()

        if handle == '参数赋值':
            self.assign.assign(rownum, variable, function)
            aresult = self.ass.assertfunction(rownum, expect)
            self.errorlist += aresult
        elif handle == '执行用例':
            logging.info('行号:' + str(rownum) + ' ' + handle + ':' + name)
            self.runcase(name)
            bresult = self.ass.assertfunction(rownum, expect)
            self.errorlist += bresult
        elif handle == '校验元素存在':
            logging.info('行号:' + str(rownum) + ' ' + handle + ':' + name)
            element = self.getelement(rownum, dr, name, int(overalldict.get('timeout')))
            result = element is not None
            cresult = self.ass.assertfunction(rownum, 'True=='+str(result))
            self.errorlist += cresult
        elif handle == '校验元素不存在':
            logging.info('行号:' + str(rownum) + ' ' + handle + ':' + name)
            element = self.getelement(rownum, dr, name, 0.6)
            result = element is None
            cresult = self.ass.assertfunction(rownum, 'True=='+str(result))
            self.errorlist += cresult
        else:
            rhandle = handledict.get(handle)
            element = self.getelement(rownum, dr, name, int(overalldict.get('timeout')))
            if element is None:
                logging.error('行号:' + str(rownum) + ' 未找到页面元素:' + name)
                pytest.fail()
            result = self.rrun.refrun(rownum, rhandle, dr, element, param)
            logging.info(
                '行号:' + str(rownum) + ' ' + handle + ':' + name + ' ' + overalldict.get('EleParam') + ' ' + param + ' ' + str(result))
            self.assign.assign(rownum, variable, str(result))
            assresult = self.ass.assertfunction(rownum, expect)
            self.errorlist += assresult

        return result

    def getelement(self, rownum, dr, elementname, timeout):
        ele = ''
        if elementname != '':
            element = self.elementdict.get(elementname)
            if element is None:
                logging.error('行号:' + str(rownum) + ' 未找到对应elementname：' + elementname)
                pytest.fail()
            bytype = element.get('定位方式')
            param = self.replace.replacevar(element.get('元素'))
            self.verify.verifyelement(elementname, bytype, param)
            ele = self.rel.getelement(dr, bytype, param, timeout)
        return ele


if __name__ == '__main__':
    run1 = runcase()
    # print(run1.reflect('tool.WL_UserFunction','readom',5))
    run1.replace.replacevar(
        '{"pageIndex":${ShipBatchNo_1}${ShipBatchNo_1}${ShipBatchNo_1}, "pageSize": ${__readomnum(${ShipBatchNo_1}${ShipBatchNo_1})}, "params": {}}')
