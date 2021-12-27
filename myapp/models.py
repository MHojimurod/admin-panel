from datetime import datetime
from django.db import models
# Create your models here.

from django.contrib.auth.models import User
from uuid import uuid4
import hashlib
def md5(string: str):
    res = hashlib.md5(string)
    return str(res.hexdigest())


def make_token():
    return md5(str(uuid4()).encode())
class Employee(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    chat_id = models.IntegerField(default=0)
    username = models.CharField(max_length=200,null=True)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmer = models.ForeignKey("self", blank=True, on_delete=models.SET_NULL, null=True)
    is_admin = models.BooleanField(default=False)
    token = models.CharField(max_length=255, default=make_token)



    @property
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "chat_id": self.chat_id,
            "username":self.username,
            "status": self.status,
            "created_at": self.created_at,
            "confirmer": self.confirmer.json if self.confirmer != None else None,
            "is_admin": self.is_admin,
            "token": self.token
        }    
    def __str__(self):
        return self.name + " " + str(self.username)

    class Meta:
        # db_table = 'Xodimlar'
        verbose_name = "Xodimlar"

class Group(models.Model):
    chat_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    @property
    def json(self):
        return {
            "name": self.name,
            "chat_id": self.chat_id
        }
    def __str__(self):
        return self.name

class RequestTypes(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True,blank=True)
    active = models.BooleanField(default=True)
    template = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmers = models.ManyToManyField(Employee, related_name="Tasdiqlovchilar")
    groups = models.ManyToManyField(Group, null=True, blank=True)

    @property
    def json(self):
        return {
            "name": self.name,
            "user": self.user.json if self.user != None else None,
            "active": self.active,
            "template": self.template,
            "created_at": self.created_at,
            "confirmers": [con.json for con in self.confirmers.all()],
            "groups": [gr.json for gr in self.groups.all()]
        }

    
class Requests(models.Model):
    req_type = models.ForeignKey(RequestTypes, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="Yuboruvchi")
    status = models.IntegerField(default=0)
    confirmer = models.ForeignKey(Employee,on_delete=models.SET_NULL, null=True, related_name="Tasdiqlovchi")
    template = models.TextField()
    desc = models.TextField(null=True)
    confirm_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def status_str(self):
        return ['Kutilmoqda', 'Tasdiqlandi', "Rad etildi"][self.status]

    @property
    def json(self):
        return {
            "id": self.id,
            "req_type": self.req_type.json,
            "user": self.user.json,
            "status": self.status,
            "confirmer": self.confirmer.json if self.confirmer != None else None,
            "template": self.template,
            "desc":self.desc,
            "confirm_data": self.confirm_date,
            "sent_date": self.created_at
        }
    
   