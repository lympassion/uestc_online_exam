from django.shortcuts import render, redirect
from . import models
from .app_helper import views_helper
from django.contrib.auth import login, logout, authenticate

# Create your views here.


# 登陆
def user_login(request):
    """
    用户登陆页面
    """
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not user.is_teacher:
                return redirect('ExamApp:学生主页', username=user.username)
            else:
                return redirect('ExamApp:老师主页', username=user.username, class_name='all')
        else:
            # 是在这里调用的登录模板
            return render(request, 'login.html', {'error': '密码错误'})
    else:
        return render(request, 'login.html')
