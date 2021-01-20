from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
SEX = (
    # value  display name
    ('male', '男'),  # max_length = 4 + 2 = 6
    ('female', '女'),
)

ACADEMY = (
    ('cs', '计算机科学与技术学院'),
    ('art', '艺术学院'),
)

# 题目难度
LEVEL = {
    ('level1', 'easy'),
    ('level2', 'general'),
    ('level3', 'difficult'),
}


# 用户
class User(AbstractUser):
    """
    用户类模型
    """
    # student.username -----> 学号
    # teacher.username -----> 教职工号
    # admin.username   -----> 管理员账号
    username = models.CharField(max_length=30, verbose_name="学号/教职工号", primary_key=True)  # 这里就是创建超级用户的唯一凭证
    # 这里如果给了password这个属性的话，那边验证不通过
    # password = models.CharField(max_length=20, verbose_name='用户密码', default='123456')
    real_name = models.CharField(max_length=30, verbose_name="姓名")
    sex = models.CharField('性别', max_length=10, choices=SEX, default='男')
    academy = models.CharField('学院', max_length=20, choices=ACADEMY, default='cs')
    is_teacher = models.BooleanField(verbose_name="是否为老师", default=False)
    class_name = models.CharField(max_length=50, verbose_name="班级", blank=True, default='1班')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = '用户'  # 在管理界面中表的名字
        ordering = ['class_name']  # 在管理界面按照班级名称排序


# 三种题型：单项选择题、填空题、判断题
class ChoiceQuestion(models.Model):
    ANSWER = (
        ('optA', 'A'),
        ('optB', 'B'),
        ('optC', 'C'),
        ('optD', 'D'),
    )
    # id = models.AutoField(primary_key=True) 自动加入
    # subject = models.CharField(max_length=20, verbose_name='科目')
    id = models.IntegerField(primary_key=True, verbose_name='题目编号', default=1)
    title = models.TextField(verbose_name='题目描述')
    answer = models.CharField(max_length=10, choices=ANSWER, verbose_name='答案')
    level = models.CharField(max_length=10, choices=LEVEL, verbose_name='题目难度')
    score = models.IntegerField(verbose_name='该题分数', default=1)

    optionA = models.TextField(max_length=30, verbose_name='A选项')
    optionB = models.TextField(max_length=30, verbose_name='B选项')
    optionC = models.TextField(max_length=30, verbose_name='C选项')
    optionD = models.TextField(max_length=30, verbose_name='D选项')

    def __str__(self):
        """
        提供组卷信息
        :return:
        """
        return '(%s): %s' % (self.id, self.title)


class FillBlankQuestion(models.Model):
    # subject = models.CharField(max_length=20, verbose_name='科目')
    id = models.IntegerField(primary_key=True, verbose_name='题目编号', default=1)
    title = models.TextField(verbose_name='题目描述')
    answer = models.CharField(max_length=200, verbose_name='答案')
    level = models.CharField(max_length=10, choices=LEVEL, verbose_name='题目难度')
    score = models.IntegerField(verbose_name='该题分数', default=2)

    def __str__(self):
        """
        提供组卷信息
        :return:
        """
        return '(%s): %s' % (self.id, self.title)


class JudgeQuestion(models.Model):
    ANSWER = (
        ('T', '正确'),
        ('F', '错误'),
    )
    # subject = models.CharField(max_length=20, verbose_name='科目')
    id = models.IntegerField(primary_key=True, verbose_name='题目编号', default=1)
    title = models.TextField(verbose_name='题目描述')
    answer = models.CharField(max_length=20, choices=ANSWER)
    level = models.CharField(max_length=10, choices=LEVEL, verbose_name='题目难度')
    score = models.IntegerField(verbose_name='该题分数', default=1)

    def __str__(self):
        """
        提供组卷信息
        :return:
        """
        return '(%s): %s' % (self.id, self.title)


def now_plus_1(day=1, hour=0):
    return datetime.now() + timedelta(days=day, hours=hour)


class Paper(models.Model):
    # 与题库为多对多关系
    id = models.IntegerField(primary_key=True, verbose_name='试卷编号', default=1)

    choice_q = models.ManyToManyField(ChoiceQuestion, verbose_name='选择题')
    # blank = True----> ManyToManyField optional
    judge_q = models.ManyToManyField(JudgeQuestion, verbose_name='判断题', blank=True)
    fill_blank_q = models.ManyToManyField(FillBlankQuestion, verbose_name='填空题', blank=True)

    # User作为外键
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='出题人')
    subject = models.CharField(max_length=20, verbose_name='考试科目', default='Python')
    academy = models.CharField(max_length=20, verbose_name='适用学院', default='cs')
    exam_start_time = models.DateTimeField(verbose_name='考试开始时间', default=now_plus_1)
    exam_stop_time = models.DateTimeField(verbose_name='考试结束时间', default=now_plus_1(hour=2))

    class Meta:
        verbose_name_plural = '试卷'  # 在管理界面中表的名字


class Grade(models.Model):
    # 学生作为成绩的外键
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=20, verbose_name='科目')
    grade = models.IntegerField()

    def __str__(self):
        return '<%s:%s>' % (self.sid, self.grade);

    class Meta:
        verbose_name_plural = '成绩'
