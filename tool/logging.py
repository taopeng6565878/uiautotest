# coding:utf-8

import logging
import os
import time
import logging.handlers
class log:
    def __init__(self):
        self.logger = logging.getLogger("")
        # 设置输出的等级
        LEVELS = {'NOSET': logging.NOTSET,
                  'DEBUG': logging.DEBUG,
                  'INFO': logging.INFO,
                  'WARNING': logging.WARNING,
                  'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL}
        # 创建文件目录
        logs_dir = "../logs"
        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
            pass
        else:
            os.mkdir(logs_dir)
        # 修改log保存位置
        timestamp = time.strftime("%Y-%m-%d", time.localtime())
        log_filename = '%s.log' % timestamp
        log_file_path = os.path.join(logs_dir, log_filename)
        rotating_file_handler = logging.handlers.RotatingFileHandler(filename=log_file_path,
                                                                     maxBytes=1024 * 1024 * 5,
                                                                     backupCount=5,encoding='utf-8')
        # 设置输出格式
        formatter = logging.Formatter('[%(asctime)s] '
                                      '[%(levelname)s] '
                                      '%(message)s',
                                      '%Y-%m-%d %H:%M:%S')
        # formatter = logging.Formatter('%(asctime)s - %(filename)s:[line:%(lineno)s] - %(name)s - %(message)s')
        rotating_file_handler.setFormatter(formatter)
        # 控制台句柄
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        # 添加内容到日志句柄中
        self.logger.addHandler(rotating_file_handler)
        self.logger.addHandler(console)
        self.logger.setLevel(logging.INFO)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message, exc_info=1)

    def error(self, message):
        self.logger.error(message, exc_info=1)


