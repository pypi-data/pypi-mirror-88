#!/usr/bin/env python
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

# with open("README.md", "rb") as fh:
#     long_description = fh.read()

setup(
    name='GFP_TEST',  # 包名，之后pip install是用到
    version='0.1.0',  # 版本号, 之后有新版本能用到
    url='https://github.com/Miss-chan/pypi_package_test',  # 源代码托管地址
    install_requires=['scrapy>=1.5.1'],   # 列出所有依赖包
    packages=find_packages(),  # 如果打包的项目中有package文件，必须配置
    # py_modules=[],  # 如果打包的项目中有modules文件, 因为它不属于任何包。必须在单独的参数py_modules中提供它的模块名
    #
    # author="Zhongqiang Shen",  # 作者, 可有可无
    # author_email="",  # 邮箱, 可有可无
    # description="add douyin effect to image",   # 项目的简短描述, 可有可无
    # # 项目的详细描述，会显示在PyPI的项目描述页面，可直接README.md中的内容做详细描述, 可有可无
    # long_description=long_description,
    # long_description_content_type="text/markdown",  # 用于指定long_description的类型，可有可无
    # # classifiers - 其他信息，一般包括项目支持的Python版本，License，支持的操作系统。没有也不影响使用
    # classifiers=(
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    # ),
)
