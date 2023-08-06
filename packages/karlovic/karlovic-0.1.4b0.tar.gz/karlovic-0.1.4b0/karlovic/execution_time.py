import bottle


def execution_time(f):
    import time

    def wrapper(*args, **kwargs):
        start_time = time.time()
        body = f(*args, **kwargs)
        end_time = time.time()

        bottle.response.headers['X-Execution-Time'] = f'{end_time-start_time:.3f} s'

        return body

    return wrapper
