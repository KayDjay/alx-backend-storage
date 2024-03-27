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
    
    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieves data from the cache using the provided key.

        Args:
            key (str): The key associated with the data in the cache.
            fn (Callable, optional): A callable function to convert the retrieved data.
                                     Defaults to None.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data from the cache,
                                                  optionally transformed by the provided function.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieves a string value from the cache using the provided key.

        Args:
            key (str): The key associated with the data in the cache.

        Returns:
            Union[str, None]: The retrieved string value from the cache,
                              or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieves an integer value from the cache using the provided key.

        Args:
            key (str): The key associated with the data in the cache.

        Returns:
            Union[int, None]: The retrieved integer value from the cache,
                              or None if the key does not exist.
        """
        return self.get(key, fn=int)
    
    # Test the Cache class
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value