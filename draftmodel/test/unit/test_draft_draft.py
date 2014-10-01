from django.db import models
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "draftmodel.test.settings")

import inspect
from unittest import TestCase
from draftmodel.draft import draft


@draft
class TestModel():
    foo_field = models.IntegerField()


class DraftDraft(TestCase):
    def test_draft_on_model___draft_model_object_is_created(self):
        self.assertTrue(hasattr(inspect.getmodule(TestModel), "Draft_TestModel"))

    def test_draft_on_model___draft_is_an_instance_of_the_original_model(self):
        self.assertIn(Draft_TestModel, TestModel.__subclasses__())

    def test_draft_on_model___model_has_a_creation_date_attribute(self):
        self.assertIsInstance(TestModel.creation_date, models.DateTimeField)

    def test_draft_on_model___model_has_a_published_date_attribute(self):
        self.assertIsInstance(TestModel.published_date, models.DateTimeField)

    def test_draft_on_model___model_has_a_edited_date_attribute(self):
        self.assertIsInstance(TestModel.edited_date, models.DateTimeField)

    def test_draft_on_model___draft_has_a_creation_date_attribute(self):
        self.assertIsInstance(Draft_TestModel.creation_date, models.DateTimeField)

    def test_draft_on_model___draft_has_a_published_date_attribute(self):
        self.assertIsInstance(Draft_TestModel.published_date, models.DateTimeField)

    def test_draft_on_model___draft_has_a_edited_date_attribute(self):
        self.assertIsInstance(Draft_TestModel.edited_date, models.DateTimeField)

    def test_draft_on_model___draft_has_fields_on_the_original_model(self):
        self.assertIsInstance(Draft_TestModel.foo_field, models.IntegerField)