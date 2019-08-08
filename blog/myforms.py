#!/usr/bin/env  python3
# -*- coding: UTF-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from blog.models import UserInfo


class UserForm(forms.Form):
    user = forms.CharField(max_length=32, error_messages={"required": "该字段不能为为空"}, label="用户名",
                           widget=widgets.TextInput(attrs={'class': 'form-control'}), )
    pwd = forms.CharField(max_length=32,error_messages={"required":"该字段不能为为空"}, label="密码", widget=widgets.PasswordInput(attrs={'class': 'form-control'}), )
    re_pwd = forms.CharField(max_length=32,error_messages={"required":"该字段不能为为空"}, label="确认密码", widget=widgets.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=32, label="邮箱地址", widget=widgets.EmailInput(attrs={'class': 'form-control'}))

    def clean_user(self):
        var = self.cleaned_data.get('user')

        user = UserInfo.objects.filter(username=var).first()

        if not user:
            return var
        else:
            raise ValidationError("该用户已注册")

    def clean(self):
        pwd = self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.get("re_pwd")

        if pwd and re_pwd:

            if pwd == re_pwd:
                return self.cleaned_data
            else:
                raise ValidationError("两次密码不一样")
        else:
            return self.cleaned_data
