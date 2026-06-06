"""
URL configuration for quiz_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from quiz.views import custom_upload_function

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz.urls')),
    path("upload/", custom_upload_function, name="custom_upload_file"),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

