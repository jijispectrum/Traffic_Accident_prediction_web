from django.urls import path
from .views import predict_future_hotspot, prediction_result, map_view

urlpatterns = [
    path('predict/', predict_future_hotspot, name='predict_future_hotspot'),
    path('result/', prediction_result, name='prediction_result'),
    path('map/', map_view, name='map_view'),
]
