from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core_views import home  # simple home view, see core_views.py

urlpatterns = [
    path("admin/", admin.site.urls),                 # <-- django-administration
    path("", home, name="home"),                      # home page
    path("accounts/", include("accounts.urls")),
    path("food/", include("food.urls")),
    path("grocery/", include("grocery.urls")),
    path("orders/", include("orders.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
