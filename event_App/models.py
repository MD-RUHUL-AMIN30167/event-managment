from django.db import models
from django.conf import settings


class Category(models.Model):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'

    CATEGORY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


    # event 
class Event(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=250)
    date=models.DateField()
    time=models.TimeField()
    location=models.CharField(max_length=250)
    event_image=models.ImageField(upload_to='image',blank=True,null=True)

    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='events')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='events_joined', blank=True)
    def __str__(self):
        return self.name


# Participant:
class Participant(models.Model):
    name=models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    events=models.ManyToManyField(Event,related_name='event_participants')
    def __str__(self):
        return self.name


