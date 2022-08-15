from django.shortcuts import render
from django.http import HttpRequest, HttpResponse,HttpResponseRedirect
from django.views.generic import View,TemplateView
import os,json,uuid,time
from PIL import Image
from .models import ArticleInfo,CarouselInfo
from django.core.cache import cache
from .cacheArticle import get_article_list,set_article_list,set_carousel_list,get_carousel_list
from tag.cacheTag import get_tag_list
from link.cacheLink import get_link_list,linkname2id,id2linkname
import datetime
from link.cacheLink import linkmd52id
import hashlib
from django.db.models import Q
# Create your views here.


class AdminWriteView(TemplateView):
    template_name = "article/write_article.html"

    def get(self, request, *args, **kwargs):
        link_list = get_link_list(False).filter(~Q(parent_id=0))
        tag_list = get_tag_list(False)
        return render(request,'article/write_article.html',locals())

    def post(self, request, *args, **kwargs):
        resp = {'status': 200, 'data': '保存成功'}
        arTitle = request.POST['arTitle']
        arContent = request.POST['arContent']
        coverPath = request.POST['coverPath']
        classification = request.POST['classification']
        tag = request.POST['tag']
        statusArticle = request.POST['statusArticle']
        sort = request.POST['sort']
       
        if((arTitle== '') or (arContent=='') or (coverPath=='') or (classification=='') or (tag=='') or (statusArticle=='') or (sort=='')) :
            resp = {'status': 100, 'data': '信息不能为空'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        
        # m = hashlib.md5()
        # m.update(classification.encode())
        # linkname_md5 = m.hexdigest()
        link_id = linkname2id[classification]

        ArticleInfo.objects.create(
            articleTitle = arTitle,
            articleContent = arContent,
            coverPath = coverPath,
            classification = link_id,
            tag  = tag,
            author = "wgh",
            articleStatus = statusArticle,
            sort = sort
        )

        set_article_list()
        return HttpResponse(json.dumps(resp), content_type="application/json")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class UpdateArticleView(TemplateView):
    template_name = "article/update_article.html"

    def get(self, request, *args, **kwargs):
        try:
            articleid = int(request.GET['articleid'])
        except BaseException:
            return HttpResponseRedirect('/')
        else:
            # 查找对应id的文章
            article_item = get_article_list(False).filter(id=articleid)[0]
            # print(article_item)
            # 获取link
            link_queryset = get_link_list(False).filter(~Q(parent_id=0))
            selected_classification = id2linkname[article_item.classification]
            link_list = []
            for link_item in link_queryset:
                link_list.append(link_item.linkname)
            try:
                link_list.index(selected_classification)
            except:
                print("没有这个元素")    
            else:
                link_list.remove(selected_classification)
            # 获取tag
            tag_queryset = get_tag_list(False)
            tag_list = []
            # 已经选中的tag
            all_tag_list = article_item.tag.split(';')
            # 将最后一个空值去掉
            all_tag_list = [i for i in all_tag_list if i != '']
            # 循环遍历，将已经选择的tag从所有tag中去掉
            for tag_item in tag_queryset:
                if(tag_item.tagName in all_tag_list):
                    continue
                else:
                    tag_list.append(tag_item.tagName)
            
            return render(request,'article/update_article.html',locals())
        
    def post(self, request, *args, **kwargs):
        try:
            articleid = int(request.GET['articleid'])
        except BaseException:
            resp = {'status': 200, 'data': '未找到文章'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            resp = {'status': 200, 'data': '修改成功'}
            arTitle = request.POST['arTitle']
            arContent = request.POST['arContent']
            coverPath = request.POST['coverPath']
            classification = request.POST['classification']
            tag = request.POST['tag']
            statusArticle = request.POST['statusArticle']
            sort = request.POST['sort']
        
            # if((arTitle== '') or (arContent=='') or (coverPath=='') or (classification=='') or (tag=='') or (statusArticle=='') or (sort=='')) :
            #     resp = {'status': 100, 'data': '信息不能为空'}
            #     return HttpResponse(json.dumps(resp), content_type="application/json")
            updatetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            link_id = linkname2id[classification]

            ArticleInfo.objects.filter(id=articleid).update(
                articleTitle = arTitle,
                articleContent = arContent,
                coverPath = coverPath,
                classification = link_id,
                tag  = tag,
                # author = "wgh",
                # articleStatus = statusArticle,
                sort = sort,
                updatetime = updatetime
            )
           
            set_article_list()
        return HttpResponse(json.dumps(resp), content_type="application/json")   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CarouseEditlView(TemplateView):
    template_name = "article/edit_carousel.html"

    def get(self, request, *args, **kwargs):
        article_list = get_article_list(False)
        return render(request,'article/edit_carousel.html',locals())

    def post(self, request, *args, **kwargs):
        carouselPath = request.POST['carouselPath']
        titleCarousel = request.POST['titleCarousel']
        description = request.POST['description']
        related = request.POST['related']
        status = request.POST['status']

        split_str = related.split('-')


        CarouselInfo.objects.create(
            CarImage = carouselPath,
            CarTitle = titleCarousel,
            CarDetail = description,
            PointArticle = split_str[0],
            status  = status,
           
        )
        set_carousel_list()
        resp = {'status': 200, 'data': '成功'}
        return HttpResponse(json.dumps(resp), content_type="application/json")   

class UpdateCarouselView(View):
    def post(self, request, *args, **kwargs):
        content = request.POST['content']
        update_id = request.POST['update_id']
        type = request.POST['type']

        if type == 'articleid':
            split_str = content.split('-')
            obj = get_carousel_list(False).filter(id=update_id).update(PointArticle=split_str[0])
            set_carousel_list()
        elif type == 'status':
            if content == 'False' or content == 'false' or content == 'False\n' or content == 'false\n':
                content = False
            else:
                content = True    
           
            obj = get_carousel_list(False).filter(id=update_id).update(status=content)
            set_carousel_list()
        elif type == 'title':
            obj = get_carousel_list(False).filter(id=update_id).update(CarTitle=content)
            set_carousel_list()
        elif type == 'detail':    
            obj = get_carousel_list(False).filter(id=update_id).update(CarDetail=content)
            set_carousel_list()

        resp = {'status': 200, 'data': '修改成功'}
        return HttpResponse(json.dumps(resp), content_type="application/json")  

class DeleteArticleView(View):
    def get(self, request, *args, **kwargs):
        articleid = int(request.GET['id'])
        obj = get_article_list(False).filter(id=articleid)
        obj.delete()
        set_article_list()
        resp = {'status': 200, 'data': '删除成功'}
        return HttpResponse(json.dumps(resp), content_type="application/json")  