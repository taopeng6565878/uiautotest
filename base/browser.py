from selenium.common.exceptions import ElementNotVisibleException, WebDriverException
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from tool.logging import *


class browser:
    def __init__(self, dr, param, element):
        self.driver = dr
        self.param = param
        self.element = element

    def getcookies(self):
        cookies = self.driver.get_cookies()
        return cookies

    def getcookie(self):
        cookie = self.driver.get_cookie(self.param)  # param=cookiename
        return cookie

    def addcookie(self):
        for line in self.param.split('; '):
            cookie = {}
            key, value = line.split('=', 1)
            cookie['name'] = key
            cookie['value'] = value
            # cookiedict = eval(self.param)
            self.driver.add_cookie(cookie_dict=cookie)  # param=cookiedict

    def deleteallcookies(self):
        self.driver.delete_all_cookies()

    def geturl(self):
        self.driver.get(self.param)  # param=url

    def refresh(self):
        self.driver.refresh()

    def movetoelement(self):
        action = ActionChains(self.driver)
        action.move_to_element(self.element).perform()
        # self.driver.move_to_element(self.element)

    def switchtoframe(self):
        self.driver.switch_to_frame(self.element)

    def switchtowindow(self):
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])

    def switchtowindow_closeOthers(self):
        windows = self.driver.window_handles
        if len(windows) > 1:
            for i in range(len(windows) - 1):
                self.driver.close()
            self.driver.switch_to.window(windows[-1])

    def click(self):
        try:
            self.element.click()
        except WebDriverException as we:
            if 'is not clickable' in repr(we):
                self.driver.execute_script('arguments[0].click();', self.element)
            else:
                raise we
        time.sleep(0.3)

    def doubleclick(self):
        self.element.double_click()

    def clear(self):
        self.element.clear()

    def sendKeys(self):
        self.clear()
        self.element.send_keys(self.param)  # param=sendkeys

    def gettext(self):
        text = self.element.text
        return text

    def selectbytext(self):
        try:
            Select(self.element).select_by_visible_text(self.param)  # param=text
        except ElementNotVisibleException as e:
            self.driver.execute_script('arguments[0].setAttribute("style", "display:block")', self.element)
            Select(self.element).select_by_visible_text(self.param)  # param=text

    def selectbyindex(self):
        try:
            Select(self.element).select_by_index(self.param)  # param=index
        except ElementNotVisibleException as e:
            self.driver.execute_script('arguments[0].setAttribute("style", "display:block")', self.element)
            Select(self.element).select_by_index(self.param)  # param=index


if __name__ == '__main__':
    from base.driver import *
    from base.element import *

    dd = driver()
    el = element()

    dd.setdriver('chrome', 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', '')
    driver = dd.getdriver()

    br = browser(driver=driver, element='', param='http://192.168.1.111:8080/cloud/auth.html').geturl()
    br.sendKeys(el.getelement(driver, 'xpath', '//li[a[@data-text="客户中心"]]'), '12312')
    # br.geturl(driver, 'http://192.168.1.111:8080/cloud/auth.html')
    # br.addcookie(driver,"{'domain': '192.168.1.111', 'expiry': 2228974300, 'httpOnly': True, 'name': 'JSESSIONID', 'path': '/cloud', 'secure': False, 'value': 'CCC166B527BF469A940F9B0E6E0DC89B'}")
    # br.addcookie(driver,"{'name': 'JSESSIONID', 'path': '/cloud','value': 'CCC166B527BF469A940F9B0E6E0DC89B'}")
    # br.geturl(driver, 'http://192.168.1.111:8080/cloud/index.html')
    # br.click(el.getelement(driver, 'xpath', '//li[a[@data-text="客户中心"]]'))
    # br.switchtoframe(driver,el.getelement(driver,'id','paneContent'))
    # br.selectbytext(el.getelement(driver,'xpath','//select[@name="cooperate_status"]'),'正常合作')

    # dd.closedriver()
