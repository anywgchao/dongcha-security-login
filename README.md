<!--
 * @Author: Daboluo
 * @Date: 2019-12-12 20:20:44
 * @LastEditTime : 2020-01-03 16:44:36
 * @LastEditors  : Do not edit
 -->

# 全网钉钉统一安全认证

结合ModHeader插件  对公司内部部分未认证系统 进行统一安全认证

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

回调域名： <https://dongcha-dinglogin.bingex.com/ding_login>
LOGO地址： <https://apkhouse.oss-cn-beijing.aliyuncs.com/vpn/icon-256x256.png>
项目名：【内网SSO】
描述：内网SSO扫码登陆

回调接口<https://dongcha-dinglogin-vpn.bingex.com/verification_code_login>
LOGO地址： <https://apkhouse.oss-cn-beijing.aliyuncs.com/vpn/icon-256x256.png>
项目名：【业务网SSO】
描述：业务网SSO扫码登陆

DNS解析
dongcha-dinglogin.bingex.com     39.107.218.219
dongcha-dinglogin-vpn.bingex.com 39.107.218.219

钉钉IP白名单-获取内部通讯录-小程序
106.39.46.254
219.143.154.194
123.56.20.195
124.127.252.242
39.105.135.137
39.105.133.23
39.105.131.102
39.105.91.107
