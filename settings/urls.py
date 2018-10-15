from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('accounts/login/', LoginView.as_view(
        template_name='admin/login.html',
        extra_context={'site_header': 'Skeleton'}),
        name='login'),
    path('admin/', admin.site.urls),
]
