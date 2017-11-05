# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django import forms


class ConstantChoiceField(forms.ChoiceField):

    def __init__(self, constants, *args, **kwargs):
        if "choices" in kwargs:
            raise ValueError("`choices` is not supported by ConstantChoiceField. Use `constants` instead.")
        kwargs["choices"] = constants.choices
        super(ConstantChoiceField, self).__init__(
            *args, **kwargs
        )


__all__ = [ConstantChoiceField]
