from django.contrib import admin
from .models import Employee,RequestTypes,Requests
# Register your models here.
admin.site.register(Employee)
admin.site.register(RequestTypes)
admin.site.register(Requests)