#!/usr/bin/env python3
"""Web view MOdule."""
import requests
import redis
import time
from functools import wraps


redis_client = redis.Redis()


def count_calls(func):
    """Decorator that keeps track of how many times a function is called
    with a particular URL and stores it in Redis."""
    @wraps(func)
    def wrapper(url):
        key = f"count:{url}"
        redis_client.incr(key)
        return func(url)
    return wrapper


def cache(func):
    """Decorator that caches the result of the function call for a given URL
    in Redis with a 10-second expiration time."""
    @wraps(func)
    def wrapper(url):
        key = f"cache:{url}"
        cached_result = redis_client.get(key)
        if cached_result:
            return cached_result.decode('utf-8')
        result = func(url)
        redis_client.setex(key, 10, result)
        return result
    return wrapper


@count_calls
@cache
def get_page(url):
    """Function that obtains the HTML content of a particular URL using the
    requests module."""
    time.sleep(2)  # to simulate slow response
    response = requests.get(url)
    return response.text
