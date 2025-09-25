"""URL configuration for the backend API."""
from __future__ import annotations

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path


def healthcheck(request):
    return HttpResponse("ok", content_type="text/plain")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", healthcheck, name="healthcheck"),
]
