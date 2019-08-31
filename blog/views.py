from django.contrib import auth
from django.shortcuts import HttpResponse, redirect, render
from django.db import transaction
from blog import models
from blog.models import UserInfo
from blog.myforms import UserForm
from blog.utils import validCode
import os
from cnblog import settings


# Create your views here.


def login(request):
    '''
    登录验证
    :param request:
    :return:
    '''
    if request.method == "POST":
        response = {"user": None, "msg": None}

        user = request.POST.get("user")
        pwd = request.POST.get('pwd')
        valid_code = request.POST.get('valid_code')
        # print(request.POST)
        valid_code_srt = request.session.get("valid_code_str")
        if valid_code.upper() == valid_code_srt.upper():
            user = auth.authenticate(username=user, password=pwd)
            if user:
                auth.login(request, user)  # request.user == 当前登录对象
                response["user"] = user.username
            else:
                # response['msg']="username or password error"
                response['msg'] = "用户名 或 密码 错误 请重新输入"
        else:
            response["msg"] = "验证码错误 请重新输入"
            # response["msg"]="valid code error"

        return JsonResponse(response)
    return render(request, 'login.html')


def get_validCode_img(request):
    # import random
    # def get_random_color():
    #     return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),)
    #
    # # 方式 1
    # # with open("lufei.jpg", 'rb') as f:
    # #     data = f.read()
    #
    # # 方式 2  # pip install Image
    # # from PIL import Image
    # # img = Image.new('RGB',(270,40),color=get_random_color())
    # # with open('validCode.png','wb') as f:
    # #     img.save(f,'png')
    # #
    # # with open('validCode.png','rb') as f:
    # #     data = f.read()
    #
    # # # 方式 3
    # # from PIL import Image
    # # from io import  BytesIO
    # # img = Image.new('RGB', (270, 40), color=get_random_color())
    # # f = BytesIO()
    # # img.save(f,'png')
    # # data = f.getvalue()
    #
    # # 方式 4
    # from PIL import Image, ImageDraw, ImageFont
    # from io import BytesIO
    # img = Image.new('RGB', (200, 40), color=get_random_color())
    # draw = ImageDraw.Draw(img)
    # kuom_font = ImageFont.truetype('static/font/kumo.ttf', size=40)
    #
    # valid_code_str = ""
    #
    # for i in range(5):
    #     random_num = str(random.randint(0, 9))  # 数字
    #     random_low_alpha = chr(random.randint(95, 122))  # 小写字母
    #     random_upper_alpha = chr(random.randint(65, 90))  # 大写字母
    #
    #     random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
    #     draw.text((i * 35 + 25, 5), random_char, get_random_color(), font=kuom_font)  # 画文子
    #
    #     # 保存验证码字符串
    #     valid_code_str += random_char
    #
    # print("valid_code_str", valid_code_str)
    # request.session['valid_code_str'] = valid_code_str
    # '''
    # # draw.line() #画线
    # # draw.point()  # 画点
    #   1 sdajsdg33dasd
    #   2 COOKIE {"sessionid":sdajsdg33dasd }
    #   3 djagno-session 表中存
    #     session-key     session-data
    #     sdajsdg33dasd  {"valid_code_str":"12345"}
    #
    #
    # '''
    # '''
    # width = 200
    # height=40
    # for i in range(5):
    #     x1 = random.randint(0,width)
    #     x2 = random.randint(0,width)
    #     y1 = random.randint(0,height)
    #     y2 = random.randint(0,height)
    #     draw.line((x1,y1,x2,y2),fill=get_random_color())
    #
    # for i in range(50):
    #     draw.point([random.randint(0,width), random.randint(0,height)],fill=get_random_color())
    #     x = random.randint(0,width)
    #     y = random.randint(0,height)
    #     draw.arc((x,y,x + 4,y + 4),0 , 90,fill = get_random_color() )
    # '''
    #
    # f = BytesIO()
    # img.save(f, 'png')
    # data = f.getvalue()

    data = validCode.get_valid_code_img(request)
    return HttpResponse(data)


def index(request):
    article_list = models.Article.objects.all()
    return render(request, 'index.html', {"article_list": article_list})


'''
from django import forms
from django.forms import widgets


class UserForm(forms.Form):
    user = forms.CharField(max_length=32, label="用户名",widget=widgets.TextInput(attrs={'class':'form-control'}) , )
    pwd = forms.CharField(max_length=32, label="密码", widget=widgets.PasswordInput(attrs={'class':'form-control'}),)
    re_pwd = forms.CharField(max_length=32, label="确认密码",  widget=widgets.PasswordInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=32, label="邮箱地址", widget=widgets.EmailInput(attrs={'class':'form-control'}))
'''


# from blog.myforms import UserForm
# from blog.models import UserInfo


def register(request):
    if request.is_ajax():

        # print(request.POST)

        form = UserForm(request.POST)

        respones = {'user': None, 'msg': None}

        if form.is_valid():
            respones['user'] = form.cleaned_data.get('user')

            # 生成一条用户记录
            users = form.cleaned_data.get("user")

            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            avatar_obj = request.FILES.get("avatar")
            extra = {}

            if avatar_obj:
                extra['avatar'] = avatar_obj

            # UserInfo.objects.create_user(username=users, password=pwd, email=email, *extra)
            UserInfo.objects.create_user(username=users, password=pwd, email=email, *extra)

            '''
            if avatar_obj:
                user_obj = UserInfo.objects.create_user(username=users,password=pwd,email=email,avatar=avatar_obj)
            else:
                user_obj = UserInfo.objects.create_user(username=users, password=pwd, email=email,)
            '''

        else:

            #     print(form.cleaned_data)
            #     print(form.errors)

            respones['msg'] = form.errors

        return JsonResponse(respones)

    form = UserForm()
    return render(request, 'register.html', {'form': form})


def logout(request):
    auth.logout(request)  # 等同于执行 request.session.flush() 这个函数模块
    return redirect("/login/")


def home_site(request, username, **kwargs):
    '''
    个人站点 视图函数
    :param request:
    :return:
    '''

    print("kwargs", kwargs)
    print('username', username)
    user = UserInfo.objects.filter(username=username).first()
    if not user:  # 判断用户是否存在
        return render(request, "not_found.html")

    # 查询当前站点对象

    blog = user.blog
    print(blog)
    # 当前用户或者当前站点对应的所有文章 过滤出来
    # 基于对象查询
    # article_list = user.article_set.all()
    # 基于双线划线查询
    # models.Article.objects.filter(user=user)
    article_list = models.Article.objects.filter(user=user)
    if kwargs:
        condition = kwargs.get("condition")
        param = kwargs.get("param")
        if condition == "category":
            # article_list = models.Article.objects.filter(user=user).filter(category__title=param)
            article_list = article_list.filter(category__title=param)
        elif condition == "tag":
            article_list = article_list.filter(tags__title=param)
        else:
            year, month = param.split("-")
            article_list = article_list.filter(create_time__year=year, create_time__month=month)

    # # 每一个后的表模型.objects.values("pk").annotate(聚合函数(关联表__统计字段)).values("表模型的所有字段以及统计字段")
    #
    # # 查询每一个分类名称以及对应的文章数
    # #
    # ret = models.Category.objects.values("pk").annotate(c=Count("article__title")).values("title", "c")
    # print(ret)
    #
    # # 查询当前站点的每一个分类名称以及对应的文章数
    #
    # cate_list = models.Category.objects.filter(blog=blog).values("pk").annotate(c=Count("article__title")).values_list(
    #     "title", "c")
    # print(cate_list)
    #
    # # 查询当前站点的每一个标签名称以及对应的文章数
    #
    # tag_list = models.Tag.objects.filter(blog=blog).values("pk").annotate(c=Count("article")).values_list("title", "c")
    # print(tag_list)
    #
    # # 查询当前站点每一个年月的名称以及对应的文章数
    #
    # ret=models.Article.objects.extra(select={"is_recent":"create_time > '2018-09-05'"}).values("title","is_recent")
    # print(ret)
    #
    # # 方式1:
    # date_list = models.Article.objects.filter(user=user).extra(
    #     select={"y_m_date": "date_format(create_time,'%%Y/%%m')"}).values("y_m_date").annotate(
    #     c=Count("nid")).values_list("y_m_date", "c")
    # print(date_list)
    #
    # # 方式2:
    # #
    # from django.db.models.functions import TruncMonth
    #
    # # ret=models.Article.objects.filter(user=user).annotate(month=TruncMonth("create_time")).values("month").annotate(c=Count("nid")).values_list("month","c")
    # # ret = models.Article.objects.first(user=user).annotate(month=TruncMonth("create_time")).values("month").annotate(c=Count("nid")).values_list("month","c")
    # # print("ret----->",ret)

    # return render(request, "home_site.html", {"username": username, "blog": blog, "article_list": article_list, 'data_list': date_list}, )
    return render(request, "home_site.html", {"username": username, "blog": blog, "article_list": article_list, }, )


def article_detail(request, username, articel_id):
    user = UserInfo.objects.filter(username=username).first()
    blog = user.blog
    article_obj = models.Article.objects.filter(pk=articel_id).first()

    commtent_list = models.Comment.objects.filter(article_id=articel_id)
    return render(request, "article_detail.html", locals())


# 点赞试图函数
import json
from django.db.models import F
from django.http import JsonResponse


def digg(request):
    print(request.POST)

    article_id = request.POST.get("article_id")
    # is_up = request.POST.get('is_up')  # 字符串 true
    is_up = json.loads(request.POST.get("is_up"))
    user_id = request.user.pk
    response = {"state": True}
    obj = models.ArticleUpDown.objects.filter(user_id=user_id, article_id=article_id).first()
    if not obj:
        queryset = models.Article.objects.filter(pk=article_id)
        ard = models.ArticleUpDown.objects.create(user_id=user_id, article_id=article_id, is_up=is_up)
        if is_up:
            queryset.update(up_count=F("up_count") + 1)
        else:
            queryset.update(down_count=F("down_count") + 1)
    else:
        response["state"] = False
        response["handled"] = obj.is_up

    return JsonResponse(response)


def comment(request):
    print(request.POST)
    article_id = request.POST.get("article_id")
    content = request.POST.get("content")
    pid = request.POST.get("pid")
    user_id = request.user.pk
    article_obj = models.Article.objects.filter(pk=article_id).first()

    # 事务操作
    with transaction.atomic():
        comment_obj = models.Comment.objects.create(user_id=user_id, article_id=article_id, content=content,
                                                    parent_comment_id=pid)
        # yuan
        models.Article.objects.filter(pk=article_id).update(comment_count=F("comment_count") + 1)
    response = {}
    response["create_time"] = comment_obj.create_time.strftime("%Y-%m-%d %X")
    response["username"] = request.user.username
    response["content"] = content

    from django.core.mail import send_mail
    from cnblog import settings

    import threading  # 多线程发送邮件通知
    t = threading.Thread(target=send_mail, args=("您的文章%s新增了一条评论内容" % article_obj.title,
                                                 content,
                                                 settings.EMAIL_HOST_USER,
                                                 ['88@qq.com'],))
    t.start()
    return JsonResponse(response)


def get_comment_tree(request):
    print(request.GET)
    article_id = request.GET.get('article_id')

    ren = list(
        models.Comment.objects.filter(article_id=article_id).order_by('pk').values('pk', 'content', 'parent_comment'))
    # [{},{},{}]

    return JsonResponse(ren, safe=False)


from django.contrib.auth.decorators import login_required


@login_required
def cn_backend(request):
    """
    后台管理的首页
    :param request:
    :return:
    """
    article_list = models.Article.objects.filter(user=request.user)

    return render(request, "backend/backend.html", locals())


from bs4 import BeautifulSoup


@login_required
def add_article(request):
    """
    后台管理的添加书籍视图函数
    :param request:
    :return:
    """
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        # 防止xss攻击,过滤script标签
        soup = BeautifulSoup(content, "html.parser")
        for tag in soup.find_all():

            print(tag.name)
            if tag.name == "script":
                tag.decompose()

        # 构建摘要数据,获取标签字符串的文本前150个符号

        desc = soup.text[0:150] + "..."

        models.Article.objects.create(title=title, desc=desc, content=str(soup), user=request.user)
        return redirect("/cn_backend/")

    return render(request, "backend/add_article.html")


def upload(request):
    """
    编辑器上传文件接受视图函数
    :param request:
    :return:
    """

    print(request.FILES)
    img_obj = request.FILES.get("upload_img")
    print(img_obj.name)

    path = os.path.join(settings.MEDIA_ROOT, "add_article_img", img_obj.name)

    with open(path, "wb") as f:
        for line in img_obj:
            f.write(line)

    response = {
        "error": 0,
        "url": "/media/add_article_img/%s" % img_obj
    }
    import json

    # return HttpResponse("ok")
    return HttpResponse(json.dumps(response))
