# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
from threading import currentThread
from django.conf import settings
from django.utils.functional import memoize
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

from .models import Credentials
import os

_db = {}


MODEL_FOR_CREDENTIALS = settings.MULTITEN_MODEL_FOR_CREDENTIALS
if '.' not in MODEL_FOR_CREDENTIALS:
    raise ImproperlyConfigured('MULTITEN_MODEL_FOR_CREDENTIALS must be a '
        'fully qualified class name')


@memoize
def get_model_for_credentials():
    module_name, model_name = MODEL_FOR_CREDENTIALS.rsplit('.', 1)
    module = import_module(module_name)
    model = getattr(module, model_name)
    if not isinstance(model, Credentials):
        raise ImproperlyConfigured('MULTITEN_MODEL_FOR_CREDENTIALS must '
            'extend multiten.models.Credentials')
    return model


def set_db(db):
    """ Sets the database for current thread to be the one passed, either
    as dictionary or as an alias, to be queried on the master DB """
    m = get_model_for_credentials()
    if isinstance(db, basestring):
        db = dict(zip(
            ('NAME', 'USER', 'PASSWORD'),
            m.objects.values_list('db_name', 'db_user', 'db_password').get(alias=db),
        ))
    _db[currentThread()] = db


def get_db():
    """ Returns the currently set dynamic database. """
    try:
        return _db[currentThread()]
    except KeyError:
        try:
            ENV_ALIAS = os.environ['MULTITEN_DB_ALIAS']
            set_db(ENV_ALIAS)
        except KeyError:
            raise ImproperlyConfigured('The dynamic database alias must be '
                'configured either in environment or by a middleware')
