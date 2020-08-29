import time
import multiprocessing
from multiprocessing import Process
from loguru import logger

from proxypool.processors.server import app
from proxypool.processors.getter import Getter
from proxypool.processors.tester import Tester
from proxypool.setting import CYCLE_GETTER, CYCLE_TESTER, \
    API_HOST, API_THREADED, API_PORT, IS_WINDOWS


if IS_WINDOWS:
    multiprocessing.freeze_support()


class Scheduler():
    def run_getter(self, cycle=CYCLE_GETTER):
        getter = Getter()
        loop = 0
        while True:
            logger.debug(f'getter loop {loop} start...')
            getter.run()
            loop += 1
            time.sleep(cycle)

    def run_tester(self, cycle=CYCLE_TESTER):
        tester = Tester()
        loop = 0
        while True:
            logger.debug(f'tester loop {loop} start...')
            tester.run()
            loop += 1
            time.sleep(cycle)

    def run_server(self):
        app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)

    def run(self, getter=True, tester=True, server=True):
        processors = []
        try:
            logger.info('starting proxypool...')
            if getter:
                getter_process = Process(name='getter', target=self.run_getter)
                processors.append(getter_process)
            if tester:
                tester_process = Process(name='tester', target=self.run_tester)
                processors.append(tester_process)
            if server:
                server_process = Process(name='server', target=self.run_server)
                processors.append(server_process)

            for p in processors:
                p.start()
                logger.info(f'{p.name}, {p.pid}, started')

            while True:
                pass

        except KeyboardInterrupt:
            for p in processors:
                p.terminate()
                logger.info(f'{p.name}, {p.pid}, terminated')
            logger.info('proxy terminated')


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
