from django_exercises.django_settings import *
from django_exercises.app_settings import *
try:
    from django_exercises.local_settings import *
except ImportError:
    pass
