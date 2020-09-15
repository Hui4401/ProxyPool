import pkgutil
import inspect

from proxypool.crawlers.base import BaseCrawler


# load classes subclass of BaseCrawler
classes = []
for finder, name, is_pkg in pkgutil.iter_modules(__path__):
    module = finder.find_module(name).load_module(name)
    for name, value in inspect.getmembers(module):
        if inspect.isclass(value) and issubclass(value, BaseCrawler) \
                and not getattr(value, 'ignore', False):
            classes.append(value)

crawlers = classes

