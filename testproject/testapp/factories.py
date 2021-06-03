import factory

from factory.django import DjangoModelFactory

from testapp.models import Location


class LocationFactory(DjangoModelFactory):
    geo_point = factory.Faker('geo_point', country_code='US')

    class Meta:
        model = Location
