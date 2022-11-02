from datetime import date
from main_app.templator import templates_render
from patterns.generative_patterns import Core, Logger
from patterns.structurial_patterns import APPRoutes, Debug
from patterns.behavior_patterns import EmailNotifier, SmsNotifier, ListView, CreateView, BaseSerializer
# from urls import routes

site = Core()
logger = Logger('api')
routes = {}
email_notifer = EmailNotifier()
sms_notifer = SmsNotifier()



@APPRoutes(routes=routes, url='/')
class Home:
    def __call__(self, request):
        return '200 OK', templates_render('index.html', objects_list=site.categories)


@APPRoutes(routes=routes, url='/about/')
class About:
    def __call__(self, request):
        return '200 OK', templates_render('about.html')


@APPRoutes(routes=routes, url='/contacts/')
class Contacts:
    def __call__(self, request):
        return '200 OK', templates_render('contacts.html')


class NotFound:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@APPRoutes(routes=routes, url='/Datetable/')
class Datetable:
    def __call__(self, request):
        return '200 OK', templates_render('datetable.html', data=date.today())  #


@APPRoutes(routes=routes, url='/disciplines/')
class DisciplineList:
    @Debug(name='Discipline_list')
    def __call__(self, request):
        logger.log('Course list')
        try:
            category = site.category_find(int(request['request_params']['id']))
            return '200 OK', templates_render('discipline_list.html',
                                              objects_list=category.courses, name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'Sorry, these course are no longer exists...'


@APPRoutes(routes=routes, url='/create_discipline/')
class CreateDiscipline:
    category_id = -1

    @Debug(name='Create_Discipline')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category = None
            if self.category_id != -1:
                category = site.category_find(int(self.category_id))

                course = site.create_discipline('record', name, category)

                course.observers.append(email_notifer)
                course.observers.append(sms_notifer)

                site.disciplines.append(course)
            return '200 OK', templates_render('discipline_list.html',
                                              objects_list=category.courses,
                                              name=category.name,
                                              id=category.id)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.category_find(int(self.category_id))
                return '200 OK', templates_render('discipline_create.html',
                                                  name=category.name,
                                                  id=category.id)
            except KeyError:
                return '200 OK', 'Sorry, these category are not exists...'


@APPRoutes(routes=routes, url='/create_category/')
class CreateCategory:
    @Debug(name='Create_Category')
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
            return '200 OK', templates_render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', templates_render('categories_create.html', categories=categories)


@APPRoutes(routes=routes, url='/categories/')
class CategoriesList:
    def __call__(self, request):
        return '200 OK', templates_render('categories_list.html', objects_list=site.categories)


@APPRoutes(routes=routes, url='/discipline_copy/')
class DisciplineCopy:
    @Debug(name='Discipline_Copy')
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
            return '200 OK', templates_render('discipline_list.html', objects_list=site.categories)
        except KeyError:
            return '200 OK', 'This course are not exists'


@APPRoutes(routes=routes, url='/students-list/')
class StudentsListView(ListView):
    queryset = site.students
    templates_name = 'students_list.html'

@APPRoutes(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_object = site.create_user('student', name)
        site.students.append(new_object)

@APPRoutes(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.disciplines
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_discipline(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@APPRoutes(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='Api')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.disciplines).save()