from rest_framework.viewsets import ModelViewSet

from testapp.models import ModelWithACreator, ModelWithADifferentNamedCreator
from testapp.serializers import TestModelWithACreatorSerializer, TestModelWithADifferentNamedCreatorSerializer


class TestModelWithACreatorViewSet(ModelViewSet):
    queryset = ModelWithACreator.objects.all()
    serializer_class = TestModelWithACreatorSerializer


class TestModelWithADifferentNamedCreatorViewSet(ModelViewSet):
    queryset = ModelWithADifferentNamedCreator.objects.all()
    serializer_class = TestModelWithADifferentNamedCreatorSerializer
