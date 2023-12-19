from djstripe.models import PaymentMethod
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ckc.serializers import PaymentMethodSerializer


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = PaymentMethod.objects.filter(customer__subscriber=self.request.user)
        return qs
