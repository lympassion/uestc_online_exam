from django.urls import path, re_path

from . import views

# 增加域名空间
app_name = 'examapp'
urlpatterns = [
    path('', views.start_page, name='start'),
    path('login/', views.user_login, name='login'),
    path('stuHome/<username>', views.stu_home, name='stuHome'),
    path('teacherHome/<username>', views.teacher_home, name='teacherHome'),
    re_path(r'^calculateScore/$', views.calculate_score, name='calculateScore'),
    re_path(r'^exam/$', views.startExam, name='exam'),
]
