from django.db import models
from django.urls import reverse

# Create your models here.

class UserInfo(models.Model):
    username = models.CharField("用户名",max_length=100,unique=True,null=True)
    password = models.CharField("密码",max_length=32,null=True)
    #状态区分账户是否可用，默认可用
    is_active = models.BooleanField("状态",default=0)
    # 用户级别区分管理员和普通用户0为普通用户，1为管理员
    rank = models.IntegerField("用户级别",default=0)
    level = models.IntegerField("用户等级",default=0)
    phone = models.CharField("手机号",max_length=11,null=True)
    email = models.EmailField("邮箱",max_length=254,null=True)
    sex = models.BooleanField("性别",null=True)
    headshot = models.ImageField("用户头像",upload_to='static/images/headshot/',null=True)
    createtime = models.DateTimeField("创建时间",auto_now_add=True)
    updatetime = models.DateTimeField("更新时间",auto_now=True)
    
        
    
    class Meta:
        db_table = 'user_info'
        managed = True
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    # 提供反向解析功能
    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
    

class UserBaseInfo(models.Model):
    uniqueid = models.CharField("用户唯一主键",max_length=32,unique=True)
    username = models.CharField("用户名",max_length=100,null=True)
    level = models.IntegerField("用户等级",default=0)
    exp = models.IntegerField("用户经验值",default=0)
    message_email = models.EmailField("消息邮箱",max_length=254,null=True)
    sex = models.BooleanField("性别",null=True)
    headshot = models.ImageField("用户头像",upload_to='static/images/headshot/',null=True)
    phone = models.CharField("手机号",max_length=11,null=True)
    wechat = models.CharField("微信",max_length=100,null=True) 
    qq = models.CharField("QQ",max_length=100,null=True) 
    realname = models.CharField("真实姓名",max_length=100,null=True)
    identity = models.CharField("身份证号",max_length=18,null=True)
    sex = models.BooleanField("性别",null=True)

    class Meta:
        db_table = 'userBaseInfo'
        managed = True
        verbose_name = '用户基础信息表'
        verbose_name_plural = verbose_name

class Users(models.Model):
    uniqueid = models.CharField("用户唯一主键",max_length=32,unique=True)
    reg_email = models.EmailField("注册邮箱",max_length=254)
    password = models.CharField("密码",max_length=32)
    #状态区分账户是否可用，默认可用
    isactive = models.BooleanField("状态",default=1)
    # 权限
    permission = models.BooleanField("权限",default=0)
    createtime = models.DateTimeField("创建时间",auto_now_add=True)
    updatetime = models.DateTimeField("更新时间",auto_now=True)
    baseinfo = models.OneToOneField(UserBaseInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'users'
        managed = True
        verbose_name = '用户登录注册表'
        verbose_name_plural = verbose_name


