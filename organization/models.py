from django.db import models
from rest_framework_api_key.models import AbstractAPIKey

from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from tenant_schemas.models import TenantMixin


class Schemas(TenantMixin):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    created_on = models.DateField(auto_now_add=True)


class Tenant(models.Model):
    # this class is to idetify for which consumer we are generating token
    name = models.CharField(max_length=128)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return smart_unicode(self.name)


class Client(models.Model):
    # this class should be named as host or Endpoint?
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='tenant_key', null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    created_on = models.DateField(auto_now_add=True)
    client_code = models.CharField(max_length=10, null=True)

    def __unicode__(self):
        return smart_unicode(self.name)


class ClientAPIKey(AbstractAPIKey):

    # create API key using this class and bind base path to the key.

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )

    basepath = models.URLField(null=True)

    def __unicode__(self):
        return smart_unicode(self.name)


