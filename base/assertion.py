import pytest
import re
from business.replacevar import *
from tool.logging import *


class assertion:
    replace = replacevar()
    conekey = '__$$$$__'
    errorlist = []

    def assertfunction(self, rownum, expect):

        expect = expect.replace('\,', self.conekey)
        expectlist = expect.split(',')

        if len(expectlist) != 0:
            if expect == '':
                return ''
            else:
                for i in expectlist:
                    exp = re.split(r'([==,!==,>,<,>=,<=,!=,=]+)', i, 1)
                    expectpram = self.replace.replacevar(exp[0])
                    assertsign = exp[1]
                    actualparam = self.replace.replacevar(exp[2])
                    expect = expectpram.replace(self.conekey, ',')
                    actual = actualparam.replace(self.conekey, ',')
                    logging.info(
                        '行号:' + str(rownum) + ' ' + 'Assert:' + expect+ ' ' + assertsign+ ' ' + actual)
                    try:
                        self.assertion(expect, actual, assertsign)
                    except AssertionError as e:
                        logging.error('Error ' + repr(e))
                        self.errorlist.append(repr(e))  # 断言失败，往errorlist写信息
                    except Exception as e:
                        logging.error('Error ' + repr(e))
                        raise e
        return self.errorlist

    def assertion(self, expect, actual, assertsign):
        global act

        if assertsign == '==':
            try:
                act = (eval(expect) - eval(actual) == 0)
            except  Exception as e:
                if expect == '' or actual == '':
                    act = (expect == actual)
                else:
                    act = (expect == actual)
        elif assertsign == '!==':
            act = (expect != actual)
        elif assertsign == '<':
            try:
                act = (eval(expect) - eval(actual) < 0)
            except  Exception as e:
                logging.error('Error ' + repr(e))
                self.errorlist.append(repr(e))  # 断言失败，往errorlist写信息
        elif assertsign == '>':
            try:
                act = (eval(expect) - eval(actual) > 0)
            except  Exception as e:
                logging.error('Error ' + repr(e))
                self.errorlist.append(repr(e))  # 断言失败，往errorlist写信息
        elif assertsign == '<=':
            try:
                act = (eval(expect) - eval(actual) <= 0)
            except  Exception as e:
                logging.error('Error ' + repr(e))
                self.errorlist.append(repr(e))  # 断言失败，往errorlist写信息
        elif assertsign == '>=':
            try:
                act = (eval(expect) - eval(actual) >= 0)
            except  Exception as e:
                logging.error('Error ' + repr(e))
                self.errorlist.append(repr(e))  # 断言失败，往errorlist写信息
        elif assertsign == '!=':
            act = (actual not in expect)
        elif assertsign == '=':
            act = (actual in expect)
        assert True == act
