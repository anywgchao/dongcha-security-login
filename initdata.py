#! /usr/bin/python3
# -*- coding:UTF-8 -*-

import os

import django


def initmenu():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SeMF.settings')
    django.setup()
    from RBAC import models
    menu_list = [
        {'title': '系统设置', 'icon': "&#xe649;"},
    ]
    for item in menu_list:
        models.Menu.objects.get_or_create(
            title=item['title'],
            icon=item['icon']
        )

    submain_list = [

        {'title': '新增用户', 'icon': "&#xe60a;", 'parent_title': '系统设置'},
        {'title': '个人资料', 'icon': "&#xe60a;", 'parent_title': '系统设置'},
        {'title': '用户列表', 'icon': "&#xe60a;", 'parent_title': '系统设置'},
        {'title': '系统日志', 'icon': "&#xe63c;", 'parent_title': '系统设置'},

    ]

    for item in submain_list:
        models.Menu.objects.get_or_create(
            title=item['title'],
            icon=item['icon'],
            parent=models.Menu.objects.filter(
                title=item['parent_title']).first(),
        )

    permission_list = [
        {'title': '新增用户', 'url': '/manage/users',
            'is_menu': True, 'menu_title': '新增用户'},
        {'title': '个人资料', 'url': '/manage/user_data',
            'is_menu': True, 'menu_title': '个人资料'},
        {'title': '用户列表', 'url': '/manage/user/',
            'is_menu': True, 'menu_title': '用户列表'},
        {'title': '系统日志', 'url': '/manage/userlog/',
            'is_menu': True, 'menu_title': '系统日志'},

    ]
    for item in permission_list:
        permission_tup = models.Permission.objects.get_or_create(
            title=item['title'],
            url=item['url']
        )
        permission = permission_tup[0]
        if item['is_menu']:
            permission.menu = models.Menu.objects.filter(
                title=item['menu_title']).first()
            permission.save()


def initrole():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SeMF.settings')
    django.setup()
    from RBAC.models import Role, Permission
    permissions_list = [
        {'title': '安全管理员', 'permissions': '新增用户'},
        {'title': '安全管理员', 'permissions': '个人资料'},
        {'title': '安全管理员', 'permissions': '用户列表'},
        {'title': '安全管理员', 'permissions': '系统日志'},
    ]
    for item in permissions_list:
        role_list = Role.objects.get_or_create(title=item['title'])
        role_list[0].permissions.add(
            Permission.objects.filter(title=item['permissions']).first())
        role_list[0].save()

    print('initrole ok')


def initsuperuser():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SeMF.settings')
    django.setup()
    from RBAC.models import Role
    from django.contrib.auth.models import User
    user_manage_list = User.objects.filter(is_superuser=True)
    role = Role.objects.filter(title='安全管理员').first()
    for user in user_manage_list:
        user.profile.roles.add(role)
        user.save()
    print('initsuperuser ok')


if __name__ == "__main__":
    initmenu()
    initrole()
    initsuperuser()
