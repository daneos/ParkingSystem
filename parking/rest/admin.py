from django.contrib import admin

from rest.models import *

from django.db import models

admin.sites.AdminSite.site_header = "Parking System Admin"
admin.sites.AdminSite.site_title = "Application administration"

admin.site.register(User)
admin.site.register(Parking)
admin.site.register(Spot)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(TransactionMethod)
admin.site.register(Reservation)
admin.site.register(FreeSpot)
admin.site.register(Code)
admin.site.register(Car)
admin.site.register(Session)