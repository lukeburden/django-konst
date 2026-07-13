# Django Konst

[![](https://img.shields.io/pypi/v/django-konst.svg)](https://pypi.python.org/pypi/django-konst/)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://pypi.python.org/pypi/django-konst/)
[![Test](https://github.com/lukeburden/django-konst/actions/workflows/test.yml/badge.svg)](https://github.com/lukeburden/django-konst/actions/workflows/test.yml)
[![Codecov](https://codecov.io/gh/lukeburden/django-konst/branch/master/graph/badge.svg)](https://codecov.io/gh/lukeburden/django-konst)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Deprecated

**`django-konst` is no longer actively maintained.** The core problem it solves -- named, labelled
constants with `choices` support -- is now covered by Django's own
[`models.IntegerChoices` / `models.TextChoices`](https://docs.djangoproject.com/en/stable/ref/models/fields/#enumeration-types)
(built on Python's `enum.Enum`, available since Django 3.0), so there's no need for a third-party
library for that. It's a trade-off rather than a strict replacement, though: you lose some
syntactic sugar -- `apple.purpose.cooking` and group-membership checks like `apple.purpose.culinary`
become explicit `==`/`in` checks -- in exchange for attributes that are visible to static analysis
and IDE autocomplete (see [below](#migrating-away-from-django-konst)).

**4.0.0 is the final planned release.** It exists to give existing dependents a version that works
with currently-supported Python (3.10-3.14) and Django (5.2 LTS, 6.0) before you migrate away, not
to signal ongoing feature development. See [Migrating away from django-konst](#migrating-away-from-django-konst)
below for the modern equivalent of each feature. No further releases, bug fixes, or new Django/Python
version support are planned; the repository will be archived at some point after this release.

## django-konst

`django-konst` is a utility for Django that makes the definition, use and storage of both integer and string based constants easy and readable. It avoids passing of constants
into template contexts and makes evaluation concise and readable.

It also makes exposure of these constants via forms and DRF serializers simple.

### Definition ###

Constants can be defined with friendly names, backed by either integers or text.

#### Constants ####

```python
from konst import Constant, Constants

# states backed by integers
states = Constants(
    Constant(pending=0),
    Constant(active=1),
    Constant(inactive=2)
)

# and another set of constants backed by strings
colours = Constants(
    Constant(red="FF0000"),
    Constant(green="00FF00"),
    Constant(yellow="FFFF80"),
    Constant(white="FFFFFF")
)

```

#### Constant groups ####

At times, it will be necessary to group constants and test membership within that group.
To achieve this, `django-konst` provides a `ConstantGroup` class.

```python
from konst import Constant, ConstantGroup

# states backed by integers
states = Constants(
    Constant(active=0),
    Constant(cancelled_ontime=1),
    Constant(cancelled_late=2),
    ConstantGroup(
        "cancelled",
        ("cancelled_ontime", "cancelled_late")
    )
)

```

#### Within a model ####

While not strictly necessary, it is advisable to effectively namespace your constants
by defining them in the scope of a model definition. This means you have your constants
wherever you have the model class, as well as any model instance.


```python
from django.db import models
from django.utils.translation import gettext_lazy as _

from konst import Constant, ConstantGroup, Constants
from konst.models.fields import (
    ConstantChoiceCharField,
    ConstantChoiceField
)

class Apple(models.Model):

    purposes = Constants(
        Constant(cooking=0, label=_("Cook me!")),
        Constant(eating=1, label=_("Eat me!")),
        Constant(juicing=2, label=_("Juice me!")),
        Constant(ornamental=3, label=_("Just look how pretty I am!")),
        ConstantGroup(
            "culinary", ("cooking", "eating", "juicing")
        )
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

```


### Use ###

The entire point of this library is to make the use of constants defined in this way
easy and concise.

#### In code ####

```python
apple = Apple.objects.get(name='Granny Smith')
apple.purpose.cooking
True
apple.colour.red
False
apple.colour.green
True

# we don't care about the specific purpose, just whether it is as food
# or not, so use the ConstantGroup!
apple.purpose.culinary
True

```

#### In templates ####

```
{% if apple.purpose.eating %}
    You should bite this {{ apple.name }}!
{% endif %}
```

#### With Django's ORM ####

```python
red_apples = Apple.objects.filter(colour=Apple.colours.red)
culinary_apples = Apple.objects.filter(
    purpose__in=Apple.purposes.culinary
)

```

#### Django Form ####

```python
from django import forms

from konst.forms.fields import ConstantChoiceField

class SomeForm(forms.Form):
    purpose = ConstantChoiceField(constants=Apple.purposes) 
```

#### With Django Rest Framework ####

Using the `konst.extras.drf.fields.ConstantChoiceField` serializer field with the
Django Rest Framework it is possible to both output and receive constant values.

```python
from konst.extras.drf.fields import ConstantChoiceField

from rest_framework import serializers


class AppleSerializer(serializers.ModelSerializer):

    purpose = ConstantChoiceField(Apple.purposes)
    colour = ConstantChoiceField(Apple.colours)

    class Meta:
        model = Apple
        fields = (
            "name", "purpose", "colour"
        )


# let's see how it handles bad values
serializer = AppleSerializer(
    data={
        "name": "Fuji",
        "colour": "blue",
        "purpose": "dicing"
    }
)
serializer.is_valid()
False
serializer.errors
{
    'colour': [u'"blue" is not a valid choice.'],
    'purpose': [u'"dicing" is not a valid choice.']
}


# and now how it handles some good values
serializer = AppleSerializer(
    data={
        "name": "Fuji",
        "colour": "red",
        "purpose": "eating"
    }
)
serializer.is_valid()
True


# let's create a database entry!
instance = serializer.save()


# and now our instance can be interacted with neatly
instance.colour.red
True


# finally, let's see how this looks when rendering JSON
AppleSerializer(instance=instance).data
{
    "name": "Fuji",
    "colour": "red",
    "purpose": "eating"
}

```

## Gotchas

### Setting a field on a model to the value of a constant rather than the Constant object

When the Django ORM instantiates a model instance from the database, it will ensure that any `ConstantChoiceField` or `ConstantChoiceCharField` fields have values set to `Constant` instances.

If you create or modify a model instance using a raw, hard-coded constant value, you're likely to hit errors along the lines of "AttributeError: 'int' object has no attribute 'attribute-name'".

Take the example below where the caller sets the colour of a model instance to the underlying value for the `Constant`:

```python
apple = Apple.objects.get(name='Granny Smith')
apple.purpose = 1  # constant for `eating` .. I know, who on earth would eat a granny smith straight up?!
apple.save()
```

Django will happily persist the data correctly, but let's say you have a `post_save` signal (or any other code, really) that does something further with the instance:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Apple

@receiver(post_save, sender=Apple)
def apple_updated_receiver(sender, instance, created, *args, **kwargs):
    if not created and instance.purpose.eating:
        print(f"Oh my, {instance.name} is now for eating!")

```

This code will sadly raise `AttributeError: 'int' object has no attribute 'purpose'`, as `instance.purpose` is just the integer we set it to before saving.

The good news is that you can avoid this by *always* setting `django-konst` fields on instances to `Constant` instances such that downstream code can happily handle the instance as if it'd come straight out of the database:

```python
apple = Apple.objects.get(name='Granny Smith')
apple.purpose = Apple.purposes.eating
apple.save()
```

Regardless of whether you're using `django-konst` for your constants, it's good practice to not hard-code constant values in order to avoid subtle mistakes and to ease changes in the future.


## Migrating away from django-konst

Django's built-in [`models.IntegerChoices` / `models.TextChoices`](https://docs.djangoproject.com/en/stable/ref/models/fields/#enumeration-types)
cover nearly everything below, with better IDE/type-checker support than `django-konst`'s dynamic
attribute lookups, and no third-party dependency.

On that last point specifically: `django-konst` resolves things like `Apple.purposes.cooking` and
`apple.purpose.culinary` via `__getattr__` and runtime `setattr` calls -- those attributes don't
exist until a `Constants(...)` call executes, so no static analyzer or IDE (mypy, pyright/Pylance,
PyCharm) can see them, and you get no autocomplete and no "unknown attribute" errors on typos.
`IntegerChoices`/`TextChoices` members are real, declared class attributes (`Purpose.COOKING` is
just an enum member), so every type checker and IDE understands them for free, with no plugin or
extra tooling required.

### Defining constants

```python
from django.db import models
from django.utils.translation import gettext_lazy as _

class Purpose(models.IntegerChoices):
    COOKING = 0, _("Cook me!")
    EATING = 1, _("Eat me!")
    JUICING = 2, _("Juice me!")
    ORNAMENTAL = 3, _("Just look how pretty I am!")

class Colour(models.TextChoices):
    RED = "FF0000", _("red")
    GREEN = "00FF00", _("green")
    YELLOW = "FFFF80", _("yellow")
    WHITE = "FFFFFF", _("white")
```

### Model fields

No custom field class needed — `IntegerChoices`/`TextChoices` members *are* `int`/`str` instances,
so a plain field with `choices=` does the job, and you get `get_purpose_display()` for free:

```python
class Apple(models.Model):
    purpose = models.IntegerField(choices=Purpose.choices)
    colour = models.CharField(choices=Colour.choices, max_length=6)
```

### Using constants

```python
apple.purpose == Apple.Purpose.COOKING  # rather than apple.purpose.cooking
apple.purpose = Apple.Purpose.EATING
apple.get_purpose_display()             # "Cook me!" -- Django provides this automatically
```

There's no built-in equivalent of `ConstantGroup`; a plain set (optionally as a classmethod or
module-level constant) covers it:

```python
CULINARY_PURPOSES = {Purpose.COOKING, Purpose.EATING, Purpose.JUICING}

apple.purpose in CULINARY_PURPOSES  # rather than apple.purpose.culinary
```

### Forms

Usually nothing to do — `ModelForm` generates the right field automatically from `choices=`. For a
bare (non-model) form field: `forms.TypedChoiceField(choices=Purpose.choices, coerce=Purpose)`.

### JSON serialization

Nothing to do — `IntegerChoices`/`TextChoices` members are plain `int`/`str` subclasses, so
`json.dumps()` handles them natively. `django-konst`'s custom encoder isn't needed.

### DRF: exposing the member name instead of the raw value

The one place stock DRF doesn't do quite what `konst.extras.drf.fields.ConstantChoiceField` did —
expose `"cooking"` over the API rather than the raw `0` — is exposing an enum by its *name*. DRF
doesn't ship a field for this, but it's a small enough one to own directly rather than depend on a
library for. Copy this into your own codebase and adapt as needed:

```python
from rest_framework.fields import Field

class EnumNameField(Field):
    """Expose a Django Choices enum member by its name (e.g. "cooking") rather
    than its underlying value (e.g. 0)."""

    default_error_messages = {"invalid_choice": '"{input}" is not a valid choice.'}

    def __init__(self, choices_enum, **kwargs):
        self.choices_enum = choices_enum
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.choices_enum[str(data).upper()]
        except KeyError:
            self.fail("invalid_choice", input=data)

    def to_representation(self, value):
        try:
            return self.choices_enum(value).name.lower()
        except ValueError:
            return None
```

```python
class AppleSerializer(serializers.ModelSerializer):
    purpose = EnumNameField(Purpose)
    colour = EnumNameField(Colour)

    class Meta:
        model = Apple
        fields = ("name", "purpose", "colour")
```


## Contribute

`django-konst` follows the [supported Python](https://endoflife.date/python) and [supported Django](https://www.djangoproject.com/download/) release lines, currently Python 3.10-3.14 against Django 5.2 (LTS) and 6.0. [GitHub Actions](https://github.com/lukeburden/django-konst/actions) runs the full matrix on every push and pull request, plus an allowed-to-fail job against Django's `main` branch to surface upcoming breakage early.

### Environment Setup

Tests run via [tox](https://tox.wiki/); install the Python versions listed in [tox.ini](tox.ini) with [pyenv](https://github.com/pyenv/pyenv), then:

```bash
pip install tox
tox
```

This runs the linter (`ruff`) plus the full Python/Django test matrix. To run a single environment, e.g. Python 3.13 against Django 5.2:

```bash
tox -e py313-dj52
```
