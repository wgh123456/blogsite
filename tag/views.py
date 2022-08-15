from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import TagInfo
from tag.cacheTag import set_tag_list
from django.core.cache import cache
from .cacheTag import set_tag_list,get_tag_list
import random
import pypinyin

# Create your views here.

color_list = [1,2,3,4,5,6,7,8]
# 1-->Primary
# 2-->Secondary
# 3-->Success
# 4-->Danger
# 5-->Warning
# 6-->Info
# 7-->Light
# 8-->Dark

def pinyins(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

def addTag(request):
    if request.method=='POST':
        tagname = request.POST.get('tagname')
        num_items = len(color_list)
        random_index = random.randrange(num_items)
        color = color_list[random_index]
        pinyin = pinyins(tagname)
        TagInfo.objects.create(tagName=tagname,pinyin=pinyin,color=color)
        set_tag_list()
        resp = {'status': 200, 'data': '保存成功'}
        return HttpResponse(json.dumps(resp), content_type="application/json")

def updateTag(request):
    if request.method=='POST':
        content = request.POST['content']
        update_id = request.POST['update_id']
        type = request.POST['type']

        if type == 'tagname':
            obj = get_tag_list(False).filter(id=update_id).update(tagName=content)
            set_tag_list()
        resp = {'status': 200, 'data': '修改成功'}
        return HttpResponse(json.dumps(resp), content_type="application/json")    