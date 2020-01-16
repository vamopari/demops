
def check_api_key(func):
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner
