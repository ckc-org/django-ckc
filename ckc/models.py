from django.db import models


class SoftDeleteModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(deleted=True)

    def all_objects(self):
        return super().get_queryset()


class SoftDeletableModel(models.Model):
    deleted = models.BooleanField(default=False)

    objects = SoftDeleteModelManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()
