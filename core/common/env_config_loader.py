import json
import os
import threading

from config.constants.envs import ConfigList, TYPE
from distutils.util import strtobool


class Config:
    _need_json_parse = [TYPE.Object, TYPE.Array]
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    def __init__(self):
        self._values = {}
        self._load_config()

    def _load_config(self):
        env_var_list = ConfigList.__members__
        for _, env_var in env_var_list.items():
            key, _type = env_var.value["key"], env_var.value["type"]
            if not os.getenv(key):
                # TODO: add logger message and custom exception
                raise KeyError("`{}` must be included in `.env` file".format(key))
            if _type in self._need_json_parse:
                self._values[key] = json.loads(os.getenv(key))
            elif _type == TYPE.Boolean:
                self._values[key] = bool(strtobool(os.getenv(key)))
            else:
                self._values[key] = os.getenv(key)

    def __getattr__(self, key):
        return self._values.get(key)

    @classmethod
    def instance(cls):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()
        return cls.__singleton_instance
