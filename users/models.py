from django.db import models
from train.models import ExistTrains
from django.contrib.auth.models import AbstractUser


class UserInformation(AbstractUser):
    phone_number  = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.phone_number

    class Meta:
        db_table = "userinformation"

class IdentityInformation(models.Model):
    user = models.OneToOneField(UserInformation, on_delete=models.CASCADE, related_name="identity")
    
    name = models.CharField(blank=True, null=True)
    nationality = models.CharField(blank=True, null=True)
    national_code = models.BigIntegerField(blank=True, null=True)
    gender = models.CharField(
        max_length= 1,
        choices=[
            ('M','Male'),
            ('F','Female'),
        ],
        blank=True, null=True,
    )
    date_of_birth = models.DateField(blank=True, null=True)
    home_number = models.BigIntegerField(blank=True, null=True)
    essential_number = models.BigIntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.name} information'
    
    class Meta:
        db_table = 'identityinformation'


class Reservation(models.Model):
    user = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    train = models.ForeignKey(ExistTrains, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveBigIntegerField(editable=False)  
    reserved_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.train and hasattr(self.train, 'price'):
            self.total_price = self.train.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} → {self.train} × {self.quantity}"
    
    class Meta:
        db_table = 'reservation'