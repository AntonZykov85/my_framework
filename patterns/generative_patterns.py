import copy
import quopri


class User:
    pass


class Teacher(User):
    pass


class Student(User):
    pass


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher,
    }

    @classmethod
    def create(cls, type_user):
        return cls.types[type_user]()


class CoursePrototype:

    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype):
    def __int__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        print(f'created category with id: {self.auto_id}')
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse,
    }

    @classmethod
    def create(cls, type_course, name, category):
        return cls.types[type_course](name, category)


class Core:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.disciplines = []
        self.categories = []

    @staticmethod
    def create_user(type_user):
        return UserFactory.create(type_user)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def category_find(self, id):
        for category in self.categories:
            print('item', category.id)
            if category.id == id:
                return category
        raise LookupError(f'Нет категории с id = {id}')

    @staticmethod
    def create_discipline(type_course, name, category):
        return CourseFactory.create(type_course, name, category)

    def get_discipline(self, name):
        for _ in self.disciplines:
            if _.name == name:
                return _
        return None

    @staticmethod
    def decode_value(val):
        val_byte = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_byte)
        return val_decode_str.decode('UTF-8')


# class SingletonByName(type):
#
#     def __init__(cls, name, bases, attrs, **kwargs):
#         super().__init__(name, bases, attrs)
#         cls.__instance = {}
#
#     def __call__(cls, *args, **kwargs):
#         name = None
#         if args:
#             name = args[0]
#         if kwargs:
#             name = kwargs['name']
#
#         if name in cls.__instance:
#             return cls.__instance[name]
#         else:
#             cls.__instance[name] = super().__call__(*args, **kwargs)
#             return cls.__instance[name]
#
# class Logger(metaclass=SingletonByName):
#
#     def __int__(self, name):
#         self.name = name
#
#     @staticmethod
#     def log(text):
#         print('log =>', text)