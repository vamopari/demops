import typing
from django.http import HttpRequest
from rest_framework_api_key.permissions import BaseHasAPIKey

from organization.models import ClientAPIKey


class HasOrganizationAPIKey(BaseHasAPIKey):
    model = ClientAPIKey

    def get_client_code(self, request: HttpRequest) -> typing.Optional[str]:
        return request.META.get('HTTP_CLIENT_CODE')

    def has_permission(self, request: HttpRequest, view: typing.Any) -> bool:

        assert self.model is not None, (
                "%s must define `.model` with the API key model to use"
                % self.__class__.__name__
        )

        key = self.get_key(request)

        if not key:
            return False

        query = key.split('.')[0]
        one = self.model.objects.get(prefix=query)
        client_code = self.get_client_code(request)

        if one.basepath == 'http://' + request.META.get('HTTP_HOST') and one.client.client_code == client_code:
            return self.model.objects.is_valid(key)

        return False
