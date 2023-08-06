# 引入构建包信息的模块
from setuptools import setup, find_packages

# 定义发布的包文件的信息
setup(
    name="singer",  # 发布的包文件名称
    version="0.1.0",   # 发布的包的版本序号
    description="singer script",  # 发布包的描述信息
    author="shay",   # 发布包的作者信息
    author_email="shoy160@qq.com",  # 作者联系邮箱信息
    url="https://github.com/shoy160/python-singer",
    keywords=[],
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.6',
    zip_safe=False
)

# python setup.py build
# python setup.py sdist
# pip install twine
# twine upload dist/*
