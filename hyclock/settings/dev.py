from .common import *

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # 1번 DB
        "TIMEOUT": 3600,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient",}, 
    }
}
