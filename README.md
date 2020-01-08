<!--
 * @Author: Daboluo
 * @Date: 2019-12-12 20:20:44
 * @LastEditTime : 2020-01-08 16:01:04
 * @LastEditors  : Do not edit
 -->

# 全网钉钉统一安全认证

结合ModHeader插件  对公司内部部分未认证系统 进行统一安全认证

## 流程图

* 1、获取 issbrowserid、issbrowsertoken

```flow
st=>start: 办公人员
e=>end: 完成
op1=>operation: Chrome插件
op2=>operation: Redis
io=>inputoutput: API认证网关
st(right)->op1(right)->io(right)->op2
```

* 2、插件携带 issbrowserid、issbrowsertoken 请求业务资源

```flow
st2=>start: 办公人员
e2=>end: 请求拦截

cond2=>condition: nginx+lua网关
io2=>operation: 业务系统
io3=>operation: chrome插件
st2->io3->cond2
cond2(yes)->io2(right)
cond2(no)->io3
```

## 接口使用说明

### 第一步、钉钉扫码登录

#### 1.1、前端调用

'<https://login-test.bingex.com/verification_code_login'>      (请求方式：GET)

参考链接:  '<https://ding-doc.dingtalk.com/doc#/serverapi2/kymkv6'>

#### 1.2、后端接收前端扫码完成传回的 code

#### 1.3、根据code、APP_KEY、APP_SECRET校验用户信息,并返回校验结果

* 1.3.1 登陆成功
将  userid:  token  键值对存入redis,有效期8小时

```JSON
{
    "msg":  "登陆成功"
    "data":  [{
        "name":  "xxxxxxx",
        "url":  "xxxxxxxx",
        "icon":  "xxxxxxx"
        },
        {
        "name":  "xxxxxxx",
        "url":  "xxxxxxxx",
        "icon":  "xxxxxxx"
    }],
    "code":  200,
    "userid":  "xxxxxxx",
    "token":  "xxxxxxx"
}
```

* 1.3.2 非合法用户

```JSON
{
    "msg":  "非合法用户"
    "data":  "Unauthorized  user",
    "code":  407
}
```

* 1.3.3 登录失败

```JSON
{
    "msg":  "登陆失败，请重新登陆认证"
    "data":  "Login  failed",
    "code":  500
}
```

## 二.  账号密码登录

2.1、前端调用
 '<https://login-test.bingex.com/account_login'>      (提交方式POST)

```JSON
data  =  {
    "username":  'xxxxx',
    "password":  'xxxxx'
    }
```

2.2、后端接收前端传回的账号密码

2.3、根据账号密码APP_KEY、APP_SECRET校验用户信息,并返回校验结果

* 2.3.1 登陆成功将 userid: token 键值对存入redis,有效期8小时

```JSON
{
    "msg":  "登陆成功"
    "data":  [{
        "name":  "xxxxxxx",
        "url":  "xxxxxxxx",
        "icon":  "xxxxxxx"
        },
        {
        "name":  "xxxxxxx",
        "url":  "xxxxxxxx",
        "icon":  "xxxxxxx"
    }],
    "code":  200,
    "userid":  "xxxxxxx",
    "token":  "xxxxxxx"
}
```

* 2.3.2 非第三方用户

```JSON
{
    "msg":  "非合法用户"
    "data":  "Unauthorized  user",
    "code":  407
}
```

* 2.3.3 账号密码不对

```JSON
{
    "msg":  "密码错误"
    "data":  "Password  mistak",
    "code":  408
}
```

* 2.3.4.账号被锁定

```JSON
{
    "msg":  "账号被锁定"
    "data":  "Account  locked",
    "code":  409
}
```

* 2.3.5 登录失败

```JSON
{
    "msg":  "登陆失败，请重新登陆认证"
    "data":  "Login  failed",
    "code":  500
}
```

### 其它配置

项目名：【内网SSO】

描述：内网SSO扫码登陆

回调接口： <https://dongcha-dinglogin.bingex.com/ding_login>

---
项目名：【业务网SSO】

描述：业务网SSO扫码登陆

回调接口：<https://dongcha-dinglogin-vpn.bingex.com/verification_code_login>

LOGO地址：
 <https://apkhouse.oss-cn-beijing.aliyuncs.com/vpn/icon-256x256.png>

---
DNS解析

* dongcha-dinglogin.bingex.com     39.107.218.219
* dongcha-dinglogin-vpn.bingex.com 39.107.218.219

---
钉钉IP白名单-获取内部通讯录-小程序
公司内部IP
106.39.46.254,
219.143.154.194,

阿里云出口IP
39.105.102.198,
39.105.131.102,
39.105.133.23,
39.105.91.107,
39.105.135.137,
39.96.58.235,
39.96.67.212,
39.96.14.231,
39.96.47.62,
123.56.20.195

---

### 安装部署服务侧

1、nginx 网关需要lua支持
2、安全控制目标站点加入 “/opt/jxwaf/”

```JAVA
location / {
    access_by_lua_file /opt/jxwaf/lualib/resty/netcontrol/accessControl.lua;
}
```

3、部署服务端程序

4、修改Reids配置（地址）

* 4.1  修改平台Redis配置，setting.py 中redis连接配置
* 4.2  修改/opt/jxwaf/lualib/resty/netcontrol/redisConn.lua redis连接配置

5、配置nginx服务

```JAVA
server {
    listen 80;
    server_name dongcha-dinglogin-vpn.bingex.com;
    add_header Strict-Transport-Security max-age=15768000;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443;
    server_name dongcha-dinglogin-vpn.bingex.com;
    access_log /opt/jxwaf/nginx/logs/login-test-vpn_access.log json;
    error_log /opt/jxwaf/nginx/logs/login-test-vpn_error.log;
    include  /opt/jxwaf/site/security_ssl;
    include  /opt/jxwaf/site/security_proxy;

    location /view/ {
        include  /opt/jxwaf/site/security_allow_ip;
    }

    location / {
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header REMOTE-HOST $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_hide_header X-Frame-Options;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass       http://127.0.0.1:8839;
    }
    location /static {
        alias /data/semf/dongcha-security-login/static;
    }
    location /static/admin {
        alias /data/semf/dongcha-security-login/venv/lib/python3.6/site-packages/django/contrib/admin/static/admin;
    }
}

```

### 安装用户侧

1、安装Chrome组件“闪送可信插件”
