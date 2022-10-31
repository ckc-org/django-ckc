import pytest
from rest_framework.test import APITestCase

from testapp.models import SnapshottedModel, SnapshottedModelMissingOverride


class TestJsonSnapshottedModels(APITestCase):
    def test_snapshot_model_asserts_method_must_be_implemented_if_it_is_missing(self):
        instance = SnapshottedModelMissingOverride()

        # make sure proper error raised when we try to snapshot with a missing method
        with pytest.raises(NotImplementedError):
            instance.take_snapshot()

    def test_snapshot_model_save_actually_saves_to_databse(self):
        instance = SnapshottedModel()
        instance.take_snapshot()

        # Snapshot was written to model...
        assert instance.snapshot == {"test": "snapshot"}

        instance.save()

        # Snapshot was saved to database, forreal
        assert SnapshottedModel.objects.get(snapshot__test="snapshot")

    def test_snapshotting_an_already_snapshotted_model_raises_exception_unless_forced(self):
        instance = SnapshottedModel()
        instance.take_snapshot()

        # trying to snapshot already snapshotted model -> shit the bed
        with pytest.raises(Exception):
            instance.take_snapshot()

        # Clear snapshot to see if we can re-set it..
        instance.snapshot = None

        # No exception raised here! And data was properly written
        instance.take_snapshot(force=True)

        # We were able to re-snapshot
        assert instance.snapshot == {"test": "snapshot"}
