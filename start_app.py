from main_app.api import API
from urls import fronts
from views import routes
from wsgiref.simple_server import make_server

app = API(routes, fronts)

with make_server('', 8000, app) as httpd:
    httpd.serve_forever()