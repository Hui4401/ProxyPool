import pkgutil
import inspect

from proxypool.crawlers.base import BaseCrawler


'''加载所有 BaseCrawler 的子类'''
classes = []
# 递归获取当前路径下所有包和模块
for finder, name, _ in pkgutil.walk_packages(__path__):
    # 加载模块
    module = finder.find_module(name).load_module(name)
    # 获取模块所有属性并筛选需要的类
    for _, value in inspect.getmembers(module):
        if inspect.isclass(value) and issubclass(value, BaseCrawler)  \
                and value is not BaseCrawler and not getattr(value, 'ignore', False):
            classes.append(value)

crawlers_cls = classes

