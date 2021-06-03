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

## distributing

```bash
# change version in setup.cfg
$ ./setup.py sdist
$ twine upload dist/*
```

## tests

```bash
$ docker build -t django-ckc . && docker run django-ckc pytest
```

## what's in this

#### `SoftDeletableModel`

Make your models have a `deleted` bool set when they are deleted instead of actuallying 
being deleted. Uses a model manager `SoftDeleteModelManager` to keep them hidden.

#### `DefaultUserCreateMixin` for `ModelSerializers`

This will automatically set `YourModel.created_by` to `request.user`. To override which
attribute the user is written to, add a `user_field` to your classes Meta information

```py
class YourModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
        

class MySerializer(DefaultUserCreateMixin, ModelSerializer):
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


#### `./manage.py` commands

| command | description|
| :---        |    :----:   |
| `upload_file <source> <destination>` | uses `django-storages` settings to upload a file |
