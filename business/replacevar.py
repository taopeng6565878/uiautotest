from conftest import *
from tool.reflect import reflect


class replacevar:
    ref = reflect()
    varkey = '${'
    varlastkey = '}'
    funckey = '${__'
    funclastkey = '}'
    funcparamkey = ';'
    replacefunckey = '__$$__'  #处理函数标识符，防止与参数混合
    conekey = '__$$$__'        #处理\;，替换后再还原
    noparamkey = '__$$$$__{'   #处理参数未找到的情况，替换后再还原成参数调用原文本
    def replacevar(self, repstr):
        result = self.checkreplace(repstr)
        result = result.replace('\,',',')
        result = result.replace('\;',';')
        result = result.replace(self.noparamkey, self.varkey)
        return result

    def _replacevar(self, repstr):
        result = self.checkreplace(repstr)
        result = result.replace(self.noparamkey, self.varkey)
        return  result

    def checkreplace(self, repstr):
        replacestr = repstr
        if (self.funckey not in replacestr) and (self.varkey in replacestr)and (self.varlastkey in replacestr):
            # 将参数替换和函数替换分开处理，因为有可能参数的值是调用函数格式
            for i in range(replacestr.count(self.varkey)):
                replacestr = self.checkvar(replacestr,self.varkey,self.varlastkey)
        if (self.funckey in replacestr)and (self.funclastkey in replacestr) and (self.varkey not in replacestr):
            for i in range(replacestr.count(self.funckey)):
                replacestr = self.checkfunc(replacestr,self.funckey,self.funclastkey)
        if (self.funckey in replacestr) and (self.varkey in replacestr)and (self.varlastkey in replacestr):
            # 替换replacestr中函数的标识符 ${__ 为__$$__，防止与参数的标识符 ${ 搞混
            replacestr = replacestr.replace(self.funckey, self.replacefunckey)
            for i in range(replacestr.count(self.varkey)):
                # 截取参数名称，从后往前替换
                replacestr=self.checkvar(replacestr,self.varkey,self.varlastkey)
                # 替换replacestr中函数的标识符 ${__ 为__$$__，防止与参数的标识符 ${ 搞混
                replacestr = replacestr.replace(self.funckey, self.replacefunckey)
            replacestr = replacestr.replace(self.noparamkey, self.varkey)
            for i in range(replacestr.count(self.replacefunckey)):
                replacestr = self.checkfunc(replacestr, self.replacefunckey, self.varlastkey)
        return  replacestr

    def checkvar(self,replacestr,varkey,varlastkey):
        # 截取参数名称，从后往前替换
        varname = replacestr[replacestr.rfind(varkey) + len(varkey):replacestr.find(varlastkey, replacestr.rfind(
            varkey) + len(varkey))]
        if (varname in overalldict) and (overalldict.get(varname) != None):
            result = str(overalldict.get(varname))
            result = self.checkreplace(result)  # 递归调用，解决嵌套调用
            result = result.replace(',','\,')
            result = result.replace(';','\;')#将参数调用结果中的, ; 加\转义
            replacestr = replacestr.replace(self.varkey + varname + self.varlastkey, result)
        elif varname not in overalldict:
            replacestr = replacestr.replace(self.varkey + varname + self.varlastkey,
                                            self.noparamkey + varname + self.varlastkey)
        #elif overalldict(varname) == None:
        else:
            replacestr = replacestr.replace(self.varkey + varname + self.varlastkey,'')
        return  replacestr

    def checkfunc(self, replacestr,funckey,funclastkey):
        replacestr = replacestr.replace('\;', self.conekey)#处理函数内参数包含\;
        # 截取函数名称，从后往前查找
        funcname = replacestr[replacestr.rfind(funckey) + len(funckey):replacestr.find('(',replacestr.rfind(
                                                                                                        funckey) + len(
                                                                                                        funckey))]
        # 截取函数参数，从后往前查找
        funcparam = replacestr[replacestr.find('(', replacestr.rfind(funckey) + len(
            funckey)) + 1:replacestr.find(
            ')' + funclastkey, replacestr.rfind(funckey) + len(funckey))]
        paramlist = []
        if funcparam != '':
            funcparams = funcparam.replace('\,', ',')
            # 将参数按funcparamkey，转换为list
            funcparamlist = funcparams.split(self.funcparamkey)
            paramlist = []
            # 遍历list，将前面参数替换掉的replaceparamkey  替换回分号
            for l in funcparamlist:
                paramlist.append(l.replace(self.conekey, ';'))

        # 反射调用，传入的参数是一个list
        result = self.ref.reflect(overalldict.get('ReflectModule'), funcname, paramlist)
        result = result.replace(';', '\;')#将函数调用结果中的; 加\转义
        replacestr = replacestr.replace(self.replacefunckey + funcname + '(' + funcparam + ')' + self.funclastkey, str(result),1)
        replacestr = replacestr.replace(self.conekey,'\;')
        return  replacestr


if __name__ == '__main__':
    r = replacevar()
    print(r.replacevar('${__CutString(ConfigValue,"DefaultReceivingUnitGroup":",")}'))