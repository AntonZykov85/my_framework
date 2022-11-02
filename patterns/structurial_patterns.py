from time import time

# decorator for routes in application

class APPRoutes:
    def __init__(self, routes, url):
        """
        :param routes: dict with routes
        :param url: route for page
        """
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        """ get callble class"""
        self.routes[self.url] = cls()


class Debug:
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            def timed(*args, **kwargs):
                start = time()
                result = method(*args, **kwargs)
                finish = time()
                delta = start - finish
                print(f'debug => {self.name} done {delta:2.2.f} ms')
                return result
            return timed
        return timeit(cls)
