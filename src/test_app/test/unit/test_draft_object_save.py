from unittest.mock import Mock
from django.test import TestCase
from test_app.models import TestModel


class DraftObjectCreation(TestCase):
    def test_object_with_draft_changed_and_saved___draft_object_reflects_the_change(self):
        m = TestModel(int_field=123)
        m.save()

        m.int_field = 456
        m.save()

        self.assertEqual(456, TestModel.objects.first().draft.int_field)

    def test_object_with_draft_changed_and_saved___base_object_matches_original(self):
        m = TestModel(int_field=123)
        m.save()

        m.int_field = 456
        m.save()

        self.assertEqual(123, TestModel.objects.first().int_field)

    def test_object_with_draft_is_saved_with_kwargs___args_and_kwargs_are_passed_to_draft_save(self):
        m = TestModel(int_field=123)
        m.save()

        m.int_field = 456

        m.draft.save = Mock()
        m.save(update_fields=["int_field"])

        m.draft.save.assert_called_once_with(update_fields=["int_field"])
