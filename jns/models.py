from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class Fiber(models.Model):
    int_name = models.CharField(max_length=200)
    date = models.DateField('date')
    switch = models.CharField(max_length=200)
    rxlevel = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.int_name
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.date <= now

class InterfaceCounters(models.Model):
    int_name = models.CharField(max_length=200)
    report_date = models.DateField('report_date')
    switch = models.CharField(max_length=200)
    int_desc = models.CharField(max_length=300)
    
    def __str__(self):
        return self.int_name

class Temperature(models.Model):
    int_name = models.CharField(max_length=200)
    date = models.DateField('date')
    switch = models.CharField(max_length=200)
    temperature = models.DecimalField(max_digits=7, decimal_places=0)

    def __str__(self):
        return self.int_name