from rest_framework.serializers import ModelSerializer

from ckc.serializers import DefaultUserCreateMixin
from testapp.models import ModelWithACreator, ModelWithADifferentNamedCreator


class TestModelWithACreatorSerializer(DefaultUserCreateMixin, ModelSerializer):
    class Meta:
        model = ModelWithACreator
        fields = []


class TestModelWithADifferentNamedCreatorSerializer(DefaultUserCreateMixin, ModelSerializer):
    class Meta:
        model = ModelWithADifferentNamedCreator
        fields = []
        user_field = 'owner'
