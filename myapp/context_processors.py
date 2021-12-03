from django.core.handlers.wsgi import WSGIRequest
from .models import Employee
import json
from django.shortcuts import redirect
def check_admin(request:WSGIRequest):
    user = request.COOKIES.get('tg_user')
    if user is not None:
        user = user.replace('\'',  '"')
        print(user)
        user = json.loads(user)
        ctx = {
            "tg_user":user['first_name'],
            "tg_photo":user['photo_url'],
            "tg_url":f"https://t.me/{user['username']}"
        }
        return ctx
    return {}

def check_user(request:WSGIRequest):
    check = Employee.objects.filter(token=request.COOKIES.get("user_token")).first()
    if check:
        if check.is_admin:
            return {"is_admin":check}
        return {"is_admin":False}

    return {}
