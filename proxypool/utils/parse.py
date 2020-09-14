import re


def parse_redis_connection_string(connection_string):
    """
    parse a redis connection string, for example:
    redis://[password]@host:port
    rediss://[password]@host:port
    :param connection_string:
    :return:
    """
    result = re.match(r'rediss?://(.*?)@(.*?):(\d+)/(\d+)', connection_string)
    if result:
        return result.group(2), result.group(3), \
               result.group(1) or None, result.group(4) or 0
    else:
        return 'localhost', 6379, None, 0
