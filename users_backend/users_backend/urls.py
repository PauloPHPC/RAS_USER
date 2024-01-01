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
from users import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('users/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
]

urlpatterns += [
    path('users/create_user', views.create_user, name='create_user'),
    path('users/<uuid:id>/', views.get_user_by_id, name='get_user_by_id'),
    path('users/<str:email>/', views.get_user_by_email, name='get_user_by_email'),
]

urlpatterns += [
    path('users/update/<uuid:id>', views.update_user, name='update_user'),
    path('users/me/<uuid:id>', views.get_current_user, name='get_current_user')
]

