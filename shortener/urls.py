from django.urls import path

from .views import DashboardView, ShortURLEditView, ShortURLDeleteView

urlpatterns = [
    path("shortener/", DashboardView.as_view(), name="dashboard"),
    path("shortener/<int:pk>/edit/", ShortURLEditView.as_view(), name="shorturl_edit"),
    path("shortener/<int:pk>/delete/", ShortURLDeleteView.as_view(), name="shorturl_delete"),
]
