from django.contrib import admin
from .models import UserInformation, IdentityInformation, Reservation


admin.site.register(UserInformation)
admin.site.register(IdentityInformation)
admin.site.register(Reservation)
