from django.urls import path
from app.views import views
# import logging


# logging.basicConfig()


# def skip_unreadable_post(record):
#     return False


# # disable default django output
# logging.config.dictConfig(
#     {
#         'version': 1,
#         'disable_existing_loggers': True,
#         "filters": {
#             "skip_unreadable_posts": {
#                 "()": "django.utils.log.CallbackFilter",
#                 "callback": skip_unreadable_post,
#             }
#         },
#         "handlers": {}
#     })

urlpatterns = [
    path('', views.index, name='index'),
    path('svc', views.view_control_svc),
    path('poste/<int:poste_id>', views.view_poste, name='poste'),
    path('obs/<int:poste_id>', views.view_last_obs, name='poste'),
    path('hour/<int:poste_id>/<str:keys>/<str:start_dt>/<str:end_dt>', views.viewAggHour),
    path('hour/<int:poste_id>/<str:keys>/<str:start_dt>', views.viewAggHour),
    path('hour/<int:poste_id>/<str:keys>', views.viewAggHour),
    path('hour/<int:poste_id>', views.viewAggHour),
    path('day/<int:poste_id>/<str:keys>/<str:start_dt>/<str:end_dt>', views.viewAggDay),
    path('day/<int:poste_id>/<str:keys>/<str:start_dt>', views.viewAggDay),
    path('day/<int:poste_id>/<str:keys>', views.viewAggDay),
    path('day/<int:poste_id>', views.viewAggDay),
    path('month/<int:poste_id>/<str:keys>', views.viewAggMonth),
    path('month/<int:poste_id>', views.viewAggMonth),
    path('year/<int:poste_id>/<str:keys>', views.viewAggYear),
    path('year/<int:poste_id>', views.viewAggYear),
    path('all/<int:poste_id>/<str:keys>', views.viewAggGlobal),
    path('all/<int:poste_id>', views.viewAggGlobal),
    path('calc/<str:file_name>', views.views_calc),
    path('recalc/<str:file_name>', views.views_recalc),
]
