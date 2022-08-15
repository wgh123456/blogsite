from django.core.cache import cache
from .models import UserInfo,Users,UserBaseInfo


def set_user_list():
    user_list = UserInfo.objects.all()
    cache.set('user_list',user_list)
    return user_list

def get_user_list(change=False):
    user_list = cache.get('user_list')
    if user_list is None or change==True:
        user_list = set_user_list()
    return user_list

def set_users_list():
    users_list = Users.objects.all()
    cache.set('users_list',users_list)
    return users_list

def get_users_list(change=False): 
    users_list =  cache.get('users_list')
    if users_list is None or change==True:
        users_list = set_users_list()
    return users_list
