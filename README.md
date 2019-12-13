### 全网钉钉统一安全认证
结合ModHeader插件  对公司内部部分未认证系统 进行统一安全认证

###接口使用说明
第一步.  钉钉扫码登录
1    前端调用    'https://login-test.bingex.com/verification_code_login'      (GET)
      参考链接:  'https://ding-doc.dingtalk.com/doc#/serverapi2/kymkv6'
2    后端接收前端扫码完成传回的  code
3    根据code、APP_KEY、APP_SECRET校验用户信息,并返回校验结果

1.登陆成功    将  userid:  token  键值对存入redis,有效期8小时
{
        "msg":  "登陆成功"
        "data":  [{
"name":  "xxxxxxx",
"url":  "xxxxxxxx",
"icon":  "xxxxxxx"
},  {
"name":  "xxxxxxx",
"url":  "xxxxxxxx",
"icon":  "xxxxxxx"
}],
        "code":  200,
        "userid":  "xxxxxxx",
        "token":  "xxxxxxx",
}

2.非合法用户
{
    "msg":  "非合法用户"
    "data":  "Unauthorized  user",
    "code":  407
}

3.登录失败
{
    "msg":  "登陆失败，请重新登陆认证"
    "data":  "Login  failed",
    "code":  500
}


二.  账号密码登录

1      前端调用      'https://login-test.bingex.com/account_login'      (POST)
  data  =  {
                            "username":  'xxxxx',
                          "password":  'xxxxx'
        }
        2      后端接收前端传回的账号密码

        3      根据账号密码    APP_KEY    APP_SECRET  校验用户信息,并返回校验结果
                1.登陆成功    将  userid:  token  键值对存入redis,有效期8小时
{
        "msg":  "登陆成功"
        "data":  [{
"name":  "xxxxxxx",
"url":  "xxxxxxxx",
"icon":  "xxxxxxx"
},  {
"name":  "xxxxxxx",
"url":  "xxxxxxxx",
"icon":  "xxxxxxx"
}],
        "code":  200,
        "userid":  "xxxxxxx",
        "token":  "xxxxxxx",
}

2.非第三方用户
{
    "msg":  "非合法用户"
    "data":  "Unauthorized  user",
    "code":  407
}

3.账号密码不对
{
    "msg":  "密码错误"
    "data":  "Password  mistak",
    "code":  408
}

4.账号被锁定
{
    "msg":  "账号被锁定"
    "data":  "Account  locked",
    "code":  409
}

5.登录失败
{
    "msg":  "登陆失败，请重新登陆认证"
    "data":  "Login  failed",
    "code":  500
}