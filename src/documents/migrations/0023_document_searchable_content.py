# Generated by Django 2.0.13 on 2019-05-30 14:50
import unicodedata

from django.db import migrations, models


def slugifyOCR(content):
    return (
        unicodedata.normalize("NFKD", content.casefold())
        .encode("ASCII", "ignore")
        .decode("utf-8")
    )


class Migration(migrations.Migration):
    dependencies = [("documents", "0022_auto_20181007_1420")]

    reversible = True

    def casefold_forwards(apps, schema_editor):
        Document = apps.get_model("documents", "Document")
        for doc in Document.objects.all():
            if doc.title is not None:
                doc.searchable_title = slugifyOCR(doc.title)
            if doc.content is not None:
                doc.searchable_content = slugifyOCR(doc.content)
            doc.save()

        Tag = apps.get_model("documents", "Tag")

        for tag in Tag.objects.all():
            tag.searchable_name = slugifyOCR(tag.name)
            tag.save()

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        migrations.RemoveField(model_name="document", name="searchable_content"),
        migrations.RemoveField(model_name="document", name="searchable_title"),
        migrations.RemoveField(model_name="tag", name="searchable_name"),

    operations = [
        migrations.AddField(
            model_name="document",
            name="searchable_content",
            field=models.TextField(blank=True, db_index=True, editable=False),
        ),
        migrations.AddField(
            model_name="document",
            name="searchable_title",
            field=models.CharField(
                max_length=128, blank=True, db_index=True, editable=False
            ),
        ),
        migrations.AddField(
            model_name="tag",
            name="searchable_name",
            field=models.CharField(
                max_length=128, blank=True, db_index=True, editable=False
            ),
        ),
        migrations.RunPython(casefold_forwards, migrations.RunPython.noop),
    ]
