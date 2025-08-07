from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('video_feed/', views.video_feed),
    path('predict_sign/', views.predict_from_frame),
]
