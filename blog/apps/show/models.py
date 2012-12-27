# -*- coding:utf-8 -*-

from django.db import models

class Tag(models.Model):
    """标签"""

    name = models.CharField('名字', max_length=20)

    def __unicode__(self):

        return self.name

class Category(models.Model):
    """文章分类"""

    name = models.CharField('名字', 
        max_length=20, unique=True)

    def __unicode__(self):

        return self.name

class Article(models.Model):
    """博文"""

    title = models.CharField('标题', 
        max_length=80, unique=True,)
    content = models.TextField('内容')
    category = models.ForeignKey(
        Category, verbose_name="分类")
    tags = models.ManyToManyField(
        Tag, verbose_name='标签', 
        null=True, blank=True)

    readtimes = models.IntegerField('阅读次数', 
        default=1, null=True)
    instime = models.DateTimeField('插入时间', 
        auto_now_add=True)
    uptime = models.DateTimeField('更新时间', 
        auto_now=True)
    
    class Meta:

        ordering = ['-instime']
        
    def __unicode__(self):

        return self.title

    @property
    def pre_one(self):

        blog = Article.objects.filter(
            pk__lt=self.id).order_by('-pk')[0:1]

        return blog[0] if blog else None

    @property
    def later_one(self):

        blog = Article.objects.filter(
            pk__gt=self.id).order_by('pk')[0:1]
        
        return blog[0] if blog else None

    @property
    def get_comment_nums(self):

        return Comment.objects.filter(
            article=self).count()

class Comment(models.Model):
    """评论"""

    name = models.CharField('评论人', max_length=10)
    email = models.CharField('email', max_length=50)
    content = models.CharField('内容', max_length=200)
    instime = models.DateTimeField('插入时间', 
        auto_now_add=True)

    article = models.ForeignKey(
        Article, verbose_name="博文")

    class Meta:

        ordering = ['instime']

class FriendLink(models.Model):
    """友情链接"""

    name = models.CharField('内容', max_length=10)
    url = models.CharField('内容', max_length=50)
    weight = models.IntegerField('权重', default=1)

    class Meta:

        ordering = ['weight']
