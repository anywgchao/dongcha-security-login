# coding:utf-8
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from SeMF.settings import APP_ID, USER_APP_SECRET, APP_KEY, APP_SECRET, INFO_LIST, VALID_TIME

# Create your views here.
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import django.utils.timezone as timezone
from django.contrib import auth
import datetime
from . import forms, models
import hashlib
from django.contrib.auth.hashers import make_password
from SeMFSetting.views import paging
from .service.init_permission import init_permission
from SeMFSetting.Functions.checkpsd import checkpsd
from SeMFSetting.Functions import mails
from django.db.models import Q
import json
import ssl

from ratelimit.decorators import ratelimit

from django.shortcuts import render
import requests
import time
import base64
import hmac
import redis

ssl._create_default_https_context = ssl._create_unverified_context

REAUEST_STATUS = {
    "0": "待审批",
    "1": "审批通过",
    "2": "审批拒绝",
}


@login_required
def main(request):
    if request.method == "POST":
        a = request.POST
        print(a)
    return render(request, "RBAC/userlist.html", {"post_url": "main"})


@login_required
def dashboard(request):
    return render(request, "Dashboard.html")


def operate_info(request, user, action, name, origin):  # 修改网站访问量和访问ip等信息
    try:
        num_id = models.UserLog.objects.latest('id').id
    except:
        num_id = 0
    if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取ip
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0]  # 所以这里是真实的ip
    else:
        client_ip = request.META['REMOTE_ADDR']  # 这里获得代理ip
    if action == '登录':
        des = '访问了系统'
    else:
        des = action + '了用户' + name

    models.UserLog.objects.create(
        uesr_logid=num_id,
        user_name=user,
        user_ip=client_ip,
        log_type='信息',
        log_origin=origin,
        user_action=action,
        action_description=str(user) + des,
    )


@login_required
def userlog(request):
    return render(request, "RBAC/userlog.html")


@login_required
@csrf_protect
def userloglist(request):
    user = request.user
    resultdict = {}
    page = request.POST.get('page')
    rows = request.POST.get('limit')

    name = request.POST.get('name')
    if not name:
        name = ''

    key = request.POST.get('key')
    if not key:
        key = ''

    log_origin = request.POST.get('origin')
    if not log_origin:
        log_origin = ''

    if user.is_superuser:
        loglist = models.UserLog.objects.filter(
            user_name__icontains=name,
            user_ip__icontains=key,
            log_origin__icontains=log_origin,
        ).all().order_by('-updatetime')
    else:
        loglist = models.UserLog.objects.filter(
            user_name__icontains=name,
            user_ip__icontains=key,
            log_origin__icontains=log_origin,
        ).all().order_by('-updatetime')
    total = loglist.count()
    loglist = paging(loglist, rows, page)
    data = []
    for log in loglist:
        dic = {}
        dic['uesr_logid'] = log.uesr_logid
        dic['user_name'] = log.user_name
        dic['user_ip'] = log.user_ip
        dic['user_origin'] = log.log_origin
        dic['user_action'] = log.user_action
        dic['action_description'] = log.action_description
        dic['updatetime'] = str(log.updatetime).split('.')[0]
        data.append(dic)
    resultdict['code'] = 0
    resultdict['msg'] = "用户访问列表"
    resultdict['count'] = total
    resultdict['data'] = data
    return JsonResponse(resultdict)


@csrf_protect
def resetpasswd(request, argu="resetpsd"):
    error = ""
    if argu == "resetpsd":
        if request.method == "POST":
            form = forms.ResetpsdRequestForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data["email"]
                user = get_object_or_404(User, email=email)
                if user:
                    hash_res = hashlib.md5()
                    hash_res.update(make_password(email).encode("utf-8"))
                    urlarg = hash_res.hexdigest()
                    models.UserResetpsd.objects.get_or_create(
                        email=email,
                        urlarg=urlarg
                    )
                    res = mails.sendresetpsdmail(email, urlarg)
                    if res:
                        error = "申请已发送，请检查邮件通知，请注意检查邮箱"
                    else:
                        error = "重置邮件发送失败，请重试"
                else:
                    error = "请检查信息是否正确"
            else:
                error = "请检查输入"
        else:
            form = forms.ResetpsdRequestForm()
        return render(request, "RBAC/resetpsdquest.html", {"form": form, "error": error})
    else:
        resetpsd = get_object_or_404(models.UserResetpsd, urlarg=argu)
        if resetpsd:
            email_get = resetpsd.email
            if request.method == "POST":
                form = forms.ResetpsdForm(request.POST)
                if form.is_valid():
                    email = form.cleaned_data["email"]
                    password = form.cleaned_data["password"]
                    repassword = form.cleaned_data["repassword"]
                    if checkpsd(password):
                        if password == repassword:
                            if email_get == email:
                                user = get_object_or_404(User, email=email)
                                if user:
                                    user.set_password(password)
                                    user.save()
                                    resetpsd.delete()
                                    return HttpResponseRedirect("/view/")

                                else:
                                    error = "用户信息有误"
                            else:
                                error = "用户邮箱不匹配"
                        else:
                            error = "两次密码不一致"
                    else:
                        error = "密码必须6位以上且包含字母、数字"
                else:
                    error = "请检查输入"
            else:
                form = forms.ResetpsdForm()
            return render(request, "RBAC/resetpsd.html", {"form": form, "error": error, "title": "重置"})


@login_required
@csrf_protect
def changeuserinfo(request):
    user = request.user
    error = ""
    if request.method == "POST":
        form = forms.UserInfoForm(request.POST, instance=user.profile)
        if form.is_valid():
            if "parent_email" in form.changed_data:
                parent_email = form.cleaned_data["parent_email"]
                parent_user = User.objects.filter(email=parent_email).first()
                if parent_user:
                    user.profile.parent = parent_user
                    user.save()
            form.save()
            operate_info(request, user, '修改', user, '')
            error = "修改成功"
        else:
            error = "请检查输入"
        return render(request, "formedit.html", {"form": form, "post_url": "changeuserinfo", "error": error})
    else:
        form = forms.UserInfoForm(instance=user.profile)
    return render(request, "formedit.html", {"form": form, "post_url": "changeuserinfo"})


@login_required
def userinfo(request):
    return render(request, "RBAC/userinfo.html")


@login_required
@csrf_protect
def changepsd(request):
    error = ""
    if request.method == "POST":
        form = forms.ChangPasswdForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["new_password"]
            re_new_password = form.cleaned_data["re_new_password"]
            username = request.user.username
            if checkpsd(new_password):
                if new_password and new_password == re_new_password:
                    if old_password:
                        user = auth.authenticate(username=username, password=old_password)
                        if user:
                            user.set_password(new_password)
                            user.save()
                            auth.logout(request)
                            error = "修改成功"
                        else:
                            error = "账号信息错误"
                    else:
                        error = "请检查原始密码"
                else:
                    error = "两次密码不一致"
            else:
                error = "密码必须6位以上且包含字母、数字"
        else:
            error = "请检查输入"
        return render(request, "formedit.html", {"form": form, "post_url": "changepsd", "error": error})
    else:
        form = forms.ChangPasswdForm()
    return render(request, "formedit.html", {"form": form, "post_url": "changepsd"})


@login_required
def logout(request):
    auth.logout(request)
    request.session.clear()
    return HttpResponseRedirect("/view/")


@csrf_protect
@ratelimit(key='ip', rate='7/h', block=True)
def login(request):
    if request.method == "POST":
        form = forms.SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user_get = User.objects.filter(username=username).first()
            if user_get:
                if user_get.profile.lock_time > timezone.now():
                    error = u"账号已锁定," + str(user_get.profile.lock_time.strftime("%Y-%m-%d %H:%M")) + "后可尝试"
                else:
                    user = auth.authenticate(username=username, password=password)
                    if user:
                        user.profile.error_count = 0
                        user.save()
                        auth.login(request, user)
                        # 这里需要加入权限初始化
                        init_permission(request, user)
                        operate_info(request, username, '登录', username, '本地')
                        return HttpResponseRedirect("/user/")
                    else:
                        user_get.profile.error_count += 1
                        if user_get.profile.error_count >= 5:
                            user_get.profile.error_count = 0
                            user_get.profile.lock_time = timezone.now() + datetime.timedelta(minutes=1)
                        user_get.save()
                        error = "登陆失败,已错误登录" + str(user_get.profile.error_count) + "次,5次后账号锁定",
            else:
                error = "请检查用户信息"

            form = forms.SigninForm()
        else:
            error = u"请检查输入"
        return render(request, "RBAC/login.html", {"form": form, "error": error})
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect("/user/")
        else:
            form = forms.SigninForm()
    return render(request, "RBAC/login.html", {"form": form})


@csrf_protect
@ratelimit(key='ip', rate='20/h', block=True)
def ding_login(request):
    form = forms.SigninForm(request.POST)
    if request.method == "POST":
        resultdict = dict()
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_get = models.UserRequest.objects.filter(
            Q(email=username) | Q(mobilephone=username)).exclude(is_use='不启用').first()
        if user_get:
            if user_get.lock_time > timezone.now():
                resultdict['code'] = 407
                resultdict['msg'] = "账号被锁定"
                resultdict['data'] = "Account locked"
                return JsonResponse(resultdict)
            else:
                psd = user_get.password
                if psd == password:
                    user_get.error_count = 0
                    user_get.save()
                    infolist = INFO_LIST
                    data_list = []
                    for i in infolist:
                        data = dict()
                        data['name'] = i[0]
                        data['url'] = i[1]
                        data['icon'] = i[2]
                        data_list.append(data)

                    token = generate_token(3600)
                    redis_connect(username, token)
                    resultdict['code'] = 200
                    resultdict['msg'] = "登录成功"
                    resultdict['data'] = data_list
                    resultdict['userid'] = username
                    resultdict['token'] = token
                    operate_info(request, username, '登录', username, '三方账号')
                    return JsonResponse(resultdict)
                else:
                    user_get.error_count += 1
                    if user_get.error_count >= 5:
                        user_get.error_count = 0
                        user_get.lock_time = timezone.now() + datetime.timedelta(minutes=1)
                        user_get.save()
                    resultdict['code'] = 407
                    resultdict['msg'] = "密码错误"
                    resultdict['data'] = 'Password mistake'
                    return JsonResponse(resultdict)
        else:
            resultdict['code'] = 407
            resultdict['msg'] = "非合法用户"
            resultdict['data'] = "Unauthorized user"
            return JsonResponse(resultdict)
    return render(request, "RBAC/login.html", {"form": form})


@login_required
@csrf_protect
def userlist(request):
    user = request.user
    error = ""
    if user.is_superuser:
        area = models.Area.objects.filter(parent__isnull=True)
        city = models.Area.objects.filter(parent__isnull=False)
        return render(request, "RBAC/userlist.html", {"area": area, "city": city})
    else:
        error = "权限错误"
    return render(request, "error.html", {"error": error})


@login_required
@csrf_protect
def userlisttable(request):
    user = request.user
    resultdict = {}
    error = ""
    page = request.POST.get("page")
    rows = request.POST.get("limit")
    email = request.POST.get("email")
    if not email:
        email = ""

    name = request.POST.get("name")
    if not name:
        name = ""

    mobilephone = request.POST.get("mobilephone")
    if not mobilephone:
        mobilephone = ""

    is_active = request.POST.get("is_active")
    if not is_active:
        is_active = ""
    else:
        is_active = is_active

    if user.is_superuser:
        user_list = models.UserRequest.objects.filter(email__icontains=email,
                                                      name__icontains=name,
                                                      mobilephone__icontains=mobilephone,
                                                      is_use__icontains=is_active).order_by("-starttime")
        total = user_list.count()
        user_list = paging(user_list, rows, page)
        data = []
        for user_item in user_list:
            dic = {}
            dic["name"] = user_item.name
            dic["nickname"] = user_item.nickname
            dic["mail"] = user_item.email
            dic["date"] = str(user_item.starttime).replace('T', ' ').split('.')[0]
            dic["mobilephone"] = user_item.mobilephone
            dic["is_use"] = user_item.is_use
            dic["lastlogin"] = str(user_item.starttime).replace('T', ' ').split('.')[0]
            dic["role"] = user_item.role
            data.append(dic)
        resultdict["code"] = 0
        resultdict["msg"] = "用户列表"
        resultdict["count"] = total
        resultdict["data"] = data
        return JsonResponse(resultdict)
    else:
        error = "权限错误"
    return render(request, "error.html", {"error": error})


@login_required
@csrf_protect
def userregisttable(request):
    user = request.user
    resultdict = {}
    error = ""
    page = request.POST.get("page")
    rows = request.POST.get("limit")

    email = request.POST.get("email")
    if not email:
        email = ""
    status = request.POST.get("status")
    if not status:
        status = ""
    is_use = request.POST.get("is_use")
    if not is_use:
        is_use = ["True", "False"]
    else:
        is_use = [is_use]
    is_check = request.POST.get("is_check")
    if not is_check:
        is_check = ["True", "False"]
    else:
        is_check = [is_check]

    if user.is_superuser:
        userrequest_list = models.UserRequest.objects.filter(email__icontains=email, status__icontains=status,
                                                             is_use__in=is_use, is_check__in=is_check).order_by(
            "is_check", "is_use", "-updatetime")
        total = userrequest_list.count()
        userrequest_list = paging(userrequest_list, rows, page)
        data = []
        for userrequest in userrequest_list:
            dic = {}
            dic["request_id"] = userrequest.id
            dic["email"] = userrequest.email
            if userrequest.is_check:
                dic["is_check"] = "已审批"
                dic["starttime"] = userrequest.starttime
                if userrequest.action_user:
                    dic["action_user"] = userrequest.action_user.username
                dic["updatetime"] = userrequest.updatetime
            else:
                dic["is_check"] = "待审批"
            if userrequest.is_use:
                dic["is_use"] = "已使用"
            else:
                dic["is_use"] = "待使用"
            dic["request_type"] = userrequest.request_type.title
            dic["status"] = REAUEST_STATUS[userrequest.status]
            data.append(dic)
        resultdict["code"] = 0
        resultdict["msg"] = "用户申请列表"
        resultdict["count"] = total
        resultdict["data"] = data
        return JsonResponse(resultdict)
    else:
        error = "权限错误"
    return render(request, "error.html", {"error": error})


# 添加用户
@login_required
@csrf_protect
def user_add(request):
    user = request.user
    if user.is_superuser:
        error = ""
        if request.method == "POST":
            name = request.POST.get('name')
            nickname = request.POST.get('nickname')
            role = request.POST.get('role')
            is_use = request.POST.get('is_use')
            email = request.POST.get('mails')
            mobilephone = request.POST.get('phone')
            password = request.POST.get('password')
            rpwd = request.POST.get('rpwd')
            user_get = models.UserRequest.objects.filter(email=email)
            if user_get:
                error = "用户已存在"
            else:
                if checkpsd(password):
                    if password == rpwd:
                        models.UserRequest.objects.get_or_create(
                            name=name,
                            nickname=nickname,
                            role=role,
                            is_use=is_use,
                            email=email,
                            mobilephone=mobilephone,
                            password=password,
                        )
                        error = '添加成功'
                        # operate_info(request, user, '添加', email)
                    else:
                        error = '两次密码不一致'
                else:
                    error = '请输入正常的密码格式'
        else:
            error = ''
    else:
        error = "请检查权限是否正确"
    return render(request, "SettingManage/add_user.html", {"post_url": "users", "error": error})


@login_required
@csrf_protect
def user_request_cancle(request):
    user = request.user
    error = ""
    if user.is_superuser:
        regist_id_list = request.POST.get("regist_id_list")
        regist_id_list = json.loads(regist_id_list)
        action = request.POST.get("action")
        for regist_id in regist_id_list:
            userregist = get_object_or_404(models.UserRequest, id=regist_id)
            userregist.status = "2"
            userregist.is_check = True
            userregist.is_use = True
            userregist.save()
            operate_info(request, user, '删除', userregist.email, '')
        error = "已禁用"
    else:
        error = "权限错误"
    return JsonResponse({"error": error})


@login_required
@csrf_protect
def user_disactivate(request):
    user = request.user
    if user.is_superuser:
        user_list = request.POST.get("user_list")
        user_list = json.loads(user_list)
        action = request.POST.get("action")
        for user_mail in user_list:
            user_get = get_object_or_404(models.UserRequest, email=user_mail)
            if action == "stop":
                user_get.is_check = True
                user_get.is_use = '不启用'
            elif action == "start":
                user_get.is_use = '启用'
            user_get.save()
        error = "已切换状态"
    else:
        error = "权限错误"
    return JsonResponse({"error": error})


@login_required
def user_data(request):
    return render(request, "SettingManage/user_info.html")


@login_required
def user_update(request, mail):
    user = request.user
    user_get = models.UserRequest.objects.filter(email=mail).first()
    result_data = dict()
    result_data['name'] = user_get.name
    result_data['nickname'] = user_get.nickname
    result_data['mobilephone'] = user_get.mobilephone
    result_data['email'] = user_get.email
    result_data['remark'] = user_get.remark
    result_data['password'] = user_get.password
    result_data['role'] = user_get.role
    result_data['is_use'] = user_get.is_use
    if user.is_superuser:
        error = ""
        if request.method == "POST":
            name = request.POST.get('name')
            nickname = request.POST.get('nickname')
            role = request.POST.get('role')
            is_use = request.POST.get('is_use')
            email = request.POST.get('mails')
            mobilephone = request.POST.get('phone')
            password = request.POST.get('password')
            rpwd = request.POST.get('rpwd')
            if checkpsd(password):
                if password == rpwd:
                    pass
                    models.UserRequest.objects.filter(email=mail).update(
                        name=str(name),
                        nickname=nickname,
                        role=role,
                        is_use=is_use,
                        email=str(email),
                        mobilephone=mobilephone,
                        password=password,
                    )
                else:
                    error = '两次密码不一致'
            else:
                error = '请输入正常的密码格式'
        else:
            error = "请检查权限是否正确"

    return render(request, "SettingManage/update_user.html",
                  {"post_url": "userupdate", 'argu': mail, 'data': result_data})


def generate_token(expire=60):
    key = 'ZGFiMjlk=ODY6NTliMz'
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")

    sha1_tshex_str = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str + ':' + sha1_tshex_str
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


def logins(request):
    """登录验证"""
    if request.method == "GET":
        resultdict = dict()
        code = request.GET.get('code', )
        if code:
            appId = APP_ID
            appSecret = USER_APP_SECRET

            token = requests.get(
                'https://oapi.dingtalk.com/sns/gettoken?appid={appId}&appsecret={appSecret}'.format(appId=appId,
                                                                                                    appSecret=appSecret))
            access_token = token.json()["access_token"]  # 获取扫码登录临时token

            tmp_auth_code = requests.post(
                "https://oapi.dingtalk.com/sns/get_persistent_code?access_token={access_token}".format(
                    access_token=access_token),
                json={
                    "tmp_auth_code": code
                })
            tmp_code = tmp_auth_code.json()
            openid = tmp_code['openid']
            persistent_code = tmp_code['persistent_code']

            sns_token_request = requests.post(
                "https://oapi.dingtalk.com/sns/get_sns_token?access_token={access_token}".format(
                    access_token=access_token),
                json={
                    "openid": openid,
                    "persistent_code": persistent_code
                })
            sns_token = sns_token_request.json()['sns_token']

            user_info_request = requests.get(
                'https://oapi.dingtalk.com/sns/getuserinfo?sns_token={sns_token}'.format(sns_token=sns_token))
            user_info = user_info_request.json()['user_info']  # 获取扫码用户信息
            unionid = user_info.get('unionid')

            access_token = requests.get(
                'https://oapi.dingtalk.com/gettoken?appkey={appId}&appsecret={appSecret}'.format(appId=APP_KEY,
                                                                                                 appSecret=APP_SECRET))
            access_token = access_token.json()["access_token"]  # 获取访问通讯录权限token

            user = requests.get(
                'https://oapi.dingtalk.com/user/getUseridByUnionid?access_token={access_token}&unionid={unionid}'.
                    format(access_token=access_token, unionid=unionid))

            user_id = user.json().get('userid')  # 根据unionid获取登录用户的userid

            if user_id:
                token = generate_token(3600)
                infolist = INFO_LIST
                data_list = []
                for i in infolist:
                    data = dict()
                    data['name'] = i[0]
                    data['url'] = i[1]
                    data['icon'] = i[2]
                    data_list.append(data)

                redis_connect(user_id, token)
                resultdict['code'] = 200
                resultdict['msg'] = "登录成功"
                resultdict['data'] = data_list
                resultdict['userid'] = user_id
                resultdict['token'] = token
                operate_info(request, user_id, '登录', user_info.get('nick'), '扫码登录')
                return JsonResponse(resultdict)
            else:
                resultdict['code'] = 407
                resultdict['msg'] = "非合法用户"
                resultdict['data'] = "Unauthorized user"
                return JsonResponse(resultdict)
        else:
            resultdict['code'] = 500
            resultdict['msg'] = "登陆失败，请重新登陆认证"
            resultdict['data'] = "Login failed"
            return JsonResponse(resultdict)


def redis_connect(username, token):
    valid_time = VALID_TIME
    # r = redis.Redis(host='127.0.0.1', port=6379, db=0, password='4cWZPP3mPyxdZzHR')
    r = redis.Redis(host='127.0.0.1', port=6379)

    r.set(username, token, ex=valid_time * 60 * 60)


def login_in(request):
    return render(request, "login.html")