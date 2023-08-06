#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : zb
# @Time    : 2020/11/17 23:21
# @Blog    : https://blog.zbmain.com

import platform
import os

# 自动判断当前系统环境
sys_ = platform.system().lower()
# 获取公共数据路径
__common_data_path = sys_ == 'linux' and '/home/common/' or sys_ == 'darwin' and '/Users/common/' or 'C:\\Users/common/'
'''
    Linux|Mac|Win 运行环境下数据文件绝对路径地址
    [Linux|Mac|Win]
    ._join()
'''


def _join(filepath):
    '''
    绝对数据路径拼接

    :param filepath:
    :return: /common/ [filepath]
    '''
    return os.path.join(__common_data_path, filepath)


if __name__ == '__main__':
    print(_join('main.py'))
