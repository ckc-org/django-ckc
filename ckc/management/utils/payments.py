import stripe
from djstripe.models import Customer


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
