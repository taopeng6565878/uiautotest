import configparser
from tool.logging import *

class readconfig:
    # 查询一条数据
    def config_read(self, path, section=None, key=None):
        logging.info('Read config:' + path)
        file = os.path.join(os.path.abspath('..'), path)
        self.config = configparser.ConfigParser()
        self.config.optionxform = str  # 修改config读取key为str类型，避免默认转为小写key
        self.config.read(file, encoding='UTF-8')
        if (key != None) & (section != None):
            value = self.config.get(section, key)
        elif section != None:
            value = self.config._sections[section]
        else:
            value = self.config._sections
        if len(value) == 0:
            try:
                raise Exception('NoconfigError')
            except Exception as e:
                logging.error('No config file:' + path)
        return value

    def config_sectionsnames(self, path):
        value = self.config.sections()
        return value

    def config_optionsnames(self, path, section):
        value = self.config.options(section)
        return value


if __name__ == '__main__':
    read = readconfig()
    read.config_read('dataconfig/config.ini')
    dict = read.config_optionsnames('dataconfig/config.ini', 'wms_db')
    print(dict)
