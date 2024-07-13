from django.db import models


class Categories(models.Model):

    category_name = models.CharField(max_length=100)