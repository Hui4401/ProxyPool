import attr


@attr.s(auto_attribs=True)
class Proxy(object):
    """
    proxy schema
    """
    host: str = None
    port: int = None
    
    def __str__(self):
        """
        to str like 8.8.8.8:8888
        """
        return f'{self.host}:{self.port}'


if __name__ == '__main__':
    proxy = Proxy(host='8.8.8.8', port=8888)
    print('proxy', proxy)
