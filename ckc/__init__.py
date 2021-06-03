# Doing a try/except here so we don't force end users of the
# django-ckc module to install factory boy.
try:
    import factory
    from .providers import DjangoGeoPointProvider

    # We import here to run the faker factory add_provider stuff...
    factory.Faker.add_provider(DjangoGeoPointProvider)
except ImportError:
    pass
