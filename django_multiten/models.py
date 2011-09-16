# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
from django.db import models


class MasterModel(models.Model):

    class Meta:
        abstract = True


class Credentials(MasterModel):
    """ A customer, along with its database credentials. In fact, several
    records may exist for the same customer, provided the 'alias' field is
    different. The 'alias' will be set from a middleware or from commandline."""

    alias = models.SlugField(unique=True)
    db_name = models.CharField(max_length=20)
    db_user = models.CharField(max_length=20)
    db_password = models.CharField(max_length=20)

    class Meta:
        abstract = True
