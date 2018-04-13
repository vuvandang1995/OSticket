from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('login/', views.login_user, name = 'login'),
    path('logout/', views.logout_user, name = 'logout'),
    path('register/', views.register, name = 'register'),
    path('', views.IndexView.as_view(), name='index'),
    path('user/', views.homeuser, name='homeuser'),
    path('profile', views.detail, name='detail'),
    path('user/create ticket',views.creat_ticket, name='create_ticket'),
]