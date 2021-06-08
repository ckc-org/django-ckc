# Doing a try/except here so we don't force end users of the
# django-ckc module to install factory boy.
from django.core.exceptions import ImproperlyConfigured

try:
    import factory
    from django.contrib.gis.geos import Point
    from faker.providers import BaseProvider

    class DjangoGeoPointProvider(BaseProvider):
        """Custom helper class giving us the 'geo_point' provider, example:

            location = factory.Faker('geo_point', country_code='US')

        (note, you must call factory.Faker.add_provider(DjangoGeoPointProvider) to add
        this provider!)
        """

        def geo_point(self, **kwargs):
            kwargs['coords_only'] = True
            faker = factory.faker.faker.Faker()

            # local_latlng returns something like:
            #   ('40.72371', '-73.95097', 'Greenpoint', 'US', 'America/New_York')
            coords = faker.local_latlng(**kwargs)
            return Point(x=float(coords[1]), y=float(coords[0]), srid=4326)
except (ImportError, ImproperlyConfigured):
    pass
