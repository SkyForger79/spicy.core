from django.db import connection


def debug_queries(func):
    """
    Print connection queries made during function execution.
    """
    def _inner(*args, **kwargs):
        old_queries = connection.queries
        connection.queries = []
        result = func(*args, **kwargs)

        name = (
            getattr(func, 'func_name', None) or
            getattr(func, 'im_func.func_name', None))

        for i, query in enumerate(connection.queries):
            print name, i, query
        print

        old_queries.extend(connection.queries)
        connection.queries = old_queries
        return result
    return _inner
