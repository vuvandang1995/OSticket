from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('login/', views.login_user, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]