from rest_framework import serializers


class PrimaryKeyWriteSerializerReadField(serializers.PrimaryKeyRelatedField):
    def __init__(self, *args, **kwargs):
        read_serializer = kwargs.pop('read_serializer', None)
        assert read_serializer is not None, (
            'PrimaryKeyWriteSerializerReadField must provide `read_serializer` argument.'
        )
        super().__init__(*args, **kwargs)
        self.read_serializer = read_serializer

    # Related fields will not look up any of the object's values for normal primary
    # key serialization. This override forces the lookup of the entire object.
    def use_pk_only_optimization(self):
        return False

    def to_representation(self, value):
        # Are we on the browsable API? if so, just return pk!
        if self.context['request'].META["HTTP_ACCEPT"].startswith("text/html"):
            return value.pk
        else:
            # Normal request, return full item read details
            return self.read_serializer(value, context=self.context).data
