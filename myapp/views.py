from functools import total_ordering
import json
from django.core.servers.basehttp import WSGIServer
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Employee, RequestTypes
from django.contrib.auth.models import User
from django.contrib import messages
import datetime
from django.core.handlers.wsgi import WSGIRequest


def login_required_decorator(f):
    def wrapper(request: WSGIRequest):
        token = request.COOKIES.get('user_token')
        user = Employee.objects.filter(token=token)
        admin = request.user
        if not admin.is_anonymous:
            return f(request)
        elif user.exists() and user.first().status == 1:
            return f(request)
        return redirect('login1')
    return wrapper


@login_required_decorator
def dashboard(request):
    # print(request.GET, "id")
    return render(request, 'dashboard/index.html')


def dashboard_login(request: WSGIRequest):
    if not request.user.is_anonymous:
        return redirect('dashboard')
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'dashboard/login.html')


@login_required_decorator
def dashboard_logout(request: WSGIRequest):
    logout(request)
    res = redirect('login')
    res.delete_cookie("user_token")
    res.delete_cookie("tg_user")
    return res


def login_employee(request: WSGIRequest):
    token = request.COOKIES.get('user_token')
    user = Employee.objects.filter(token=token)
    if user.exists() and user.first().status == 1:
        return redirect('dashboard')
    data = request.GET.get('id')
    user = Employee.objects.filter(chat_id=data)
    if user.exists() and user.first().status == 1:
        res = redirect('dashboard')
        res.set_cookie("user_token", user[0].token)
        res.set_cookie("tg_user", json.dumps(request.GET.dict()))

        return res
    else:
        messages.info(request, "Hello wolrd")
        return render(request, "dashboard/login1.html")


@login_required_decorator
def employee_list(request):
    employee = Employee.objects.order_by('-id').filter(status=False).all()
    ctx = {
        'employee': employee,
        "t_active": 'active',
    }
    return render(request, 'dashboard/trainers/list.html', ctx)

# @login_required_decorator


def employee_deny(request):
    employee = Employee.objects.order_by('-id').filter(status=2).all()
    ctx = {
        'employee': employee,
        "f_active": 'active'
    }
    return render(request, 'dashboard/faculty/list.html', ctx)


# @login_required_decorator
def update_status_deny(request, pk):
    Employee.objects.filter(pk=pk).update(status=2)
    return redirect("employee_false")


# @login_required_decorator
def update_status_accept(request, pk):
    Employee.objects.filter(pk=pk).update(status=1)
    return redirect("employee_false")


def update_status_api(request):
    data = json.loads(request.body.decode("utf-8"))
    print(data)
    if data:
        user = Employee.objects.filter(id=data['rq']).first()
        print(data)
        user.status = int(data['status'])
        user.confirmer = Employee.objects.filter(id=int(data['admin'])).first()
        user.save()
        return JsonResponse({
            "ok": True,
            "status": int(data['status'])
        })
    return JsonResponse({
        "ok": False
    })


# @login_required_decorator
def employee_accept_list(request):
    employee = Employee.objects.order_by('-id').filter(status=True).all()
    # print(check.is_admin,'Admin')
    # print(check[0].is_admin,"Adfmin")
    return render(request, 'dashboard/user/list.html', {"employee": employee, "u_active": "active"})


def create_request(request: WSGIRequest):
    data = json.loads(request.body.decode('UTF-8'))
    data = Employee.objects.create(**data)
    print(data.id, type(data))
    a = {"ok": True,
         "rq_id": data.id}
    return JsonResponse(a)


def check_user(request: WSGIRequest):
    chat_id = json.loads(request.body.decode('UTF-8'))['chat_id']
    print(chat_id)
    data = Employee.objects.filter(chat_id=chat_id)
    if data.exists():
        return JsonResponse({
            "ok": True,
            "id": data[0].id,
            "name": data[0].name,
            "phone": data[0].phone,
            "chat_id": data[0].chat_id,
            "username": data[0].username,
            "desc": data[0].desc,
            "status": data[0].status,
            "is_admin": data[0].is_admin
        })
    return JsonResponse({
        "ok": False,
        "status": None
    })


# @login_required_decorator
def admins(request: WSGIRequest):
    data = Employee.objects.filter(is_admin=True).all()
    return render(request, "dashboard/order/list.html", {"admins": data, "a_active": "active"})


def admins_list(request: WSGIRequest):
    check = json.loads(request.body.decode("UTF-8"))['chat_id']
    if check:
        data = Employee.objects.filter(is_admin=True).all()
        if data:
            a = {
                "ok": True,
                "data": [
                    {
                        "id": i.id,
                        "chat_id": i.chat_id,
                    }for i in data
                ]
            }
            return JsonResponse(a, safe=False)
        return JsonResponse({
            "ok": False,
            "data": []
        })
    return JsonResponse({
        "ok": False,
        "data": []
    })


# @login_required_decorator
def update_admin(request, pk, stat=None):
    if stat == 1:
        Employee.objects.filter(pk=pk).update(is_admin=True)
        return redirect("employee_list")
    else:
        Employee.objects.filter(pk=pk).update(is_admin=False)
        return redirect("admins")


# @login_required_decorator
def request_types(request: WSGIRequest):
    check = json.loads(request.body.decode("UTF-8"))['chat_id']
    if check:
        data = RequestTypes.objects.all()
        if data:
            return JsonResponse({
                "ok": True,
                "data": [
                    {
                        "id": i.id,
                        "name": i.name,
                        "user": i.user.name,
                        "active": i.active,

                    }for i in data
                ]
            })
        return JsonResponse(
            {
                "ok": False,
                "data": []
            }
        )
    return JsonResponse({
        "ok": False,
        "data": []
    })


def get_users_list(request: WSGIRequest):
    users = Employee.objects.filter(status=1)
    return JsonResponse({
        "ok": True,
        "data": [
            {
                "id": user.id,
                "name": user.name,
                "username": user.username
            } for user in users
        ]
    })


def create_request_data(request: WSGIRequest):
    data = json.loads(request.body.decode('UTF-8'))
    data = Employee.objects.create(**data)
    a = {"ok": True, }
    return JsonResponse(a)




