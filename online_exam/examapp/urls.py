from django.urls import path

from . import views

# 增加域名空间
app_name = 'examapp'
urlpatterns = [
    path('login/', views.user_login, name='login'),
]