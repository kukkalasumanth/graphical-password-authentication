from django.urls import path
#now import the views.py file into this code
from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('login', views.login, name='login'),
    path('login_level_2', views.login_level_2, name='login_level_2'),
    path('login_level_3', views.login_level_3, name='login_level_3'),
    path('register', views.register, name='register'),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('forgot_password_1',views.forgot_password_1,name='forgot_password_1'),
    path('forgot_password_2',views.forgot_password_2,name='forgot_password_2'),
    path('register_level_2', views.register_level_2, name='register_level_2'),
    path('register_level_3',views.register_level_3,name='register_level_3')
    ]
