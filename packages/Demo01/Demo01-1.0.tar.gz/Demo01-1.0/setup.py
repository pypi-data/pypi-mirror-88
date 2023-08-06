#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    @Author: lrq
    @Blog: https://blog.csdn.net/qq_44214671
    @Time: 2020/12/17 15:53
    @Desc:
"""
from distutils.core import setup


setup(
    name='Demo01',  # 对外我们模块的名字
    version='1.0',  # 版本号
    description='测试本地发布模块',  # 描述
    author='runqian_lee',  # 作者
    author_email='runqian0813@163.com',
    py_modules=['Demo01.demo1', 'Demo01.demo2'],  # 要发布的模块
)
