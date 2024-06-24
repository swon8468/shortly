from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # 메인 화면
    path('login/', views.login, name='login'), # 로그인
    path('logout/', views.logout_process, name='logout_process'), # 로그아웃
    path('join/', views.join, name='join'), # 회원가입
    path('form_process/', views.form_process, name='form_process'), # 폼 처리
    path('my_profile/', views.my_profile, name='my_profile'), # 내 정보 수정
    path('url_list', views.url_list, name='url_list'), # URL 리스트
]