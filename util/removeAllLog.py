# -*- coding:utf8 -*-
import os

# 清空log文件夹下的所有文件
file_dir = "../log"
for root, dirs, files in os.walk(file_dir):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))
