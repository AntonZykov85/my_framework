from datetime import date
from main_app.templator import render
from patterns.generative_patterns import Core

site = Core()
# logger = Logger()

class Home:
    def __call__(self, request):
        return '200 OK', render('index.html', data=request.get('data'))

class About:
    def __call__(self, request):
        return '200 OK', render('about.html')

class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html')

class NotFound:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'



class Datetable:
    def __call__(self, request):
        return '200 OK', render('datetable.html', data = date.today()) #


class DisciplineList:
    def __call__(self, request):
        # logger.log('Course list')
        try:
            category = site.category_find(int(request['request_params']['id']))
            return '200 OK', render('discipline_list.html',
                                             objects_list = category.courses, name = category.name, id = category.id)
        except KeyError:
            return '200 OK', 'Sorry, these course are no longer exists...'


class CreateDiscipline:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category = None
            if self.category_id != -1:
                category = site.category_find(int(self.category_id))

                course = site.create_discipline('record', name, category)
                site.disciplines.append(course)
            return '200 OK', render('discipline_list.html', objects_list=category.courses,
                                             name=category.name, id=category.id)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.category_find(int(self.category_id))
                return '200 OK', render('discipline_create.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'Sorry, these category are not exists...'


class CreateCategory:
    def __call__(self, request):
        if request['method'] == 'POST':
            print(request)
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None

            if category_id:
                category = site.category_find(int(category_id))
            new_category = site.create_category(name, category)
            site.categories.append(new_category)
            return '200 OK', render('index.html', objects_list = site.categories)
        else:
            categories = site.categories
            return '200 OK', render('categories_create.html', categories=categories)


class CategoriesList:
    def __call__(self, request):
        return '200 OK', render('categories_list.html', objects_list = site.categories)


class DisciplineCopy:
    def __call__(self, request):
        request_params = request['request_params']
        try:
            name = request_params['name']
            old_course = site.get_discipline(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.disciplines.append(new_course)
            return '200 OK', render('discipline_list.html', objects_list = site.categories)
        except KeyError:
            return '200 OK', 'This course are not exists'









