# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.utils.deconstruct import deconstructible
from django.utils.encoding import python_2_unicode_compatible

# https://code.djangoproject.com/wiki/CookBookChoicesContantsClass
# modified to work with translation plus fields


@deconstructible
@python_2_unicode_compatible
class Constant(object):

    def __init__(self, label=None, **kwargs):
        self.constants = None
        assert(len(kwargs) == 1)
        for k, v in kwargs.items():
            self.id = k
            self.v = v
        self.label = label or self.id

    def __str__(self):
        return u"{}".format(self.v)

    def __repr__(self):
        return u"{} ({})".format(
            self.id, self.v
        )

    def __resolve_other(self, other):
        if isinstance(other, Constant):
            return other.v
        return other

    def __eq__(self, other):
        return self.v == self.__resolve_other(other)

    def __ne__(self, other):
        return self.v != self.__resolve_other(other)

    def __gt__(self, other):
        return self.v > self.__resolve_other(other)

    def __ge__(self, other):
        return self.v >= self.__resolve_other(other)

    def __lt__(self, other):
        return self.v < self.__resolve_other(other)

    def __le__(self, other):
        return self.v <= self.__resolve_other(other)

    def __hash__(self):
        if isinstance(self.v, str):
            return hash(self.v)
        return self.v

    def __getattr__(self, attr):
        """Allow dynamic lookup of equality and label."""
        if attr == u"constants":
            # https://nedbatchelder.com/blog/201010/surprising_getattr_recursion.html
            raise AttributeError(
                u"`constants` not set on Constant so cannot check equality"
            )
        if attr in self.constants.by_id:
            return self.v == self.constants.by_id[attr].v
        if attr in self.constants.groups:
            return self.id in self.constants.groups[attr].constant_ids
        else:
            raise AttributeError(
                u"'{}' object has no attribute '{}'".format(
                    self.__class__.__name__, attr
                )
            )

    def __len__(self):
        """Allow for underlying string values."""
        return len(self.v)

    def __bool__(self):
        """Evaluate all Constant instances to True."""
        return True

    __nonzero__ = __bool__


class ConstantGroup(object):

    def __init__(self, name, constant_ids):
        self.name = name
        self.constant_ids = set(constant_ids)


class Constants(object):

    def __init__(self, *args):
        self.constants = []
        self.groups = {}
        for a in args:
            if isinstance(a, Constant):
                self.constants.append(a)
                setattr(self, a.id, a)
                # add a reference to this class to the Constant instance
                setattr(a, "constants", self)
            elif isinstance(a, ConstantGroup):
                self.groups[a.name] = a
            else:
                raise ValueError(u"Received unexpected arg: {}".format(a))

        # setup useful precomputed lookups
        self.choices = [(k.v, k.label) for k in self.constants]
        self.by_value = dict([(k.v, k) for k in self.constants])
        self.by_id = dict([(k.id, k) for k in self.constants])

        # setup groups
        for name, group in self.groups.items():
            if hasattr(self, name):
                raise ValueError(
                    u"ConstantGroup with name `{}` clashes with existing attribute.".format(
                        name
                    )
                )
            setattr(self, a.name, set([self.by_id[i] for i in group.constant_ids]))
