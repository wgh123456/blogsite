from django.shortcuts import render
from . import send_email
from django.http import HttpResponse,HttpResponseRedirect
import json
import time
import os,uuid


# Create your views here.

#文件名hash化
def _hash_filename(filename):
    _, suffix = os.path.splitext(filename)
    return '%s%s' % (uuid.uuid4().hex, suffix) 


def emailcheckcode(request):
    if request.method == 'POST':
        last_time = request.session.get('checkcode_date')
        if last_time is None:
            last_time = 0
        now_time = time.time()
        if last_time+60>=now_time:
            resp = {'status': 100, 'data': '校验码在有效时间内'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        email_list = []   
        email = request.POST['email']
        if email=='':
            resp = {'status': 100, 'data': '邮箱不能为空'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        email_list.append(email)
        checkcode = send_email.create_sms_code()    
        request.session['checkcode'] = checkcode
        request.session['checkcode_date'] = time.time()

        send_email.send_sms_code(checkcode,1,email_list)
        resp = {'status': 200, 'data': '邮件已发送'}
        return HttpResponse(json.dumps(resp), content_type="application/json")

def generateUrl(filetype,source,file):
    if filetype=='image' and source=='cover':
        local_save_path = "static/images/cover/"
    elif filetype=='image' and source=='carousel':
        local_save_path = "static/images/carousel/"
    elif filetype=='image' and source=='contentImage':
        local_save_path = "static/images/detail/" + time.strftime("%Y%m%d", time.localtime()) + '/'
    elif filetype=='image' and source=='headshot':
        local_save_path = "static/images/headshot/"
    print(local_save_path)
    isExists = os.path.exists(local_save_path)
    if not isExists:
        os.makedirs(local_save_path) 
    hash_file_name = _hash_filename(file.name)

    local_save_file = local_save_path + hash_file_name
    # 图片拷贝
    with open(local_save_file, 'wb') as f:
        for line in file.chunks():
            f.write(line)
        f.close()

    url = 'http://www.memcpy.top/' + local_save_file
    print(url)
    return url

def uploadfile(request):
    if request.method == 'POST':
        source = request.POST['source']
        filetype = request.POST['filetype']
        filelist = request.FILES.getlist('file',None)
        print(filelist)
        
        if filelist == None:
            resp = {'status': 100, 'data': '请选择图片'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        imageUrl = []
        for file in filelist:
            url = generateUrl(filetype,source,file)
            imageUrl.append(url)

        if source=='contentImage':
            resp = {'errno': 0, 'data': imageUrl}
        else:
            resp = {'status': 200, 'data': imageUrl}
    return HttpResponse(json.dumps(resp), content_type="application/json")