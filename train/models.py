from django.db import models
from django.utils import timezone
#from datetime import datetime , date

# Create your models here.


class ExistTrains(models.Model):
    traintype = models.CharField(max_length=100)
    depratordate = models.DateField()
    depratortime = models.TimeField(default=timezone.now)
    price = models.BigIntegerField(default=2000000)
    returndate = models.DateField(blank=True)
    returntime = models.TimeField(blank=True)
    origin = models.CharField(max_length=300)
    destination = models.CharField(max_length=300)
    capacity = models.IntegerField(default=100)
    available = models.BooleanField(default=True)
    rules = models.TextField(default="""
        از زمان صدور تا ساعت ۱۲ ظهر روز قبل از حرکت
        %10 جریمه
        از ۱۲ ظهر روز قبل تا ۳ ساعت قبل از حرکت قطار
        %30 جریمه
        از ۳ ساعت قبل از حرکت قطار تا لحظه حرکت
        %50 جریمه
        پس از حرکت قطار
        %100 جریمه""")
    services = models.TextField(default="catering, train resturant available")
    #trainstations = models.ArrayField(models.CharField(blank=True))

    def __str__(self):
        return f'{self.origin} / to : {self.destination}'
    
    class Meta():
        db_table = 'existtrains'

class City (models.Model):
    country = models.CharField(max_length=300)
    cityname = models.CharField(max_length=300)
    
    def __str__(self):
        return f'{self.country} , {self.cityname}'
    
    class Meta():
        db_table = 'city'