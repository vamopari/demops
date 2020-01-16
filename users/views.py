# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response

from .serializers import UserSerializer
from .token_generator import get_access_token

USERNAME_PASSEWORD_MISSING = 'Username and Password are required'

class UserViewSet(CreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        username = request.data.get('username')
        print(username)
        print(request.get_host())
        application = 'Schema1-Fintify'
        user = self.model.objects.get(username=username)
        token = get_access_token(user, application)
        if token:
            return Response(token,
                            status=status.HTTP_200_OK)
        return Response(token.json(), status.HTTP_400_BAD_REQUEST)


