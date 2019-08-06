#!/usr/bin/env  python3
# -*- coding: UTF-8 -*-

from django.urls import path
from django.urls import re_path
from blog import views

urlpatterns = [
    path('login/', views.login),
    path('get_validCode.img',views.get_validCode_img),

]
