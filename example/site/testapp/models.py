# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
from django_multiten.models import Credentials, MasterModel
from django.db import models


class Customer(Credentials):
    customer_name = models.SlugField()

class Setting(MasterModel):
    """ This is going to be stored in the master database, so it needs a FK to
    the customer """
    customer = models.ForeignKey(Customer)
    name = models.SlugField()
    value = models.CharField(max_length=512)

    class Meta:
        unique_together = (('customer', 'name'),)


class PrivateThing(models.Model):
    """ Does not need a FK to customer because it's in a private DB """
    title = models.SlugField()
    content = models.TextField()
