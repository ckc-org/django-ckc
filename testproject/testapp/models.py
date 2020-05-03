from django.db import models

from ckc.models import SoftDeletableModel


class TestModel(SoftDeletableModel):
    title = models.CharField(max_length=255, default="I'm a test!")
