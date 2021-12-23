from django.urls import path
from app.views import views
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    # path('', include('django_prometheus.urls')),
    path('api/stationlist', views.viewStationList, name='list station'),
    path('api/stationdata/<str:station>', views.viewStationData, name='ViewData'),
    path('api/stationdata', views.view_all_station_data, name='ViewAllData'),
    path('svc', views.view_control_svc),
    path('poste/<int:poste_id>', views.view_poste, name='poste'),
    path('obs/<int:poste_id>/<str:str_keys>/<str:start_dt>/<str:end_dt>', views.view_obs, name='poste'),
    path('obs/<int:poste_id>/<str:str_keys>/<str:start_dt>', views.view_obs, name='poste'),
    path('obs/<int:poste_id>/<str:str_keys>', views.view_obs, name='poste'),
    path('obs/<int:poste_id>', views.view_obs, name='poste'),
    path('agg/<str:period>/<int:poste_id>/<str:keys>/last/<int:nb_items>', views.view_last_agg),
    path('agg/<str:period>/<int:poste_id>/<str:keys>/last', views.view_last_agg),
    path('agg/<str:period>/<int:poste_id>/<str:keys>/<str:start_dt>/<str:end_dt>', views.view_agg),
    path('agg/<str:period>/<int:poste_id>/<str:keys>/<str:start_dt>', views.view_agg),
    path('agg/<str:period>/<int:poste_id>/<str:keys>', views.view_last_agg),
    path('agg/<str:period>/<int:poste_id>', views.view_last_agg),
    path('calc/<str:file_name>', views.views_calc),
    path('recalc/<str:file_name>', views.views_recalc),
]
