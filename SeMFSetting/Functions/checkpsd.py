#coding:utf-8

import re

def checkpsd(passwd):  
    p = re.match(r'^(?=.*?\d)(?=.*?[a-zA-Z]).{6,}$',passwd)
    if p:  
        return True  
    else:  
        return False


def checkmail(apply_user):
    p = re.match(r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$',apply_user)
    if p:
        return True
    else:
        return False