from django.db import models
# Create your models here.

from django.contrib.auth.models import User

class Employee(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    chat_id = models.IntegerField(default=0)
    username = models.CharField(max_length=200,null=True)
    desc = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmer = models.OneToOneField("self", blank=True, on_delete=models.SET_NULL, null=True)
    is_admin = models.BooleanField(default=False)


    def __str__(self):
        return self.name

    class Meta:
        # db_table = 'Xodimlar'
        verbose_name = "Xodimlar"



class RequestTypes(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
class Requests(models.Model):
    req_type = models.ForeignKey(RequestTypes, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="Yuboruvchi")
    status = models.IntegerField()
    confirmers = models.ManyToManyField(Employee, related_name="Tasdiqlovchilar")
    confirmer = models.OneToOneField(Employee, on_delete=models.SET_NULL, null=True, related_name="Tasdiqlagan_odam")
    template = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)