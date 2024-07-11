from django.urls import path, re_path
from app.views.views_telemetry_test import home_page_view

urlpatterns = [
    path('', home_page_view, name='home_page_view')
]
