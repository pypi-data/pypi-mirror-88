import functools
import time
import logging
import inspect

def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        try:
            args[0].tracked_time.setdefault(func.__name__, 0)
            args[0].tracked_time[func.__name__] += run_time
        except:
            pass
        logging.debug(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer


def debug(func):
    """Print the function signature and return value"""

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]  # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)  # 3
        logging.debug(f"Caller {inspect.stack()[1][3]} is calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        logging.debug(f"{func.__name__!r} returned {value!r}")  # 4
        return value

    return wrapper_debug