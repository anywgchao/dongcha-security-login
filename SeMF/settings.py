# coding:utf-8

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5o@#+%b-%j_-47tzgdy6-e#hz+cu%*^#0$^%(2*ie!7++=&a)%'

# DEBUG = True
DEBUG = False


ALLOWED_HOSTS = ['*']
REGEX_URL = '{url}'  # url作严格匹配
# 设置不需要权限的页面
SAFE_URL = [
    '/view/',
    '/user/',
    '/login/',
    '/verification_code_login/',
    '/account_login/',
    '/data_transfer/',
    '/check_status/',
]

EMAIL_HOST = 'smtp.exmail.qq.com'  # SMTP地址
EMAIL_PORT = 465  # SMTP端口
EMAIL_HOST_USER = 'security@ishansong.com'  # 我自己的邮箱
EMAIL_HOST_PASSWORD = 'YjdS73embjf6YXRz'  # 我的邮箱密码
EMAIL_SUBJECT_PREFIX = u'[shansong]'  # 为邮件Subject-line前缀,默认是'[django]'
EMAIL_USE_SSL = True  # 与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false
# 管理员站点
SERVER_EMAIL = 'security@ishansong.com'
DEFAULT_FROM_EMAIL = '安全管控平台<security@ishansong.com>'

VALID_TIME = 8

# 设置网站根地址
WEB_URL = 'https://local-test-vpn.bingex.com'

INFO_LIST = [['运营系统', 'http://admin.ishansong.com/', WEB_URL + '/static/images/operation.png'],
             ['wiki', 'http://wiki.bingex.com/', WEB_URL + '/static/images/wiki.png'],
             ['客服系统', 'http://cs.ishansong.com/', WEB_URL + '/static/images/service.png'],
             ['sso系统', 'http://sso.ishansong.com/', WEB_URL + '/static/images/account.png']]
# 设置登录初始路径
LOGIN_URL = '/view/'

# 设置缓存文件路径
TMP_PATH = os.path.join(BASE_DIR, 'tmp')

# 设置登录session有效时间
SESSION_COOKIE_AGE = 60 * 500
# 设置session管理历览器失效
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# 设置上传路径
MEDIA_ROOT = os.path.join(BASE_DIR, 'files')
MEDIA_URL = "/uploads/"

# 定义session 键：
# 保存用户权限url列表
# 保存 权限菜单 和所有 菜单
SESSION_PERMISSION_URL_KEY = 'spuk'
SESSION_MENU_KEY = 'smk'
ALL_MENU_KEY = 'amk'
PERMISSION_MENU_KEY = 'pmk'

APP_ID = 'dingoaqsukcpmmvsaarq8o'
USER_APP_SECRET = 'f2oGACNfw3zFCLhi40UCplJv-dAmMV4ujCGS1AZbfsT90Jpg4BF5kPDkbx2z3W4J'

APP_KEY = 'dingc19i7nhs75vwtiel'
APP_SECRET = '78VVKXBdPb5J-BPK5I5hB83bLdFqGkwB2hYlBYGzijaO7JzjYHFjnNHvuOxgCJKc'

# APP_KEY = 'dingh3dxlg3xqe4pmqp6'
# APP_SECRET = 'buzJSrSCgQFZXCw9HsCcCRF2fcqiDVFBAoZ6l0syqgVRHH5Dy3rIM1IxC0Ufj8hk'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'RBAC',
    'SeMFSetting',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'RBAC.middleware.rbac.RbacMiddleware',
]

ROOT_URLCONF = 'SeMF.urls'

# 设置静态模板文件路径
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_PATH],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SeMF.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""

# 设置mysql数据配置信息
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'SeMF',
        'USER': 'semf_user',
        'PASSWORD': 'DdJLsiq8RhEgzX9u',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES' ",
            'charset': 'utf8',
        }
    }
}
"""

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/
LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

APPEND_SLASH = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collectstatic')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
