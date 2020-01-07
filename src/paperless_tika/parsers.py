import os
import subprocess
from requests.exceptions import ConnectionError

import tika
from tika import parser
from django.conf import settings

from documents.parsers import DocumentParser, ParseError
from paperless_tesseract.parsers import strip_excess_whitespace


class TikaDocumentParser(DocumentParser):
    """
    This parser uses Apache Tika to try and get some text out of
    """

    CONVERT = settings.CONVERT_BINARY

    def __init__(self, path):
        super().__init__(path)
        self._text = None

    def get_thumbnail(self):
        """
        The thumbnail of a text file is just a 500px wide image of the text
        rendered onto a letter-sized page.
        """
        # The below is heavily cribbed from https://askubuntu.com/a/590951

        bg_color = "white"  # bg color
        text_color = "black"  # text color
        psize = [500, 647]  # icon size
        n_lines = 50  # number of lines to show
        out_path = os.path.join(self.tempdir, "convert.png")

        temp_bg = os.path.join(self.tempdir, "bg.png")
        temp_txlayer = os.path.join(self.tempdir, "tx.png")
        picsize = "x".join([str(n) for n in psize])
        txsize = "x".join([str(n - 8) for n in psize])

        def create_bg():
            work_size = ",".join([str(n - 1) for n in psize])
            r = str(round(psize[0] / 10))
            rounded = ",".join([r, r])
            run_command(
                self.CONVERT,
                "-size ", picsize,
                ' xc:none -draw ',
                '"fill ', bg_color, ' roundrectangle 0,0,', work_size, ",", rounded, '" ',  # NOQA: E501
                temp_bg
            )

        def read_text():
            return self.get_text()

        def create_txlayer():
            run_command(
                self.CONVERT,
                "-background none",
                "-fill",
                text_color,
                "-pointsize", "12",
                "-border 4 -bordercolor none",
                "-size ", txsize,
                ' caption:"', read_text(), '" ',
                temp_txlayer
            )

        create_txlayer()
        create_bg()
        run_command(
            self.CONVERT,
            temp_bg,
            temp_txlayer,
            "-background None -layers merge ",
            out_path
        )

        return out_path

    def get_text(self):

        if self._text is not None:
            return self._text

        try:
            # Workaround for tika-python#273
            result = parser.from_file(
                self.document_path,
                "all",
                "http://tika-server:9998"
            )
            # Strip out excess white space to allow matching to go smoother
            self._text = strip_excess_whitespace(result["content"])
            return self._text
        except ConnectionError as e:
            raise ParseError(e)


def run_command(*args):
    environment = os.environ.copy()
    if settings.CONVERT_MEMORY_LIMIT:
        environment["MAGICK_MEMORY_LIMIT"] = settings.CONVERT_MEMORY_LIMIT
    if settings.CONVERT_TMPDIR:
        environment["MAGICK_TMPDIR"] = settings.CONVERT_TMPDIR

    if not subprocess.Popen(' '.join(args), env=environment,
                            shell=True).wait() == 0:
        raise ParseError("Convert failed at {}".format(args))
