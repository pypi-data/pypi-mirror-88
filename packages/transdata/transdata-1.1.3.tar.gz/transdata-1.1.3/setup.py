#!/usr/bin/python
# -*- coding: UTF-8 -*-

from os import path as os_path
from setuptools import setup, find_packages

this_directory = os_path.abspath(os_path.dirname(__file__))
print(this_directory)

# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

# 获取依赖
# def read_requirements(filename):
#     return [line.strip() for line in read_file(filename).splitlines()
#             if not line.startswith('#')]

setup(
    name='transdata',  # 包名
    python_requires='>=3.4.0',  # python环境
    version='1.1.3',  # 包的版本
    description="Test publish own pypi.",  # 包简介，显示在PyPI上
    long_description=read_file('README.md'),  # 读取的Readme文档内容
    long_description_content_type="text/markdown",  # 指定包文档格式为markdown
    author="petzhang",  # 作者相关信息
    author_email='zhanghauchao-ghq@sinosig.com',
    url='https://github.com/zhc7335/oracle2mysql',
    # 指定包信息，还可以用find_packages()函数
    packages=find_packages(),
    # package_data = {
    #     'parser_code': ['metadata/shared/*.json']
    # },#读取需要的数据文件
    install_requires=[
        'cx_Oracle',
        'xlwt',
        'pandas',
        'pymysql',
    ],  # 指定需要安装的依赖
    include_package_data=True,
    license="MIT",
    keywords=['transdata'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities'
    ],
)