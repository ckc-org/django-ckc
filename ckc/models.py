from django.db import models
from django.utils.timezone import now


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return self.update(deleted=True)


class SoftDeleteModelManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).exclude(deleted=True)


class SoftDeletableModel(models.Model):
    deleted = models.BooleanField(default=False)

    objects = SoftDeleteModelManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class JsonSnapshotModel(models.Model):
    """This mixin is meant to be inherited by a model class. It creates a snapshot field for the class that it is a part of.
     This field is used to solidify data at a given point in time.

    The create_json_snapshot() method must be overridden in the class inheriting this mixin. Inside this method you will build
    a custom JSON object of your model state. Include the fields you wish to be solidified.

    Lastly, call take_snapshot() at the point in your code you want data to be saved. The time and date this occurs will
    also be saved in a separate field called snapshot_date.
    """
    snapshot = models.JSONField(null=True, blank=True, default=dict)
    snapshot_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def _create_json_snapshot(self) -> dict:
        """Override this method to take a "snapshot" of the relevant data on this model"""
        raise NotImplementedError

    def take_snapshot(self, force=False):
        if not force:
            assert not self.snapshot, "Can not override an existing snapshot instance."

        self.snapshot = self._create_json_snapshot()

        # TODO: Do we want to test these edge cases?
        # assert self.snapshot is not None, ""

        self.snapshot_date = now()
