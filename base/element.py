from selenium.webdriver.common.by import By
from conftest import overalldict
from tool.logging import *

class element:
    def getelement (self, driver, bytype, param, timeout):
        by = self.getby(bytype,param)
        element = self.findelement(driver,by,int(timeout))
        return element

    def getby(self, bytype, param):
        global by
        if bytype == 'xpath':
            by = (By.XPATH, param)
        elif bytype == 'id':
            by = (By.ID, param)
        elif bytype == 'name':
            by = (By.NAME, param)
        elif bytype == 'cssSelector':
            by = (By.CSS_SELECTOR, param)
        elif bytype == 'className':
            by = (By.CLASS_NAME, param)
        elif bytype == 'linkText':
            by = (By.LINK_TEXT, param)
        elif bytype == 'tagName':
            by = (By.TAG_NAME, param)
        elif bytype == 'partialLinkText':
            by = (By.PARTIAL_LINK_TEXT, param)
        #element = self.findelement(driver, by)
        return by

    def findelement(self, driver, locator,timeout):
        global element
        elements = driver.find_elements(*locator)
        logging.debug('Element:'+str(locator))
        if len(elements) > 1:
            element = self.isvsible(elements)
        elif len(elements) == 0:
            waittime = 0
            while (len(elements) == 0) & (waittime < timeout):
                time.sleep(0.5)
                elements = driver.find_elements(*locator)
                waittime = waittime + 0.5
                logging.info('Auto Wait:' + str(waittime))
            if waittime >= timeout:
                element = None
            else:
                element = elements[0]
        else:
            element = elements[0]
        return element

    def isvsible(self, elements):
        global element
        i = 1
        for e in elements:
            if (e.is_displayed() & e.is_enabled()):
                element = e
                i += 1
        if i > len(elements):
            element = elements[0]
        return element


if __name__ == '__main__':
    el = element()
