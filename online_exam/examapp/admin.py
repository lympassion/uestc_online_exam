from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Paper, ChoiceQuestion, JudgeQuestion, FillBlankQuestion

admin.site.site_header = '系统后台'
admin.site.site_title = '在线考试'


@admin.register(User)
class UserAdmin(UserAdmin):

    def is_teacher(self):
        if self.is_teacher:
            return '老师'
        else:
            return '学生'

    # 自定义管理界面
    is_teacher.short_description = '身份'
    list_display = ['username', 'real_name', 'class_name', is_teacher]
    list_filter = ['class_name', 'is_teacher']
    search_fields = ['class_name', 'username', 'real_name']
    list_per_page = 20

    # 这里需要有fieldsets, 否则会出来很多属性
    fieldsets = [
        ("用户信息",
         {"fields":
              ['username', 'password', 'real_name',
               'sex', 'academy', 'is_teacher',
               'class_name', 'is_superuser', ]
          },
         ),
    ]


@admin.register(ChoiceQuestion)
class PaperAdmin(admin.ModelAdmin):
    list_display = ['id', ]
    search_fields = ['id', ]
    list_per_page = 20


@admin.register(JudgeQuestion)
class PaperAdmin(admin.ModelAdmin):
    list_display = ['id', ]
    search_fields = ['id', ]
    list_per_page = 20


@admin.register(FillBlankQuestion)
class PaperAdmin(admin.ModelAdmin):
    list_display = ['id', ]
    search_fields = ['id', ]
    list_per_page = 20


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'subject', 'academy', ]
    search_fields = ['subject', 'academy', ]
    list_per_page = 20
