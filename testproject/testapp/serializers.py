from rest_framework.serializers import ModelSerializer

from ckc.fields import PrimaryKeyWriteSerializerReadField
from ckc.serializers import DefaultUserCreateMixin
from testapp.models import ModelWithACreator, ModelWithADifferentNamedCreator, AModel, BModel


class TestModelWithACreatorSerializer(DefaultUserCreateMixin, ModelSerializer):
    class Meta:
        model = ModelWithACreator
        fields = []


class TestModelWithADifferentNamedCreatorSerializer(DefaultUserCreateMixin, ModelSerializer):
    class Meta:
        model = ModelWithADifferentNamedCreator
        fields = []
        user_field = 'owner'


class AModelSerializer(ModelSerializer):
    class Meta:
        model = AModel
        fields = (
            'id',
            'title',
        )


class BModelSerializer(ModelSerializer):
    a = PrimaryKeyWriteSerializerReadField(
        queryset=AModel.objects.all(),
        read_serializer=AModelSerializer,
    )

    class Meta:
        model = BModel
        fields = (
            'id',
            'a'
        )
