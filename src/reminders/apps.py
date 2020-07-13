from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class RemindersConfig(AppConfig):
    name = "reminders"
    verbose_name = _(name)
    
