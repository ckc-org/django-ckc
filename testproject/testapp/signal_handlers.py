from django.core.exceptions import ValidationError
from django.dispatch import receiver

from ckc.stripe.signals import post_subscribe, post_cancel
from ckc.stripe.views import SubscribeViewSet
from testapp.models import SubscriptionThroughModel


@receiver(post_subscribe, sender=SubscribeViewSet)
def subscribe_signal_handler(sender, **kwargs):
    """ example function for how to define a post subscribe signal handler. """
    if sender != SubscribeViewSet:
        raise ValidationError('sender must be SubscribeViewSet')
    SubscriptionThroughModel.objects.get_or_create(user=kwargs['user'], subscription=kwargs['subscription'])

@receiver(post_cancel, sender=SubscribeViewSet)
def cancel_signal_handler(sender, **kwargs):
    if sender != SubscribeViewSet:
        raise ValidationError('sender must be SubscribeViewSet')
    SubscriptionThroughModel.objects.filter(user=kwargs['user'], subscription=kwargs['subscription']).delete()
