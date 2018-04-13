from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('logout/', views.logout_user, name = 'logout'),
    path('', views.login_user, name = 'login'),
    path('user/', views.homeuser, name='homeuser'),
    path('profile', views.detail, name='detail'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('user/create_ticket',views.create_ticket, name='create_ticket'),
]