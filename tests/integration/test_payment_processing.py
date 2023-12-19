from django.urls import reverse
from djstripe.models import PaymentMethod, Customer
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

User = get_user_model()


class TestExceptions(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.client.force_authenticate(user=self.user)
        return super().setUp()

    def test_payment_method(self):
        # simulate card being created on the frontend
        url = reverse('payment-methods-list')
        payload = {"token": "pm_card_visa"}
        resp = self.client.post(url, data=payload, format='json')

        # assert payment method and customer creation
        assert resp.status_code == 201
        assert PaymentMethod.objects.count() == 1
        assert Customer.objects.count() == 1
