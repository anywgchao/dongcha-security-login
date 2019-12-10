# coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import django.utils.timezone as timezone


class Area(models.Model):
    name = models.CharField('属地信息', max_length=90, unique=True)
    parent = models.ForeignKey('self', verbose_name='父级属地', related_name='assetarea_area', null=True, blank=True,
                               on_delete=models.CASCADE)

    def __str__(self):
        # 显示层级菜单
        title_list = [self.name]
        p = self.parent
        while p:
            title_list.insert(0, p.name)
            p = p.parent
        return '-'.join(title_list)

    class Meta:
        # 设置模型的名字，但是记得复数形式也要设置，否则有些地方就变成 verbose_name + s 了
        verbose_name = '地区管理'
        verbose_name_plural = '地区管理'


# 设置菜单
class Menu(models.Model):
    title = models.CharField(u'菜单标题', max_length=25, unique=True)
    icon = models.CharField(u'菜单图标', max_length=50)
    parent = models.ForeignKey('self', verbose_name=u'父菜单', related_name='menu_menu', null=True, blank=True,
                               on_delete=models.CASCADE)

    def __str__(self):
        # 显示层级菜单
        title_list = [self.title]
        p = self.parent
        while p:
            title_list.insert(0, p.title)
            p = p.parent
        return '-'.join(title_list)

    class Meta:
        # 设置模型的名字，但是记得复数形式也要设置，否则有些地方就变成 verbose_name + s 了
        verbose_name = '菜单管理'
        verbose_name_plural = '菜单管理'


# 设置访问链接
class Permission(models.Model):
    title = models.CharField(u'权限标题', max_length=50, unique=True)
    is_menu = models.BooleanField('菜单显示', default=False)
    url = models.CharField(max_length=128)
    menu = models.ForeignKey(Menu, null=True, verbose_name=u'权限菜单', related_name='permission_menu',
                             on_delete=models.CASCADE)

    def __str__(self):
        return '{menu}--{permission}'.format(menu=self.menu, permission=self.title)

    class Meta:
        # 设置模型的名字，但是记得复数形式也要设置，否则有些地方就变成 verbose_name + s 了
        verbose_name = '权限管理'
        verbose_name_plural = '权限管理'


# 设置角色和权限
class Role(models.Model):
    title = models.CharField(u'角色名称', max_length=25, unique=True)
    permissions = models.ManyToManyField(Permission, verbose_name=u'权限菜单', related_name='role_permission')

    def __str__(self):
        return self.title

    class Meta:
        # 设置模型的名字，但是记得复数形式也要设置，否则有些地方就变成 verbose_name + s 了
        verbose_name = '角色管理'
        verbose_name_plural = '角色管理'


# 注册有审批时使用
class UserRequest(models.Model):
    name = models.CharField('用户名', max_length=50)
    nickname = models.CharField('昵称', max_length=50)
    mobilephone = models.CharField('手机号', max_length=50)
    email = models.EmailField('申请邮箱')
    remark = models.CharField('备注', max_length=50)
    password = models.CharField('密码', max_length=100)
    role = models.CharField('角色', max_length=100)
    is_use = models.CharField('状态', max_length=100)
    fail_num = models.CharField(u'失败次数', max_length=50, null=True, blank=True)
    time_space = models.CharField(u'登录时间间隔', max_length=50, null=True, blank=True)
    forbid_time_space = models.CharField(u'禁止登录时间间隔', max_length=50, null=True, blank=True)
    lock_time = models.DateTimeField(u'锁定时间', default=timezone.now)
    starttime = models.DateTimeField('申请时间', auto_now_add=True)

    action_user = models.ForeignKey(User, related_name='regist_for_actionuser', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.email

    class Meta:
        # 设置模型的名字，但是记得复数形式也要设置，否则有些地方就变成 verbose_name + s 了
        verbose_name = '用户请求'
        verbose_name_plural = '用户请求'


# 用户操作记录
class UserLog(models.Model):
    uesr_logid = models.CharField('编号', max_length=50, null=True)
    user_name = models.CharField('用户名', max_length=50, null=True)
    user_ip = models.CharField('来源ip', max_length=50, null=True)
    log_type = models.CharField('日志类型', max_length=50, null=True)
    log_origin = models.CharField('登录来源', max_length=50, null=True)
    user_action = models.CharField('操作内容', max_length=50, null=True)
    action_description = models.TextField('操作描述', null=True)
    updatetime = models.DateTimeField('时间', auto_now=True)

    def __str__(self):
        return self.user_name

    class Meta:
        # 设置模型的名字，但是记得复数形式也要设置，否则有些地方就变成 verbose_name + s 了
        verbose_name = '用户操作记录'
        verbose_name_plural = '用户操作记录'


# 重置密码时使用
class UserResetpsd(models.Model):
    email = models.EmailField('申请邮箱')
    urlarg = models.CharField('重置参数', max_length=50)

    is_check = models.BooleanField('是否使用', default=False)
    updatetime = models.DateField('更新时间', auto_now=True)

    def __str__(self):
        return self.email


class captcha(models.Model):
    captcha_name = models.CharField('验证', max_length=20, null=True)

    def __str__(self):
        return self.captcha_name


# 用户附加属性
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_num = models.CharField(u'员工编号', max_length=50, null=True, blank=True)
    title = models.CharField(u'职位名称', max_length=50)

    telephone = models.CharField(u'座机号码', max_length=50, null=True, blank=True)
    mobilephone = models.CharField(u'手机号码', max_length=50)
    description = models.TextField(u'用户简介')
    error_count = models.IntegerField(u'错误登陆', default=0)
    fail_num = models.CharField(u'失败次数', max_length=50, null=True, blank=True)
    time_space = models.CharField(u'登录时间间隔', max_length=50, null=True, blank=True)
    forbid_time_space = models.CharField(u'禁止登录时间间隔', max_length=50, null=True, blank=True)
    lock_time = models.DateTimeField(u'锁定时间', default=timezone.now)

    parent_email = models.EmailField('上级邮箱', null=True, blank=True)
    parent = models.ForeignKey(User, verbose_name='上级汇报', related_name='user_parent', null=True, blank=True,
                               on_delete=models.CASCADE)
    area = models.ForeignKey(Area, verbose_name='所属区域', related_name='user_area', null=True, on_delete=models.CASCADE,
                             limit_choices_to={'parent__isnull': True})

    roles = models.ManyToManyField(Role, verbose_name=u'所属角色', related_name='user_role')

    def __str__(self):
        return self.user.username

    class Meta:
        # 设置模型的名字，但是记得复数形式也要设置，否则有些地方就变成 verbose_name + s 了
        verbose_name = '用户附加属性'
        verbose_name_plural = '用户附加属性'


# 同步保存信息
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
