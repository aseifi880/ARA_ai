from django.contrib import admin
from django.urls import path, include

import jobyabi

urlpatterns = [
    path("admin/", admin.site.urls),
    include("jobyabi/", jobyabi.urls, namespace="jobyabi")
]
