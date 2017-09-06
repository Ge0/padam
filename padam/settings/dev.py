# flake8: noqa
from .base import *

DEBUG = True

# This key is only intended for development purposed and has nothing
# that secret:
SECRET_KEY = 'SECRET_KEY_DEV'
GOOGLEMAP_KEY = os.environ.get('PADAM_DJANGO_GOOGLEMAP_KEY')