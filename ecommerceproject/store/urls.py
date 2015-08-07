from django.conf.urls import url
from . import views
 
urlpatterns = [
 url(r'^$', views.index, name = 'index'),
 url(r'^admin/', views.admin, name = 'admin'),
 url(r'^(\d+)/$', views.closeup, name = 'closeup'),
 url(r'^cart/', views.cart, name = 'cart'),
 url(r'^checkout/', views.checkout, name = 'checkout'),
]