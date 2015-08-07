from django.conf.urls import url
from . import views
 
urlpatterns = [
 url(r'^$', views.index, name = 'index'),
 url(r'^no_user/$', views.no_user, name = 'no_user'),
 url(r'^login/$', views.login, name = 'login'),
 url(r'^login/success/', views.login_success, name = 'login_success'),
 url(r'^logout/', views.logout, name = 'logout'),
 url(r'^signup/$', views.signup, name = 'signup'),
 url(r'^signup/success/', views.signup_success, name = 'signup_success'),
]