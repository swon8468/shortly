from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Group
from django.contrib.auth import authenticate, logout, login as auth_login
from .decorators import role_required
from django.http import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def join(request):
    return render(request, 'join.html')

def form_process(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'join':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 != password2:
                messages.error(request, 'Error!\nComfirm your Password and Re-password')
                return redirect('join')
            if password1 == password2:
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, 'Error!\nThe email already exists')
                else:
                    user = CustomUser.objects.create_user(email=email, name=name, password=password1)
                    user.save()
                    messages.success(request, 'Success!\nLogin your account')
                    return redirect('login')
        if form_type == 'login':
            print('login process')
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user = CustomUser.objects.get(email=email)
            except:
                messages.error(request, 'No User in DB')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                print('login')
                return redirect('index')
            else:
                messages.error(request, 'Error!\nYour email or Password not joined')
                return redirect('login')
        if form_type == 'edit_profile':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if password1 and password2 and password1 == password2:
                request.user.set_password(password1)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Update your new password')
                return redirect('my_profile')
            else:
                messages.error(request, 'Error\nYou wrong input password')
                return redirect('my_profile')
        if form_type == 'group':
            group_name = request.POST.get('group_name')
            super_admin_email = request.POST.get('super_admin_email')

            if Group.objects.filter(name=group_name).exists():
                messages.error(request, 'A group with this name already exist.')
                return redirect('create_group')
            
            try:
                super_admin = CustomUser.objects.get(email=super_admin_email)
            except CustomUser.DoesNotExist:
                messages(request, 'Super Admin with this email does not exist.')
                return redirect('create_group')
            
            group = Group.objects.create(name=group_name, creator=request.user, super_admin=super_admin)
            messages.success(request, 'Group created successfully.')
            return redirect('group_list')
        if form_type == 'edit_group':
            group_id = request.POST.get('group_id')
            group_name = request.POST.get('group_name')
            super_admin_email = request.POST.get('super_admin_email')
            status = request.POST.get('status')

            group = get_object_or_404(Group, id=group_id)

            if group_name != group.name and Group.objects.filter(name=group_name).exists():
                messages.error(request, 'A group with this name already exists.')
                return redirect('group_list')

            try:
                super_admin = CustomUser.objects.get(email=super_admin_email)
            except CustomUser.DoesNotExist:
                messages.error(request, 'Super Admin with this email does not exist.')
                return redirect('group_list')

            group.name = group_name
            group.super_admin = super_admin
            group.status = status
            group.save()

            # 그룹의 슈퍼관리자 그룹도 업데이트
            super_admin.group = group
            super_admin.save()

            messages.success(request, 'Group updated successfully.')
            return redirect('group_list')

    return render(request, 'index.html')

def logout_process(request):
    logout(request)
    messages.success(request, 'Logged out.')
    return redirect('index')

@login_required
def my_profile(request):
    return render(request, 'my_profile.html')

@login_required
@role_required(['ADMIN', 'OWNER'])
def url_list(request):
    return render(request, 'url_list.html')

@login_required
@role_required(['ADMIN', 'OWNER'])
def create_group(request):
    return render(request, 'create_group.html')

@login_required
@role_required(['ADMIN', 'OWNER'])
def group_list(request):
    groups = Group.objects.all()
    context = {
        'groups' : groups
    }
    return render(request, 'group_list.html', context)