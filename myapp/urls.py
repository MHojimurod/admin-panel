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
    path("update_status_back/<int:pk>/",update_status_back,name='update_status_back'),
    path("employee_accept/<int:pk>/",update_status_accept,name='employee_accept'),
    path("employee_delete/<int:pk>/",employee_delete,name='employee_delete'),
    path("employee_delete_list/",employee_delete_list,name='employee_delete_list'),
    path("employee_del/<int:pk>/",employee_del,name='employee_del'),
    path("create_request/",create_request,name='create_request'),
    path("create_request_user/",create_request_user),
    path("check_user/",check_user,name='check_user'),
    path("admins/",admins,name='admins'),
    path("admin_list/",admins_list),
    path("request_types/",request_types),
    path("requests_list/",requests_list,name='requests_list'),
    path("create_request_type/",create_request_type,name="create_request_type"),
    path("update_admin/<int:pk>/<int:stat>/",update_admin,name='update_admin'),
    path("update_status/",update_status_api),
    path("users_list/", get_users_list,name='users_list'),
    path("create_request_data/", create_request_data),
    path('get_request/', get_request),
    path('get_admins_by_list/', get_confirmers_list),
    path('get_request_from_user/', get_request_from_user),
    path('request_status_update/', request_status_update),
    path('get_waiting_sent_requests/', get_waiting_sent_requests),
    path('all_requests/',all_requests,name='all_requests'),
    path('register_group/',register_group),
    path('get_group/',get_group),
    path('get_excel/',get_excel,name='get_excel'),

    
]