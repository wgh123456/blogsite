from ast import And
from django.shortcuts import render
from django.http import HttpResponse
import json
import hashlib
import pypinyin
from .models import LinkInfo
from .cacheLink import set_link_list,get_link_list,linkname2id,id2linkname

# Create your views here.

def pinyins(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

def addLink(request):
    if request.method=='POST':
        linkname = request.POST['linkname']
        parentlinkname = request.POST['parentlinkname']

        if linkname=='':
            resp = {'status': 100, 'data': '导航不能为空'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        m = hashlib.md5()
        m.update(linkname.encode())
        linkname_md5 = m.hexdigest()
        
        if(parentlinkname):
            parent_id = linkname2id.get(parentlinkname)
        else:
            parent_id = 0
        pinyin = pinyins(linkname)
        LinkInfo.objects.create(linkname=linkname,parent_id=parent_id,pinyin=pinyin,linkname_md5=linkname_md5)
        set_link_list()
        resp = {'status': 200, 'data': '保存成功'}
        return HttpResponse(json.dumps(resp), content_type="application/json")

def updateLink(request):
    if request.method=='POST':
        content = request.POST['content']
        update_id = request.POST['update_id']
        type = request.POST['type']

        if type == 'linkname':
            m = hashlib.md5()
            m.update(content.encode())
            linkname_md5 = m.hexdigest()

            pinyin = pinyins(content)

            obj = get_link_list(False).filter(id=update_id).update(linkname=content,linkname_md5=linkname_md5,pinyin=pinyin)
            set_link_list()
        elif type == 'isactive':
            if content == 'False' or content == 'false' or content == 'False\n' or content == 'false\n':
                content = False
            else:
                content = True    
            num = get_link_list(False).filter(parent_id=update_id).count()
            if num != 0 :
                resp = {'status': 100, 'data': '含有子链接，不可禁用'}
                return HttpResponse(json.dumps(resp), content_type="application/json")
            obj = get_link_list(False).filter(id=update_id).update(isactive=content)
            set_link_list()
        elif type == 'parentLink':
            split_str = content.split('-')
            obj = get_link_list(False).filter(id=update_id).update(parent_id=split_str[0])
            set_link_list()
        resp = {'status': 200, 'data': '修改成功'}
        return HttpResponse(json.dumps(resp), content_type="application/json")