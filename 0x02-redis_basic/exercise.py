#!/usr/bin/env python3
"""
Writing strings to Redis
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    Represents an object for storing data in a Redis data storage
    """
    def __init__(self) -> None:
        """
        Initializes a Cache instance
        """
        self._redis = redis.Redis()
        (self._redis).flushdb()  # flush the current database (DB 0)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores a value in a Redis data storage and returns the key
        """
        key = str(uuid.uuid4())
        (self._redis).set(key, data)
        return key  # return the randomly generated key


if __name__ == "__main__":
    cache = Cache()

    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))
