# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
from django_multiten.utils import set_db
from django.conf import settings
from django.http import HttpResponseBadRequest

try:
    DB_RESOLVER = settings.MULTITEN_DB_RESOLVER
except AttributeError:
    DB_RESOLVER = lambda request: request.get_host().split(".")[0]


class DynamicDBMiddleware:
    def process_request(self, request):
        try:
            set_db(DB_RESOLVER(request))
        except KeyError:
            return HttpResponseBadRequest('No database credentials for this host')
