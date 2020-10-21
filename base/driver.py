from selenium import webdriver
from tool.logging import *

class driver:
    def setdriver(self, browsertype, path, isMobole):
        if browsertype == 'ie':
            self.driver = self.getiedriver(path)

        elif browsertype == 'chrome':
            self.driver = self.getchromdriver(path)

        elif browsertype == 'firefox':
            self.driver = self.getfirefoxdriver(path)

    def getdriver(self):
        return self.driver

    def closedriver(self):
        self.driver.close()

    def getiedriver(self, path):
        dr = webdriver.ie
        return dr

    def getchromdriver(self, path):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        dr = webdriver.Chrome(path, options=options)
        dr.maximize_window()
        dr.set_page_load_timeout(20)

        return dr

    def getfirefoxdriver(self, path):
        dr = webdriver.firefox
        return dr


if __name__ == '__main__':
    aaa = driver()
    aaa.setdriver('chrome', 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', '')
    print(aaa.getdriver())
