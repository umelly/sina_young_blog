#-*- coding: utf-8 -*-

import re

from django import forms

from models import Article, Category, Tag

class ArticleForm(forms.ModelForm):

    title = forms.CharField(label="标题",
        max_length=50,
        widget=forms.TextInput({'placeholder':'文章标题'}))
    category = forms.ModelChoiceField(label="分类",
        queryset=Category.objects.all(),
        widget=forms.Select({'class':'span2'}))
    tags = forms.CharField(label="标签",
        required=False,
        widget=forms.TextInput({'placeholder':'文章标签'}))
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={'style':"width:680px"}))

    def clean_tags(self):

        result= []
        tags = self.data.get('tags','').strip()
        for item in tags.split():
            tag = Tag.objects.get_or_create(
                name =  item
            )[0]
            result.append(tag)

        return result
   
    class Meta:
        model = Article
        exclude=('comments', 'readtimes')

class CategoryForm(forms.ModelForm):

    name = forms.CharField(label="名字",
        widget=forms.TextInput({'placeholder':'添加分类'}))

    class Meta:
        model = Category
        exclude=('articles')
