from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Group

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'role', 'group', 'is_active', 'is_staff')
    search_fields = ('email', 'name', 'role', 'group__name')
    list_filter = ('role', 'is_active', 'is_staff', 'group')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'role', 'school', 'group')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'school', 'password1', 'password2', 'group', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    ordering = ('email',)

admin.site.register(Group)
