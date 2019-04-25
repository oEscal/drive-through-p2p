# coding: utf-8

import logging

from Clerk import Clerk

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')


def main():

    clerk = Clerk()

    clerk.start()

    clerk.join()

    return 0


if __name__ == '__main__':
    main()
