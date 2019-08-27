#!/usr/bin/env  python3
# -*- coding: UTF-8 -*-

from django import template
from blog import models
from blog.models import  UserInfo
from django.db.models import Count
register = template.Library()


@register.simple_tag
def multi_tag(x, y):
    return x * y

@register.inclusion_tag("classification.html")
def  get_classification_style(username):
    user = UserInfo.objects.filter(username=username).first()
    print(user)
    blog = user.blog
    cate_list = models.Category.objects.filter(blog=blog).values("pk").annotate(c=Count("article__title")).values_list( "title", "c")
    print(cate_list)
    tag_list = models.Tag.objects.filter(blog=blog).values("pk").annotate(c=Count("article")).values_list("title", "c")
    print(tag_list)
    date_list = models.Article.objects.filter(user=user).extra(select={"y_m_date": "date_format(create_time,'%%Y/%%m')"}).values("y_m_date").annotate(c=Count("nid")).values_list("y_m_date", "c")
    print(date_list)
    return  {"blog":blog,"cate_list":cate_list,"tag_list":tag_list,"date_list":date_list}