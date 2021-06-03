from django.contrib.auth import get_user_model
from django.contrib.gis.db.models import PointField
from django.db import models

from ckc.models import SoftDeletableModel


User = get_user_model()


class AModel(SoftDeletableModel):
    title = models.CharField(max_length=255, default="I'm a test!")


class ModelWithACreator(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class ModelWithADifferentNamedCreator(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Location(models.Model):
    geo_point = PointField()
