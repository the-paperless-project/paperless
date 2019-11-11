from unittest import mock

from django.test import TestCase

from ..models import Tag


class TestTag(TestCase):
    def test_searchable_name(self):
        tag = Tag.objects.create(name="Titlé")
        self.assertEqual(tag.name, "Titlé")
        self.assertEqual(tag.searchable_name, "title")
