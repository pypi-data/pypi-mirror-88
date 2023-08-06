
#!/usr/bin/env python3

import logging

from configator.engine.connector import RedisClient
from configator.utils.function import assure_not_null, json_dumps, json_loads
from typing import List, Tuple, Dict, Optional, Union, Any

LOG = logging.getLogger(__name__)

class SettingStorage(object):
    #
    def __init__(self, *args, topic='storage', connector=None, **kwargs):
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
        super(SettingStorage, self).__init__()
    #
    ##
    @property
    def connector(self):
        return self.__connector
    #
    ##
    def get(self, key:str):
        value = self.__open_connection().get(self.__gen_absolute_key(key))
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        if isinstance(value, str):
            obj, err = json_loads(value)
            if err:
                raise err
            return obj
        return value
    #
    ##
    def store(self, key:str, obj:Union[dict,list,str,float,int,bool]):
        value, err = json_dumps(obj)
        if err:
            raise err
        return self.__open_connection().set(self.__gen_absolute_key(key), value)
    #
    ##
    def clear(self, key:str):
        return self.__open_connection().delete(self.__gen_absolute_key(key))
    #
    ##
    def close(self):
        if not self.__use_shared_connector:
            self.__connector.close()
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, "SettingStorage has closed")
    #
    #
    def __open_connection(self):
        return assure_not_null(self.__connector.rewind().connect(pinging=False, retrying=False))
    #
    def __gen_absolute_key(self, key):
        if key:
            return self.__default_key + ':' + str(key)
        return self.__default_key
