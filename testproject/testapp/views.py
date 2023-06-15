from rest_framework.views import APIView

from ckc.exceptions import SnackbarError


class TestExceptionsViewSet(APIView):
    def get(self, request, *args, **kwargs):
        raise SnackbarError('This is a test exception')
