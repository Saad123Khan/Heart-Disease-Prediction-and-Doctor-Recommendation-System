from django.urls import path
from . import views

urlpatterns = [

    path('login', views.loginaction , name = 'login'),
    path('sign', views.signaction , name = 'sign'),
    
    path('admin', views.adnminlogin , name = 'admin'),
    
    path('Adminhome', views.admin , name = 'adminhome'),
    path('mess', views.message , name = 'mess'),
    path('pred', views.prediction , name = 'pred'),
    path('userlist', views.userlist , name = 'userlist'),
    
    
    
    
    path('message', views.adminmessage , name = 'record'),
    path('main', views.Main , name = 'main'),
    path('outputs', views.Output , name = 'outputs'),
    path('contactus', views.Contactus , name = 'contactus'),
    path('about', views.About , name = 'about'),
    path('output',views.formInfo,name = 'output'),
    path('yp', views.recommendation , name = 'yp'),

 ]