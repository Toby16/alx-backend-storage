#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """
    Caches the output of fetched data
    """
    @wraps(method)
    def invoker(url) -> str:
        """
        The wrapper function for caching the output.
        """
        redis_store.incr("count:{}".format(url))
        result = redis_store.get("result:{}".format(url))
        if result:
            return result.decode("utf-8")
        result = method(url)
        redis_store.set("count:{}".format(url), 0)
        redis_store.setex("result:{url}".format(url), 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the request's response,
    and tracking the request
    """
    context = requests.get(url).text
    return context
