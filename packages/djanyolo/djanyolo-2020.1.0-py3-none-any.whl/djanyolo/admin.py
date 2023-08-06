from django.contrib import admin
from .models import AnnotationImageModel, YoloClassModel


@admin.register(AnnotationImageModel)
class ObjectClassAdmin(admin.ModelAdmin):
    pass


@admin.register(YoloClassModel)
class YoloClassAdmin(admin.ModelAdmin):
    pass