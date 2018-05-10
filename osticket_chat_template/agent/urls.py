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
    path('give_up/<int:id>', views.give_up, name="give_up"),
    path('assign/<int:id>', views.assign_ticket, name="assign_ticket"),
    path('process/<int:id>', views.process, name="process"),
    path('done/<int:id>', views.done, name="done"),
    path('history/<int:id>', views.history, name="history"),
    path('inbox', views.inbox, name="inbox"),
    path('inbox/<int:foa>_<int:choose>_<int:id>', views.inbox_interaction, name="inbox_interaction"),
    path('outbox', views.outbox, name="outbox"),
    path('outbox/<int:foa>_<int:id>', views.outbox_interaction, name="outbox_interaction"),
    path('profile', views.profile, name="profile"),
    path('manage_user', views.manager_user, name="manage_user"),
    path('manage_user/<int:choose>_<int:id>', views.manager_user_interaction, name="manage_user_interaction"),
    path('closed_ticket', views.closed_ticket, name='closed_ticket'),
    path('processing_ticket/conversation_<int:id>', views.conversation, name='conversation'),
]