from rest_framework.views import exception_handler
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.http import Http404
from tenant_schemas.utils import get_tenant_model, remove_www_and_dev, get_public_schema_name
from django.db import utils
from django.utils.deprecation import MiddlewareMixin


def custom_exception_handler(exc, context):
    # modify this function depending on status code
    # set all error codes in errors files as having constants by field name.

    response = exception_handler(exc, context)

    # Update the structure of the response data.
    if response is not None:
        customized_response = {'errors': []}
        if response.status_code == 400:

            for key, value in response.data.items():
                error = {'field': key, 'message': value[0]}
                customized_response['errors'].append(error)

            response.data = customized_response

        if response.status_code == 401:

            for key, value in response.data.items():
                error = {'field': 'Authentication Failure', 'message': value}
                customized_response['errors'].append(error)

            response.data = customized_response

        if response.status_code == 500:
            error = {"server failure": "Oops!!! something went wrong"}

            customized_response['errors'].append(error)
            response.data = customized_response

    return response


class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        connection.set_schema_to_public()
        hostname_without_port = remove_www_and_dev(request.get_host().split(':')[0])

        TenantModel = get_tenant_model()
        print("TenantModel : ", TenantModel)
        try:
            request.tenant = TenantModel.objects.get(domain_url=hostname_without_port)
        except utils.DatabaseError:
            request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
            return
        except TenantModel.DoesNotExist:
            if hostname_without_port in ("127.0.0.1", "localhost"):
                request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
                return
            else:
                raise Http404

        connection.set_tenant(request.tenant)
        ContentType.objects.clear_cache()

        if hasattr(settings, 'PUBLIC_SCHEMA_URLCONF') and request.tenant.schema_name == get_public_schema_name():
            request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
