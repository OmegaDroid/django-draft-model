import inspect
from django.db import models


def draft(cls):
    cls.creation_date = models.DateTimeField(null=True, default=None)
    cls.published_date = models.DateTimeField(null=True, default=None)
    cls.edited_date = models.DateTimeField(null=True, default=None)

    class _Draft(cls):
        pass

    class_name = "Draft_{cls}".format(cls=cls.__name__)
    setattr(inspect.getmodule(cls), class_name, _Draft)

    return cls

