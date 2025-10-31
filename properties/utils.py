import logging
from django_redis import get_redis_connection
from .models import Property
from django.core.cache import cache

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Return all Property objects, cached in Redis for 1 hour.
    """
    all_properties = cache.get('all_properties')
    if all_properties is None:
        all_properties = list(Property.objects.all())
        cache.set('all_properties', all_properties, 3600)  # 1 hour
    return all_properties

def get_redis_cache_metrics():
    """
    Retrieves Redis cache metrics: keyspace_hits, keyspace_misses, and hit_ratio.
    Logs metrics and returns them as a dictionary.
    """
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = keyspace_hits / total_requests if total_requests > 0 else 0

        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'hit_ratio': hit_ratio
        }

        logger.info(f"Redis Cache Metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {e}")
        return {'keyspace_hits': 0, 'keyspace_misses': 0, 'hit_ratio': 0}
