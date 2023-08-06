import aiocache


class Cache:
    global_use_cache = False

    @staticmethod
    def use_cache(decorated_function):
        decorator = aiocache.cached(ttl=60 * 60 * 24)(decorated_function)

        def wrapper(*args, **kw):
            if Cache.use_cache:
                return decorator(*args, **kw)
            return decorated_function(*args, **kw)

        return wrapper
