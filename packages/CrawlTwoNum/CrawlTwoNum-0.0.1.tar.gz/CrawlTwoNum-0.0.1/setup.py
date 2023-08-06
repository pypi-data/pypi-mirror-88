#-*- coding:utf-8 -*-


'''
@Time  : 2020/12/14 17:24
@Author: ZhangQiang
'''


import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CrawlTwoNum", # Replace with your own username
    version="0.0.1",
    author="Juliet",
    author_email="zh_juiet@163.com",
    description="a common package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zh-Juliet/CrawlTwoNum",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)