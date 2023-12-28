import stripe
from djstripe.models import Product, Price, Plan


def create_subscription_plan(amount, interval, interval_count=1, currency="usd", product_name="Sample Product Name"):
    # product, created = Product.get_or_create(
    #     name=product_name,
    #     description="Sample Description",
    #     type="service",
    # )
    stripe_product = stripe.Product.create(
        name=product_name,
        description="Sample Description",
    )
    product = Product.sync_from_stripe_data(stripe_product)

    price = Price.create(
        unit_amount=amount,
        currency=currency,
        recurring={
            "interval": interval,
            "interval_count": interval_count,
        },
        product=product,
        active=True,
    )
    from pprint import pprint
    pprint(price)

    # print(price)
    # print(created)
    # plan, created = Plan.objects.get_or_create(
    #     active=True,
    #     amount=amount,
    #     interval=interval,
    #     interval_count=interval_count,
    #     product=product,
    #     currency=currency,
    # )
    return price
