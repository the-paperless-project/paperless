#!/usr/bin/env python3
import os
import sys
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paperless.settings")

    from django.conf import settings
    from django.core.management import execute_from_command_line

    # The runserver and consumer need to have access to the passphrase, so it
    # must be entered at start time to keep it safe.
    if "runserver" in sys.argv or "document_consumer" in sys.argv:
        if not settings.PASSPHRASE:
            settings.PASSPHRASE = input(
                "settings.PASSPHRASE is unset.  Input passphrase: ")

    execute_from_command_line(sys.argv)
