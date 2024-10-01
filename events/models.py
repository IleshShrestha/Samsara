from django.db import models



# Create your models here.
class Event(models.Model):
    name = models.CharField('event_name', max_length=255)
    date = models.DateField('event_date')
    description = models.TextField('event_description', max_length=300, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True )

