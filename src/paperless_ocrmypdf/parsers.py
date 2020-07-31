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
        self._pagecount = None

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

    def get_text(self):

        if self._text is not None:
            return self._text
        else:
            self._do_work()
            return self._text    

    def get_pagecount(self):

        if self._pagecount is not None:
            return self._pagecount
        else:
            self._do_work()
            return self._pagecount    

    def _do_work(self):
        
        if not self.OCR_ALWAYS:
            # Extract text and infos from PDF using pdftotext
            self._extract_pdf(self.document_path)

            # We assume, that a PDF with at least 50 characters contains text
            # (so no OCR required)
            if len(self._text) > 50:
                self.log("info", "Skipping OCR, using Text from PDF")
                return

        try:
            self._ocr(self.document_path)
            self._extract_pdf(self.archive_path)
        except ParseError as e:
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
        except:
            raise ParseError("Ocrmypdf failed for {}".format(self.document_path))


    def _extract_pdf(self, path):

        with open(path, "rb") as f:
            try:
                pdf = pdftotext.PDF(f)
                text = "\n".join(pdf)
                self._pagecount = len(pdf)
            except pdftotext.Error:
                raise ParseError("pdftotext failed for {}".format(path))
        
        collapsed_spaces = re.sub(r"([^\S\r\n]+)", " ", text)
        no_leading_whitespace = re.sub(
            r"([\n\r]+)([^\S\n\r]+)", '\\1', collapsed_spaces)
        no_trailing_whitespace = re.sub(
            r"([^\S\n\r]+)$", '', no_leading_whitespace)

        self._text = no_trailing_whitespace


def run_convert(*args):

    environment = os.environ.copy()
    if settings.CONVERT_MEMORY_LIMIT:
        environment["MAGICK_MEMORY_LIMIT"] = settings.CONVERT_MEMORY_LIMIT
    if settings.CONVERT_TMPDIR:
        environment["MAGICK_TMPDIR"] = settings.CONVERT_TMPDIR

    if not subprocess.Popen(args, env=environment).wait() == 0:
        raise ParseError("Convert failed at {}".format(args))

