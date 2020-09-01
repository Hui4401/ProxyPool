import platform
from os.path import dirname, abspath, join
from environs import Env
from loguru import logger

from proxypool.utils.parse import parse_redis_connection_string


env = Env()
env.read_env()

IS_WINDOWS = platform.system().lower() == 'windows'
ROOT_DIR = dirname(dirname(abspath(__file__)))
LOG_DIR = join(ROOT_DIR, env.str('LOG_DIR', 'logs'))

# like rediss://[password]@host:port/0
REDIS_URL = env.str('REDIS_URL', 'redis://@localhost:6379')
REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB = parse_redis_connection_string(REDIS_URL)
REDIS_KEY = env.str('REDIS_KEY', 'proxies')

# definition of proxy scores
PROXY_SCORE_MAX = 100
PROXY_SCORE_MIN = 0
PROXY_SCORE_INIT = 10

# definition of proxy number
PROXY_NUMBER_MAX = 50000
PROXY_NUMBER_MIN = 0

CYCLE_GETTER = env.int('CYCLE_GETTER', 100)
CYCLE_TESTER = env.int('CYCLE_TESTER', 20)

GET_TIMEOUT = env.int('GET_TIMEOUT', 10)

TEST_URL = env.str('TEST_URL', 'https://www.baidu.com')
TEST_BATCH = env.int('TEST_BATCH', 20)
TEST_TIMEOUT = env.int('TEST_TIMEOUT', 10)

# only save anonymous proxy
TEST_ANONYMOUS = True
TEST_VALID_STATUS = env.list('TEST_VALID_STATUS', [200])

# definition of api
API_HOST = env.str('API_HOST', '0.0.0.0')
API_PORT = env.int('API_PORT', 5555)
API_THREADED = env.bool('API_THREADED', True)

logger.add(env.str('LOG_RUNTIME_FILE', join(LOG_DIR, 'debug.log')),
           level='DEBUG', rotation='1 week', retention='10 days', encoding='utf-8')
logger.add(env.str('LOG_ERROR_FILE', join(LOG_DIR, 'error.log')),
           level='ERROR', rotation='1 week', encoding='utf-8')

