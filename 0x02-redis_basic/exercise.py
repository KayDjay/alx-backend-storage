#!/usr/bin/env python3
""" Writing Strings To Redis Module """

import redis
import uuid
from typing import Union
from typing import Callable
from functools import wraps


class Cache:
    """
    A class representing a cache using Redis.

    Attributes:
        _redis (redis.Redis): A Redis client object.
    """
    def __init__(self):
        """
        Initializes the Cache object by connecting to Redis and flushing
        the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @classmethod
    def _normalize_args(cls, args):
        """
        Normalize arguments to string representation for storage in Redis.

        Args:
            args: The arguments to normalize.

        Returns:
            str: The normalized string representation of the arguments.
        """
        return str(args)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the provided data in the cache and returns the generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored
            in the cache.

        Returns:
            str: The key under which the data is stored in the cache.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int,
                                                          float, None]:
        """
        Retrieves data from the cache using the provided key.

        Args:
            key (str): The key associated with the data in the cache.
            fn (Callable, optional): To convert the retrieved data.
                                     Defaults to None.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data from the
                        cache, optionally transformed by the provided function.
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


# # Test the Cache class
# cache = Cache()

# TEST_CASES = {
#     b"foo": None,
#     123: int,
#     "bar": lambda d: d.decode("utf-8")
# }

# for value, fn in TEST_CASES.items():
#     key = cache.store(value)
#     assert cache.get(key, fn=fn) == value

def count_calls(method: Callable) -> Callable:
    """
    A decorator to count the number of calls to a method.

    Args:
    method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


# Decorate Cache.store with count_calls
Cache.store = count_calls(Cache.store)


def call_history(method: Callable) -> Callable:
    """
    A decorator to store the history of inputs and outputs.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store input arguments
        self._redis.rpush(input_key, self._normalize_args(args))

        # Execute the original method
        result = method(self, *args, **kwargs)

        # Store the output result
        self._redis.rpush(output_key, self._normalize_args(result))

        return result
    return wrapper


# Decorate Cache.store with call_history
Cache.store = call_history(Cache.store)


def replay(method: Callable) -> None:
    """this method replay the redis history"""
    name = method.__qualname__

    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")

    print(f"{name} was called {calls} times:")

    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)

    for i, o in zip(inputs, outputs):
        _input = i.decode("utf-8")
        _output = o.decode("utf-8")
        print(f"{name}(*{_input}) -> {_output}")
