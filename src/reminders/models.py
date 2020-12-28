from django.db import models
from django.utils.translation import ugettext_lazy as _


class Reminder(models.Model):

    document = models.ForeignKey(
        "documents.Document",
        on_delete=models.PROTECT,
        verbose_name=_('document')
    )

    date = models.DateTimeField(
        verbose_name=_('datetime')
    )

    note = models.TextField(
        blank=True,
        verbose_name=_('note')
    )

    class Meta:
        verbose_name = _('reminder')
        verbose_name_plural = _('reminders')
