from django.conf.urls.defaults import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   (r'^', include('commonlab.urls')),

    # admin urls
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
 
    # for testing in dev env only
    #(r'^404/$', TemplateView.as_view(template_name='404.html')),
    #(r'^500/$', TemplateView.as_view(template_name='500.html')),
)

# serving media and static files via django in dev under apache & dev server
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
