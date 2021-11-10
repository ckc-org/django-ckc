from django.db import models


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
