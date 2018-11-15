from django.conf.urls import url
from userAuthApp import views



app_name = 'userAuthApp'


urlpatterns = [

    url(r'^register/$', views.register, name = 'register'),
    url(r'^user_login/$', views.user_login, name = 'user_login'),
]
