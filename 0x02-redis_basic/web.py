#!/usr/bin/env python3
""" This module contains a function that retrieves Redis web catche tracker """
import redis
import requests
from functools import wraps
from typing import Callable

redis_ = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """this method count requests"""

    @wraps(method)
    def wrapper(url):
        """count wrapper decorator """
        redis_.incr(f"count:{url}")
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        redis_.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ get HTML content of a URL """
    req = requests.get(url)
    return req.text
