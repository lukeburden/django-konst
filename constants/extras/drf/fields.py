# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.utils import six
from django.utils.translation import ugettext_lazy as _

from rest_framework.fields import Field


class ConstantChoiceField(Field):
    """
    Extension of rest_framework.fields.ChoiceField.

    Allows exposure and receipt of string values from Constants.
    """

    default_error_messages = {
        "invalid_choice": _("\"{input}\" is not a valid choice.")
    }

    def __init__(self, constants, **kwargs):
        self.constants = constants
        self.allow_blank = kwargs.pop("allow_blank", False)
        super(ConstantChoiceField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        """Given a string, convert to an integer value."""
        if data == "" and self.allow_blank:
            return ""
        try:
            return self.constants.by_id[six.text_type(data)]
        except KeyError:
            self.fail("invalid_choice", input=data)

    def to_representation(self, value):
        """Given a Constant instance, convert to the string representation."""
        if value in ("", None):
            return value
        # if the value is not mappable in our Constants then we've mucked up and
        # removed a Constant choice while leaving rows in our db with the removed
        # value. Rather than fail catastrophically, we indicate a current value
        # of null
        c = self.constants.by_value.get(value)
        if c:
            return c.id
        return None
