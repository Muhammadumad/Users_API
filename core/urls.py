from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def api_home(_request):
    return JsonResponse(
        {
            'message': 'Users API is running.',
            'endpoints': {
                'users_list_create': '/api/users/',
                'user_detail': '/api/users/<uuid:user_id>/',
            },
        }
    )

urlpatterns = [
    path('', api_home, name='api-home'),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('blog.urls')),
]

# This serves uploaded files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)