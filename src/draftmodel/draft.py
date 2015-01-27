import inspect
from django.db import models
from django.db.models.signals import pre_save
from django.utils.timezone import now


def _is_copyable_field(field):
    return type(field).__name__ != "AutoField"


def _draft_save(instance, *args, **kwargs):
    current_time = now()

    instance.creation_time = current_time
    instance.edited_time = current_time

    if not instance.draft_id:
        draft_instance = instance.draft_class()
    else:
        draft_instance = instance.draft

    for field in instance._meta.local_fields:
        if _is_copyable_field(field):
            setattr(draft_instance, field.attname, getattr(instance, field.attname))

    draft_instance.save(*args, **kwargs)

    instance.draft = draft_instance


def _patch_methods(cls):

    # patch out the save method
    _orig_save = cls.save

    def _new_save(self, *args, **kwargs):
        _draft_save(self, *args, **kwargs)

        if not self._state.adding:
            kwargs["update_fields"] = []
        _orig_save(self, *args, **kwargs)

    cls.save = _new_save

    return cls


def draft(cls):
    cls.add_to_class("creation_time", models.DateTimeField(null=True, default=None))
    cls.add_to_class("published_time", models.DateTimeField(null=True, default=None))
    cls.add_to_class("edited_time", models.DateTimeField(null=True, default=None))

    class _Draft(models.Model):
        pass

    for field in cls._meta.local_fields:
        if _is_copyable_field(field):
            _Draft.add_to_class(field.attname, field)

    class_name = "Draft_{cls}".format(cls=cls.__name__)
    setattr(inspect.getmodule(cls), class_name, _Draft)
    draft_class = getattr(inspect.getmodule(cls), class_name)

    cls.draft_class = draft_class

    cls.add_to_class("draft", models.ForeignKey(draft_class))

    return _patch_methods(cls)
