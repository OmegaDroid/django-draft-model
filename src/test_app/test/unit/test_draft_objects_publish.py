from datetime import datetime
from unittest.mock import Mock, patch
from django.test import TestCase
from django.utils.timezone import utc
from test_app.models import TestModel


class DraftObjectPublish(TestCase):
    @patch("draftmodel.draft.now", Mock(return_value=datetime(2014, 1, 1, tzinfo=utc)))
    def test_object_is_published___object_published_date_is_updated(self):
        m = TestModel(int_field=123)
        m.save()
        m.publish()

        instance = TestModel.objects.first()

        self.assertEqual(datetime(2014, 1, 1, tzinfo=utc), instance.published_time)

    @patch("draftmodel.draft.now", Mock(return_value=datetime(2014, 1, 1, tzinfo=utc)))
    def test_object_is_published___draft_published_date_is_updated(self):
        m = TestModel(int_field=123)
        m.save()
        m.publish()

        instance = TestModel.objects.first()

        self.assertEqual(datetime(2014, 1, 1, tzinfo=utc), instance.draft.published_time)

    def test_object_is_published___object_field_is_correct(self):
        m = TestModel(int_field=123)
        m.save()
        m.publish()

        instance = TestModel.objects.first()

        self.assertEqual(123, instance.int_field)