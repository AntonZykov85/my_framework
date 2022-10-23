from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment

import os


# def render(template_name, folder='templates', **kwargs):
#     file_path = os.path.join(folder, template_name)
#     with open(file_path, encoding='utf-8') as file:
#         template = Template(file.read())
#     return template.render(**kwargs)

def templates_render(template_name, folder='templates', **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)
