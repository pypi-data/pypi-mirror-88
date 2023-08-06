# 引入构建包信息的模块
from distutils.core import setup

# 定义发布的包文件的信息
setup(
    name="singer",  # 发布的包文件名称
    version="0.0.1",   # 发布的包的版本序号
    description="singer script",  # 发布包的描述信息
    author="shay",   # 发布包的作者信息
    author_email="shoy160@qq.com",  # 作者联系邮箱信息
    py_modules=[
        '__init__',
        'main',
        'config'
    ]  # 发布的包中的模块文件列表
)

# python setup.py build
# python setup.py sdist
# pip install twine
# twine upload dist/*
