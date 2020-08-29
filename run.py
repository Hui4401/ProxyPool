import argparse
from proxypool.scheduler import Scheduler


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--processors', type=str, nargs='*',
                    choices=['getter', 'tester', 'server'],
                    help='getter，tester，server，可多选，默认全部运行')
args = parser.parse_args()
processors = args.processors

if __name__ == '__main__':
    scheduler = Scheduler()
    if not processors:
        scheduler.run()
    else:
        getter = True if 'getter' in processors else False
        tester = True if 'tester' in processors else False
        server = True if 'server' in processors else False
        scheduler.run(getter, tester, server)
