from django.contrib.auth import get_user_model
from django.contrib.gis.db.models import PointField
from django.db import models

from ckc.models import SoftDeletableModel, JsonSnapshotModel


User = get_user_model()


# ----------------------------------------------------------------------------
# Testing soft deletable model
# ----------------------------------------------------------------------------
class AModel(SoftDeletableModel):
    title = models.CharField(max_length=255, default="I'm a test!")


# ----------------------------------------------------------------------------
# PrimaryKeyWriteSerializerReadField related model
# ----------------------------------------------------------------------------
class BModel(models.Model):
    a = models.ForeignKey(AModel, on_delete=models.CASCADE)


# ----------------------------------------------------------------------------
# DefaultCreatedByMixin models
# ----------------------------------------------------------------------------
class ModelWithACreator(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class ModelWithADifferentNamedCreator(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


# ----------------------------------------------------------------------------
# For testing geo points in factories
# ----------------------------------------------------------------------------
class Location(models.Model):
    geo_point = PointField()


# ----------------------------------------------------------------------------
# For testing JSON snapshots
# ----------------------------------------------------------------------------
class SnapshottedModel(JsonSnapshotModel, models.Model):

    def _create_json_snapshot(self) -> dict:
        return {
            "test": "snapshot"
        }


class SnapshottedModelMissingOverride(JsonSnapshotModel, models.Model):
    # No _create_json_snapshot here! This is for testing purposes, to confirm we raise
    # an assertion when this method is missing
    pass
