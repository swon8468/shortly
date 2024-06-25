from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import timedelta

# 커스텀 사용자 관리자 정의
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)

# 커스텀 사용자 모델 정의
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICE = (
        ('ADMIN', '관리자'),
        ('USER', '사용자'),
        ('NORMAL', '일반'),
        ('OWNER', '소유주'),
    )

    email = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=30)
    role = models.CharField(max_length=20, choices=ROLE_CHOICE, default='NORMAL')
    school = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

# 그룹 모델 정의
class Group(models.Model):
    STATUS_CHOICES = [
        ('active', '활성화'),
        ('inactive', '비활성화'),
    ]

    name = models.CharField(max_length=100, unique=True)
    creator = models.ForeignKey(CustomUser, related_name='created_groups', on_delete=models.CASCADE)
    super_admin = models.OneToOneField(CustomUser, related_name='super_admin_group', on_delete=models.CASCADE)
    admins = models.ManyToManyField(CustomUser, related_name='admin_groups', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.creator.group:
            self.creator.group = self
            self.creator.save()
        if not self.super_admin.group:
            self.super_admin.group = self
            self.super_admin.save()

    def __str__(self):
        return self.name

# URL 모델 정의
class URL(models.Model):
    STATUS_CHOICES = [
        ('accessible', '접속 가능'),
        ('inaccessible', '접속 불가능'),
        ('group_modified', '그룹 관리자 수정'),
        ('owner_modified', '소유자 수정'),
    ]

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    owner_group = models.CharField(max_length=255)  # 필요에 따라 변경 가능
    original_link = models.URLField(max_length=1024)
    shortened_link = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(days=30))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='accessible')

    def __str__(self):
        return self.shortened_link

    @staticmethod
    def get_original_url(shortened_link):
        try:
            url_object = URL.objects.get(shortened_link=shortened_link)
            return url_object.original_link
        except URL.DoesNotExist:
            return None
