from django.core.cache import cache
from .models import Property

def get_all_properties():
    all_properties = cache.get('all_properties')
    if all_properties is None:
        all_properties = list(Property.objects.all())
        cache.set('all_properties', all_properties, 3600)  # cache 1 hour
    return all_properties
