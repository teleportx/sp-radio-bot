from datetime import datetime
import logging
import os


def setup():
    if not os.path.isdir('logs'):
        os.mkdir('logs')

    now_all = datetime.now()
    name = '%s-%s-%s %s.%s.%s' % (
        now_all.year, now_all.month, now_all.day, now_all.hour, now_all.minute, now_all.second)

    file_log = logging.FileHandler(f'logs/{name}.log')
    console_out = logging.StreamHandler()

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] : %(message)s',
                        handlers=(file_log, console_out))
