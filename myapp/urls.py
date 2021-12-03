from django.urls import path
from .views import *
urlpatterns = [
    path("dashboard/",dashboard,name="dashboard"),
    path("",login_employee,name="login1"),
    path("login/",dashboard_login,name='login'),   
    path("logout/",dashboard_logout,name='logout'),
    path("employee/",employee_list,name='employee_false'),
    path("employee_list/",employee_accept_list,name='employee_list'),
    path("employee_deny/",employee_deny,name='employee_deny'),
    path("employee_denied/<int:pk>/",update_status_deny,name='employee_denied'),
    path("employee_accept/<int:pk>/",update_status_accept,name='employee_accept'),
    path("create_request/",create_request,name='create_user'),
    path("check_user/",check_user,name='check_user'),
    path("admins/",admins,name='admins'),
    path("admin_list/",admins_list),
    path("request_types/",request_types),
    path("update_admin/<int:pk>/<int:stat>/",update_admin,name='update_admin'),
    path("update_status/",update_status_api),
    path("users_list/", get_users_list,name='users_list'),
    path("create_request_data/", create_request_data),
    
]