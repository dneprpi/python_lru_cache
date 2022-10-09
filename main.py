from datetime import timedelta, datetime
from functools import lru_cache, wraps

import requests


def timed_lru_cache(seconds: int, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


def print_hi(name):
    print(f'{name} started...')
    url = "https://jsonplaceholder.typicode.com/todos/"
    for x in range(1, 10):
        print(get_todo_by_id(f"{url}{x}"))
    for x in range(1, 10):
        print(get_todo_by_id(f"{url}{x}"))


@timed_lru_cache(60)
def get_todo_by_id(url: str):
    print("Получение статьи с сервера...")
    try:
        send_result = requests.get(url).json()
    except requests.exceptions.RequestException as e:
        send_result = {"error": f"Requests error: {e}"}

    return send_result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('LRU')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
