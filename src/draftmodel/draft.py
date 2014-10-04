import inspect
from django.db import models
from django.db.models.signals import pre_save
from django.utils.timezone import now


def _draft_creation(sender, **kwargs):
    current_time = now()

    instance = kwargs["instance"]
    instance.creation_time = current_time
    instance.edited_time = current_time
    draft_instance = sender.draft_class()
    draft_instance.save()

    instance.draft = draft_instance


def draft(cls):
    cls.add_to_class("creation_time", models.DateTimeField(null=True, default=None))
    cls.add_to_class("published_time", models.DateTimeField(null=True, default=None))
    cls.add_to_class("edited_time", models.DateTimeField(null=True, default=None))

    class _Draft(models.Model):
        pass

    class_name = "Draft_{cls}".format(cls=cls.__name__)
    setattr(inspect.getmodule(cls), class_name, _Draft)
    draft_class = getattr(inspect.getmodule(cls), class_name)

    cls.draft_class = draft_class

    cls.add_to_class("draft", models.ForeignKey(draft_class))

    pre_save.connect(_draft_creation, sender=cls)

    return cls
