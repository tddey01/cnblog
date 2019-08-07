from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.

def login(request):
    if request.method == "POST":
        response = {"user":None,"msg":None}

        user = request.POST.get("user")
        pwd = request.POST.get('pwd')
        valid_code = request.POST.get('valid_code')

        valid_code_srt = request.session.get("valid_code_str")
        if valid_code.upper() == valid_code_srt.upper():
            pass
        else:
            response["msg"]="valid code error"

        return JsonResponse(response)
    return render(request, 'login.html')


def get_validCode_img(request):
    import random
    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),)

    # 方式 1
    # with open("lufei.jpg", 'rb') as f:
    #     data = f.read()

    # 方式 2  # pip install Image
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
    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO
    img = Image.new('RGB', (200, 40), color=get_random_color())
    draw = ImageDraw.Draw(img)
    kuom_font = ImageFont.truetype('static/font/kumo.ttf', size=40)

    valid_code_str = ""

    for i in range(5):
        random_num = str(random.randint(0, 9))  # 数字
        random_low_alpha = chr(random.randint(95, 122))  # 小写字母
        random_upper_alpha = chr(random.randint(65, 90))  # 大写字母

        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
        draw.text((i * 35 + 25, 5), random_char, get_random_color(), font=kuom_font)  # 画文子

        # 保存验证码字符串
        valid_code_str += random_char

    print("valid_code_str", valid_code_str)
    request.session['valid_code_str'] = valid_code_str
    '''
    # draw.line() #画线
    # draw.point()  # 画点
      1 sdajsdg33dasd
      2 COOKIE {"sessionid":sdajsdg33dasd }
      3 djagno-session 表中存
        session-key     session-data
        sdajsdg33dasd  {"valid_code_str":"12345"}
        
    
    '''
    '''
    width = 200
    height=40
    for i in range(5):
        x1 = random.randint(0,width)
        x2 = random.randint(0,width)
        y1 = random.randint(0,height)
        y2 = random.randint(0,height)
        draw.line((x1,y1,x2,y2),fill=get_random_color())

    for i in range(50):
        draw.point([random.randint(0,width), random.randint(0,height)],fill=get_random_color())
        x = random.randint(0,width)
        y = random.randint(0,height)
        draw.arc((x,y,x + 4,y + 4),0 , 90,fill = get_random_color() )
    '''

    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()
    return HttpResponse(data)
