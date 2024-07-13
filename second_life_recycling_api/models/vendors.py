from django.db import models


class Vendors(models.Model):
    vendor_name = models.CharField(max_length=100)
    vendor_address = models.CharField(max_length=100)