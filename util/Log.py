# -*- coding: utf-8 -*-
# !/usr/bin/python3
import logging
import logging.config
import logging.handlers
import os
from app import log_path

if not os.path.exists(log_path):
    os.mkdir(os.path.dirname(log_path))


def get_logger(TAG, file_name="crs", file_flag=False, level=logging.INFO):
    """
    按照文件大小进行分割
    :param TAG:
    :param file_name: 默认后缀为.log，不需要带后缀
    :param file_flag: 日志信息是否写入文件,默认不显示
    :param level:
    :return:
    """
    fmt = "[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s] %(message)s"
    formatter = logging.Formatter(fmt)
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.INFO)
    logger = logging.getLogger(TAG)
    # 切记以下两行不能顺序颠倒，会导致没条log有两次输出
    logger.addHandler(console)
    if file_flag:
        # formatter = logging.Formatter(
        #     '%(asctime)s  %(levelname)s  %(message)s')

        file_hanlder = logging.handlers.RotatingFileHandler(filename=log_path + file_name + ".log", encoding='utf-8',
                                                            maxBytes=1024 * 1024, backupCount=10)
        file_hanlder.setFormatter(formatter)
        logger.addHandler(file_hanlder)
    logger.setLevel(level)
    return logger
