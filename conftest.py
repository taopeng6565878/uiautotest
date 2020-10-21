import pytest
from data.readelement import *
from data.readcase import *
from data.readconfig import *
from base.driver import *
from tool.logging import *

readcase = readcase()
readelement = readelement()
readconfig = readconfig()
rdr = driver()
log = log()
overalldict = {}

@pytest.fixture(scope="session", autouse=True)
def prepare():
    log.info('Start Test')
    configpath = 'casefile\config.ini'
    overalldict['configpath'] = configpath
    config = dict(readconfig.config_read(configpath))
    for k in config:
        overalldict.update(dict(config[k]))
    casedict = readcase.get_data(overalldict.get('casefile'))
    readelement.get_data(overalldict.get('elementfile'))
    casename = casedict.keys()
    #print(casename)

    rdr.setdriver(overalldict.get('browsertype'), overalldict.get('browserpath'), overalldict.get('MoboleModel'))
    yield
    rdr.closedriver()


@pytest.fixture(scope="function", autouse=True)
def deletecookie():
    rdr.getdriver().delete_all_cookies()




@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = '../report/'+item.name.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra

def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        #item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")



def _capture_screenshot(name):
    rdr.getdriver().get_screenshot_as_file(name)
