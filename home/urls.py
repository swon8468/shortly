from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # 메인 화면
    path('login/', views.login, name='login'), # 로그인
    path('join', views.join, name='join'), # 회원가입
    path('form_process', views.form_process, name='form_process'), # 폼 처리
]