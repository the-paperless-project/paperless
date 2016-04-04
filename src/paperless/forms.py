from django.contrib.auth.forms import AuthenticationForm
from django.forms.utils import ErrorList
from django.forms.widgets import (
    CheckboxInput, RadioSelect, CheckboxSelectMultiple)
from django.utils.safestring import mark_safe


class BootstrapErrorList(ErrorList):

    def __unicode__(self):
        return self.as_bs()

    def as_ul(self):
        if not self:
            return ""
        return mark_safe("".join(
            ['<div class="alert alert-danger">%s</div>' % e for e in self]
        ))


class BootstrapMixin(object):

    def __init__(self, star_required=True):

        self.error_class = BootstrapErrorList

        skip = (CheckboxInput, RadioSelect, CheckboxSelectMultiple)

        for field_name in self.fields.keys():

            if isinstance(self.fields[field_name].widget, skip):
                continue

            properties = {"class": "form-control"}

            self.fields[field_name].widget.attrs.update(properties)

            # Required fields
            if self.fields[field_name].required:
                self.fields[field_name].widget.attrs.update(
                    {"required": "required"})
                if star_required and self.fields[field_name].label:
                    self.fields[field_name].label += "*"


class BootstrappedAuthenticationForm(BootstrapMixin, AuthenticationForm):

    def __init__(self, *args, **kwargs):

        AuthenticationForm.__init__(self, *args, **kwargs)
        BootstrapMixin.__init__(self)
