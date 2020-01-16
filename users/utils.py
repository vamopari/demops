
import requests
from django.conf import settings

from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet


def generate_oauth_token(host, username):

    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'grant_type': 'password',
               'username': username,
               'password': '',
               'client_id': client_id,
               'client_secret': client_secret}

    return (requests.post(settings.SERVER_PROTOCOLS + host + "/o/token/",
                          data=payload, headers=headers))



