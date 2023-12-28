import json

import stripe
from djstripe.models import Customer

from django.conf import settings


def create_checkout_session(user, success_url, cancel_url, line_items, metadata=None, payment_method_types=None):
    """
    create and return a stripe checkout session

    @param user: the user to associate the session with
    @param success_url: the url to redirect to after a successful payment
    @param cancel_url: the url to redirect to after a cancelled payment
    @param line_items: a list of line items to add to the session
    @param metadata: optional metadata to add to the session
    @param payment_method_types: optional payment method types to accept. defaults to ["card"]


    metadata = {},
    success_url = "https://example.com/success",
    cancel_url = "https://example.com/cancel",
    line_items = [{
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
    }]

    @returns stripe.checkout.Session
    """
    if not metadata:
        metadata = {}
    if not payment_method_types:
        payment_method_types = ["card"]

    customer, created = Customer.get_or_create(subscriber=user)
    session = stripe.checkout.Session.create(
        payment_method_types=payment_method_types,
        customer=customer.id,
        payment_intent_data={
            "setup_future_usage": "off_session",
            # so that the metadata gets copied to the associated Payment Intent and Charge Objects
            "metadata": metadata
        },
        line_items=line_items,
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata=metadata,
    )
    return session


def create_payment_intent(payment_method_id, customer_id, amount, currency="usd", confirmation_method="automatic"):
    """
    create and return a stripe payment intent
    @param payment_method_id: the id of the payment method to use
    @param amount: the amount to charge
    @param currency: the currency to charge in. defaults to "usd"
    @param confirmation_method: the confirmation method to use. choices are "manual" and "automatic". defaults to "automatic"
        if set to manual, you must call confirm_payment_intent to confirm the payment intent
    @returns stripe.PaymentIntent
    """
    if not payment_method_id:
        raise ValueError("payment_method_id must be set")

    intent = None
    try:
        # Create the PaymentIntent
        intent = stripe.PaymentIntent.create(
            customer=customer_id,
            payment_method=payment_method_id,
            amount=amount,
            currency=currency,
            # confirmation_method=confirmation_method,
            confirm=confirmation_method == "automatic",
            api_key=settings.STRIPE_PRIVATE_KEY,
            automatic_payment_methods={
                "enabled": True,
                "allow_redirects": 'never'
            },

        )
    except stripe.error.CardError:
        pass
    return intent


def confirm_payment_intent(payment_intent_id):
    """
    confirm a stripe payment intent
    @param payment_intent_id: the id of the payment intent to confirm
    @returns a tuple of (data, status_code)
    """
    intent = stripe.PaymentIntent.confirm(
        payment_intent_id,
        api_key=settings.STRIPE_PRIVATE_KEY,
    )

    if intent.status == "requires_action" and intent.next_action.type == "use_stripe_sdk":
        # Tell the client to handle the action
        return_data = json.dumps({
            "requires_action": True,
            "payment_intent_client_secret": intent.client_secret
        }), 200
        pass
    elif intent.status == "succeeded":
        # The payment did not need any additional actions and completed!
        # Handle post-payment fulfillment
        return_data = json.dumps({"success": True}), 200
    else:
        # Invalid status
        return_data = json.dumps({"error": "Invalid PaymentIntent status"}), 500
    return return_data
