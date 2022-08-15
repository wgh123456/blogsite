from django.core.cache import cache
from .models import ArticleInfo,CarouselInfo


def set_article_list():
    article_list = ArticleInfo.objects.all()
    cache.set('article_list',article_list)
    return article_list

def get_article_list(change=False):
    article_list = cache.get('article_list')
    if article_list is None or change==True:
        article_list = set_article_list()
    return article_list

def set_carousel_list():
    carousel_list = CarouselInfo.objects.all()
    cache.set('carousel_list',carousel_list)
    return carousel_list

def get_carousel_list(change=False):
    carousel_list = cache.get('carousel_list')
    if carousel_list is None or change==True:
        carousel_list = set_carousel_list()
    return carousel_list


