# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from constants.constants import Constant, Constants
from constants.models.fields import (
    ConstantChoiceCharField,
    ConstantChoiceField
)


class Apple(models.Model):

    purposes = Constants(
        Constant(cooking=0, label=_("Cook me!")),
        Constant(eating=1, label=_("Eat me!")),
        Constant(juicing=2, label=_("Juice me!")),
        Constant(ornamental=3, label=_("Just look how pretty I am!")),
        # ConstantGroup(
        #     name="culinary", includes=("cooking", "eating", "juicing")
        # )
    )
    colours = Constants(
        Constant(red="FF0000", label=_("red")),
        Constant(green="00FF00", label=_("green")),
        Constant(yellow="FFFF80", label=_("yellow")),
        Constant(white="FFFFFF", label=_("white")),
    )

    name = models.CharField(max_length=30)
    purpose = ConstantChoiceField(constants=purposes)
    colour = ConstantChoiceCharField(constants=colours, max_length=30)
