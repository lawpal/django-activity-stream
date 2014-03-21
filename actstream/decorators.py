from functools import wraps


def stream(func):
    """
    Stream decorator to be applied to methods of an ``ActionManager`` subclass

    Syntax::

        from actstream.decorators import stream
        from actstream.managers import ActionManager

        class MyManager(ActionManager):
            @stream
            def foobar(self, ...):
                ...

    """
    @wraps(func)
    def wrapped(manager, *args, **kwargs):
        offset, limit = kwargs.pop('_offset', None), kwargs.pop('_limit', None)
        if hasattr(func, 'fetch_generic_relations'):
            try:
                return func(manager, *args, **kwargs)[offset:limit]\
                    .fetch_generic_relations()
            except AttributeError:
                return func(manager, *args, **kwargs).fetch_generic_relations()
        else:
            try:
                return func(manager, *args, **kwargs)[offset:limit]
            except AttributeError:
                return func(manager, *args, **kwargs)

    return wrapped