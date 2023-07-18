from django.contrib import admin
from .models import *
# Register your models here.


class UserProfilePanel(admin.ModelAdmin):
    search_fields = ['user__username', 'email', 'address', 'phone_number']
    list_display = ['user', 'email', 'address', 'phone_number']


class EventPanel(admin.ModelAdmin):
    search_fields = ['event_organizer__user__username', 'event_name', 'event_guest_speakers']
    list_display = ['event_organizer', 'event_name', 'event_date', 'event_time', 'event_location']

class EventRegistrationPanel(admin.ModelAdmin):
    search_fields = ['event__event_organizer__user__username', 'event__event_name', 'event__event_guest_speakers', 'user__user__username', 'user__email', 'user__address', 'user__phone_number']
    list_display = ['user', 'event']


admin.site.register(UserProfile, UserProfilePanel)
admin.site.register(Event, EventPanel)
admin.site.register(EventRegistration, EventRegistrationPanel)
