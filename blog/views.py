from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.shortcuts import render


# Create your views here.

def login(request):
    if request.method == "POST":
        response = {"user": None, "msg": None}

        user = request.POST.get("user")
        pwd = request.POST.get('pwd')
        valid_code = request.POST.get('valid_code')
        print(request.POST)
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
    from blog.utils.validCode import get_valid_code_img
    data = get_valid_code_img(request)
    return HttpResponse(data)


def index(request):
    return render(request, 'index.html')


'''
from django import forms
from django.forms import widgets


class UserForm(forms.Form):
    user = forms.CharField(max_length=32, label="用户名",widget=widgets.TextInput(attrs={'class':'form-control'}) , )
    pwd = forms.CharField(max_length=32, label="密码", widget=widgets.PasswordInput(attrs={'class':'form-control'}),)
    re_pwd = forms.CharField(max_length=32, label="确认密码",  widget=widgets.PasswordInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=32, label="邮箱地址", widget=widgets.EmailInput(attrs={'class':'form-control'}))
'''


from blog.myforms import UserForm
from blog.models import UserInfo
def register(request):

    if request.is_ajax():

        print(request.POST)

        form = UserForm(request.POST)

        respones = {'user':None,'msg':None}

        if form.is_valid():
            respones['user'] = form.cleaned_data.get('user')

            # 生成一条用户记录
            users = form.cleaned_data.get("user")

            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            avatar_obj = request.FILES.get("avatar")
            user_obj = UserInfo.objects.create_user(username=users,password=pwd,email=email,avatar=avatar_obj)

        else:
            print(form.cleaned_data)
            print(form.errors)

            respones['msg'] = form.errors

        return JsonResponse(respones)

    form = UserForm()
    return render(request, 'register.html', {'form': form})
