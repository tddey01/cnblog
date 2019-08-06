from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect


# Create your views here.

def login(request):
    return render(request, 'login.html')


def get_validCode_img(request):
    import random
    def get_random_color():
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255),)
    # 方式 1
    # with open("lufei.jpg", 'rb') as f:
    #     data = f.read()

    #方式 2  # pip install Image
    # from PIL import Image
    # img = Image.new('RGB',(270,40),color=get_random_color())
    # with open('validCode.png','wb') as f:
    #     img.save(f,'png')
    #
    # with open('validCode.png','rb') as f:
    #     data = f.read()

    # # 方式 3
    # from PIL import Image
    # from io import  BytesIO
    # img = Image.new('RGB', (270, 40), color=get_random_color())
    # f = BytesIO()
    # img.save(f,'png')
    # data = f.getvalue()

    # 方式 4
    from PIL import Image,ImageDraw,ImageFont
    from io import  BytesIO
    img = Image.new('RGB', (200, 40), color=get_random_color())
    draw = ImageDraw.Draw(img)
    kuom_font = ImageFont.truetype('static/font/kumo.ttf',size=40)


    for  i in range(5):
        random_num  = str(random.randint(0, 9))  # 数字
        random_low_alpha = chr(random.randint(95,122)) # 小写字母
        random_upper_alpha = chr(random.randint(65,90)) # 大写字母

        random_char = random.choice([random_num,random_low_alpha,random_upper_alpha])
        draw.text((i*35+20,5),random_char,get_random_color(),font=kuom_font) #画文子

    # draw.line() #画线
    # draw.point()  # 画点

    f = BytesIO()
    img.save(f,'png')
    data = f.getvalue()
    return HttpResponse(data)
