from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'name', 'school', 'role','email',
    )
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('계정 정보', {'fields': ('name', 'school')}),
        ('권한', {'fields': ('role',)}),
        ('계정 상태', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
        ('접속 정보', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'school', 
                    'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
