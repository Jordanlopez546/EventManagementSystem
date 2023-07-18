from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('account-setting', views.setting, name='setting'),
    path('add-event/', views.add_event, name='add_event'),
    path('delete-event/', views.delete_event, name='delete_event'),
    path('added-event/', views.added_event, name='added_event'),
    path('event-registration/', views.event_registration, name='event_registration'),
    path('event-unregistration/', views.event_unregistration, name='event_unregistration'),
    path('registered-event/', views.registered_event, name='registered_event'),
]