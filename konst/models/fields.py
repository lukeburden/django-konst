# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.db.models import CharField, PositiveSmallIntegerField

from .. import Constant


class ConstantChoiceFieldMixin(object):
    def __init__(self, *args, **kwargs):
        self.constants = kwargs.pop("constants", None)
        if self.constants:
            kwargs["choices"] = self.constants.choices
        super(ConstantChoiceFieldMixin, self).__init__(*args, **kwargs)

    def to_python(self, value):
        # print "to_python: {}: {}".format(type(value), value)
        if value is None:
            return value
        if isinstance(value, Constant):
            return value
        return self.constants.by_value.get(int(value))

    def get_prep_value(self, value):
        # print "get_prep_value: {}: {}".format(type(value), value)
        if isinstance(value, Constant):
            return value.v
        return value

    def from_db_value(self, value, expression, connection):
        # print "from_db_value: {}: {}".format(type(value), value)
        if value is None:
            return value
        # in some circumstances the field is loaded without constants
        if self.constants is None:
            return value
        return self.constants.by_value.get(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        value = super(ConstantChoiceFieldMixin, self).get_db_prep_value(
            value, connection, prepared
        )
        # print "get_db_prep_value: {}: {}".format(type(value), value)
        if value is None:
            return None
        elif isinstance(value, Constant):
            return value.v
        else:
            return value


class ConstantChoiceField(ConstantChoiceFieldMixin, PositiveSmallIntegerField):
    pass


class ConstantChoiceCharField(ConstantChoiceFieldMixin, CharField):
    def to_python(self, value):
        # print "to_python: {}: {}".format(type(value), value)
        if value is None:
            return value
        if isinstance(value, Constant):
            return value
        return self.constants.by_value.get(u"{}".format(value))


__all__ = [ConstantChoiceField, ConstantChoiceCharField]
