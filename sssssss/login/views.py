from django.shortcuts import render,redirect
from .forms import UserForm,RegisterForm
from . import models
import time
import hashlib
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect,Http404,HttpResponse,render_to_response




def hash_code(s, salt='mysite'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

@csrf_exempt
def index(request):
    if request.method == 'POST':
        username=request.POST['a']
        if not request.FILES.get('img'):
            # return render(request, 'login/index.html')
            return HttpResponseRedirect('index')
        data=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        img = models.Img(img_url=request.FILES.get('img'),
            name=username,dataTime=data)
        img.save()
        # return render(request, 'login/index.html')
        return HttpResponseRedirect('index')
    else:
        numbers=models.dianzan.objects.all()
        c=models.comment.objects.all()
        imgs = models.Img.objects.all().order_by('-id')
        return render_to_response('login/index.html',locals()) #必须用这个return
    
def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对  # 确保用户名和密码都不为空
                    # 用户名字符合法性验证
                    # 密码长度验证
                    # 更多的其它验证.....
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)  # 使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")
@csrf_exempt
def uploadImg(request): # 图片上传函数
    if request.method == 'POST':
        username=request.POST['a']
        if not request.FILES.get('img'):
            return render(request, 'login/index.html')
        data=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        img = models.Img(img_url=request.FILES.get('img'),
            name=username,dataTime=data,dianzans=0,comments=0)
        img.save()
    # return render(request, 'login/index.html')
        return HttpResponseRedirect('index')

# Create your views here.
def add(request):
    a = request.GET['a']
    usrid=request.GET['usrid']
    print(a,usrid)
    
    if models.dianzan.objects.filter(name=a,userid=usrid):
        models.dianzan.objects.filter(name=a,userid=usrid).delete()
    else:
        models.dianzan.objects.create(userid=usrid,name=a,number=1)
    time.sleep(0.1)
    nu=models.dianzan.objects.filter(userid=usrid)
    if nu:
        number=len(nu)
    else:
        number=0
    models.Img.objects.filter(id=usrid).update(dianzans=number)
    time.sleep(0.1)
    return HttpResponse(number)

def text(request):
    texts=request.GET['texts']
    usrname=request.GET['name']
    usrid=request.GET['usrid']
    data=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(texts)
    models.comment.objects.create(name=usrname,text=texts,
        dataTime=data,userid=usrid)
    c=models.comment.objects.all()
    return HttpResponse(c)
@csrf_exempt    
def comment(request):
    if request.method=='GET':
        a = request.GET['a']
        usrid=request.GET['userid']
        usrname=request.GET['username']
        print(usrid)
        print(usrname)
    imgs=models.Img.objects.get(id=usrid)
    try:
        c=models.comment.objects.filter(userid=usrid)
        count=len(c)
    except:
        count=0
    models.Img.objects.filter(id=usrid).update(comments=count)
    try:
        zan=models.dianzan.objects.filter(userid=usrid)
        number=len(zan)
    except:
        number=0
    
    if models.dianzan.objects.filter(name=a).filter(userid=usrid):
        clas='cs'
    else:
        clas='like'

    return render_to_response('login/comment.html',locals())








 # d=models.dianzan.objects.all()
 #    nu=len(d)-1
 #    models.dianzan.objects.filter(name='zan').update(number=nu)       
 #    numbers=models.dianzan.objects.get(name='zan')