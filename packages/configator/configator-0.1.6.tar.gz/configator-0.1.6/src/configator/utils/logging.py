#!/usr/bin/env python3

import logging

def defineLogLevel(level: int, level_name: str):
    if logging.getLevelName(level).startswith('Level'):
        logging.addLevelName(level, level_name)

defineLogLevel(5, 'VERBOSE')

