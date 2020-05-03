from django.test import TestCase

from testapp.models import TestModel


class TestSoftDelete(TestCase):

    def test_soft_delete_model_doesnt_really_delete(self):
        instance = TestModel.objects.create()
        instance.delete()
        assert not TestModel.objects.filter(pk=instance.pk).exists()
        assert TestModel.all_objects.filter(pk=instance.pk).exists()
