import logging
import sys
from datetime import date


def start_logging():
    today = date.today()
    date_sortable = f'{today.year}{today.month}{today.day}'

    # https://docs.python.org/3.13/library/logging.html#logging.basicConfig
    # https://docs.python.org/3.13/library/stdtypes.html#printf-style-string-formatting
    # https://docs.python.org/3.13/library/logging.html#formatter-objects
    # https://docs.python.org/3.13/library/logging.html#logrecord-attributes

    stdout_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(f'./logs/{date_sortable}.log')

    logging.basicConfig(
        # filename=f'./logs/{date_sortable}.log',
        # filemode='a',
        # format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        style='{',
        format='{asctime} {msecs:003.0f} {levelname:9s} {message} - {module}({lineno})',
        datefmt='%H:%M:%S',
        level=logging.DEBUG,
        handlers=[stdout_handler, file_handler]
    )


if __name__ == "__main__":
    from time import sleep

    start_logging()
    sleep(3)
    logging.debug('Test debug message')
    sleep(0.5)
    logging.info('Test info message')
    sleep(0.5)
    logging.warning('Test warning message')
    sleep(1)
    logging.error('Test error message')
    sleep(2)
    logging.critical('Test critical message')
