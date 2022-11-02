from datetime import date
# from views import Home, About, Contacts, NotFound, Datetable, DisciplineList, CreateDiscipline, CreateCategory, CategoriesList, DisciplineCopy
# routes = {}


def secret_front(request):
    request['data'] = date.today()

def other_fronts(request):
    request['key'] = 'key'

fronts = [secret_front, other_fronts]

# routes = {
#     # '/': Home(),
#     # '/about/': About(),
#     # '/contacts/': Contacts(),
#     # '/Datetable/': Datetable(),
#     # '/disciplines/': DisciplineList(),
#     # '/categories/': CategoriesList(),
#     # '/create_discipline/': CreateDiscipline(),
#     # '/create_category/': CreateCategory(),
#
# }
