from functools import total_ordering
import json
from django.core.servers.basehttp import WSGIServer
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout

from myapp.forms import RequestTypesForm
from .models import Employee, RequestTypes, Requests
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
    if request.GET:
        username = request.GET.get('username')
        password = request.GET.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'dashboard/login1.html')


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
    if user.exists() and user.first().status == 1 or not request.user.is_anonymous:
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


def employee_delete(request,pk):
    Employee.objects.filter(pk=pk).update(status=3)
    return redirect("employee_list")

def employee_del(request,pk):
    data = Employee.objects.filter(pk=pk)
    data.delete()
    return redirect("employee_delete_list")

def employee_delete_list(request):
    employee = Employee.objects.order_by('-id').filter(status=3).all()
    ctx = {
        'employee': employee,
        "d_active": 'active'
    }
    return render(request, 'dashboard/course/list.html', ctx)


# @login_required_decorator
def update_status_deny(request, pk):
    Employee.objects.filter(pk=pk).update(status=2)
    return redirect("employee_false")


# @login_required_decorator
def update_status_accept(request, pk):
    Employee.objects.filter(pk=pk).update(status=1)
    return redirect("employee_false")
def update_status_back(request, pk):
    Employee.objects.filter(pk=pk).update(status=1)
    return redirect("employee_delete_list")


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
    print(data)
    print('req_type = RequestTypes.objects.get(data[\'req_type\'])')

    req_type = RequestTypes.objects.get(id=data['req_type'])

    confirmers = []
    user = Employee.objects.filter(chat_id=data['user'])
    if user.exists():
        user = user.first()

    new_req = Requests(req_type=req_type, user=user, template=data['request_template'])
    new_req.save()

    for coner in data['req_confirmers']:
        con = Employee.objects.get(id=coner)
        if con:
            confirmers.append({
                "id": con.id,
                "name": con.name,
                "chat_id": con.chat_id,
                "username": con.username
            })
            new_req.confirmers.add(con)
    
    return JsonResponse({
        "ok": True,
        "data": {
            "id": new_req.id,
            "confirmers": confirmers,
            "template": new_req.template
        }
    })
    
def create_request_user(request):
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
            "is_admin": data[0].is_admin,
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
                        "templates": i.templates

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
                "username": user.username,
                "chat_id": user.chat_id,
            } for user in users
        ]
    })


def create_request_data(request: WSGIRequest):
    data = json.loads(request.body.decode('UTF-8'))
    print(data)
    return JsonResponse({})




def get_request(request: WSGIRequest):
    data = json.loads(request.body.decode('utf-8'))
    req = Employee.objects.filter(id=data['req'])
    if req.exists():
        return JsonResponse({
            "ok": True,
            "data": {
                "id": req.first().id,
                "name": req.first().name,
                "username": req.first().username,
                "number": req.first().phone
            }
        })
    return JsonResponse({
        "ok": False,
        "data":None
    })





def get_confirmers_list(request: WSGIRequest):
    data =json.loads(request.body.decode('utf-8'))
    confirmers = []
    print(data)
    for coner in data['confirmers']:
        con = Employee.objects.get(id=coner)
        if con:
            confirmers.append({
                "id": con.id,
                "name": con.name,
                "chat_id": con.chat_id,
                "username": con.username
            })
    
    return JsonResponse({
        "ok": True,
        "data": confirmers
    })


def get_request_from_user(request: WSGIRequest):
    data = json.loads(request.body.decode('utf-8'))
    req = Requests.objects.get(id=data['req_id'])
    if req:
        return JsonResponse({
            "ok": True,
            "data": {
                "id": req.id,
                "req_type": {
                    "id": req.req_type.id,
                    "name": req.req_type.name
                },
                "user": {
                    "id": req.user.id,
                    "name": req.user.name,
                    "username": req.user.username,
                    "chat_id": req.user.chat_id
                },
                "confirmers": [{
                    "id": coner.id,
                    "name": coner.name,
                    "username": coner.username
                } for coner in req.confirmers.all()],
                "template":req.template,
                "description": req.desc 
            }
        })


def test(request: WSGIRequest):
    return render(request,"dashboard/requests/test.html")



def create_request_type(request: WSGIRequest):
    employee = Employee.objects.filter(token=request.COOKIES.get('user_token'))
    model  = RequestTypes()
    forms  =RequestTypesForm(request.POST, instance=model)
    print(request.POST,"AAA")
    if forms.is_valid():
        forms.save()
        return redirect('requests_list')
    return render(request,"dashboard/events/form.html",{'data':employee.first()})

def requests_list(request: WSGIRequest):
    employee = Employee.objects.filter(token=request.COOKIES.get('user_token'))
    data = RequestTypes.objects.order_by('-id').all()
    return render(request,"dashboard/events/list.html",{"data":data,'employee':employee.first()})


def request_status_update(request: WSGIRequest):
    data = json.loads(request.body.decode('utf-8'))
    if data:
        coner = Employee.objects.filter(chat_id=data['chat_id']).first()
        print('keldi')
        Requests.objects.filter(pk=data['req_id']).update(status=data['status'], confirmer=coner)
        return JsonResponse({
            "ok": True
        })

    return JsonResponse({
        "ok":False
    })



def get_waiting_sent_requests(request: WSGIRequest):
    data = json.loads(request.body.decode('utf-8'))
    user = Employee.objects.filter(chat_id=data['chat_id'])
    if user.exists():
        user = user.first()
        reqs = Requests.objects.filter(user=user.id, status=0)
        if reqs:
            return JsonResponse({
                "ok": True,
                "data": [
                    {
                        "id": req.id,
                        "template": req.template,
                        "req_type": {
                    "id": req.req_type.id,
                    "name": req.req_type.name
                },
                        "confirmers": [{
                        "id": coner.id,
                        "name": coner.name,
                        "username": coner.username
                    } for coner in req.confirmers.all()],
                    } for req in reqs
                ]
            })
        return JsonResponse({
            "ok":False,
            "error": "requests_not_found",
        })
    return JsonResponse({
        "ok":False,
        "error": "user_not_found"
    })


def get_waiting_come_requests(request: WSGIRequest):
    data = json.loads(request.body.decode('utf-8'))
    user = Employee.objects.filter(chat_id=data['chat_id'])
    if user.exists():
        user = user.first()
        reqs = Requests.objects.filter(Tasdiqlovchilar__in=[user.id])
        if reqs:
            return JsonResponse({
                "ok": True,
                "data": [
                    {
                        "id": req.id,
                        "template": req.template,
                        "req_type": req.req_type,
                        "user":{
                            "id": req.user.id,
                            "name": req.user.name,
                            "chat_id": req.user.chat_id,
                            "username": req.user.username,
                        }
                    } for req in reqs
                ]
            })
        return JsonResponse({
            "ok":False
        })
    return JsonResponse({
        "ok":False
    })

