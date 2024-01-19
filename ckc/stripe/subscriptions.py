import stripe
from djstripe.models import Price, Product


# def create_price(amount=None, interval=None, interval_count=1, currency="usd", product_name="Sample Product Name", **kwargs):
def create_price(product_kwargs, **price_kwargs):
    """
    create and return a stripe price object
    @param amount: the amount to charge
    @param interval: the interval to charge at
    @param interval_count: the number of intervals to charge at
    @param currency: the currency to charge in
    @param product_name: the name of the product to create
    @param kwargs: additional arguments to pass to the stripe.Product.create method
    @returns stripe.Price

    """
    try:

        stripe_product = stripe.Product.create(
            **product_kwargs,
        )
    except stripe.error.StripeError:
        raise ValueError("Error creating Stripe Product")
    product = Product.sync_from_stripe_data(stripe_product)
    # recurring = kwargs.pop("recurring", {})
    # recurring.update({
    #     "interval": interval,
    #     "interval_count": interval_count,
    # })
    price = Price.create(
        product=product,
        **price_kwargs
        # unit_amount=amount,
        # currency=currency,
        # recurring={
        #     "interval": interval,
        #     "interval_count": interval_count,
        # },
        # product=product,
        # active=True,
        # **kwargs
    )

    return price
