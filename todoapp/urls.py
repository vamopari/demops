from django.urls import include, path
from django.contrib import admin

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from .organization_middleware import check_api_key

api_info = openapi.Info(title="TODO API", default_version='v1', )

schema_view = get_schema_view(api_info, public=True, permission_classes=(AllowAny,), )

api_urls = [
    path('todos/', include('todos.urls')),
    path('', include('users.urls'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

urlpatterns += [

    # path('swagger(<format>.json|.yaml)', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=None),
        name='schema-swagger-ui')
]
