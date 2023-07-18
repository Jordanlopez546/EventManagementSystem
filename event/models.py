from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

# Create your models here.

User = get_user_model()

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    email = models.CharField(max_length=10000000)
    bio = models.TextField(blank=True)
    address = models.CharField(max_length=10000000)
    profileimg = models.ImageField(upload_to='user_profile_photos', default='blank-profile-picture.png')
    phone_number = models.CharField(max_length=1000000)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.user.username}'
    


class Event(models.Model):
    event_organizer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=1000000)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=1000000)
    event_agenda = models.TextField()
    event_guest_speakers = models.CharField(max_length=1000000)
    event_ticket_price = models.FloatField()
    created_at = models.DateTimeField(default=datetime.now)
    event_registered_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.event_organizer.user.username} - {self.event_name}"
    


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    events_registered_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.user.username} - {self.event.event_name}"
    


