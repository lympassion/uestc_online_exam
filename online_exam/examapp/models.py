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
        verbose_name_plural = '用户'  # 在管理界面中表的名字
        ordering = ['class_name']  # 在管理界面按照班级名称排序


# 三种题型：单项选择题、填空题、判断题
class ChoiceQuestion(models.Model):
    ANSWER = (
        ('optionA', 'A'),
        ('optionB', 'B'),
        ('optionC', 'C'),
        ('optionD', 'D'),
    )
    # id = models.AutoField(primary_key=True) 自动加入
    subject = models.CharField(max_length=20, verbose_name='科目')
    title = models.TextField(verbose_name='题目描述')
    answer = models.CharField(max_length=10, choices=ANSWER, verbose_name='答案')
    level = models.CharField(max_length=10, choices=LEVEL, verbose_name='题目难度')
    score = models.IntegerField(verbose_name='该题分数', default=1)

    optionA = models.TextField(max_length=30, verbose_name='A选项')
    optionB = models.TextField(max_length=30, verbose_name='B选项')
    optionC = models.TextField(max_length=30, verbose_name='C选项')
    optionD = models.TextField(max_length=30, verbose_name='D选项')


class FillBlankQuestion(models.Model):
    subject = models.CharField(max_length=20, verbose_name='科目')
    title = models.TextField(verbose_name='题目描述')
    answer = models.CharField(max_length=200, verbose_name='答案')
    level = models.CharField(max_length=10, choices=LEVEL, verbose_name='题目难度')
    score = models.IntegerField(verbose_name='该题分数', default=2)


class JudgeQuestion(models.Model):
    ANSWER = (
        ('T', 'True'),
        ('F', 'False'),
    )
    subject = models.CharField(max_length=20, verbose_name='科目')
    title = models.TextField(verbose_name='题目描述')
    answer = models.CharField(max_length=20, choices=ANSWER)
    level = models.CharField(max_length=10, choices=LEVEL, verbose_name='题目难度')
    score = models.IntegerField(verbose_name='该题分数', default=1)


class Paper(models.Model):
    # 与题库为多对多关系
    choice_q = models.ManyToManyField(ChoiceQuestion)
    fill_blank_q = models.ManyToManyField(FillBlankQuestion)
    judge_q = models.ManyToManyField(JudgeQuestion)
    # User作为外键
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=20, verbose_name='考试科目', default='Python')
    academy = models.CharField(max_length=20, verbose_name='适用学院', default='cs')
    exam_start_time = models.DateTimeField()
    exam_stop_time = models.DateTimeField()


class Grade(models.Model):
    # 学生作为成绩的外键
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=20, verbose_name='科目')
    grade = models.IntegerField()
