# Cloud_Security_Platform

#### 项目介绍
企业内网安全管理平台，包含资产管理，漏洞管理，账号管理，知识库管、安全扫描自动化功能模块，可用于企业内部的安全管理。
本平台旨在帮助公司实现，周期巡检，自动化安全扫描，更好的实现企业内部的安全管理。

#### 软件架构
后端系统 python3 + django2 + rabbitmq 实现。
前端显示 layui + bootstarp,使用开源模板 X-admin:http://x.xuebingsi.com/

#### 项目特点
1.  可自定义用户类型及权限信息
2.  资产类型和资产属性可在后台自定义，根据需要进行扩展
3.  内网资产发现和端口扫描可自动化进行
4.  完整的漏洞跟进和扫描器漏洞过滤
5.  包含web/主机扫描,git代码泄露扫描,0day精确扫描,公司全网段扫描等



#### 安装教程

1. 准备centos7系统，安装python3，mysql（选用），rabbitmq，nmap，安装方法可参照项目根目录中的文档《SeMF安装指南》
    
2. 下载解压本项目，并切换到项目路径，修改项目setting.py文件，根据需要设置 发件邮箱、rabbitmq参数以及数据库信息
    ```
    WEB_URL = 'http://localhost:8000'   //这里用来修改网站域名，可根据部署需要修改
    EMAIL_HOST/EMAIL_PORT...等邮件相关设置
    BROKER_URL    //用来设置队列信息和地址
    DATABASES    //可根据需要选择sqlite和mysql或其他数据库，设置文件中给出mysql设置方法，注意数据库的字符编码
    ```
3. 切换到项目根目录执行,分别执行以下命令
    ```
    pip install  -r requirements.txt         //安装python库
    python manage.py makemigrations        //数据表生成
    python manage.py migrate
    python manage.py createsuperuser    //创建超级管理员
    python initdata.py        //初始化数据库，主要生成角色，权限等信息
    python cnvd_xml.py        //用于同步cnvd漏洞数据文件，文件位于cnvd_xml目录下，可自行调整，该文件夹每周更新一次，
    celery -A SeMF worker -l info    //用于开启消费者，执行异步任务
    python manage.py runserver 0.0.0.0:8000    //运行成功，访问即可
    
    如需使用周期巡检和漏洞同步功能，需前往
    http://localhost:8000/semf/        页面设置扫描器API参数，当前支持nessus，后续会根据反馈添加其他扫描器
    ```

  


