import functools

def default():
    def inner(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return inner

def test():
    def inner(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs) + [('Lana Del Rey', 32, 'voice')]
        return wrapper
    return inner