import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from data.readconfig import *
from data.readcase import *

readconfig = readconfig()
readcase = readcase()

startdict = {}


class main_run:
    casenames = []

    def mainfunc(self):
        cmd = 'pytest -s case.py --reruns 1 --html=../report/Result_test.html --self-contained-html'
        os.system(cmd)

    #解析用例中第一行开关为ON的用例名称
    def getcasename(self):
        configpath = 'casefile/config.ini'
        startdict['configpath'] = configpath
        config = dict(readconfig.config_read(configpath))
        for k in config:
            startdict.update(dict(config[k]))
        casedict = readcase.get_data(startdict.get('casefile'))
        names = list(casedict.keys())
        for casename in names:
            casestep = casedict.get(casename)
            valve = casestep[0].get('开关')
            if valve == 'ON':
                self.casenames.append(casename)
        return self.casenames


if __name__ == "__main__":
    main_run().mainfunc()
