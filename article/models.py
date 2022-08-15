from contextlib import nullcontext
from distutils.command.upload import upload
from statistics import mode
from django.db import models

# Create your models here.

class ArticleInfo(models.Model):
    articleTitle = models.CharField("文章标题",max_length=200,null=False)
    articleContent = models.TextField("内容",null=True)
    coverPath = models.ImageField(upload_to='static/images/cover/')
    classification = models.CharField("分类",max_length=200,null=False)
    tag = models.CharField("标签",max_length=200,null=False)
    author = models.CharField("作者",max_length=50,null=False,default='wgh')
    articleStatus = models.CharField("文章状态",max_length=30,null=False)
    sort = models.IntegerField("排序",default=100)
    createtime = models.DateTimeField("创建时间",auto_now_add=True)
    updatetime = models.DateTimeField("更新时间",auto_now=True)

    class Meta:
        db_table = 'article_info'
        managed = True
        verbose_name = '文章信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.articleTitle

class CarouselInfo(models.Model):
    CarTitle = models.CharField("轮播图标题",max_length=200,null=True)
    CarDetail = models.CharField("轮播图描述",max_length=200,null=True)
    CarImage = models.ImageField("轮播图图片",upload_to='static/images/carousel/')
    PointArticle = models.IntegerField("关联文章",default=1)
    status = models.BooleanField("状态",default=False)
    createtime = models.DateTimeField("创建时间",auto_now_add=True)
    updatetime = models.DateTimeField("更新时间",auto_now=True)

    class Meta:
        db_table = 'carousel_info'
        managed = True
        verbose_name = '轮播图信息'
        verbose_name_plural = verbose_name



   