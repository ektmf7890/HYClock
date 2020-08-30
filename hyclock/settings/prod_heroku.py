from .common import *
import django_heroku
django_heroku.settings(locals())

CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = {
#     '',
# }