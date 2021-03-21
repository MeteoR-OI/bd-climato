from django.urls import path
from app.views import views

urlpatterns = [
    path('', views.index, name='index'),
    path('poste/<int:poste_id>', views.view_poste, name='poste'),
    path('obs/<int:poste_id>', views.view_last_obs, name='poste'),
    path('hour/<int:poste_id>/<str:keys>/<str:start_dt>/<str:end_dt>', views.view_agg_hour),
    path('hour/<int:poste_id>/<str:keys>/<str:start_dt>', views.view_agg_hour),
    path('hour/<int:poste_id>/<str:keys>', views.view_agg_hour),
    path('hour/<int:poste_id>', views.view_agg_hour),
    path('day/<int:poste_id>/<str:keys>/<str:start_dt>/<str:end_dt>', views.view_agg_day),
    path('day/<int:poste_id>/<str:keys>/<str:start_dt>', views.view_agg_day),
    path('day/<int:poste_id>/<str:keys>', views.view_agg_day),
    path('day/<int:poste_id>', views.view_agg_day),
    path('month/<int:poste_id>/<str:keys>', views.view_agg_month),
    path('month/<int:poste_id>', views.view_agg_month),
    path('year/<int:poste_id>/<str:keys>', views.view_agg_year),
    path('year/<int:poste_id>', views.view_agg_year),
    path('all/<int:poste_id>/<str:keys>', views.view_agg_all),
    path('all/<int:poste_id>', views.view_agg_all),
    path('calc/<str:file_name>', views.views_calc),
    path('debug0', views.testComputeJ0),
    path('debug1', views.testComputeJ1),
    path('debug2', views.testComputeJ2),
    path('debug3', views.testComputeJ3),
    path('debug4', views.testComputeJ4)
]
