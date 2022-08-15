from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse,HttpResponseRedirect
from link.cacheLink import get_link_list,linkname2pinyin,pinyin2linkname,linkmd52id
from tag.cacheTag import get_tag_list,pinyin2tagname
from article.cacheArticle import get_article_list,get_carousel_list
from user.cacheUser import get_users_list
from django.core.paginator import Paginator
from user.views import LoginStatus,checkLogin
from django.utils.decorators import method_decorator

# Create your views here.

def formatting_link_list():
    item_list = []
    first_item = get_link_list(False).filter(parent_id=0).filter(isactive=1)

    for item in first_item :
        second_list = get_link_list(False).filter(parent_id=item.id).filter(isactive=1)
        dict_t = {}
        dict_t["first_item"] = item
        if second_list.exists() :
            dict_t["second_item"] = second_list
        else:
            dict_t["second_item"] = ''
        item_list.append(dict_t)

    return item_list
    
def recent_add_article():
    recent_add_article = get_article_list(False).order_by('-createtime')[:5]
    return recent_add_article

def recent_update_article():
    recent_update_article_list = get_article_list(False).order_by('-updatetime')[:5]
    return recent_update_article_list  


class FrontIndexView(TemplateView):
    template_name = "front/index.html"


    def get(self,request,*args,**kwargs):
        item_list = formatting_link_list()
        tag_list = get_tag_list(False)
        recent_add_article_list = recent_add_article()
        recent_update_article_list = recent_update_article()
        carousel_list = get_carousel_list(False).filter(status=1).order_by('-updatetime')[:5]

        loginStatus = LoginStatus(request)
        if loginStatus:
            user_uniqueid = request.session.get('user_uniqueid')
            user_info = get_users_list(False).get(uniqueid=user_uniqueid)

        article_list =get_article_list(False).order_by('-updatetime')
        paginator = Paginator(article_list,10)
        num_p = request.GET.get('page',1) #以page为键得到默认的页面1
        page=paginator.page(int(num_p))

       
        
        return render(request,'front/index.html',locals())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReadArticleView(TemplateView):
    template_name = "front/readarticle.html"

    def get(self,request,*args,**kwargs):
        item_list = formatting_link_list()
        tag_list = get_tag_list(False)
        recent_add_article_list = recent_add_article()
        recent_update_article_list = recent_update_article()

        loginStatus = LoginStatus(request)
        if loginStatus:
            user_uniqueid = request.session.get('user_uniqueid')
            user_info = get_users_list(False).get(uniqueid=user_uniqueid)

        try:
            articleid = int(request.GET['articleid'])
        except BaseException:
            return HttpResponse("error")
        else:
            # 查找对应id的文章
            article_item = get_article_list(False).filter(id=articleid)[0]
            all_tag_list = article_item.tag.split(';')
            # 将最后一个空值去掉
            all_tag_list = [i for i in all_tag_list if i != '']

        return render(request,"front/readarticle.html",locals())



class LinkGroupArticleView(TemplateView):
    template_name = "front/index.html"

    def get(self,request,*args,**kwargs):
        group = kwargs.get('group')
        linkid = linkmd52id.get(group)

        item_list = formatting_link_list()
        tag_list = get_tag_list(False)
        recent_add_article_list = recent_add_article()
        recent_update_article_list = recent_update_article()

        loginStatus = LoginStatus(request)
        if loginStatus:
            user_uniqueid = request.session.get('user_uniqueid')
            user_info = get_users_list(False).get(uniqueid=user_uniqueid)

        article_list =get_article_list(False).filter(classification=linkid).order_by('-updatetime')
        paginator = Paginator(article_list,10)
        num_p = request.GET.get('page',1) #以page为键得到默认的页面1
        page=paginator.page(int(num_p))

        return render(request,"front/index.html",locals())

class TagGroupArticleView(TemplateView):
    template_name = "front/index.html"

    def get(self,request,*args,**kwargs):
        group = kwargs.get('group')
        tagname = pinyin2tagname.get(group)

        item_list = formatting_link_list()
        tag_list = get_tag_list(False)
        recent_add_article_list = recent_add_article()
        recent_update_article_list = recent_update_article()

        loginStatus = LoginStatus(request)
        if loginStatus:
            user_uniqueid = request.session.get('user_uniqueid')
            user_info = get_users_list(False).get(uniqueid=user_uniqueid)

        article_list =get_article_list(False).filter(tag__contains=tagname).order_by('-updatetime')
        paginator = Paginator(article_list,10)
        num_p = request.GET.get('page',1) #以page为键得到默认的页面1
        page=paginator.page(int(num_p))

        return render(request,"front/index.html",locals())   


class SearchArticleView(TemplateView):
    template_name = "front/index.html"
    
    def get(self,request,*args,**kwargs):
        group = kwargs.get('group')
        # content = request.GET['content']
        

        item_list = formatting_link_list()
        tag_list = get_tag_list(False)
        recent_add_article_list = recent_add_article()
        recent_update_article_list = recent_update_article()

        loginStatus = LoginStatus(request)
        if loginStatus:
            user_uniqueid = request.session.get('user_uniqueid')
            user_info = get_users_list(False).get(uniqueid=user_uniqueid)


        article_list =get_article_list(False).filter(articleTitle__icontains=group).order_by('-updatetime')
        paginator = Paginator(article_list,10)
        num_p = request.GET.get('page',1) #以page为键得到默认的页面1
        page=paginator.page(int(num_p))

        return render(request,"front/index.html",locals())   