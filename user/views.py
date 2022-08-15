import hashlib
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO
import os,json
import user
import time
import re
from .cacheUser import set_users_list,get_user_list,get_users_list
from user.models import Users,UserBaseInfo
from utils.views import generateUrl


# Create your views here.

def checkLogin(fn):
    def wrapper(request,*args,**kwargs):
        if 'user_uniqueid' not in request.session or 'user_email' not in request.session:
            return HttpResponseRedirect('/')
        else:
            c_user_uniqueid = request.COOKIES.get('user_uniqueid')
            c_user_email = request.COOKIES.get('user_email')
            if not c_user_uniqueid or not c_user_email:
                return HttpResponseRedirect('/')
        user_uniqueid = request.session.get('user_uniqueid')
        try:
            obj = get_users_list(False).get(uniqueid=user_uniqueid)
        except BaseException:
            return HttpResponseRedirect('/')
        else:
            if obj.permission!=1:
                return HttpResponseRedirect('/')

        return fn(request,*args,**kwargs)        
    return wrapper

def LoginStatus(request):
    if 'user_uniqueid' not in request.session or 'user_email' not in request.session:
        return False
    else:   
        c_user_uniqueid = request.COOKIES.get('user_uniqueid')
        c_user_email = request.COOKIES.get('user_email')
        if not c_user_uniqueid or not c_user_email:
            return False        
    return True

def login_user(request):
    
    if request.method == 'POST':
        resp = {'status': 100, 'data': '输入信息有误'}

        email = request.POST['email']
        password = request.POST['password']
        verify = request.POST['verify'].upper()
        remember = request.POST['remember']


        verify_session = request.session.get('verifycode','')
        if verify_session != verify:
            resp = {'status': 100, 'data': '验证码错误'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        try:
            user_obj = get_users_list(False).get(reg_email=email)
        except BaseException:
             return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            if user_obj.isactive !=1:
                resp = {'status': 100, 'data': '用户未激活，请联系管理员'}
                return HttpResponse(json.dumps(resp), content_type="application/json")
            m = hashlib.md5()
            m.update(password.encode())
            password_m = m.hexdigest()
            if email==user_obj.reg_email and password_m == user_obj.password:
                resp = {'status': 200, 'data': 'success'}   
            else:
                resp = {'status': 100, 'data': '输入信息有误错误'}
                return HttpResponse(json.dumps(resp), content_type="application/json")

        request.session['user_uniqueid'] = user_obj.uniqueid
        request.session['user_email']  = user_obj.reg_email
        resp = HttpResponse(json.dumps(resp), content_type="application/json")
        if remember=='true':
            resp.set_cookie('user_uniqueid',user_obj.uniqueid,3600*24*3)
            resp.set_cookie('user_email',user_obj.reg_email,3600*24*3)
        else:
            resp.set_cookie('user_uniqueid',user_obj.uniqueid,3600*12)
            resp.set_cookie('user_email',user_obj.reg_email,3600*12)
        return resp

def logout_user(request):
    if 'user_uniqueid' not in request.session or 'user_email' not in request.session:
        del request.session['user_uniqueid']
        del request.session['user_email']
   
    resp = HttpResponseRedirect('/')
    resp.delete_cookie('user_uniqueid')
    resp.delete_cookie('user_email')
    return resp

def register_user(request):
    if request.method == 'POST':
        resp = {'status': 100, 'data': '输入信息有误'}

        email = request.POST['email']
        checkcode = request.POST['checkcode']
        password = request.POST['password']
        ack_password = request.POST['ack_password']
        verify = request.POST['verify'].upper()

        # 密码
        if password!=ack_password:
            resp = {'status': 100, 'data': '两次密码不一致'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        # 校验码
        last_time = request.session.get('checkcode_date','')
        now_time = time.time()
        if last_time+60<now_time:
            resp = {'status': 100, 'data': '校验码已过期'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        checkcode_session = request.session['checkcode']  
        if checkcode != checkcode_session:
            resp = {'status': 100, 'data': '校验码错误'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        # 验证码
        verify_session = request.session.get('verifycode','')
        if verify_session != verify:
            resp = {'status': 100, 'data': '验证码错误'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        # 邮箱
        pattern = re.compile('\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}')
        if not re.fullmatch(pattern, email):
            resp = {'status': 100, 'data': '邮箱格式不正确'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        # 密码加密
        m = hashlib.md5()
        m.update(password.encode())
        password_md5 = m.hexdigest()

        uniqueid_md5 = hashlib.md5()
        uniqueid_md5.update(email.encode())
        uniqueid = uniqueid_md5.hexdigest()

        users_list = get_users_list(False)
        user_find = users_list.filter(reg_email=email)
        if user_find.count()!=0:
            resp = {'status': 100, 'data': '当前邮箱已注册'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        try:
            user_info_add = {
                'uniqueid':uniqueid,
                'level':0,
                'exp':0
            }

            user_info_obj = UserBaseInfo.objects.create(**user_info_add)

            user_add = {
                'uniqueid':uniqueid,
                'reg_email':email,
                'password':password_md5,
                'isactive':1,
                'permission':0
            }
            user_add_obj = Users.objects.create(**user_add,baseinfo=user_info_obj)

           
        except BaseException:    
            resp = {'status': 100, 'data': '注册失败'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            set_users_list()
            resp = {'status': 200, 'data': '注册成功'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

def verify_code(request):
    # 1，定义变量，用于画面的背景色、宽、高
    # random.randrange(20, 100)意思是在20到100之间随机找一个数
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 25
    # 2，创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 3，创建画笔对象
    draw = ImageDraw.Draw(im)
    # 4，调用画笔的point()函数绘制噪点，防止攻击
    for i in range(0, 100):
        # 噪点绘制的范围
        xy = (random.randrange(0, width), random.randrange(0, height))
        # 噪点的随机颜色
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        # 绘制出噪点
        draw.point(xy, fill=fill)
    # 5，定义验证码的备选值
    str1 = 'ABCD123EFGHJK456LMNPQRS789TUVWXYZ0'
    # 6，随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 7，构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('DejaVuSans.ttf', 23)
    # font = ImageFont.truetype('/home/code/blogsite/static/fonts/glyphicons-halflings-regular.ttf', 23)
    # 8，构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 9，绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 9，用完画笔，释放画笔
    del draw
    # 10，存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 11，内存文件操作
    buf = BytesIO()
    # 12，将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 13，将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

def update_user(request):
    if request.method=='POST':
        update_id = request.POST['update_id']
        type = request.POST['type']

        if type=='permission':
            content = request.POST['content']
            obj = get_users_list(False).filter(id=update_id).update(permission=content)
            set_users_list()
        elif type=='isactive':
            content = request.POST['content']
            obj = get_users_list(False).filter(id=update_id).update(isactive=content)
            set_users_list()
        elif type=='headshot':
            filelist = request.FILES.getlist('content',None)
            url = generateUrl('image','headshot',filelist[0])
            
            obj = get_users_list(False).get(id=update_id)
            UserBaseInfo.objects.filter(uniqueid=obj.uniqueid).update(headshot=url)
            set_users_list()
            resp = {'status': 200, 'data': url}
            return HttpResponse(json.dumps(resp), content_type="application/json") 
        elif type == 'username':
            content = request.POST['content']
            UserBaseInfo.objects.filter(uniqueid=update_id).update(username=content)
            set_users_list()
        elif type == 'sex':
            content = request.POST['content']
            UserBaseInfo.objects.filter(uniqueid=update_id).update(sex=content)
            set_users_list()    
        elif type == 'phone':
            content = request.POST['content']
            UserBaseInfo.objects.filter(uniqueid=update_id).update(phone=content)
            set_users_list()        
                   
    resp = {'status': 200, 'data': '修改成功'}
    return HttpResponse(json.dumps(resp), content_type="application/json")    



