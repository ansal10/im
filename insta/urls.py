from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from hw import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gettingstarted.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^index/?$' , views.index, name='index'),
    url(r'^register/?$', views.register, name='register'),
    url(r'^login/?$', views.login, name='login'),
    url(r'^accounts/login/?$', views.login, name='login'),
    url(r'^recharge/?$', views.recharge, name='recharge'),
    url(r'^logout/?$', views.logout, name='logout'),

    url(r'^dashboard/bids/?$', views.bids, name='bids'),
    url(r'^dashboard/(?P<subject>[a-zA-Z ]+)?/?(?P<project_id>[\d]+)?$', views.dashboard, name='dashboard'),

    url(r'^projects/?$', views.projects, name='Projects'),
    url(r'^projects/new/?$', views.newproject, name='new Project'),
    url(r'^projects/all/?$', views.listproject, name='List Project'),
    url(r'^projects/(?P<pid>[\d]+)/?$', views.projectdetails, name='Project Details'),
    url(r'^projects/(?P<pid>[\d]+)/edit/?', views.editproject, name='Edit Project'),
    url(r'^projects/(?P<pid>[\d]+)/bid/(?P<b_id>[\d]+)/?', views.bid, name='bid'),
    url(r'^permission_denied/?$', views.permission_denied, name='Permission Denied'),
    url(r'^admin/', include(admin.site.urls)),

)
