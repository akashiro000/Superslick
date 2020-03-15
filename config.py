# coding: utf-8

import json


class Config(object):
    with open('./config.json', encoding='utf-8') as f:
        __config = json.load(f)

    @classmethod
    def get(self, key, default=None):
        return self.__config.get(key) or default
