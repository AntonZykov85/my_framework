from datetime import date
from views import Home, About

'''front controller'''

def secret_front(request):
    request['data'] = date.today

def other_fronts(request):
    request['key'] = 'key'

fronts = [secret_front, other_fronts]

routes = {
    '/' : Home(),
    'about' : About()
}
