from jsonpickle import dumps, loads
from my_framework.main_app.templator import templates_render

#observer pattern
class Observer:
    def update(self, subject):
        pass

class Subject:
    def __init__(self):
        self.observers = []

    def notify(self):
        for i in self.observers:
             i.update(self)

class SmsNotifier(Observer):
    def update (self, subject):
        print('SMS', subject.students[-1].name, 'join us')

class EmailNotifier(Observer):
    def update (self, subject):
        print('EMAIL', subject.students[-1].name, 'join us')

class BaseSerializer:
    def __init__(self, object):
        self.object = object

    def save(self):
        return dumps(self.object)

    @staticmethod
    def load(data):
        return loads(data)

#template method pattern

class TemplateView:
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_contex(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', templates_render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_contex()

class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context

class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_object(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_object(data)
            return self.render_template_with_contex()

        else:
            return super().__call__(request)

#strategy pettern

class ConsoleWriter:
    def write(self, text):
        print(text)

class FileWriter:
    def __init__(self):
        self.file_name = 'log'

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as file:
            file.write(f'{text}\n')


