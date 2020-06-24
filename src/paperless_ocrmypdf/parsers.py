import os
import re
import subprocess

from django.conf import settings
from PIL import Image
import ocrmypdf

import pdftotext
from documents.parsers import DocumentParser, ParseError

class OCRError(Exception):
    pass

class PdfDocumentParser(DocumentParser):
    """
    This parser uses Tesseract to try and get some text out of a rasterised
    image, whether it's a PDF, or other graphical format (JPEG, TIFF, etc.)
    """

    CONVERT = settings.CONVERT_BINARY
    GHOSTSCRIPT = settings.GS_BINARY
    DENSITY = settings.CONVERT_DENSITY if settings.CONVERT_DENSITY else 300
    THREADS = int(settings.OCR_THREADS) if settings.OCR_THREADS else None
    DEFAULT_OCR_LANGUAGE = settings.OCR_LANGUAGE
    OCR_ALWAYS = settings.OCR_ALWAYS

    def __init__(self, path):
        super().__init__(path)
        self._text = None

    def get_thumbnail(self):
        """
        The thumbnail of a PDF is just a 500px wide image of the first page.
        """

        out_path = os.path.join(self.tempdir, "convert.png")

        # Run convert to get a decent thumbnail
        try:
            run_convert(
                self.CONVERT,
                "-scale", "500x5000",
                "-alpha", "remove",
                "-strip", "-trim",
                "{}[0]".format(self.archive_path),
                out_path
            )
        except ParseError:
            # if convert fails, fall back to extracting
            # the first PDF page as a PNG using Ghostscript
            self.log(
                "warning",
                "Thumbnail generation with ImageMagick failed, "
                "falling back to Ghostscript."
            )
            gs_out_path = os.path.join(self.tempdir, "gs_out.png")
            cmd = [self.GHOSTSCRIPT,
                   "-q",
                   "-sDEVICE=pngalpha",
                   "-o", gs_out_path,
                   self.archive_path]
            if not subprocess.Popen(cmd).wait() == 0:
                raise ParseError("Thumbnail (gs) failed at {}".format(cmd))
            # then run convert on the output from gs
            run_convert(
                self.CONVERT,
                "-scale", "500x5000",
                "-alpha", "remove",
                "-strip", "-trim",
                gs_out_path,
                out_path
            )

        return out_path

    def _is_ocred(self):

        # Extract text from PDF using pdftotext
        text = get_text_from_pdf(self.archive_path)

        # We assume, that a PDF with at least 50 characters contains text
        # (so no OCR required)
        return len(text) > 50

    def get_text(self):

        if self._text is not None:
            return self._text

        if not self.OCR_ALWAYS and self._is_ocred():
            self.log("info", "Skipping OCR, using Text from PDF")
            self._text = get_text_from_pdf(self.archive_path)
            return self._text

        try:
            self._ocr(self.document_path)
            self._text = get_text_from_pdf(self.archive_path)
            return self._text
        except OCRError as e:
            raise ParseError(e)

    def _ocr(self, path):
        """
        Performs a single OCR attempt.
        """
        self.log("info", "OCRing the document")
        self.log("info", "Parsing for {}".format(self.DEFAULT_OCR_LANGUAGE))

        out_path = os.path.join(self.tempdir, "ocrmypdf.pdf")

        try:
            ocrmypdf.ocr(self.document_path, 
                         out_path,
                         language=self.DEFAULT_OCR_LANGUAGE, 
                         output_type="pdf",
                         progress_bar=False,
                         image_dpi=300)
            self.archive_path = out_path
        except OCRError as e:
            raise ParseError(e)


def run_convert(*args):

    environment = os.environ.copy()
    if settings.CONVERT_MEMORY_LIMIT:
        environment["MAGICK_MEMORY_LIMIT"] = settings.CONVERT_MEMORY_LIMIT
    if settings.CONVERT_TMPDIR:
        environment["MAGICK_TMPDIR"] = settings.CONVERT_TMPDIR

    if not subprocess.Popen(args, env=environment).wait() == 0:
        raise ParseError("Convert failed at {}".format(args))

def get_text_from_pdf(pdf_file):

    with open(pdf_file, "rb") as f:
        try:
            pdf = pdftotext.PDF(f)
        except pdftotext.Error:
            return ""

    return "\n".join(pdf)
