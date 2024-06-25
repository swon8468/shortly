from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'), # 메인 화면
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), # 로그인
    path('logout/', views.logout_process, name='logout_process'), # 로그아웃
    path('join/', views.join, name='join'), # 회원가입
    path('form_process/', views.form_process, name='form_process'), # 폼 처리
    path('my_profile/', views.my_profile, name='my_profile'), # 내 정보 수정
    path('url_list', views.url_list, name='url_list'), # URL 리스트
    path('create_group/', views.create_group, name='create_group'), # 그룹 생성
    path('group_list/', views.group_list, name='group_list'), # 그룹 리스트
]