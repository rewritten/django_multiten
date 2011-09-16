# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

""" Patch for django connection handler, to load
database credentials from the specified model.
"""

from django.db.utils import load_backend, ConnectionHandler, DEFAULT_DB_ALIAS
from .utils import get_db

def __connection_handler__getitem__(self, alias):
    if alias in self._connections:
        return self._connections[alias]
    # This is a new customer database, so make a copy of the default DB, 
    # set the alias, and other database details and store it in the 
    # dictionary of databases
    if not alias in self.databases:
        #Get db details from threadlocal. Aha! Call Pollution Control now!
        db_details = get_db()
        new_db = self.databases[DEFAULT_DB_ALIAS].copy()
        new_db['NAME'] = db_details['db_name']
        new_db['USER'] = db_details['db_user']
        new_db['PASSWORD'] = db_details['db_password']
        self.databases[alias] = new_db
    self.ensure_defaults(alias)
    db = self.databases[alias]
    backend = load_backend(db['ENGINE'])
    conn = backend.DatabaseWrapper(db, alias)
    self._connections[alias] = conn
    return conn

ConnectionHandler.__getitem__ = __connection_handler__getitem__
