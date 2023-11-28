from django.contrib import admin
from owner.models import *
# Register your models here.
admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(Carts)
admin.site.register(Reviews)
admin.site.register(Orders)