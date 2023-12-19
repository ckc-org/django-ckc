from django.urls import path
from rest_framework import routers

from ckc.views import PaymentMethodViewSet
from testapp.views import TestExceptionsViewSet
from testapp.viewsets import TestModelWithACreatorViewSet, TestModelWithADifferentNamedCreatorViewSet, BModelViewSet


router = routers.SimpleRouter()
router.register(r'creators', TestModelWithACreatorViewSet)
router.register(r'creators-alternative', TestModelWithADifferentNamedCreatorViewSet)
router.register(r'bmodel', BModelViewSet)
router.register(r'payment-methods', PaymentMethodViewSet, basename='payment-methods')

urlpatterns = router.urls + [
    path('test-exceptions/', TestExceptionsViewSet.as_view(), name='test-exceptions'),
]
