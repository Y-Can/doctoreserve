# __init__.py à la racine de votre projet Django

from __future__ import absolute_import, unicode_literals

# Cela permettra à 'celery' d'être toujours importé lors du démarrage de Django
from .celery import app as celery_app

__all__ = ('celery_app',)
