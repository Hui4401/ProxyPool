from loguru import logger

from proxypool.storages.redis_client import RedisClient
from proxypool.setting import PROXY_NUMBER_MAX
from proxypool.crawlers import crawlers_cls


class Getter(object):
    """
    getter of proxypool
    """

    def __init__(self):
        """
        init db and crawlers
        """
        self.redis = RedisClient()
        self.crawlers = [crawler_cls() for crawler_cls in crawlers_cls]

    def is_full(self):
        """
        if proxypool if full
        return: bool
        """
        return self.redis.count() >= PROXY_NUMBER_MAX

    @logger.catch
    def run(self):
        """
        run crawlers to get proxy
        :return:
        """
        if self.is_full():
            return
        for crawler in self.crawlers:
            logger.info(f'crawler {crawler} to get proxy')
            proxies = crawler.run()
            if proxies:
                for proxy in proxies:
                    self.redis.add(proxy)
                logger.info(f'crawled {len(proxies)} proxies from {crawler}')
            else:
                logger.info(f'cannot crawl proxies from {crawler}')


if __name__ == '__main__':
    getter = Getter()
    getter.run()
