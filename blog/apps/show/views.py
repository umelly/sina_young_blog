# -*- coding:utf-8 -*-

import random
import datetime

from django.template import RequestContext
from django.http import HttpResponse, \
    Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, \
    get_object_or_404
from django.db import transaction

from django.contrib.auth.decorators import login_required

from forms import ArticleForm, CategoryForm
from models import Article, Comment

def index(request):

    tags_clouds = {}

    blogs = Article.objects.all()
    for blog in blogs:
        for tag in blog.tags.all():
            tags_clouds.setdefault(tag.name, 1.0)
            tags_clouds[tag.name] += 1/20.0

    recent_comments = Comment.objects.all()[:5]
    arts = Article.objects.all()
    if arts.count()<=5:
        random_blog = arts
    else:
        random_blog = arts[random.randint(arts.count())-5:]

    return render_to_response('index.html',
        {"blogs":blogs,
         "tags_clouds": tags_clouds,
         "random_blog": random_blog,
         "recent_comments": recent_comments,},
        context_instance=RequestContext(request))

def show_blog(request, blog_id=0):
    
    blog = get_object_or_404(Article, pk=blog_id)
    comments = Comment.objects.filter(
        article__pk=blog.id)

    tags_clouds = {}

    blogs = Article.objects.all()
    for _blog in blogs:
        for tag in _blog.tags.all():
            tags_clouds.setdefault(tag.name, 1.0)
            tags_clouds[tag.name] += 1/20.0

    recent_comments = Comment.objects.all()[:5]
    arts = Article.objects.all()
    if arts.count()<=5:
        random_blog = arts
    else:
        random_blog = arts[random.randint(arts.count())-5:]

    return render_to_response('show_blog.html',
        {"blog":blog,
         "tags_clouds": tags_clouds,
         "random_blog": random_blog,
         "recent_comments": recent_comments,
         "comments": comments,},
        context_instance=RequestContext(request))

def about_tag_blogs(request, tag_str):

    blogs = []

    tags_clouds = {}

    _blogs = Article.objects.all()
    for _blog in _blogs:
        for tag in _blog.tags.all():
            tags_clouds.setdefault(tag.name, 1.0)
            tags_clouds[tag.name] += 1/20.0

    recent_comments = Comment.objects.all()[:5]
    arts = Article.objects.all()
    if arts.count()<=5:
        random_blog = arts
    else:
        random_blog = arts[random.randint(arts.count())-5:]

    for blog in Article.objects.all():
        for tag in blog.tags.select_related():
            if tag_str == tag.name.strip():
                blogs.append(blog)

    return render_to_response('about_tag_blog.html',
        {"blogs":blogs,
         "tag_str":tag_str,
         "tags_clouds": tags_clouds,
         "random_blog": random_blog,
         "recent_comments": recent_comments},
        context_instance=RequestContext(request))

@transaction.commit_on_success
def post_comment(request):

    user = request.POST.get('user')
    content = request.POST.get('content')
    email = request.POST.get('email')
    blog_id = request.POST.get('blog_id')
    quote = request.POST.get("quote", "").split("###")

    #过滤content里面的JS字符
    content = content.replace("<", "&lt;").replace(">", "&gt; ")

    blog = get_object_or_404(Article, pk=blog_id)
    if len(quote) == 3 and \
        Comment.objects.filter(pk=quote[2]):
        content = u"""
        <p>
        引用来自<code>%s楼-%s</code>的发言
        </p>""" % (quote[0], quote[1]) + content

    comment = Comment(
        article=blog,
        email=email,
        name=user, 
        content=content)
    comment.save()

    return HttpResponse("%d" % comment.id)

def about(request):

    return render_to_response('about.html',
        context_instance=RequestContext(request))

#########backend##########
@login_required
def post_article(request):

    form = ArticleForm()
    if request.method=='POST':

        form = ArticleForm(request.POST)
        print form.errors
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/')

    return render_to_response('post_article.html',
        {"form":form,},
        context_instance=RequestContext(request))

@login_required
def post_category(request):

    form = CategoryForm()
    if request.method=='POST':

        form = CategoryForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return HttpResponse('''
            <script type="text/javascript">
                var cate = frameElement.api.opener.document.getElementById("id_category");
                cate.innerHTML = cate.innerHTML+"<option value='%s' selected='selected'>%s</option>";
                frameElement.api.close();
            </script>''' %(obj.id, obj.name))

    return render_to_response('post_category.html',
        {"form":form,},
        context_instance=RequestContext(request)) 

# def resetpwd(request):

#     from django.contrib.auth.models import User
#     u = User.objects.get(username__exact='hef')
#     u.set_password('lovemin5201314')
#     u.last_login = datetime.datetime.now()
#     u.date_joined = datetime.datetime.now()

#     u.save()

#     return HttpResponse('success')

