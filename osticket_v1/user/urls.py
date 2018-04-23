from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('logout/', views.logout_user, name = 'logout'),
    path('', views.login_user, name = 'login'),
    path('user/', views.homeuser, name='homeuser'),
    path('submitadmin/', views.submitadmin, name='submitadmin'),
    path('profile', views.detail_user, name='detail_user'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path(r'^resetpassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.resetpwd, name='resetpassword'),
    path('user/<int:id>',views.close_ticket, name='close_ticket'),
]