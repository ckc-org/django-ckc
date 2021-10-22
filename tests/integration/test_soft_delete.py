import pytest
from django.test import TestCase

from testapp.models import AModel


class TestSoftDelete(TestCase):

    def test_soft_delete_model_doesnt_really_delete(self):
        instance = AModel.objects.create()

        # normal model deletion..
        instance.delete()
        assert not AModel.objects.filter(pk=instance.pk).exists()
        assert AModel.all_objects.filter(pk=instance.pk).exists()

        # bulk deletion from queryset also protected...
        with pytest.raises(NotImplementedError, match="Delete is allowed on SoftDeleteQuerySet."):
            AModel.objects.all().delete()
