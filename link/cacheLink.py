from django.core.cache import cache
from pypinyin import pinyin
from .models import LinkInfo

linkname2id = {}
id2linkname = {}
linkname2pinyin = {}
pinyin2linkname = {}
linkmd52id = {}

def set_link_list():
    link_list = LinkInfo.objects.all()
    cache.set('link_list',link_list)
    for link in link_list:
        linkname2id[link.linkname] = link.id
        id2linkname[str(link.id)] = link.linkname
        linkname2pinyin[link.linkname] = link.pinyin
        pinyin2linkname[link.pinyin] = link.linkname
        linkmd52id[link.linkname_md5] = link.id
    return link_list

def get_link_list(change=False):
    link_list = cache.get('link_list')
    if link_list is None or change==True:
        link_list = set_link_list()
    return link_list
