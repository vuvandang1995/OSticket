from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'agent'
urlpatterns = [
    path('admin/', views.home_admin, name='home_admin'),
    path('admin/data', views.home_admin_data, name='home_admin_data'),
    path('topic/', views.manager_topic, name='manager_topic'),
    path('department/', views.manager_department, name='manager_department'),
    path('agent/', views.manager_agent, name='manager_agent'),
    path('', views.home_agent, name="index"),
    path('logout', views.logout, name="logout"),
    path('assign/<int:id>', views.assign_ticket, name="assign_ticket"),
    path('history/<int:id>', views.history, name="history"),
    path('history_all_ticket/<str:date>_<str:date2>', views.history_all_ticket, name="history_all_ticket"),
    path('inbox', views.inbox, name="inbox"),
    path('outbox', views.outbox, name="outbox"),
    path('processing_ticket/', views.processing_ticket, name="processing_ticket"),
    path('processing_ticket/data', views.processing_ticket_data, name="processing_ticket_data"),
    path('closed_ticket', views.closed_ticket, name='closed_ticket'),
    path('manage_user/', views.manager_user, name="manage_user"),
    path('manage_user/data', views.manage_user_data, name="manage_user_data"),
    path('profile', views.profile, name="profile"),
    path('logout_admin/', views.logout_admin, name='logout_admin'),
]