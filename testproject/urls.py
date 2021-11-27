from rest_framework import routers

from testapp.viewsets import TestModelWithACreatorViewSet, TestModelWithADifferentNamedCreatorViewSet, BModelViewSet

router = routers.SimpleRouter()
router.register(r'creators', TestModelWithACreatorViewSet)
router.register(r'creators-alternative', TestModelWithADifferentNamedCreatorViewSet)
router.register(r'bmodel', BModelViewSet)

urlpatterns = router.urls
