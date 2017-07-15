import os
import re
from unittest import mock, skipIf

import pyocr
from django.test import TestCase

from ..parsers import image_to_string, strip_excess_whitespace


class TestOCR(TestCase):

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

    SAMPLE_FILES = os.path.join(os.path.dirname(__file__), "samples")
    TESSERACT_INSTALLED = bool(pyocr.get_available_tools())

    def test_strip_excess_whitespace(self):
        for source, result in self.text_cases:
            actual_result = strip_excess_whitespace(source)
            self.assertEqual(
                result,
                actual_result,
                "strip_exceess_whitespace({}) != '{}', but '{}'".format(
                    source,
                    result,
                    actual_result
                )
            )

    @skipIf(not TESSERACT_INSTALLED, "Tesseract not installed. Skipping")
    @mock.patch(
        "paperless_tesseract.parsers.RasterisedDocumentParser.SCRATCH",
        SAMPLE_FILES
    )
    def test_simple_image_with_text(self):
        self.assertIn(
            "It protects fools little children and ships named Enterprise",
            re.sub(
                "[^a-z A-Z]",
                "",
                image_to_string(("riker-ipsum.tif", "eng")).replace("\n", " ")
            )
        )
