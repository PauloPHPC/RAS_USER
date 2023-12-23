"""
URL configuration for users_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
]"""

from django.contrib import admin
from django.urls import include, path
from users.views import create_user, get_user_by_id, get_user_by_email, update_user, user_login, user_logout, get_current_user, refresh_access_token


urlpatterns = [
    path('Users/create_user', create_user, name='create_user'),
    path('Users/<uuid:id>/', get_user_by_id, name='get_user_by_id'),
    path('Users/<str:email>/', get_user_by_email, name='get_user_by_email'),
    path('Users/<uuid:id>/', update_user, name='update_user'),
    path('Users/login/', user_login, name='user_login'),
    path('Users/logout/', user_logout, name='user_logout'),
    path('Users/me/', get_current_user, name='get_current_user'),
    path('Users/refresh/', refresh_access_token, name='refresh_access_token'),
]