from django.urls import reverse
from rest_framework.test import APITestCase


class TestExceptions(APITestCase):

    def test_raising_snackbar_exception_returns_snackbar_message_to_user(self):
        resp = self.client.get(reverse('test-exceptions'))
        assert resp.status_code == 400
        assert resp.data['snackbar_message'] == 'This is a test exception'
