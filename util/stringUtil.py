# -*- coding:utf8 -*-
import re
from util.strings import func_return, _stop_words


def sql_str(sql):
    return str(sql).replace('"', '""').replace("'", "''")


def is_num(text):
    for x in text:
        if x in range(0, 10):
            return True
    return False


def to_int(text):
    # 提取字符串中的数字、返回数字类型
    rs = to_num(text)
    try:
        rs = int(rs)
    except ValueError:
        rs = 0
    finally:
        return rs


def to_num(text):
    """
    返回字符串
    :param text:
    :return:
    """
    text = clean(text)
    rs = re.sub('[\D\s]', "", text)
    return rs


def to_money(text):
    text = clean(text)
    rs = re.sub('[\$,]', "", text)
    try:
        rs = float(rs)
    except ValueError:
        rs = 0
    finally:
        return rs


def list_to_string(list=[]):
    return '\t'.join(list)


def dict_to_string(tag, dict={}):
    return dict[tag]


def list_dict_to_string(tag, list=[]):
    rs = []
    for cell in list:
        if type(cell) == type({}):
            rs.append(str(cell[tag]).strip())
    return '\t'.join(rs)


def clean(text):
    # 清除字符串中的空白字符,包括换页（‘\f’）、换行（‘\n’）、回车（‘\r’）、水平制表符（‘\t’）、垂直制表符（‘\v’），以及多个连续的空格
    if not text:
        return ""
    rs = re.sub("[\n\t\v\f]", '', text.strip())
    rs = re.sub(' {1,}', ' ', rs)
    return rs


def segment(text):
    """
    英文分词,包括词的清洗
    :param text:句子
    :return:返回分词结果-list
    """
    text = clean(text)
    rs = []
    data = []
    rs = text.lower().split()
    data = [x for x in rs if x not in _stop_words]
    return data


def deep_select(selector, order=-1, xpath="", return_type="str"):
    """
    执行xpath检索，返回检索结果,当出错时返回："",避免出错
    :param selector:
    :param xpath:
    :param order:
    :return:
    """
    rs = None
    try:
        rs = selector.xpath(xpath)
    except Exception as e:
        rs = func_return[return_type]
    finally:
        if order < 0:
            if not rs:
                return ''
            return rs
        if rs and len(rs) >= order:
            return rs[order]


def flatten(array=[], dtype='i'):
    """
    将多维数组降到一维
    :param array:
    :param type:数组中元素的类型，分为int:i和str:s,默认为i
    :return: []
    """
    rs = []
    temp = str(array).replace('[', '').replace(']', '')
    if dtype == 's':
        temp = temp.replace("'", '')
    rs = temp.split(', ')
    return rs



if __name__ == '__main__':
    a = segment("Exploring water data\n       21          with high school students in Flint, MI")
    print(a)
