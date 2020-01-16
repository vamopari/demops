from django.urls import path

from .views import *


urlpatterns = [
    path('user/registration/', UserViewSet.as_view()),
]
