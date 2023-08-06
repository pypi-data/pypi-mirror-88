import inspect


def get_plugin_value(f, context, keyword):
    def wrap(get):
        args = inspect.getfullargspec(context.callback)[0]

        if keyword in args:
            def _f(*args, **kwargs):
                kwargs[keyword] = get()
                value = f(*args, **kwargs)
                return value

            return _f
        else:
            return f

    return wrap
