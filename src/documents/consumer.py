from django.db import transaction
import datetime
import hashlib
import logging
import os
import re
import time
import uuid
import shutil

from operator import itemgetter
from django.conf import settings
from django.utils import timezone
from paperless.db import GnuPG

from .models import Document, FileInfo, Tag
from .parsers import ParseError
from .signals import (
    document_consumer_declaration,
    document_consumption_finished,
    document_consumption_started
)


class ConsumerError(Exception):
    pass


class Consumer:
    """
    Loop over every file found in CONSUMPTION_DIR and:
      1. Convert it to a greyscale pnm
      2. Use tesseract on the pnm
      3. Store the document in the MEDIA_ROOT with optional encryption
      4. Store the OCR'd text in the database
      5. Delete the document and image(s)
    """

    def __init__(self, consume=settings.CONSUMPTION_DIR,
                 scratch=settings.SCRATCH_DIR,
                 move=settings.CONSUMER_MOVES):

        self.logger = logging.getLogger(__name__)
        self.logging_group = None

        self._ignore = []
        self._files = []
        self.consume = consume
        self.scratch = scratch
        self.move = move

        self.processed = os.path.join(consume, "processed")
        self.ignored = os.path.join(consume, "ignored")
        self.duplicate = os.path.join(consume, "duplicate")

        """ ignore all dot-files """
        self.ABSOLUTELY_IGNORED_FILES = re.compile(r"^\.+[^\/]*$")

        os.makedirs(self.scratch, exist_ok=True)

        self.storage_type = Document.STORAGE_TYPE_UNENCRYPTED
        if settings.PASSPHRASE:
            self.storage_type = Document.STORAGE_TYPE_GPG

        if not self.consume:
            raise ConsumerError(
                "The CONSUMPTION_DIR settings variable does not appear to be "
                "set."
            )

        if not os.path.exists(self.consume):
            raise ConsumerError(
                "Consumption directory {} does not exist".format(self.consume))

        if self.move:
            os.makedirs(self.processed, exist_ok=True)
            os.makedirs(self.ignored, exist_ok=True)
            os.makedirs(self.duplicate, exist_ok=True)

        self.parsers = []
        for response in document_consumer_declaration.send(self):
            self.parsers.append(response[1])

        if not self.parsers:
            raise ConsumerError(
                "No parsers could be found, not even the default.  "
                "This is a problem."
            )

    def log(self, level, message):
        getattr(self.logger, level)(message, extra={
            "group": self.logging_group
        })

    def consume_new_files(self):
        """
        Find non-ignored files in consumption dir and consume them if they have
        been constant in size for FILES_MIN_UNMODIFIED_DURATION.
        """
        ignored_files = []
        candidate_files = []
        remaining_files = []

        for entry in os.scandir(self.consume):
            # Silently skip well-known names without warning
            if (entry.path == self.processed or
                    entry.path == self.ignored or
                    entry.path == self.duplicate):
                continue

            if not entry.is_file():
                self.logger.warning(
                    "Skipping {} as it is not a file".
                    format(entry.path))
                continue

            if self.ABSOLUTELY_IGNORED_FILES.match(entry.name):
                continue

            file = (entry.path, os.path.getmtime(entry.path),
                    os.path.getsize(entry.path))

            # skip zero length files, maybe a copy in progress
            if file[2] == 0:
                continue

            if file in self._ignore:
                ignored_files.append(file)
                if self.move:
                    self.logger.info(
                        "Moving {} to {}: file is ignored.".
                        format(entry.path, self.ignored))
                    self._safe_move(entry.path, self.ignored)
            elif file in self._files:
                # this means no changes in name, mtime and size from last check
                candidate_files.append(file)
            else:
                # file was changed or is new compared to last run
                self.logger.info("New or changing file: {}".format(entry.path))
                remaining_files.append(file)

        # Set _ignore and _files to only include files that still exist.
        # This keeps it from growing indefinitely.
        self._ignore[:] = ignored_files
        self._files[:] = remaining_files

        candidate_files.sort(key=itemgetter(1))

        for cfile in candidate_files:
            self.logger.info(
                "Candidate file: {}, {} Byte".
                format(cfile[0], cfile[2]))
            if not self.try_consume_file(cfile[0]):
                self._ignore.append(cfile)

    def try_consume_file(self, file):
        """
        Return True if file was consumed
        """

        # function is called directly via inotify watcher, so this
        # check is needed here again
        if self.ABSOLUTELY_IGNORED_FILES.match(file):
            return False

        if not re.match(FileInfo.REGEXES["title"], file):
            return False

        doc = file

        """
        We calculate the checksum for the unmodified file!
        So we can change the format while processing and
        still can detect duplicates
        """
        with open(doc, "rb") as f:
            original_checksum = hashlib.md5(f.read()).hexdigest()

        if self._is_duplicate(original_checksum):
            self.logger.info(
                "Skipping {} as it appears to be a duplicate".
                format(doc))

            if self.move:
                self.logger.info(
                    "Moving {} to {}: file is duplicate.".
                    format(doc, self.duplicate))
                self._safe_move(doc, self.duplicate)

            return False

        parser_class = self._get_parser_class(doc)
        if not parser_class:
            self.logger.error("No parsers could be found for {}".format(doc))
            return False

        self.logging_group = uuid.uuid4()

        self.logger.info("Consuming {}".format(doc))

        document_consumption_started.send(
            sender=self.__class__,
            filename=doc,
            logging_group=self.logging_group
        )

        parsed_document = parser_class(doc)

        try:
            document = self._store(
                parsed_document.get_text(),
                parsed_document.get_archive_docname(),
                parsed_document.get_optimised_thumbnail(),
                parsed_document.get_date(),
                original_checksum,
                parsed_document.get_pagecount()
            )
        except ParseError as e:
            self.logger.error("PARSE FAILURE for {}: {}".format(doc, e))
            parsed_document.cleanup()
            return False
        else:
            parsed_document.cleanup()

            self.logger.info(
                "Document {} consumption finished".
                format(document))

            document_consumption_finished.send(
                sender=self.__class__,
                document=document,
                logging_group=self.logging_group
            )

            return self._cleanup_doc(doc)

    def _get_parser_class(self, doc):
        """
        Determine the appropriate parser class based on the file
        """

        options = []
        for parser in self.parsers:
            result = parser(doc)
            if result:
                options.append(result)

        self.log(
            "info",
            "Parsers available: {}".format(
                ", ".join([str(o["parser"].__name__) for o in options])
            )
        )

        if not options:
            return None

        # Return the parser with the highest weight.
        return sorted(
            options, key=lambda _: _["weight"], reverse=True)[0]["parser"]

    @transaction.atomic
    def _store(self, text, doc, thumbnail, date, checksum, pagecount):

        file_info = FileInfo.from_path(doc)

        stats = os.stat(doc)

        self.log("debug", "Saving record to database")

        created = file_info.created or date or timezone.make_aware(
            datetime.datetime.fromtimestamp(stats.st_mtime))

        document = Document.objects.create(
            correspondent=file_info.correspondent,
            title=file_info.title,
            content=text,
            file_type=file_info.extension,
            checksum=checksum,
            created=created,
            modified=created,
            storage_type=self.storage_type,
            pages=pagecount
        )

        relevant_tags = set(list(Tag.match_all(text)) + list(file_info.tags))
        if relevant_tags:
            tag_names = ", ".join([t.slug for t in relevant_tags])
            self.log("debug", "Tagging with {}".format(tag_names))
            document.tags.add(*relevant_tags)

        document.create_source_directory()

        self._write(document, doc, document.source_path)
        self._write(document, thumbnail, document.thumbnail_path)

        document.set_filename(document.source_filename)
        document.save()

        self.log("info", "Completed")

        return document

    def _write(self, document, source, target):
        with open(source, "rb") as read_file:
            with open(target, "wb") as write_file:
                if document.storage_type == Document.STORAGE_TYPE_UNENCRYPTED:
                    write_file.write(read_file.read())
                    return
                self.log("debug", "Encrypting")
                write_file.write(GnuPG.encrypted(read_file))

    def _cleanup_doc(self, doc):
        if self.move:
            self.log(
                "debug",
                "Moving document {} to {}".
                format(doc, self.processed))
            return self._safe_move(doc, self.processed)
        else:
            self.log("debug", "Deleting document {}".format(doc))
            try:
                os.unlink(doc)
            except Exception:
                return False
            else:
                return True

    @staticmethod
    def _is_duplicate(checksum):
        return Document.objects.filter(checksum=checksum).exists()

    def _safe_move(self, src, dst):
        try:
            shutil.copy2(src, dst, follow_symlinks=False)
            os.unlink(src)
        except IOError as e:
            self.log(
                "info",
                "Unable to move file {} to {} : {}".
                format(src, dst, e))
            return False
        except PermissionError as e:
            self.log("info", "{}".format(e))
            return False
        except Exception:
            self.log("info", "Unknown error when moving file {}".format(src))
            return False
        else:
            return True
