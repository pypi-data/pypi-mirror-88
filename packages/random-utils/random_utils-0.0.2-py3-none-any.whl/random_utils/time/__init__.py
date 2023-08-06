import time


def time_this(orig_func):
    def wrapper(*args, **kwargs):
        s = time.time()
        result = orig_func(*args, **kwargs)
        print(f"Function: {orig_func.__name__}, Time: {time.time() - s}")
        return result

    return wrapper
