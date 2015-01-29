from unittest.mock import patch, Mock
from datetime import datetime
from django.test import TestCase
from django.utils.timezone import utc
from test_app.models import TestModel


class DraftObjectCreation(TestCase):
    def test_object_with_draft_created___draft_object_is_created(self):
        m = TestModel()
        m.save()

        self.assertIsNotNone(TestModel.objects.first().draft)

    @patch("draftmodel.draft.now", Mock(return_value=datetime(2014, 1, 1, tzinfo=utc)))
    def test_object_with_draft_created___created_instance_has_no_creation_time(self):
        m = TestModel()
        m.save()

        self.assertIsNone(TestModel.objects.first().creation_time)

    @patch("draftmodel.draft.now", Mock(return_value=datetime(2014, 1, 1, tzinfo=utc)))
    def test_object_with_draft_created___created_instance_has_no_edited_time(self):
        m = TestModel()
        m.save()

        self.assertIsNone(TestModel.objects.first().edited_time)

    @patch("draftmodel.draft.now", Mock(return_value=datetime(2014, 1, 1, tzinfo=utc)))
    def test_object_with_draft_created___created_instance_draft_has_correct_creation_time(self):
        m = TestModel()
        m.save()

        self.assertEqual(datetime(2014, 1, 1, tzinfo=utc), TestModel.objects.first().draft.creation_time)

    @patch("draftmodel.draft.now", Mock(return_value=datetime(2014, 1, 1, tzinfo=utc)))
    def test_object_with_draft_created___created_instance_draft_has_correct_edited_time(self):
        m = TestModel()
        m.save()

        self.assertEqual(datetime(2014, 1, 1, tzinfo=utc), TestModel.objects.first().draft.edited_time)

    def test_object_with_draft_created___created_instance_publish_time_is_None(self):
        m = TestModel()
        m.save()

        self.assertIsNone(TestModel.objects.first().published_time)

    def test_object_with_draft_is_created_with_int_field___draft_has_correct_field_value(self):
        m = TestModel(int_field=123)
        m.save()

        self.assertEqual(123, m.draft.int_field)

    def test_object_with_draft_is_created_and_changed___draft_object_is_the_same_object(self):
        m = TestModel()
        m.save()

        draft_id = m.draft.id

        m.int_field = 123
        m.save()
        
        self.assertEqual(draft_id, m.draft.id)
