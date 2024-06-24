from django.shortcuts import render, redirect
from .models import CustomUser
from home.models import CustomUser
from django.contrib.auth import authenticate, logout, login as auth_login
from django.http import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

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

    return render(request, 'index.html')

def logout_process(request):
    logout(request)
    messages.success(request, 'Logged out.')
    return redirect('index')

def my_profile(request):
    return render(request, 'my_profile.html')

def url_list(request):
    return render(request, 'url_list.html')