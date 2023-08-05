#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from utility import system

#
# GLOBALS
#

logger = None

#
# FUNCTIONS
#


def init_logger():
    """
    Initialize the logger instance
    :return:
    """
    global logger
    logger = logging.getLogger('db_sync_tool')
    logger.setLevel(logging.DEBUG)

    if system.config:
        if 'log_file' in system.config['host']:
            fh = logging.FileHandler(system.config['host']['log_file'])
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            logger.addHandler(fh)


def get_logger():
    """
    Return the logger instance
    :return:
    """
    if logger is None:
        init_logger()
    return logger
