from collections import OrderedDict
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
        return self.read_serializer(value, context=self.context).data

    def get_choices(self, cutoff=None):
        """Copied from base get_choices, replacing to_representation directly with PK, 
        since our to_representation returns a dict."""
        queryset = self.get_queryset()
        if queryset is None:
            # Ensure that field.choices returns something sensible
            # even when accessed with a read-only field.
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                # Instead of to_representation, just snag pk!
                # self.to_representation(item),
                item.pk,
                self.display_value(item)
            )
            for item in queryset
        ])
