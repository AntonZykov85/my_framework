from webob import Request, Response
from .requests import GetRequest, PostRequest
from .templator import templates_render
from wsgiref.util import setup_testing_defaults
import quopri


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'

class API:
    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        method = environ['REQUEST_METHOD']

        request['method'] = method

        if method == 'POST':
            data = PostRequest().get_request_parameters(environ)
            request['data'] = API.decode_value(data)
            print(f'Get post-request: {API.decode_value(data)}')
        if method == 'GET':
            request_params = GetRequest().get_request_param(environ)
            request['request_params'] = API.decode_value(request_params)
            print(f'get GET-parametres:'
                  f' {API.decode_value(request_params)}')

        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        for front in self.fronts_lst:
            front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data

class DebugApplication(API):

    def __init__(self, routes_obj, fronts_obj):
        self.application = API(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)


class FakeApplication(API):

    def __init__(self, routes_obj, fronts_obj):
        self.application = API(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']