from django.conf import settings
from commonlab.models import *

def base(request):
    project_list = Project.objects.all()
    projectcategory_list = ProjectCategory.objects.all()
    people_list = Person.objects.all()
    peoplecategory_list = PersonCategory.objects.all()

    return { 'people_list' : people_list, 'peoplecategory_list' : peoplecategory_list,
             'project_list' : project_list, 'projectcategory_list' : projectcategory_list }

