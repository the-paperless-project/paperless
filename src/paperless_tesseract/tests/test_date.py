import datetime
import os
import shutil

from dateutil import tz
from django.conf import settings
from django.test import TestCase, override_settings
from tempfile import TemporaryDirectory
from unittest import mock

from ..parsers import RasterisedDocumentParser


class TestDate(TestCase):
    SAMPLE_FILES = os.path.join(os.path.dirname(__file__), "samples")

    def setUp(self):
        self.scratchdir = TemporaryDirectory()
        scratchdir_override = override_settings(
                SCRATCH_DIR=self.scratchdir.name)
        scratchdir_override.enable()

    def tearDown(self):
        self.scratchdir.cleanup()

    def test_date_format_1(self):
        input_file = os.path.join(self.SAMPLE_FILES, "")
        document = RasterisedDocumentParser(input_file)
        document._text = "lorem ipsum 130218 lorem ipsum"
        self.assertEqual(document.get_date(), None)

    def test_date_format_2(self):
        input_file = os.path.join(self.SAMPLE_FILES, "")
        document = RasterisedDocumentParser(input_file)
        document._text = "lorem ipsum 2018 lorem ipsum"
        self.assertEqual(document.get_date(), None)

    def test_date_format_3(self):
        input_file = os.path.join(self.SAMPLE_FILES, "")
        document = RasterisedDocumentParser(input_file)
        document._text = "lorem ipsum 20180213 lorem ipsum"
        self.assertEqual(document.get_date(), None)

    def test_date_format_4(self):
        input_file = os.path.join(self.SAMPLE_FILES, "")
        document = RasterisedDocumentParser(input_file)
        document._text = "lorem ipsum 13.02.2018 lorem ipsum"
        date = document.get_date()
        self.assertEqual(
            date,
            datetime.datetime(
                2018, 2, 13, 0, 0,
                tzinfo=tz.gettz(settings.TIME_ZONE)
            )
        )

    def test_date_format_5(self):
        input_file = os.path.join(self.SAMPLE_FILES, "")
        document = RasterisedDocumentParser(input_file)
        document._text = (
            "lorem ipsum 130218, 2018, 20180213 and lorem 13.02.2018 lorem "
            "ipsum"
        )
        date = document.get_date()
        self.assertEqual(
            date,
            datetime.datetime(
                2018, 2, 13, 0, 0,
                tzinfo=tz.gettz(settings.TIME_ZONE)
            )
        )

    def test_date_format_6(self):
        input_file = os.path.join(self.SAMPLE_FILES, "")
        document = RasterisedDocumentParser(input_file)
        document._text = (
            "lorem ipsum\n"
            "Wohnort\n"
            "3100\n"
            "IBAN\n"
            "AT87 4534\n"
            "1234\n"
            "1234 5678\n"
            "BIC\n"
            "lorem ipsum"
        )
        self.assertEqual(document.get_date(), None)

    def test_date_format_7(self):
        input_file = os.path.join(self.SAMPLE_FILES, "")
        document = RasterisedDocumentParser(input_file)
        document._text = (
            "lorem ipsum\n"
            "März 2019\n"
            "lorem ipsum"
        )
        date = document.get_date()
        self.assertEqual(
            date,
            datetime.datetime(
                2019, 3, 1, 0, 0,
                tzinfo=tz.gettz(settings.TIME_ZONE)
            )
        )

    def test_date_format_8(self):
        input_file = os.path.join(self.SAMPLE_FILES, "")
        document = RasterisedDocumentParser(input_file)
        document._text = (
            "lorem ipsum\n"
            "Wohnort\n"
            "3100\n"
            "IBAN\n"
            "AT87 4534\n"
            "1234\n"
            "1234 5678\n"
            "BIC\n"
            "lorem ipsum\n"
            "März 2020"
        )
        self.assertEqual(
            document.get_date(),
            datetime.datetime(
                2020, 3, 1, 0, 0,
                tzinfo=tz.gettz(settings.TIME_ZONE)
            )
        )

    def test_date_format_9(self):
        input_file = os.path.join(self.SAMPLE_FILES, "")
        document = RasterisedDocumentParser(input_file)
        document._text = (
            "lorem ipsum\n"
            "27. Nullmonth 2020\n"
            "März 2020\n"
            "lorem ipsum"
        )
        self.assertEqual(
            document.get_date(),
            datetime.datetime(
                2020, 3, 1, 0, 0,
                tzinfo=tz.gettz(settings.TIME_ZONE)
            )
        )

    @mock.patch(
        "paperless_tesseract.parsers.RasterisedDocumentParser.get_text",
        return_value="01-07-0590 00:00:00"
    )
    def test_crazy_date_past(self, *args):
        document = RasterisedDocumentParser("/dev/null")
        document.get_text()
        self.assertIsNone(document.get_date())

    @mock.patch(
        "paperless_tesseract.parsers.RasterisedDocumentParser.get_text",
        return_value="01-07-2350 00:00:00"
    )
    def test_crazy_date_future(self, *args):
        document = RasterisedDocumentParser("/dev/null")
        document.get_text()
        self.assertIsNone(document.get_date())

    @mock.patch(
        "paperless_tesseract.parsers.RasterisedDocumentParser.get_text",
        return_value="20 408000l 2475"
    )
    def test_crazy_date_with_spaces(self, *args):
        document = RasterisedDocumentParser("/dev/null")
        document.get_text()
        self.assertIsNone(document.get_date())

    @mock.patch(
        "paperless_tesseract.parsers.RasterisedDocumentParser.get_text",
        return_value="No date in here"
    )
    @override_settings(FILENAME_DATE_ORDER="YMD")
    def test_filename_date_parse_invalid(self, *args):
        document = RasterisedDocumentParser("/tmp/20 408000l 2475 - test.pdf")
        document.get_text()
        self.assertIsNone(document.get_date())
