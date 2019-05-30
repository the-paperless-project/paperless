from unittest import mock

from django.test import TestCase

from ..models import Document, Correspondent


class TestDocument(TestCase):

    def test_file_deletion(self):
        document = Document.objects.create(
            correspondent=Correspondent.objects.create(name="Test0"),
            title="Title",
            content="content",
            checksum="checksum",
        )
        file_path = document.source_path
        thumb_path = document.thumbnail_path
        with mock.patch("documents.signals.handlers.os.unlink") as mock_unlink:
            document.delete()
            mock_unlink.assert_any_call(file_path)
            mock_unlink.assert_any_call(thumb_path)
            self.assertEqual(mock_unlink.call_count, 2)

    def test_sulgified_title_and_content(self):
        document = Document.objects.create(
            title="Title",
            content="Content",
            checksum="azerty1"
        )
        self.assertEqual(document.title, "Title")
        self.assertEqual(document.content, "Content")
        self.assertEqual(document.searchable_title, "title")
        self.assertEqual(document.searchable_content, "content")

        document = Document.objects.create(
            title="Zürich Weiß",
            content="Telefónica ééé aaa",
            checksum="azerty2"
        )
        self.assertEqual(document.searchable_title, "zurich weiss")
        self.assertEqual(document.searchable_content, "telefonica eee aaa")


        document = Document.objects.create(checksum="azerty3")
        self.assertEqual(document.title, '')
        self.assertEqual(document.content, '')
        self.assertEqual(document.searchable_title, '')
        self.assertEqual(document.searchable_content, '')
