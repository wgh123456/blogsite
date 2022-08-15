from django.shortcuts import render
from django.http import HttpRequest,HttpResponse,HttpResponse
from django.http.response import JsonResponse
from django.views.generic import View,ListView,TemplateView
import json,time, uuid, os.path
from PIL import Image
from article.models import ArticleInfo
# from article.cacheArticle import ArticleCache
from article.cacheArticle import get_article_list,get_carousel_list
from tag.cacheTag import get_tag_list
from link.cacheLink import get_link_list,id2linkname
from django.views.decorators.cache import never_cache,cache_page
from django.core.paginator import Paginator
from user.views import checkLogin
from user.cacheUser import get_user_list,set_user_list,get_users_list,set_users_list
from django.utils.decorators import method_decorator


# Create your views here.

pageItem = 7


def admin_index(request):
    return HttpResponse("ok")

@method_decorator(checkLogin, name='dispatch')
class AdminIndexView(TemplateView):
    template_name = "myadmin/admin_index_data.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(checkLogin, name='dispatch')
class AdminUserxView(TemplateView):
    template_name = "myadmin/admin_user_manager.html"
    def get(self, request, *args, **kwargs):
        user_list = get_users_list(False)
        paginator = Paginator(user_list,pageItem)
        num_p = request.GET.get('page',1) #以page为键得到默认的页面1
        page=paginator.page(int(num_p))
        return render(request,'myadmin/admin_user_manager.html',locals())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(checkLogin, name='dispatch')
class AdminArticleView(TemplateView):
    template_name = "myadmin/admin_article_manager.html"

    def get(self, request, *args, **kwargs):
        article_list =get_article_list(False)
        paginator = Paginator(article_list,pageItem)
        num_p = request.GET.get('page',1) #以page为键得到默认的页面1
        page=paginator.page(int(num_p))
        return render(request,'myadmin/admin_article_manager.html',locals())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # article_list =get_article_list(False)
        # context['article_result'] = article_list
        return context

@method_decorator(checkLogin, name='dispatch')
class AdminTagView(TemplateView):
    template_name = "myadmin/admin_tag_manager.html"

    def get(self,request,*args,**kwargs):
        tag_list = get_tag_list(False)
        paginator = Paginator(tag_list,pageItem)
        num_p = request.GET.get('page',1) #以page为键得到默认的页面1
        page=paginator.page(int(num_p))
        return render(request,'myadmin/admin_tag_manager.html',locals())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_list = get_tag_list(False)
        context['tag_result'] = tag_list
        return context


@method_decorator(checkLogin, name='dispatch')
class AdminLinkView(TemplateView):
    template_name = "myadmin/admin_link_manager.html"

    def get(self,request,*args,**kwargs):
        link_list = get_link_list(False)
        paginator = Paginator(link_list,pageItem)
        num_p = request.GET.get('page',1) #以page为键得到默认的页面1
        page=paginator.page(int(num_p))
        parent_link_list = link_list.filter(parent_id=0)
        linkid2linkname = id2linkname
        return render(request,'myadmin/admin_link_manager.html',locals())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        link_list = get_link_list(False)
        context['link_result'] = link_list
        return context

@method_decorator(checkLogin, name='dispatch')
class AdminCarouselView(TemplateView):
    template_name = "myadmin/admin_carousel_manager.html"

    def get(self,request,*args,**kwargs):
        article_list =get_article_list(False)
        carousel_list = get_carousel_list(False)
        paginator = Paginator(carousel_list,pageItem)
        num_p = request.GET.get('page',1) #以page为键得到默认的页面1
        page=paginator.page(int(num_p))

        return render(request,'myadmin/admin_carousel_manager.html',locals())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carousel_list = get_carousel_list(False)
        context['carousel_result'] = carousel_list
        return context        