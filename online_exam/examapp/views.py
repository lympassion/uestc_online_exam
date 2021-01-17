from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404

from . import models


# Create your views here.

def start_page(request):
    """
    起始页面(跳转到登陆界面)
    """
    return redirect('examapp:login')


# 用户登陆
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
            # return redirect('examapp:home', username = user.username)
            if user.is_teacher:
                return redirect('examapp:teacherHome', username=user.username)
            else:
                return redirect('examapp:stuHome', username=user.username)
        else:
            # 是在这里调用的登录模板
            return render(request, 'login.html', {'error': '密码错误'})
    else:
        return render(request, 'login.html')


# 学生登陆之后的home_page
def stu_home(request, username):
    # 其中get_object_or_404()第一个参数是对象，后面都是这个对象要满足的条件
    # 可以不需要用下面这种方式获取学生实体
    # 通过学号获取该学生实体
    # student = models.Student.objects.get(username=username)
    student = get_object_or_404(models.User, username=username, is_teacher=False)
    # 查询考试信息
    paper = models.Paper.objects.filter(academy=student.academy)
    # 查询成绩信息
    grade = models.Grade.objects.filter(student=student.username)
    context = {
        'student': student,
        'paper': paper,
        'grade': grade,
    }
    return render(request, 'stuHome.html', context)


# 老师登陆之后的home_page
def teacher_home(request, username):
    teacher = get_object_or_404(models.User, username=username, is_teacher=True)

    # 在试卷表 paper 找到该老师发布的试题
    paper = models.Paper.objects.filter(author=teacher.username)

    context = {
        'teacher': teacher,
        'paper':   paper,
    }

    return render(request, 'teacherHome.html', context)
