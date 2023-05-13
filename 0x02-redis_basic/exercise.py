#!/usr/bin/env python3
"""Redis Module."""
import redis
import requests
import uuid
from typing import Callable

redis_client = redis.Redis()


class Cache:
    """
    A Redis-based cache class.
    """
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def _serialize(data):
        """
        Serialize data to a string.
        """
        if isinstance(data, (int, float)):
            return str(data)
        elif isinstance(data, bytes):
            return data.decode("utf-8")
        else:
            return data

    @staticmethod
    def _deserialize(data, fn=None):
        """
        Deserialize data from a string.
        """
        if fn:
            return fn(data)
        else:
            return data

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in cache and return the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, self._serialize(data))
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        Get data from cache given a key.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        else:
            return self._deserialize(data, fn)

    def get_str(self, key: str) -> Union[str, None]:
        """
        Get string data from cache given a key.
        """
        return self.get(key, str)

    def get_int(self, key: str):
        """
        Get integer data from cache given a key.
        """
        return self.get(key, int)


def count_calls(method: Callable) -> Callable:
    """
    A decorator that counts the number of times a function is called with a particular URL
    and stores it in Redis.
    """
    def wrapper(*args, **kwargs):
        key = method.__qualname__
        redis_client.incr(key)
        return method(*args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A decorator that stores the inputs and outputs of a function call in Redis.
    """
    def wrapper(*args, **kwargs):
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"
        redis_client.rpush(inputs_key, str(args))
        output = method(*args, **kwargs)
        redis_client.rpush(outputs_key, output)
        return output

    return wrapper


@count_calls
@call_history
def store_data(data: str) -> str:
    """
    Store data in cache and return the key.
    """
    return Cache().store(data)

def replay(func):
    inputs_key = f"{func.__qualname__}:inputs"
    outputs_key = f"{func.__qualname__}:outputs"
    inputs = redis_client.lrange(inputs_key, 0, -1)
    outputs = redis_client.lrange(outputs_key, 0, -1)

    print(f"{func.__qualname__} was called {len(inputs)} times:")
    for args, output in zip(inputs, outputs):
        print(f"{func.__qualname__}(*{args.decode('utf-8').strip()},) -> {output.decode('utf-8').strip()}")


def get_page(url: str) -> str:
    """
    Get the HTML content of a particular URL using requests and cache the result
    with an expiration time of 10 seconds in Redis.
    """
    count_key = f"count:{url}"
    page_key = f"page:{url}"
    cached_page = redis_client.get(page_key)
    if cached_page:
        return cached_page.decode("utf-8")
    else:
        response = requests.get(url)
        page_content = response.content.decode("utf-8")
        redis_client.incr(count_key)
        redis_client.setex(page_key, 10, page_content)
        return page_content

if __name__ == "__main__":
    print(store_data("Hello world"))
    print(store_data("Hello again"))
    print(store_data("Third time's the charm"))
    print(store_data("Last one"))
    print(redis_client.keys())

    print(get_page("http://slowwly.robertomurray.co.uk"))
    print(get_page("http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.co.uk"))
    print(get_page("http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.bbc.co.uk"))
    print(redis_client.keys())
