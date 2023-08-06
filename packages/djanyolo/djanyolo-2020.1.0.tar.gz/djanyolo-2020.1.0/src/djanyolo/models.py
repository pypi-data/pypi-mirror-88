import base64
import os

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

path = "darknet/data"


class AnnotationImageModel(models.Model):
    image = models.FileField(upload_to=path)
    annotate = models.FileField(upload_to=path)

    def __str__(self):
        return str(image)


class DontFakeMe(models.Model):
    image = models.ImageField(upload_to='images')

    def get_cover_base64(self, format='png'):
        return image_as_base64(self.image.path, format)

    def __str__(self):
        return self.image


def image_as_base64(image_file, format='png'):
    """
    :param image_file: complete path of image
    :param format: supports png, jpg
    """
    print(image_file)
    if not os.path.isfile(image_file):
        return None

    encoded_string = ''
    with open(image_file, 'rb') as img_f:
        encoded_string = base64.b64encode(img_f.read())
    return 'data:image/%s;base64,%s' % (format, encoded_string.decode('utf-8'))


class YoloClassModel(models.Model):
    name = models.CharField(max_length=30, unique=True)
    total = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name)


class ImageDetectionModel(models.Model):
    image = models.ImageField(upload_to='uploaded')


class ConfigurationModel(models.Model):
    train_percentage = models.IntegerField(default=80, validators=[MaxValueValidator(100), MinValueValidator(1)])
    test_percentage = models.IntegerField(default=20)
