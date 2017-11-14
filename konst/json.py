# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json

from django.core.serializers.json import DjangoJSONEncoder

from konst import Constant


class ExtendedJSONEncoder(DjangoJSONEncoder):
    """Add support for serializing our class Constant."""

    def default(self, obj):
        if isinstance(obj, Constant):
            return obj.v
        else:
            return super(ExtendedJSONEncoder, self).default(obj)


def dumps(*args, **kwargs):
    kwargs["cls"] = kwargs.pop("cls", ExtendedJSONEncoder)
    return json.dumps(*args, **kwargs)


def loads(*args, **kwargs):
    return json.loads(*args, **kwargs)
