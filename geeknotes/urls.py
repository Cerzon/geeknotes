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
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as authtoken
from rest_framework_simplejwt import views as simplejwt
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from graphene_django.views import GraphQLView

from usersapp import views as usersapp
from notesapp import views as notesapp


router = DefaultRouter()
router.register('users', usersapp.GeekUserModelViewSet)
router.register('projects', notesapp.ProjectModelViewSet)
router.register('notes', notesapp.NoteModelViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="ToDo Notes",
      default_version='v0.1',
      description="Documentation",
      terms_of_service="http://localhost/terms/",
      contact=openapi.Contact(email="admin@local.host"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    re_path(r'^api/v(?P<version>\d\.\d)/', include(router.urls)),
    path('api/token-auth/', authtoken.obtain_auth_token),
    path('api/jwt/', simplejwt.TokenObtainPairView.as_view()),
    path('api/jwt/refresh/', simplejwt.TokenRefreshView.as_view()),
    path('api/jwt/verify/', simplejwt.TokenVerifyView.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
]
