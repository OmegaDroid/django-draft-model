from django.db import models
from draftmodel.draft import draft


@draft
class TestModel(models.Model):
    int_field = models.IntegerField(null=True)
