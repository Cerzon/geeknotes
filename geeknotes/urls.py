"""geeknotes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as authtoken
from rest_framework_simplejwt import views as simplejwt

from usersapp import views as usersapp
from notesapp import views as notesapp


router = DefaultRouter()
router.register('users', usersapp.GeekUserModelViewSet)
router.register('projects', notesapp.ProjectModelViewSet)
router.register('notes', notesapp.NoteModelViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token-auth/', authtoken.obtain_auth_token),
    path('api/jwt/', simplejwt.TokenObtainPairView.as_view()),
    path('api/jwt/refresh/', simplejwt.TokenRefreshView.as_view()),
    path('api/jwt/verify/', simplejwt.TokenVerifyView.as_view()),
]
