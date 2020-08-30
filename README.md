# ProxyPool

简易高效的代理池，提供如下功能：

* 定时抓取免费代理网站，简易可扩展。
* 使用 Redis 对代理进行存储并对代理可用性进行排序。
* 定时测试和筛选，剔除不可用代理，留下可用代理。
* 提供代理 API，随机取用测试通过的可用代理。

代理池原理解析可见「[如何搭建一个高效的代理池](https://cuiqingcai.com/7048.html)」。

## 安装过程

### 需要环境

- Python>=3.7
- Redis

### 安装依赖包

```bash
pip3 install -r requirements.txt
```

### 安装和配置 Redis

本地安装 Redis、Docker 启动 Redis、远程 Redis 都是可以的，只要能正常连接使用即可。

修改 .env 文件中的redis连接字符串为自己的redis环境：

```bash
REDIS_URL = redis:[密码]//@IP:端口/db
```

默认设置（无密码）为：

```bash
REDIS_URL = redis://@localhost:6379/0
```

### 运行代理池

两种方式运行代理池，一种是 Tester、Getter、Server 全部运行，另一种是按需分别运行。

一般来说可以选择全部运行，命令如下：

```bash
python3 run.py
```

运行之后会启动 Tester、Getter、Server，这时访问 [http://localhost:5555/random](http://localhost:5555/random) 即可获取一个随机可用代理。

或者如果你弄清楚了代理池的架构，可以按需运行，命令如下：

```bash
python3 run.py -p getter tester ...
```

这里 -p 也可以改为 --processor ，后面可以跟getter、tester、server中的一个多个，未添加则不运行。

## 使用

成功运行之后可以通过 [http://localhost:5555/random](http://localhost:5555/random) 获取一个随机可用代理。

可以用程序对接实现，下面的示例展示了获取代理并爬取网页的过程：

```python
import requests

proxypool_url = 'http://127.0.0.1:5555/random'
target_url = 'http://httpbin.org/get'

def get_random_proxy():
    """
    get random proxy from proxypool
    :return: proxy
    """
    return requests.get(proxypool_url).text.strip()

def crawl(url, proxy):
    """
    use proxy to crawl page
    :param url: page url
    :param proxy: proxy, such as 8.8.8.8:8888
    :return: html
    """
    proxies = {'http': 'http://' + proxy}
    return requests.get(url, proxies=proxies).text


def main():
    """
    main method, entry point
    :return: none
    """
    proxy = get_random_proxy()
    print('get random proxy', proxy)
    html = crawl(target_url, proxy)
    print(html)

if __name__ == '__main__':
    main()
```

运行结果如下：

```bash
get random proxy 116.196.115.209:8080
{
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.22.0", 
    "X-Amzn-Trace-Id": "Root=1-5e4d7140-662d9053c0a2e513c7278364"
  }, 
  "origin": "116.196.115.209", 
  "url": "https://httpbin.org/get"
}
```

可以看到成功获取了代理，并请求 httpbin.org 验证了代理的可用性。

## 可配置项

代理池可以通过设置 .env 文件中的环境变量来配置一些参数。

### 环境

* FLASK_ENV：运行环境，可以设置 development、production，即开发、生产环境，默认 development

### Redis 连接

* REDIS_URL：Redis 连接字符串
* REDIS_KEY：Redis 储存代理使用字典的名称

### 处理器

* CYCLE_TESTER：Tester 运行周期，即间隔多久运行一次测试，默认 20 秒
* CYCLE_GETTER：Getter 运行周期，即间隔多久运行一次代理获取，默认 100 秒
* TEST_URL：测试 URL，默认百度
* TEST_BATCH：批量测试数量，默认 20 个代理
* TEST_TIMEOUT：测试超时时间，默认 10 秒
* TEST_VALID_STATUS：测试有效的状态吗
* API_HOST：代理 Server 运行 Host，默认 0.0.0.0
* API_PORT：代理 Server 运行端口，默认 5555
* API_THREADED：代理 Server 是否使用多线程，默认 true

### 日志

* LOG_DIR：日志相对路径
* LOG_RUNTIME_FILE：运行日志文件名称
* LOG_ERROR_FILE：错误日志文件名称

## 扩展代理爬虫

代理的爬虫均放置在 proxypool/crawlers 文件夹下，目前对接了有限几个代理的爬虫。

若扩展一个爬虫，只需要在 crawlers 文件夹下新建一个 Python 文件声明一个 Class 即可。

写法规范如下：

```python
from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler

BASE_URL = 'http://www.664ip.cn/{page}.html'
MAX_PAGE = 5

class Daili66Crawler(BaseCrawler):
    """
    daili66 crawler, http://www.66ip.cn/1.html
    """
    urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE + 1)]
    
    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        trs = doc('.containerbox table tr:gt(0)').items()
        for tr in trs:
            host = tr.find('td:nth-child(1)').text()
            port = int(tr.find('td:nth-child(2)').text())
            yield Proxy(host=host, port=port)
```

在这里只需要定义一个 Crawler 继承 BaseCrawler 即可，然后定义好 urls 变量和 parse 方法即可。

* urls 变量即为爬取的代理网站网址列表，可以用程序定义也可写成固定内容。
* parse 方法接收一个参数即 html，代理网址的 html，在 parse 方法里只需要写好 html 的解析，解析出 host 和 port，并构建 Proxy 对象 yield 返回即可。

网页的爬取不需要实现，BaseCrawler 已经有了默认实现，如需更改爬取方式，重写 crawl 方法即可。

## LICENSE

MIT
