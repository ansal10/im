from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from hw import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gettingstarted.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^index$' , views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^recharge$', views.recharge, name='recharge'),
    url(r'^admin/', include(admin.site.urls)),

)
