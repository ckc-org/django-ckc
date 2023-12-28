import json

import stripe
from django.urls import reverse
from djstripe.models import PaymentMethod, Customer, Price, Product
# from djstripe.core import Price
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

from ckc.utils.payments import create_checkout_session, create_payment_intent, confirm_payment_intent
from tests.integration.utils import create_subscription_plan

User = get_user_model()


class TestPaymentProcessing(APITestCase):
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
        assert json.loads(response_data).get('success', False)

        # automatic payment intent confirmation
        intent = create_payment_intent(payment_method.id, customer.id,  2000, confirmation_method="automatic")
        assert intent is not None
        assert intent.status == "succeeded"

    def test_subscriptions(self):
        # create the subscription plan through dj stripe price object
        price = create_subscription_plan(2000, "month", product_name="Sample Product Name: 0", currency="usd")
        assert price is not None
        assert price.id is not None

        customer, created = Customer.get_or_create(subscriber=self.user)
        customer.add_payment_method("pm_card_visa")
        # subscribe the customer to the plan
        subscription = customer.subscribe(price=price.id)

        stripe_sub = stripe.Subscription.retrieve(subscription.id)
        assert stripe_sub is not None
        assert stripe_sub.status == "active"
        assert stripe_sub.customer == customer.id

        # cancel the subscription
        subscription.cancel()
        stripe_sub = stripe.Subscription.retrieve(subscription.id)
        assert stripe_sub is not None
        assert stripe_sub.status == "canceled"

    def test_subscription_plan_list(self):
        for i in range(3):
            create_subscription_plan(2000 + i, "month", product_name=f"Sample Product Name: {i}", currency="usd")

        url = reverse('prices-list')
        resp = self.client.get(url)
        assert resp.status_code == 200
        assert len(resp.data) == 3
