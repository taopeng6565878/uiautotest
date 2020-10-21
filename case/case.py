import os
import sys

from case.main_run import main_run
from business.runcase import *
from tool.logging import *
import pytest

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


class Test_case:
    run = runcase()
    #反射调用main_run，获取要执行用例名称列表prepare
    dd = main_run()
    tager_func = getattr(dd, 'getcasename')
    prepare = tager_func()

    @pytest.mark.parametrize('casename', prepare)
    def test_p001(self, casename):
        self.run.run(casename)




if __name__ == "__main__":
    pytest.main(['-s', 'case.py', '--html=../report/Result_test.html'])
    # cmd = 'pytest -s case.py --reruns 1 --html=../report/Result_test.html --self-contained-html'
    # os.system(cmd)
    # pytest -s case.py --reruns 1 --html=../report/Result_test.html --self-contained-html
