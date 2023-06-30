import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from RetailProject import settings
from django.conf.urls.static import static
from order_api.urls import api_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('order-api/', include(api_router.urls)),
    path('order-app/', include('order_app.urls')),
    path('order-manager/', include('order_manager.urls')),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'static')}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)