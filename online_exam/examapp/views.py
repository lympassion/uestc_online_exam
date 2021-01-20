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
        # print(username, password)
        # user = get_object_or_404(models.User, username=username, is_teacher=False)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # print('user 有')
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
    # 查询考试信息，根据学生所在学院查询要考的试题
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
        'paper': paper,
    }

    return render(request, 'teacherHome.html', context)


# 学生考试 的视图函数
def startExam(request):
    username = request.GET.get('sid')
    paper_id = request.GET.get('pid')
    subject = request.GET.get('subject')

    student = get_object_or_404(models.User, username=username, is_teacher=False)
    # 确保学生唯一的一张考试试题
    paper = get_object_or_404(models.Paper, id=paper_id)

    context = {
        'student': student,
        'paper': paper,
        'subject': subject,
    }

    return render(request, 'exam.html', context)


# 计算由exam.html模版传过来的数据计算成绩
def calculate_score(request):
    if request.method == 'POST':
        sid      = request.POST['sid']
        pid      = request.POST['pid']
        subject = request.POST['subject']

        # 重新生成Student实例，Paper实例，Grade实例，名字和index中for的一致，可重复渲染
        student = models.User.objects.get(username=sid)
        paper   = models.Paper.objects.filter(id=pid)
        grade   = models.Grade.objects.filter(student=student.username)

        mygrade  = 0  # 初始化一个成绩为0

        # 选择题成绩
        # 其中models.Paper.objects.filter(id=pid).values('choice_q')，返回id=pid的试卷中所有的选择题(集合，可迭代)
        choice_q = models.Paper.objects.filter(id=pid).values('choice_q').values('choice_q__id', 'choice_q__answer',
                                                                                'choice_q__score')
        for q in choice_q:
            qid = 'choice' + str(q['choice_q__id'])  # 这里一定要与exam.html中对应的name一致
            myans = request.POST[qid]  # 通过 qid 得到学生关于该题的作答
            # print('myans', myans)
            okans = q['choice_q__answer']  # 得到正确答案
            # print('okans', okans)
            if myans == okans:  # 判断学生作答与正确答案是否一致
                mygrade += q['choice_q__score']  # 若一致,得到该题的分数,累加mygrade变量
            print('mygrade', mygrade)


        # 判断题成绩
        judge_q = models.Paper.objects.filter(id=pid).values('judge_q').values('judge_q__id', 'judge_q__answer',
                                                                                 'judge_q__score')
        for q in judge_q:
            qid = 'judge' + str(q['judge_q__id'])
            myans = request.POST[qid]
            print('myans', myans)
            okans = q['judge_q__answer']  # 得到正确答案
            print('okans', okans)
            if myans == okans:  # 判断学生作答与正确答案是否一致
                mygrade += q['judge_q__score']  # 若一致,得到该题的分数,累加mygrade变量


        # 向Grade表中插入数据          外键
        models.Grade.objects.create(student_id=sid, subject=subject, grade=mygrade)
        print(mygrade)
        # 重新渲染index.html模板
        return render(request, 'stuHome.html', {'student': student, 'paper': paper, 'grade': grade})
