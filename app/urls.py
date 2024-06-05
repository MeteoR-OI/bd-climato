from django.urls import path
# from app.views import views
# from django.conf import settings
# from django.conf.urls.static import static
# from app.views.views_telemetry_test import home_page_view
from app.views.v_svcrpc import viewControlSvc
from app.classes.json_rest_server.restServer import upload_file

urlpatterns = [
    # path('telemetry', home_page_view, name='telemetry test'),
    path('svc', viewControlSvc, name='service control'),
    path('send_json', upload_file, name='upload_file')
    # path('', include('django_prometheus.urls')),
    # path('api/stationlist', views.viewStationList, name='list station'),
]
