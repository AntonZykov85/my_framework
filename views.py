from main_app.templator import render

class Home:
    def __call__(self, request):
        return '200 OK', render('index.html', data=request.get('data', None))

class About:
    def __call__(self, request):
        return '200 OK', render('about.html', data=request.get('data', None))

class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html', data=request.get('data', None))

class NotFound:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'

