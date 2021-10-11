import json
import functools


def to_json(func_to_decorate):
    @functools.wraps(func_to_decorate)
    def wrapper_func(*args, **kwargs):
        result = func_to_decorate(*args, **kwargs)
        return json.dumps(result)
    return wrapper_func
