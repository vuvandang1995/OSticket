from django.urls import path

from . import views

app_name = 'agent'
urlpatterns = [
    path('admin/', views.home_admin, name = 'home_admin'),
    path('topic/', views.manager_topic, name = 'manager_topic'),
    path('agent/', views.manager_agent, name = 'manager_agent'),
    path('logout_admin/', views.logout_admin, name = 'logout_admin'),
    path('', views.home_agent, name="home_agent"),
    path('logout', views.logout, name="logout"),
    path('processing_ticket', views.processing_ticket, name="processing_ticket"),
    path('assign/<int:id>', views.assign_ticket, name="assign_ticket"),
    path('process/<int:id>', views.process, name="process"),
    path('done/<int:id>', views.done, name="done"),
    path('forward_ticket', views.forward_ticket, name="forward_ticket"),
    path('accept_forward/<int:id>', views.accept_forward, name="accept_forward"),
    path('deny_forward/<int:id>', views.deny_forward, name="deny_forward"),
    path('closed_ticket', views.closed_ticket, name='closed_ticket'),
]