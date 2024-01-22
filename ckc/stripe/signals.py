from django.dispatch import Signal

# Define a signal for post-subscription
post_subscribe = Signal()

# Define a signal for post-cancellation
post_cancel = Signal()
