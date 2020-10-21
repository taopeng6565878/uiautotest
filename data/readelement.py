import xlrd
from tool.logging import *

class readelement:
    dictc = {}
    def get_data(self,dir_case):
        logging.info('Read File:' + dir_case)
        #file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), dir_case)
        file = os.path.join(os.path.abspath('..'), dir_case)
        data = xlrd.open_workbook(file)
        tables = data.sheets()
        for table in tables:
            nor = table.nrows
            noc = table.ncols

            for i in range(1, nor):
                dict = {}
                for j in range(noc):
                    title = table.cell_value(0, j)
                    value = table.cell_value(i, j)
                    dict[title] = value#遍历文件，将表头和单元格的值组成dict{接口名称:1,方法:2}
                self.dictc[dict.get(table.cell_value(0, 0))]=dict
        return  self.dictc

    def get_datadict(self):
        return self.dictc

if __name__ == '__main__':
    read = readelement()
    print(read.get_data('file\Element_ruirenyun.xls'))