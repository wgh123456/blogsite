from django.core.cache import cache
from .models import TagInfo

tagname2pinyin = {}
pinyin2tagname = {}

def set_tag_list():
    tag_list = TagInfo.objects.all()
    cache.set('tag_list',tag_list)
    for tag in tag_list:
        tagname2pinyin[tag.tagName] = tag.pinyin
        pinyin2tagname[tag.pinyin] = tag.tagName
        
    return tag_list

def get_tag_list(change=False):
    tag_list = cache.get('tag_list')
    if tag_list is None or change==True:
        tag_list = set_tag_list()
    return tag_list