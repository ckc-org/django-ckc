from rest_framework.views import APIView

from ckc.exceptions import SnackbarException


class TestExceptionsViewSet(APIView):
    def get(self, request, *args, **kwargs):
        raise SnackbarException('This is a test exception')
