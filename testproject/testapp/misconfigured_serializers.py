from rest_framework.serializers import ModelSerializer

from ckc.fields import PrimaryKeyWriteSerializerReadField
from testapp.models import AModel, BModel


class MisconfiguredSerializer(ModelSerializer):
    a = PrimaryKeyWriteSerializerReadField(
        queryset=AModel.objects.all(),  # This field requires a read_serializer kwarg
    )

    class Meta:
        model = BModel
        fields = (
            'id',
            'a'
        )
