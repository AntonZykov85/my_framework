from webob import Request, Response

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

        ''' page controller pattern'''

        if path in self.route_list:
            view = self.route_list[path]
        else:
            view = PageNotFound()

        request = {}

        '''front controller pattern'''

        for front in self.front_list:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return  [body.encode('utf-8')]


    def handle_request(self, request):
        user_agent = request.environ.get("HTTP_USER_AGENT", "No user agent found")
        response = Response()
        response.text = f'Hello user {user_agent}'
        return response
