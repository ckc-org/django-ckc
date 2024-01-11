from djstripe.models import PaymentMethod, Price, Customer
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from ckc.stripe.serializers import PaymentMethodSerializer, PriceSerializer, SubscribeSerializer


class PaymentMethodViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = PaymentMethod.objects.filter(customer__subscriber=self.request.user)
        return qs


class PriceViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_class = PriceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Price.objects.all()
        return qs


class SubscribeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_serialzer_class(self):
        if self.action == 'subscribe':
            return SubscribeSerializer

    @action(methods=['post'], detail=False)
    def subscribe(self, request):
        # get stripe customer
        customer, created = Customer.get_or_create(subscriber=request.user)
        if customer.subscription:
            return Response(status=400, data={'error': 'already subscribed'})

        serializer = SubscribeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer.subscribe(price=serializer.data['price_id'])
        return Response(status=204)

    @action(methods=['post'], detail=False)
    def cancel(self, request):
        # get stripe customer
        customer, created = Customer.get_or_create(subscriber=request.user)
        customer.subscription.cancel()
        return Response(status=204)
