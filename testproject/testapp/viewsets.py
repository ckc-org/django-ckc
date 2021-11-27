from rest_framework.viewsets import ModelViewSet

from testapp.models import ModelWithACreator, ModelWithADifferentNamedCreator, BModel
from testapp.serializers import TestModelWithACreatorSerializer, TestModelWithADifferentNamedCreatorSerializer, \
    BModelSerializer


class TestModelWithACreatorViewSet(ModelViewSet):
    queryset = ModelWithACreator.objects.all()
    serializer_class = TestModelWithACreatorSerializer


class TestModelWithADifferentNamedCreatorViewSet(ModelViewSet):
    queryset = ModelWithADifferentNamedCreator.objects.all()
    serializer_class = TestModelWithADifferentNamedCreatorSerializer


class BModelViewSet(ModelViewSet):
    queryset = BModel.objects.all()
    serializer_class = BModelSerializer
