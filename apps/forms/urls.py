from django.conf.urls.defaults import *

handler500 = 'views.server_error'
urlpatterns = patterns('',
    (r'^$', 'apps.forms.views.index'),
    #(r'^edit/$','apps.forms.views.edit'),
    #(r'^edit/(?P<formId>\w+)/$','apps.forms.views.edit'),
    (r'^(?P<formId>\d+)/b(?P<barcode>\w+)/$', 'apps.forms.views.viewForm'),
    (r'^/b(?P<barcode>\w+)/$', 'apps.forms.views.viewLatestForm'),
    (r'^list/',include('apps.forms.inventory.urls')),
    (r'^editrev/(?P<formnumber>\d+)/$', 'apps.forms.inventory.views.exportRevision'),
    (r'^(?P<formId>\d+)/(?P<refNo>\d+)/$','apps.forms.views.viewForm'),
)
