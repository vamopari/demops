
from django.contrib.auth.models import User
from oauth2_provider.models import RefreshToken

from rest_framework import serializers, status
from rest_framework import status
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        # for some reason, default framework behaviour is saving password without
        # hashing, hence overriding create method for now so that i can user User models
        # set_password method. Need to find reason of this weird behaviour.
        # TODO: generate user specific password string and encrypt it
        instance.save()
        return instance


class ResetTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        refresh_token = RefreshToken.objects.filter(token=attrs.get('refresh_token', None))
        if not refresh_token.exists():
            return Response({'msg': 'Refresh token not exist.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        attrs['refresh_token'] = refresh_token.first()

        return attrs


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password',)


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
