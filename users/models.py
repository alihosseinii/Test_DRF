from django.db import models

# Create your models here.
class UserInformation(models.Model):
    phone_number  = models.BigIntegerField()
    password = models.CharField()


class IdentityInformation(models.Model):
    name = models.CharField(blank=True)
    nationality = models.CharField(blank=True)
    national_code = models.BigIntegerField(blank=True)
    gender = models.CharField(
        max_length= 1,
        choices=[
            ('M','Male'),
            ('F','Female'),
        ],
        blank=True,
    )
    date_of_birth = models.DateField(blank=True)
    home_number = models.BigIntegerField(blank=True)
    essential_number = models.BigIntegerField(blank=True)
    address = models.TextField(blank=True)
