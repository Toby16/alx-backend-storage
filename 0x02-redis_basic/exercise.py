#!/usr/bin/env python3
"""
Writing strings to Redis
"""

import redis
import uuid
from functools import wraps
from typing import Union, Callable, Any

def count_calls(method: Callable) -> Callable:
    """
    Tracks the number of calls made to a method in a Cache class
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        Invokes the given method after incrementing its call counter
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker



class Cache:
    """
    Represents an object for storing data in a Redis data storage
    """
    def __init__(self) -> None:
        """
        Initializes a Cache instance
        """
        self._redis = redis.Redis(host="localhost", port=6379, db=0)
        (self._redis).flushdb()  # flush the current database (DB 0)

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores a value in a Redis data storage and returns the key
        """
        key: str = str(uuid.uuid4())
        (self._redis).set(key, data)
        return key  # return the randomly generated key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        """
        Retrieves a value from a Redis data storage
        """
        data = (self._redis).get(key)
        if fn is not None:
            return fn(data)
        else:
            return data

    def get_str(self, key: str) -> str:
        """
        Retrieves a string value from a Redis data storage
        """
        return self.get(key).decode('utf-8')

    def get_int(self, key: Union[str, int]) -> int:
        """
        Retrieves an integer value from a Redis data storage
        """
        return int(self.get(key))


if __name__ == "__main__":
    cache = Cache()

    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))
