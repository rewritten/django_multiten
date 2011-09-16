# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
from .models import MasterModel
from .utils import get_db

try:
    from django.conf import settings
    MASTER_DB = settings.MULTITEN_MASTER_DB
except AttributeError:
    MASTER_DB = 'default'


class DynamicDBRouter(object):

    def db_for_read(self, model, **hints):
        if isinstance(model, MasterModel):
            return MASTER_DB
        return get_db()

    def db_for_write(self, model, **hints):
        if isinstance(model, MasterModel):
            return MASTER_DB
        return get_db()

    def allow_syncdb(self, db, model):
        if isinstance(model, MasterModel):
            return db == MASTER_DB
        return get_db()
