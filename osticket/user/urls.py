from django.urls import path
from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

app_name = 'user'
urlpatterns = [
    path('logout/', views.logout_user, name='logout'),
    path('', views.login_user, name='login'),
    path('user/', views.homeuser, name='homeuser'),
    path('submitadmin/', views.submitadmin, name='submitadmin'),
    path('profile', views.detail_user, name='detail_user'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path(r'^resetpassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.resetpwd, name='resetpassword'),
    path(r'^agresetpassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.agresetpwd, name='agresetpassword'),
    path('user/history_<int:id>', views.history, name='history'),
    path('user/data/', views.user_data, name='user_data'),
]