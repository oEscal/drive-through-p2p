# coding: utf-8

import logging

from Waiter import Waiter

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')


def main():

    waiter = Waiter()

    waiter.start()

    waiter.join()

    return 0


if __name__ == '__main__':
    main()
