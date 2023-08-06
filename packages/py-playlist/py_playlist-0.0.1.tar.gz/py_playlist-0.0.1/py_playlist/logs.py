import logging
import functools


def start_logs(log_level):
    logging.basicConfig(level=log_level)


def log_function(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_str = tuple(repr(a) for a in args)
        kwargs_str = tuple(f'{k}={repr(v)}' for k,v in kwargs.items())
        sig = ', '.join(args_str + kwargs_str)
        logging.debug(f'calling {func.__name__}({sig})')
        return_value = func(*args, **kwargs)
        logging.debug(f'{func.__name__} returning value {repr(return_value)}')
        return return_value
    return wrapper


def log_generator(gen_func):
    @functools.wraps(gen_func)
    def wrapper(*args, **kwargs):
        args_str = tuple(repr(a) for a in args)
        kwargs_str = tuple(f'{k}={repr(v)}' for k,v in kwargs.items())
        sig = ', '.join(args_str + kwargs_str)
        logging.debug(f'calling {gen_func.__name__}({sig})')
        gen = gen_func(*args, **kwargs)
        for value in gen:
            logging.debug(f'yielding from {gen_func.__name__} value {repr(value)}')
            yield value
    return wrapper
