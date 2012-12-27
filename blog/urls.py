from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('blog.apps.show.views',
    url(r'^$', 'index', name='show_index'),
    url(r'^blog/(?P<blog_id>\d+)$', 
        'show_blog', name='show_blog'),
    url(r'^blog/tags/(?P<tag_str>\S+)$', 
        'about_tag_blogs', name='about_tag_blogs'),

    url(r'^about$', 'about', name='about'),

    url(r'^post_article$', 
        'post_article', name='post_article'),
    url(r'^post_comment$', 
        'post_comment', name='post_comment'),
    url(r'^post_category$', 
        'post_category', name='post_category'),
)

urlpatterns += patterns('',
    (r'^pyer/login/$', 
        'django.contrib.auth.views.login', 
        {'template_name': 'login.html'}),
    )