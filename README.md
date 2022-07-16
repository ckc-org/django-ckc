django-ckc [<img src="https://ckcollab.com/assets/images/badges/badge.svg" alt="CKC" height="20">](https://ckcollab.com)
==========
tools, utilities
, etc. we use across projects @ [ckc](https://ckcollab.com)


## installing

```bash
pip install django-ckc
```

```python
# settings.py
INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",

    # ... add ckc
    "ckc",
)
```

## tests

```bash
$ docker build -t django-ckc . && docker run django-ckc pytest
```

## what's in this

#### `SoftDeletableModel`

Make your models have a `deleted` bool set when they are deleted instead of actuallying 
being deleted. Uses a model manager `SoftDeleteModelManager` to keep them hidden.

#### `PrimaryKeyWriteSerializerReadField`

A DRF field for writing via PK and reading via a serializer. Useful for when you want to
connect 2 models together and immediately display to the user some useful information.

For example, if you had an `Order` model with `LineItem` objects pointing to it, it may be
useful to create a new line item via order PK and return back the complete order with
new totals and other calculations:

```py
class LineItemUpdateSerializer(serializers.ModelSerializer):
    order = PrimaryKeyWriteSerializerReadField(
        queryset=Order.objects.all(),
        read_serializer=OrderDetailSerializer
    )
    
    class Meta:
        model = LineItem
        fields = ["id", "order", "product"]
```

`POST` data for adding product #123 to order #5 would look like 

```js
// REQUEST
{"order": 5, "product": 123}"}

// RESPONSE
{"order": {"total_amount": "$1,000.00"}, "product": 123}
```



#### `DefaultCreatedByMixin` for `ModelSerializers`

This will automatically set `YourModel.created_by` to `request.user`. To override which
attribute the user is written to, add a `user_field` to your classes Meta information

```py
class YourModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
        

class MySerializer(DefaultCreatedByMixin, ModelSerializer):
    class Meta:
        model = YourModel
```

#### `DjangoGeoPointProvider`

Helps generate geo points in Factory Boy factories.

```py
# factories.py
class SomeLocationFactory(DjangoModelFactory):
    location = factory.Faker('geo_point', country_code='US')

    class Meta:
        model = SomeLocation

# test_whatever.py
from django.contrib.gis.geos import Point


class WhateverTest(TestCase):
    def test_something(self):
        SomeLocationFactory()  # random location
        SomeLocationFactory(location=Point(x=60, y=60))  # specified location
```


#### Slack logging

Get a Slack webhook URL and set `SLACK_WEBHOOK_URL` env var. You can also set `DJANGO_SLACK_LOG_LEVEL`
with info, warning, etc.

Modify your Celery settings:
```py
# Let our slack logger handle celery stuff
CELERY_WORKER_HIJACK_ROOT_LOGGER = False
```

Example `LOGGING` configuration that turns on Slack logging if `SLACK_WEBHOOK_URL` env var is found:
```py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': "%(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s",
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        }
    },
}

SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', '')
if SLACK_WEBHOOK_URL:
    LOGGING['handlers']['slack'] = {
        'class': 'ckc.logging.CkcSlackHandler',
        'level': os.getenv('DJANGO_SLACK_LOG_LEVEL', 'ERROR'),
    }

    LOGGING['loggers']['django']['handlers'] = ['console', 'slack']
    LOGGING['loggers']['']['handlers'] = ['console', 'slack']
```


#### `./manage.py` commands

| command | description|
| :---        |    :----:   |
| `upload_file <source> <destination>` | uses `django-storages` settings to upload a file |
