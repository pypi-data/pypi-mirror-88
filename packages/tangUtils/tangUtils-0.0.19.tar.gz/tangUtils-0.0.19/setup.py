#!/usr/bin/env python
# coding: utf-8

"""
see
  https://zhuanlan.zhihu.com/p/26159930
  https://pypi.org/project/twine/

1. python setup.py sdist
2. twine upload dist/tangUtils-0.0.19.tar.gz
"""

from setuptools import setup

setup(
    name='tangUtils',
    version='0.0.19',
    author='xiaomingtang',
    author_email='1038761793@qq.com',
    url='https://github.com/xiaomingTang/python-utils',
    description=u'文件/目录相关utils',
    packages=['tangUtils'],
    install_requires=[
      "pillow"
    ],
    entry_points={
        'console_scripts': [
        ]
    }
)