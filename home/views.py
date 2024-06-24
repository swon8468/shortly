from django.shortcuts import render, redirect
from .models import CustomUser
from home.models import CustomUser
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
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
        elif form_type == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/index')
            else:
                messages.error(request, 'Error!\nYour email or Password not joined')
                return redirect('login')


    return render(request, 'index.html')
