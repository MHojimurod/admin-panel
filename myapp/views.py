import json
from django.core.servers.basehttp import WSGIServer
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Employee
# from .forms import TrainerForm,EventsForm,FacultyForm,CourseForm
import datetime
from django.core.handlers.wsgi import WSGIRequest

def login_required_decorator(f):
    return login_required(f, login_url="login")

@login_required_decorator
def dashboard(request):
    return render(request, 'dashboard/index.html')

def dashboard_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'dashboard/login.html')

@login_required_decorator
def dashboard_logout(request):
    logout(request)
    return redirect('login')

def employee_list(request):
    employee = Employee.objects.order_by('-id').filter(status=False).all()
    ctx = {
        'employee':employee,
        "t_active": 'active'
    }
    return render(request,'dashboard/trainers/list.html',ctx)

def employee_deny(request):
    employee = Employee.objects.order_by('-id').filter(status=2).all()
    ctx = {
        'employee':employee,
        "f_active": 'active'
    }
    return render(request,'dashboard/faculty/list.html',ctx)


def trainer_create(request):
    # model = Trainers()
    # form = TrainerForm(request.POST,request.FILES, instance=model)
    # if request.POST:
        # print(request.POST)
        # if form.is_valid():
            # form.save()
            # return redirect('trainer_list')
        # else:
            # print(form.errors)
    ctx = {
        # "form": form
    }
    return render(request, 'dashboard/trainers/form.html', ctx)
def trainer_edit(request, pk):
    # model = Trainers.objects.get(id=pk)
    # form = TrainerForm(request.POST or None, instance=model)
    # if request.POST:
        # if form.is_valid():
            # form.save()
            # return redirect('trainer_list')
    ctx = {
        # "form": form
    }
    return render(request, 'dashboard/trainers/form.html', ctx)






def update_status_deny(request,pk):
    Employee.objects.filter(pk=pk).update(status=2)
    return redirect("employee_false")

def update_status_accept(request,pk):
    Employee.objects.filter(pk=pk).update(status=1)
    return redirect("employee_false")

def employee_accept_list(request):
    employee = Employee.objects.order_by('-id').filter(status=True).all()
    return render(request, 'dashboard/user/list.html',{"employee":employee,"u_active":"active"})


def create_request(request: WSGIRequest):
    data = json.loads(request.body.decode('UTF-8'))
    Employee.objects.create(**data)
    a = {}
    return JsonResponse(a)

def check_user(request:WSGIRequest):
    chat_id = json.loads(request.body.decode('UTF-8'))['chat_id']
    print(chat_id)
    data = Employee.objects.filter(chat_id=chat_id)
    if data.exists():
        return JsonResponse({
            "ok": True,
            "name":data[0].name,
            "phone":data[0].phone,
            "chat_id":data[0].chat_id,
            "username":data[0].username,
            "desc":data[0].desc,
            "status":data[0].status
        })
    return JsonResponse({
        "ok": False,
        "status":None
    })

