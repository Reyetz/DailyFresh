from django.shortcuts import render, redirect
import re
from apps.user.models import User
from django.urls import reverse
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from celery_tasks.tasks import send_register_active_email
from django.contrib.auth import authenticate, login
# Create your views here.


# /user/register
def register(request):
    '''注册'''
    if request.method == 'GET':
        # 显示注册页面
        return render(request, 'register.html')
    else:
        # 进行注册处理
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 校验用户名
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})
        # 校验密码
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式错误'})
        # 校验协议勾选
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请勾选同意'})
        # 业务处理（用户注册）
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
        # 返回应答,跳转到首页
        return redirect(reverse('goods:index'))


class RegisterView(View):
    '''注册'''
    def get(self, request):
        # 显示注册页面
        return render(request, 'register.html')

    def post(self, request):
        # 进行注册处理
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 校验用户名
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式错误'})
        # 校验协议勾选
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请勾选同意'})
        # 业务处理（用户注册）
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
        # 发送激活链接：http://127.0.0.1:8000/user/active/1
        # 激活链接中需包含用户身份信息，并把身份信息加密
        # 加密用户身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)
        token = token.decode()
        # 发邮件
        send_register_active_email.delay(email, username, token)
        # 返回应答,跳转到首页
        return redirect(reverse('goods:index'))


class ActiveView(View):
    '''用户激活'''
    def get(self, request, token):
        '''进行用户激活'''
        # 解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取id
            user_id = info['confirm']
            # 根据id获取信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            # 跳转登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            # 激活链接过期
            return HttpResponse('激活链接已过期')


# /user/login
class LoginView(View):
    '''登录'''
    def get(self, request):
        '''显示登录页面'''
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        # 使用模板
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        '''登录校验'''
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})
        # 业务处理，校验
        auth_user = authenticate(username=username, password=password)
        if auth_user:
            if auth_user.is_active:
                # 用户已激活
                # 记录用户登录状态
                login(request, auth_user)

                # 获取登录后要跳转的地址
                next_url = request.GET.get('next')
                # 跳转到首页
                response = redirect(reverse('goods:index'))

                # 判断是否需 要记住用户名
                remember = request.POST.get('remember')
                if remember == 'on':
                    # 记住用户名
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')

                # 返回response
                return response
            else:
                # 用户未激活
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})
        # 返回应答

# /user
class UserInfoView(View):
    '''用户中心-信息页'''
    def get(self, request):
        '''显示'''
        # page = 'user'
        return render(request, 'user_center_info.html', {'page': 'user'})

# /user/order
class UserOrderView(View):
    '''用户中心-订单页'''
    def get(self, request):
        '''显示'''
        # page = 'order'
        return render(request, 'user_center_order.html', {'page': 'order'})

# /user/address
class AddressView(View):
    '''用户中心-地址页'''
    def get(self, request):
        '''显示'''
        # page = 'address'
        return render(request, 'user_center_site.html', {'page': 'address'})