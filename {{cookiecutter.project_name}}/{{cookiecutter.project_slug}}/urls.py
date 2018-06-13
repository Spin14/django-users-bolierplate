from django.conf.urls import url, include
from django.shortcuts import render

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from users.views import UserViewSet, CreateUserViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'users')


def index(request):
    return render(request, 'index.html')


urlpatterns = [
    url(r'^$', index),
    url(r'^api/', include(router.urls)),
    url(r'^api/create-user', CreateUserViewSet.as_view()),
    url(r'^api/token-auth', obtain_auth_token),
]
