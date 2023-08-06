import os
import pprint
import tempfile

from loguru import logger
from diskcache import Cache

from src.utils.Singleton import Singleton


class CacheManager(Singleton):

    _key = "last_call"
    _path = os.path.join(tempfile.gettempdir(), "koha_sync_cache")

    def __init__(self):
        self.cache = Cache(directory=CacheManager._path)
        self.records = self.get_cache()

    def get_cache(self):
        with Cache(self.cache.directory) as reference:
            if reference.get(self._key) is None:
                return []
            else:
                return reference.get(self._key)

    def set_cache(self, value):
        with Cache(self.cache.directory) as reference:
            reference.set(self._key, value)
            self.records = value
