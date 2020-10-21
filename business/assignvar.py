from conftest import overalldict
from business.replacevar import *


class assignvar:
    replace = replacevar()
    conekey = '__$$$$__'

    def assign(self, rownum, namelist, paramlist):
        if namelist != '':
            names = namelist.replace('\,', self.conekey)
            params = paramlist.replace('\,', self.conekey)
            namelist = names.split(',')
            paramlist = params.split(',')
            if len(namelist) != len(paramlist):
                logging.warn('行号:' + str(rownum) + ' 参数名称和参数个数不一致！')
            for i in range(len(namelist)):
                result = self.replace.replacevar(paramlist[i].replace(self.conekey, '\,'))

                if (namelist[i] != '') and (namelist[i] != None):
                    try:
                        #result = eval(result)  # eval执行result   可进行加减乘除等运算
                        result = result
                    except  Exception as e:
                        result = result
                    overalldict[namelist[i].replace(self.conekey, ',')] = result
                logging.info(
                    '行号:' + str(rownum) + ' 参数赋值:' + namelist[i].replace(self.conekey, '\,') + ' = ' + str(result))
