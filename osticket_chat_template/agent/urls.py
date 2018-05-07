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
    path('inbox', views.inbox, name="inbox"),
    path('outbox', views.outbox, name="outbox"),
    path('profile', views.profile, name="profile"),
    path('manage_user', views.manager_user, name="manage_user"),
    path('block_user/<int:id>', views.block_user, name="block_user"),
    path('unblock_user/<int:id>', views.unblock_user, name="unblock_user"),
    path('accept_forward/<int:id>', views.accept_forward, name="accept_forward"),
    path('deny_forward/<int:id>', views.deny_forward, name="deny_forward"),
    path('cancel_forward/<int:id>', views.cancel_forward, name="cancel_forward"),
    path('accept_add/<int:id>', views.accept_add, name="accept_add"),
    path('deny_add/<int:id>', views.deny_add, name="deny_add"),
    path('cancel_add/<int:id>', views.cancel_add, name="cancel_add"),
    path('closed_ticket', views.closed_ticket, name='closed_ticket'),
    path('processing_ticket/conversation_<int:id>', views.conversation, name='conversation'),

]