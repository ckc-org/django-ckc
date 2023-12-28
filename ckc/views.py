from djstripe.models import PaymentMethod, Price, Plan
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny

from ckc.serializers import PaymentMethodSerializer, PriceSerializer


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = PaymentMethod.objects.filter(customer__subscriber=self.request.user)
        return qs


class PriceViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Price.objects.all()
        return qs
