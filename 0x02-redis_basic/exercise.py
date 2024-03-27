#!/usr/bin/env python3
""" Writing Strings To Redis Module """

import redis
import uuid
from typing import Union

class Cache:
    """
    A class representing a cache using Redis.

    Attributes:
        _redis (redis.Redis): A Redis client object.
    """
    def __init__(self):
        """
        Initializes the Cache object by connecting to Redis and flushing the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the provided data in the cache and returns the generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored in the cache.

        Returns:
            str: The key under which the data is stored in the cache.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key