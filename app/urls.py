from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('poste/<int:poste_id>', views.view_poste, name='poste'),
    path('obs/<int:poste_id>', views.view_last_obs, name='poste'),
    path('hour/<int:poste_id>', views.view_agg_hour),
    path('day/<int:poste_id>', views.view_agg_day),
    path('month/<int:poste_id>', views.view_agg_month),
    path('year/<int:poste_id>', views.view_agg_year),
    path('all/<int:poste_id>', views.view_agg_all),
    path('debug', views.test_compute),
]
