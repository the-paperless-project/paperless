import os
import subprocess
import gnupg

from django.conf import settings
from django.db import migrations, models

class GnuPG(object):
    """
    A handy singleton to use when handling encrypted files.
    """

    gpg = gnupg.GPG(gnupghome=settings.GNUPG_HOME)

    @classmethod
    def decrypted(cls, file_handle):
        return cls.gpg.decrypt_file(
            file_handle, passphrase=settings.PASSPHRASE).data

    @classmethod
    def encrypted(cls, file_handle):
        return cls.gpg.encrypt_file(
            file_handle,
            recipients=None,
            passphrase=settings.PASSPHRASE,
            symmetric=True
        ).data

def create_jpg_thumbnails(apps, schema_editor):
    thumb_files = os.listdir(os.path.join(settings.MEDIA_ROOT, "documents", "thumbnails"))

    for thumb in thumb_files:
        if thumb.endswith(".jpg") or thumb.endswith(".jpg.gpg"):
            continue
        new_thumb = thumb[:-4] + ".jpg"
        if thumb.endswith(".png"):            
            convert_png_to_jpg(thumb, new_thumb)
            os.remove(thumb)
        if thumb.endswith(".png.gpg"):
            thumb_decrypted = thumb[:-4]
            with open(thumb, "rb") as encrypted:
                with open(thumb_decrypted, "wb") as unencrypted:
                    unencrypted.write(GnuPG.decrypted(encrypted))
            convert_png_to_jpg(thumb_decrypted, new_thumb)
            new_thumb_encrypted = new_thumb + ".gpg"
            with open(new_thumb, "rb") as unencrypted:
                with open(new_thumb_encrypted, "wb") as encrypted:
                    encrypted.write(GnuPG.decrypted(unencrypted))
            os.remove(thumb)
            os.remove(thumb_decrypted)
            os.remove(new_thumb)


def convert_png_to_jpg(png_path, jpg_path):
    subprocess.Popen((
        settings.CONVERT_BINARY,
        "-scale", "500x5000",
        "-alpha", "remove",
        "-strip", "-trim",
        png_path,
        jpg_path
    )).wait()


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0022_auto_20181007_1420'),
    ]

    operations = [
        migrations.RunPython(create_jpg_thumbnails),
    ]