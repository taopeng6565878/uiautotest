import xlrd
from tool.logging import *

class readcase:
    dictall = {}

    def get_data(self, dir_case):
        logging.info('Read File:' + dir_case)
        #file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), dir_case)
        file = os.path.join(os.path.abspath('..'), dir_case)
        data = xlrd.open_workbook(file)
        tables = data.sheets()
        for table in tables:
            nor = table.nrows
            noc = table.ncols
            casename = []
            for k in range(1, nor):
                if table.cell_value(k, 0) != '':
                    casename.append(table.cell_value(k, 0))  # 遍历文件所有用例名称

            for name in casename:  # 按用例名称遍历，读取用例步骤
                dictcase = []
                namerow = 1
                nextnamerow = 1

                if casename.index(name) != len(casename) - 1:  # 判断是否是最后一条用例
                    namenext = casename[casename.index(name) + 1]
                    for i in range(1, nor):  # 获取用例名称行号和下一个用例名称行号
                        if table.cell_value(i, 0) == name:
                            namerow = i
                        if table.cell_value(i, 0) == namenext:
                            nextnamerow = i
                else:
                    for i in range(1, nor):
                        if table.cell_value(i, 0) == name:
                            namerow = i
                    nextnamerow = nor
                a = 1
                for n in range(namerow, nextnamerow):  # 两条用例名称行号之间的行数就是用例的行数
                    dictrow = {}

                    for j in range(1, noc):
                        title = table.cell_value(0, j)
                        ctype = table.cell(n, j).ctype  # 表格的数据类型
                        value = table.cell_value(n, j)
                        # if ctype == 2 and value % 1 == 0.0:  # ctype为2且为浮点
                        #     value = int(value)  # 浮点转成整型
                        dictrow[title] = value  # 遍历文件，将表头和单元格的值组成字典
                    steprownum = namerow + a
                    a += 1
                    dictrow['行号'] = steprownum  # 每条步骤存入行号
                    dictcase.append(dictrow)  # 将字典存入list  dictcase中，顺序为用例的步骤顺序
                self.dictall[name] = dictcase  # 将dictcase按用例名称存入字典{用例名称：[{步骤1字段},{步骤2字段},{步骤3字段}]}
        return self.dictall

    def get_datadict(self):
        return self.dictall
