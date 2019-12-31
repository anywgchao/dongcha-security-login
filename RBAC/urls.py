#coding:utf-8


from django.urls import path, re_path

from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('view/', views.login, name='login'),
    # path('view/', views.login_in, name='login'),
    path('verification_code_login/', views.logins, name='logins'),
    path('account_login/', views.ding_login, name='ding_login'),
    path('data_transfer/', views.data_transfer, name='data_transfer'),
    path('check_status/', views.check_status, name='check_status'),
    # re_path(r'^login', views.login_in, name='login'),
    # re_path(r'^logins', views.log_in, name='logins'),

    path('view/resetpsd/<str:argu>/', views.resetpasswd, name='resetpsds'),
    path('user/', views.dashboard, name='dashboard'),
    path('user/main/', views.main, name='main'),
    path('user/logout/', views.logout, name='logout'),
    path('user/changepsd/', views.changepsd, name='changepsd'),
    path('user/info/', views.userinfo, name='userinfo'),
    path('user/changeinfo/', views.changeuserinfo, name='changeuserinfo'),

    path('manage/user/', views.userlist, name='userview'),
    path('manage/user/list/', views.userlisttable, name='userlist'),
    path('manage/user/disactivate/', views.user_disactivate, name='userdisactivate'),

    path('manage/userrequest/list/', views.userregisttable, name='userregistlist'),
    path('manage/userrequest/stop/', views.user_request_cancle, name='userregiststop'),

    path('manage/userlog/', views.userlog, name='userlog'),
    path('manage/userlog/userloglist', views.userloglist, name='userloglist'),

    path('manage/users/', views.user_add, name='users'),
    path('manage/user_data/', views.user_data, name='user_data'),

    path('manage/users/user_update/<str:mail>/', views.user_update, name='userupdate'),

]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)