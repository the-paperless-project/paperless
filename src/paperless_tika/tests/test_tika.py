import os
import shutil
from unittest import mock
from uuid import uuid4
from requests.exceptions import ConnectionError

from django.test import TestCase

from ..parsers import TikaDocumentParser
from documents.parsers import ParseError
from paperless_tesseract.parsers import strip_excess_whitespace


class TestDate(TestCase):

    SAMPLE_FILES = os.path.join(os.path.dirname(__file__), "samples")
    SCRATCH = "/tmp/paperless-tests-{}".format(str(uuid4())[:8])

    MOCK_SCRATCH = "paperless_tika.parsers.TikaDocumentParser.SCRATCH"  # NOQA: E501

    def setUp(self):
        os.makedirs(self.SCRATCH, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.SCRATCH)

    @mock.patch(MOCK_SCRATCH, SCRATCH)
    @mock.patch(
        "paperless_tika.parsers.parser.from_file",
        return_value={"content": "tika"}
    )
    def test_text_processed(self, from_file_mock):
        uut = TikaDocumentParser("/dev/null")

        self.assertEqual(uut.get_text(), "tika")
        from_file_mock.assert_called_with(
            "/dev/null",
            'all',
            'http://tika-server:9998'
        )

    @mock.patch(MOCK_SCRATCH, SCRATCH)
    @mock.patch(
        "paperless_tika.parsers.parser.from_file",
        return_value={"content": "tika"}
    )
    def test_text_cached(self, from_file_mock):
        uut = TikaDocumentParser("/dev/null")

        self.assertIsNone(uut._text)
        uut.get_text()
        uut.get_text()
        assert from_file_mock.call_count == 1

    # TODO deduplicate from test_ocr.py
    text_cases = [
        ("simple     string", "simple string"),
        (
            "simple    newline\n   testing string",
            "simple newline\ntesting string"
        ),
        (
            "utf-8   строка с пробелами в конце  ",
            "utf-8 строка с пробелами в конце"
        )
    ]

    @mock.patch(MOCK_SCRATCH, SCRATCH)
    @mock.patch("paperless_tika.parsers.parser.from_file")
    def test_strip_excess_whitespace(self, from_file_mock):
        for source, result in self.text_cases:
            uut = TikaDocumentParser("/dev/null")
            from_file_mock.return_value = {"content": source}
            actual_result = uut.get_text()
            self.assertEqual(
                result,
                actual_result,
                "strip_exceess_whitespace({}) != '{}', but '{}'".format(
                    source,
                    result,
                    actual_result
                )
            )

    @mock.patch(MOCK_SCRATCH, SCRATCH)
    @mock.patch(
        "paperless_tika.parsers.parser.from_file",
        return_value={"content": "tika"}
    )
    def test_text_throws(self, from_file_mock):
        uut = TikaDocumentParser("/dev/null")

        from_file_mock.side_effect = ConnectionError()
        with self.assertRaises(ParseError):
            uut.get_text()
