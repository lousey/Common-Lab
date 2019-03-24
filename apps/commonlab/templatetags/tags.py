from django import template

register = template.Library()

@register.simple_tag
def active(request, pattern):
    import re
    arr = request.path.split("/")
    if re.search(pattern, '/%s/' % (arr[1])):
        return 'active'
    return ''

@register.filter
def get_subsection(project, subsection_name):
    arr = project.sections.filter(name=subsection_name)
    if len(arr) == 1:
        return arr[0]
    return None

@register.filter
def custom_content(img_width):
    if img_width:
        return 770 - img_width
    return 770
