from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Cafe)
admin.site.register(models.Coupon)