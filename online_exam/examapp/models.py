from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
SEX = (
    ('male', '男'),  # max_length = 4 + 2 = 6
    ('female', '女'),
)

ACADEMY = (
    ('cs', '计算机科学与技术学院'),
    ('art', '艺术学院'),
)


# 用户
class User(AbstractUser):
    """
    用户类模型
    """
    username = models.CharField(max_length=30, verbose_name="学号", primary_key=True)  # 这里就是创建超级用户的唯一凭证

    real_name = models.CharField(max_length=30, verbose_name="姓名")
    sex = models.CharField('性别', max_length=10, choices=SEX, default='男')
    academy = models.CharField('学院', max_length=20, choices=ACADEMY, default=None, null=True)  # null=True,负责创建用户不成功
    is_teacher = models.BooleanField(verbose_name="是否为老师", default=False)

    class_name = models.CharField(max_length=50, verbose_name="班级", blank=True, default='未知')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = '用户'    # 在管理界面中表的名字
        ordering = ['class_name']       # 在管理界面按照班级名称排序


# 与student相关的model
# class Student(models.Model):
#     # 除了需要将模型类作为第一个参数的，verbose_name关键词可省略
#     id      = models.IntegerField(primary_key=True, verbose_name='学号')
#     name    = models.CharField(max_length=20)
#     sex     = models.CharField(max_length=10, choices=SEX)
#     academy = models.CharField(max_length=30, choices=ACADEMY)
#     major   = models.CharField(max_length=20)
#     pw      = models.CharField(max_length=20, verbose_name='密码')

class Grade(models.Model):
    # 学生作为成绩的外键
    # student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=20, verbose_name='科目')
    grade   = models.IntegerField()


# 与老师相关的model
# class Teacher(models.Model):
#     id      = models.IntegerField(primary_key=True, verbose_name='教职工号')
#     name    = models.CharField(max_length=20)
#     sex     = models.CharField(max_length=10, choices=SEX)
#     academy = models.CharField(max_length=30, choices=ACADEMY)
#     major   = models.CharField(max_length=20)
#     pw      = models.CharField(max_length=20, verbose_name='密码')


# 与试题相关的model
class Problem(models.Model):
    ANSWER = (
        ('optionA', 'A'),
        ('optionB', 'B'),
        ('optionC', 'C'),
        ('optionD', 'D'),
    )
    LEVEL = {
        ('level1', 'easy'),
        ('level2', 'general'),
        ('level3', 'difficult'),
    }
    # id = models.AutoField(primary_key=True) 自动加入
    subject = models.CharField(max_length=20, verbose_name='科目')
    title   = models.TextField(verbose_name='题目描述')
    optionA = models.TextField('A选项', max_length=30)
    # optionA  = models.TextField('A选项')
    optionB = models.TextField('B选项', max_length=30)
    optionC = models.TextField('C选项', max_length=30)
    optionD = models.TextField('D选项', max_length=30)
    answer  = models.CharField('答案', max_length=10, choices=ANSWER)
    level   = models.CharField('等级', max_length=10, choices=LEVEL)
    score   = models.IntegerField('分数', default=1)

class Paper(models.Model):
    # 与题库为多对多关系
    problem         = models.ManyToManyField(Problem)
    # teacher         = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject         = models.CharField(max_length=20)
    major           = models.CharField(max_length=20, verbose_name='适用专业')
    exam_start_time = models.DateTimeField()
    exam_stop_time  = models.DateTimeField()
