# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from constants.constants import Constant, Constants
from constants.models.fields import (
    ConstantChoiceCharField,
    ConstantChoiceField
)


class Fruit(models.Model):

    colours = Constants(
        Constant(red="FF0000", label=_("red")),
        Constant(green="00FF00", label=_("green")),
        Constant(yellow="FFFF80", label=_("yellow")),
        Constant(white="FFFFFF", label=_("white")),
    )

    purposes = Constants(
        Constant(cooking=0, label=_("Cook me!")),
        Constant(eating=1, label=_("Eat me!")),
        Constant(juicing=2, label=_("Juice me!")),
        Constant(ornamental=3, label=_("Just look how pretty I am!")),
        # ConstantGroup(
        #     name="culinary", includes=("cooking", "eating", "juicing")
        # )
    )

    name = models.CharField(max_length=30)
    colour = ConstantChoiceField(constants=colours)
    purpose = ConstantChoiceCharField(constants=purposes)
