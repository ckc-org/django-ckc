import stripe
from django.urls import reverse
from djstripe.models import PaymentMethod, Customer
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

from ckc.management.utils.payments import create_checkout_session, create_payment_intent, confirm_payment_intent

User = get_user_model()


class TestExceptions(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.client.force_authenticate(user=self.user)
        return super().setUp()

    def test_payment_method(self):
        # simulate card being created on the frontend
        url = reverse('payment-methods-list')
        payload = {"pm_id": "pm_card_visa"}
        resp = self.client.post(url, data=payload, format='json')

        # assert payment method and customer creation
        assert resp.status_code == 201
        assert PaymentMethod.objects.count() == 1
        assert Customer.objects.count() == 1

    def test_create_checkout_session(self):
        session = create_checkout_session(
            self.user,
            'https://example.com/success',
            'https://example.com/cancel',
            [{
                "quantity": 1,
                "price_data": {
                    "currency": "usd",
                    "unit_amount": 2000,
                    "product_data": {
                        "name": "Sample Product Name",
                        "images": ["https://i.imgur.com/EHyR2nP.png"],
                        "description": "Sample Description",
                    },
                },
            }],
            metadata={
                "test": "metadata"
            },
        )
        assert session is not None

    def test_payment_intents(self):
        # assume we already have a stripe customer with a payment method attatched
        customer, created = Customer.get_or_create(subscriber=self.user)
        payment_method = customer.add_payment_method("pm_card_visa")
        customer.add_payment_method(payment_method.id)

        # manual payment intent confirmation

        # create a payment intent
        intent = create_payment_intent(payment_method.id, customer.id, 2000, confirmation_method="manual")

        # assert payment intent creation
        assert intent is not None
        assert intent.status == "requires_confirmation"

        # assert payment intent confirmation
        response_data, status_code = confirm_payment_intent(intent.id)
        assert status_code == 200
        assert response_data.get('success', False)

        # automatic payment intent confirmation
        intent = create_payment_intent(payment_method.id, 2000, confirmation_method="automatic")
        assert intent is not None
        assert intent.status == "succeeded"


