import stripe
from djstripe.models import PaymentMethod, Customer, Price, Product

from rest_framework import serializers

class PaymentMethodSerializer(serializers.ModelSerializer):
    token = serializers.CharField(write_only=True)

    class Meta:
        model = PaymentMethod
        fields = (
            'pm_id',
            'id',
            'type',

            # 'customer',
            # 'stripe_id',
            # 'card_brand',
            # 'card_last4',
            # 'card_exp_month',
            # 'card_exp_year',
            # 'is_default',
            # 'created',
            # 'modified',
        )
        read_only_fields = (
            'id',
            'type',
            # 'customer',
            # 'stripe_id',
            # 'card_brand',
            # 'card_last4',
            # 'card_exp_month',
            # 'card_exp_year',
            # 'is_default',
            # 'created',
            # 'modified',
        )

    def create(self, validated_data):
        customer, created = Customer.get_or_create(subscriber=self.context['request'].user)
        try:
            payment_method = customer.add_payment_method(validated_data['pm_id'])
        except (stripe.error.InvalidRequestError) as e:
            raise serializers.ValidationError(e)

        return payment_method


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'type',
        )
        read_only_fields = (
            'id',
            'name',
            'description',
            'type',
        )


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = (
            'id',
            'unit_amount',
            'currency',
            'recurring',
        )
        read_only_fields = (
            'id',
            'unit_amount',
            'currency',
            'recurring',
        )


class SubscribeSerializer(serializers.Serializer):
    price_id = serializers.CharField()

    class Meta:
        fields = (
            'price_id'
        )
