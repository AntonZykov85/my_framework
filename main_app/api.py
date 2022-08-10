from webob import Request, Response
from requests import GetRequest, PostRequest
from wsgiref.util import  setup_testing_defaults
import quopri

class PageNotFound:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'

class API:
    def __init__(self, route_items, front_items):
        self.route_list = route_items
        self.front_list = front_items

    def __call__(self, environ, start_response):
        # request = Request(environ)
        # response = self.handle_request(request)
        # return response(environ, start_response)
        path = environ['PATH_INFO']

        request = {}

        # get request method from environ

        method = environ['REQUEST_METHOD']
        request['method'] = method

        #handling of get & post - requests

        if method == 'POST':
            data =   PostRequest().get_request_parameters(environ)
            request['data'] = data
            print(f'post request: {API.decode_value(data)}')
        if method == 'GET':
            req_param = GetRequest.get_request_param(environ)
            request['get_request_parameters'] = req_param
            print(f'get request {req_param}')

        if path in self.route_list:
            view = self.route_list[path]
        else:
            view = PageNotFound()

        for front in self.front_list:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return  [body.encode('utf-8')]

    #
    # def handle_request(self, request):
    #     user_agent = request.environ.get("HTTP_USER_AGENT", "No user agent found")
    #     response = Response()
    #     response.text = f'Hello user {user_agent}'
    #     return response
    def decode_value (data):
        fixed_data = {}
        for k, v in data.items():
            fixed_value = bytes(v.replace('%', '=').replace("+", " ", 'UTF-8'))
            fixed_value_str = quopri.decodestring(fixed_value).decode('UTF-8')
            fixed_data[k] = fixed_value_str
        return fixed_data