from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

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

    fieldsets = [
        ("用户信息", {"fields": ['real_name', 'username', 'password',
                             'class_name', 'is_superuser', 'is_teacher']}),
    ]