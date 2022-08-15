from django.db import models

# Create your models here.

class LinkInfo(models.Model):
    linkname = models.CharField('导航名',max_length=50,null=False)
    linkname_md5 = models.CharField("linkname序列化",max_length=32,null=False)
    parent_id = models.IntegerField('父导航id',null=True)
    pinyin = models.CharField('拼音',max_length=500,null=False)
    isactive = models.BooleanField('是否可用',null=False,default=True)
    createtime = models.DateTimeField("创建时间",auto_now_add=True)
    updatetime = models.DateTimeField("更新时间",auto_now=True)

    class Meta:
        db_table = 'link_info'
        managed = True
        verbose_name = '导航信息'
        verbose_name_plural = verbose_name