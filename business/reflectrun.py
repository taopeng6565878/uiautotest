from selenium.common.exceptions import NoSuchElementException, WebDriverException, StaleElementReferenceException

from base.browser import *
from conftest import *
from business.replacevar import replacevar
from tool.verifydata import verifydata


class reflectrun:
    replace = replacevar()
    verify = verifydata()
    def refrun(self, rownum, handle,dr, element, param):
        result = ''
        rbr = browser(dr, param, element)
        if hasattr(rbr, handle):
            try:
                func = getattr(rbr, handle)
                result = func()
            except TimeoutError as e:
                dr.execute_script('windows.stop()')
                logging.error('行号:' + str(rownum) + 'TimeoutError：windows.stop ' + repr(e))
            except NoSuchElementException as ne:
                timeout = 0
                while (('NoSuchElementException' in repr(ne))) & (timeout < int(overalldict.get('timeout'))):
                    time.sleep(0.5)
                    try:
                        func = getattr(rbr, handle)
                        result = func()
                    except NoSuchElementException:
                        timeout = timeout + 0.5
                        logging.info('Auto Wait:' + str(timeout))
            rbr = browser(dr, None, None)
            func = getattr(rbr, 'switchtowindow_closeOthers')
            func()
            if result is None:
                result =''
        return result

