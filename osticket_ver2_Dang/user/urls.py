from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('login/', views.login_user, name = 'login'),
    path('logout/', views.logout_user, name = 'logout'),
    path('register/', views.register, name = 'register'),
    path('', views.IndexView.as_view(), name='index'),
    #path('<int:user_id>/', views.homeuser, name='homeuser'),
    #path('<int:user_id>/profile', views.detail, name='detail'),
    path('user/', views.homeuser, name='homeuser'),
    path('profile', views.detail, name='detail'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]