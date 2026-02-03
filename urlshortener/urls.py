from django.contrib import admin
from django.urls import path, include

from shortener.views import redirect_short, home

urlpatterns = [
    path("", home, name="home"), 
    
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("shortener.urls")),
    path("<str:short_key>/", redirect_short, name="redirect_short"),
]
