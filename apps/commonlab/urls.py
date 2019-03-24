from django.conf.urls.defaults import *
from django.views.generic import TemplateView, DetailView, RedirectView, ListView
from commonlab.models import Project, Person, Partner, ContactInfo
from commonlab.views import ProjectDetailView, PersonDetailView
import commonlab

urlpatterns = patterns('',
    url(r'^$',
        RedirectView.as_view(url='/projects/'),
        name='home'),
    url(r'^projects/$',
        TemplateView.as_view(template_name='projects/projects_main.html'),
        name='projects'),
    url(r'^projects/(?P<slug>[-\w]+)/$',
        ProjectDetailView.as_view(model=Project, section="overview", template_name="projects/overview.html")),
    url(r'^projects/(?P<slug>[-\w]+)/overview/$',
        ProjectDetailView.as_view(model=Project, section="overview", template_name="projects/overview.html")),
    url(r'^projects/(?P<slug>[-\w]+)/impact/$',
        ProjectDetailView.as_view(model=Project, section="impact", template_name="projects/impact.html")),
    url(r'^projects/(?P<slug>[-\w]+)/press/$',
        ProjectDetailView.as_view(model=Project, section="press", template_name="projects/press.html")),
    url(r'^projects/(?P<slug>[-\w]+)/process/$',
        ProjectDetailView.as_view(model=Project, section="process", template_name="projects/process.html")),
    url(r'^projects/(?P<slug>[-\w]+)/(?P<section>[-\w]+)/$',
        ProjectDetailView.as_view(model=Project, template_name="projects/custom.html")),
    url(r'^people/$',
        TemplateView.as_view(template_name='people/people_main.html'),
        name='people'),
    url(r'^people/(?P<slug>[-\w]+)/$',
        PersonDetailView.as_view(model=Person, template_name="people/people_detail.html")),   
    url(r'^partners/$',
        ListView.as_view(model=Partner, template_name='partners/partners_main.html'),
        name='partners'),
    url(r'^contact/$',
        ListView.as_view(model=ContactInfo, template_name="contact/contact.html"),
        name='contact'),
)


