from django.urls import path
from .views import upload, home, stat, yolo_class, detection_image, model, model_settings


urlpatterns = [
    path('', home, name="home"),
    path('upload/', upload, name="upload"),
    path('stat', stat, name="stat"),
    path('stat/class', yolo_class, name="yolo_class"),
    path('detection_image', detection_image, name="detection_image"),
    path('model', model, name="model"),
    path('settings', model_settings, name="model_settings"),
]