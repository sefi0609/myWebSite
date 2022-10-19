from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Event model for an sql table
class Event(models.Model):
    # Each event has an woner (user) - each user can see only their events 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'