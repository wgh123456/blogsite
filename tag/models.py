from django.db import models

# Create your models here.

class TagInfo(models.Model):
    tagName = models.CharField('标签名',max_length=50,null=False)
    pinyin = models.CharField('拼音',max_length=200,null=False)
    color = models.IntegerField('标签颜色',null=True)
    createtime = models.DateTimeField("创建时间",auto_now_add=True)
    updatetime = models.DateTimeField("更新时间",auto_now=True)

    class Meta:
        db_table = 'tag_info'
        managed = True
        verbose_name = '标签信息'
        verbose_name_plural = verbose_name