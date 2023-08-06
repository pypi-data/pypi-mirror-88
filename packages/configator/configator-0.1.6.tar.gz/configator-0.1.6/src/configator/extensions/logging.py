#!/usr/bin/env python3

import logging

from datetime import datetime
from configator.engine import SettingCapsule

class LoggingConfigUpdater():
    def __init__(self, *args, label='LOGGING_CONFIG', level_mappings=None, **kwargs):
        self.__capsule = SettingCapsule(label=label, loader=self.update)
    #
    #
    @property
    def capsule(self):
        return self.__capsule
    #
    #
    def update(self, *args, **kwargs):
        if 'change_level_tasks' in kwargs:
            return self.change_level_tasks(kwargs['change_level_tasks'])
        return None
    #
    #
    def change_level_tasks(self, descriptors):
        result = list()
        if isinstance(descriptors, list):
            for clt in descriptors:
                if not isinstance(clt, dict):
                    continue
                module_name = clt.get('module_name')
                level_name = str(clt.get('level', 'unknown')).upper()
                level = self.level_mappings.get(level_name)
                if module_name and level:
                    logger = logging.getLogger(module_name)
                    if logger:
                        logger.setLevel(level)
                    result.append(dict(module=module_name, level=level_name))
        return {
            "timestamp": datetime.now().timestamp(),
            "result": result
        }
    #
    #
    @property
    def level_mappings(self):
        return dict(
            CRITICAL = logging.CRITICAL,
            ERROR = logging.ERROR,
            WARNING = logging.WARNING,
            INFO = logging.INFO,
            DEBUG = logging.DEBUG,
            NOTSET = logging.NOTSET,
        )
