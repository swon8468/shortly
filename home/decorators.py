from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            if request.user.role not in allowed_roles:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('index')  # 권한이 없는 경우 index 페이지로 리다이렉트

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator