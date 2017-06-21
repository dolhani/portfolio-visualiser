from django.conf import settings
from django.conf.urls import url, include
from django.views.generic import TemplateView

from . import views

#URLs listed as following
#Top view is the leftmost, every functionalities related to that is step right
#Example Homepage is the top(found in navbar)
#Visualizations on the page (path, projectdependencies, 4-field) are step right
ajax_patterns = [
    url(r'^get_sheets$', views.get_sheets, name='get_sheets'),
    url(r'^get_orgs$', views.get_orgs, name='get_orgs'),
    url(r'^get_pers$', views.get_pers, name='get_pers'),
    url(r'^get_proj$', views.get_proj, name='get_proj'),
    url(r'^get_multiple/(?P<field_type>[A-Za-z]+)/(?P<field_id>[0-9]+)$', views.get_multiple, name='get_multiple'),
]

urlpatterns = [
    url(r'^$', views.home, name='homepage'),
        url(r'^path$', TemplateView.as_view(template_name="path.html"), name='path'),
        url(r'^projectdependencies$', TemplateView.as_view(template_name="projectdependencies.html"), name='projectdependencies'),
        url(r'^fourfield$', TemplateView.as_view(template_name="fourfield.html"), name='fourfield'),
    url(r'^projects$', views.projects, name='projects'),
        url(r"^projects/(?P<project_id>[0-9]+)$", views.show_project, name='show_project'),
            url(r'^projects/(?P<project_id>[0-9]+)/edit/(?P<field_type>[A-Za-z]+)$', views.project_edit, name='project_edit'),
    url(r'^admin_tools$', views.admin_tools, name='admin_tools'),
        url(r"^importer$", views.importer, name='importer'),
        url(r'^create_org$', views.create_org, name='create_org'),
        url(r'^create_person$', views.create_person, name='create_person'),
    url(r'^database$', views.databaseview, name='databaseview'),
    url(r"^about$", TemplateView.as_view(template_name="about.html"), name='about'),
    url(r'^addproject$', views.addproject, name='addproject'),
    url(r'^add_field$', views.add_field, name='add_field'),
    url(r'^snapshots(/(?P<vis_type>[A-Za-z]+))?(/(?P<snapshot_id>[0-9]+))?$', views.snapshots, name='snapshots'),
    url(r'^create_snapshot$', views.create_snapshot, name='create_snapshot'),

    #For stuff
    url(r"^json$", views.json, name='json'),
    # these are for ajax requests
    url(r'', include(ajax_patterns)),
]