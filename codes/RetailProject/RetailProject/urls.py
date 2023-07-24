import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from RetailProject import settings
from django.conf.urls.static import static
from order_api.urls import api_router, api_urlpatterns
from django.views.generic import TemplateView

urlpatterns = [
    path('', include('order_manager.urls')),
    path('admin/', admin.site.urls),
    path('order-api/', include(api_router.urls )),
    path('order-api/', include(api_urlpatterns)),
    path('order-app/', include('order_app.urls')),
    path('order-manager/', include('order_manager.urls')),
    path("firebase-messaging-sw.js",
        TemplateView.as_view(
            template_name="firebase-messaging-sw.js",
            content_type="application/javascript",
        ),
        name="firebase-messaging-sw.js"
    ),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'static')}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)