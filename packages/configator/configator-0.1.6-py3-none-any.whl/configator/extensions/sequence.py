
#!/usr/bin/env python3

import logging

from configator.engine.connector import RedisClient
from configator.utils.function import assure_not_null
from typing import List, Tuple, Dict, Optional, Union, Any

LOG = logging.getLogger(__name__)

class AutoIncrement(object):
    #
    def __init__(self, *args, topic='counter', connector=None, **kwargs):
        if isinstance(connector, RedisClient):
            self.__use_shared_connector = True
            self.__connector = connector
        else:
            self.__use_shared_connector = False
            self.__connector = RedisClient(**kwargs)
        #
        self.__topic = topic
        self.__default_key = ':'.join([self.__connector.CHANNEL_GROUP, self.__topic])
        #
        super(AutoIncrement, self).__init__()
    #
    ##
    @property
    def connector(self):
        return self.__connector
    #
    ##
    def init(self, label:Optional[str]=None, value:Optional[int]=0):
        return self.__open_connection().set(self.__gen_absolute_key(label), value, nx=True)
    #
    ##
    def incr(self, label:Optional[str]=None, amount:Optional[int]=1):
        return self.__open_connection().incr(self.__gen_absolute_key(label), amount=amount)
    #
    #
    def clear(self, label:Optional[str]=None):
        return self.__open_connection().delete(self.__gen_absolute_key(label))
    #
    #
    def reset(self, label:Optional[str]=None, value:Optional[int]=0):
        return self.__open_connection().set(self.__gen_absolute_key(label), value)
    #
    #
    def close(self):
        if not self.__use_shared_connector:
            self.__connector.close()
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, "AutoIncrement has closed")
    #
    #
    def __open_connection(self):
        return assure_not_null(self.__connector.rewind().connect(pinging=False, retrying=False))
    #
    def __gen_absolute_key(self, label):
        if label:
            return self.__default_key + ':' + str(label)
        return self.__default_key
