from distutils.core import setup

setup(
    name="ModuleTest1", # 对外我们模块的名称，即新建目录下的python包名
    version="1.0.0",  #发布版本号
    description="首个模板，待测试",  #版本内容描述
    author="zeonLam", #作者
    url="",          # 服务器地址
    author_email="zeonLam@gmail.com", #联系邮箱
    py_modules=["ModuleTest1.csvOpa","ModuleTest1.exception","ModuleTest1.测试文件2"]  #发布模块列表
)