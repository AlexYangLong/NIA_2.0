import re


def check_param_format(param_name, pattern_list=None):
    """
    检查字符串格式
    :param param_name:  待检查字符串
    :param pattern_list:  正则表达式列表
    :return:  匹配返回True,否则False
    """
    if not (pattern_list and isinstance(pattern_list, list)):
        return False
    for pattern in pattern_list:
        if re.match(pattern, param_name):
            return True
    return False
