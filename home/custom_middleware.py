from django.shortcuts import redirect
from django.contrib import messages

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path.startswith('/admin-dashboard/') and request.user.role != 'ADMIN':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')

        if path.startswith('/superuser-dashboard/') and request.user.role != 'SUPERUSER':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')

        response = self.get_response(request)
        return response