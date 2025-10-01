from django.db import models
from train.models import ExistTrains
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("phone_number is necessary")
        phone_number = str(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
class UserInformation(AbstractBaseUser):
    phone_number  = models.CharField(max_length=20, unique=True)
    # password = models.CharField(max_length=128)

    # def set_password(self, raw_password):
    #     super().set_password(raw_password)
    #     self.save()

    def __str__(self):
        return self.phone_number
        
    
    

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    object = UserManager()
    
    class Meta:
        db_table = "userinformation"

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
    
    def __str__(self):
        return f'{self.name} information '
    
    class Meta:
        db_table = 'identityinformation'


class Reservation(models.Model):
    user = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    train = models.ForeignKey(ExistTrains, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveBigIntegerField()
    reserved_at = models.DateField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.user} → {self.train} × {self.quantity}"
    
    class Meta:
       db_table = 'reservation'
    