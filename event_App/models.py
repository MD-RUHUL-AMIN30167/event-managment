from django.db import models


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

    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='events')
    def __str__(self):
        return self.name


# Participant:
class Participant(models.Model):
    name=models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    events=models.ManyToManyField(Event,related_name='participants')
    def __str__(self):
        return self.name


