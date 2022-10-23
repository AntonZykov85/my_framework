from webob import Request, Response
from .requests import GetRequest, PostRequest
from .templator import templates_render
from wsgiref.util import setup_testing_defaults
import quopri


class PageNotFound:
    def __call__(self, request):
        return '404 WHAT', templates_render('404_not_found.html')


class API:
    def __init__(self, route_items, front_items):
        self.route_list = route_items
        self.front_list = front_items

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}

        # get request method from environ

        method = environ['REQUEST_METHOD']
        request['method'] = method

        # handling of get & post - requests

        if method == 'POST':
            data = PostRequest().get_request_parameters(environ)
            request['data'] = API.decode_value(data)
            print(f'post request: {API.decode_value(data)}')

        if method == 'GET':
            req_param = GetRequest.get_request_param(environ)
            request['get_request_parameters'] = API.decode_value(req_param)
            print(f'get request {req_param}')

        if path in self.route_list:
            view = self.route_list[path]
        else:
            view = PageNotFound()

        for front in self.front_list:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]


    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            fixed_value = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            fixed_value_str = quopri.decodestring(fixed_value).decode('UTF-8')
            new_data[k] = fixed_value_str
        return
