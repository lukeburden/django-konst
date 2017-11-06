# Django Constants

[![](https://img.shields.io/pypi/v/django-constants.svg)](https://pypi.python.org/pypi/django-constants/)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://pypi.python.org/pypi/django-constants/)

[![Codecov](https://img.shields.io/codecov/c/github/lukeburden/django-constants.svg)](https://codecov.io/gh/lukeburden/django-constants)
[![CircleCI](https://circleci.com/gh/lukeburden/django-constants.svg?style=svg)](https://circleci.com/gh/lukeburden/django-constants)
![](https://img.shields.io/github/contributors/lukeburden/django-constants.svg)
![](https://img.shields.io/github/issues-pr/lukeburden/django-constants.svg)
![](https://img.shields.io/github/issues-pr-closed/lukeburden/django-constants.svg)


## django-constants

`django-constants` is a utility for Django that makes the definition, use and storage of both integer and string based constants easy and readable. It avoids passing of constants
into template contexts and makes evaluation concise and readable.

It also makes exposure of these constants via forms and DRF serializers simple.

### Definition ###

Constants can be defined with friendly names, backed by either integers or text.

#### Constants ####

```python
from constants.constants import Constant

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
To achieve this, `django-constants` provides a `ConstantGroup` class.

```python
from constants.constants import Constant, ConstantGroup

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
from django.utils.translation import ugettext_lazy as _

from constants.constants import Constant, ConstantGroup, Constants
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
apple.purpose.cooking == True
True
apple.colour.red == True
True
apple.colour.green == True
False

# we don't care about the specific purpose, just whether it is as food
# or not, so use the ConstantGroup!
apple.purpose.culinary == True
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

#### With Django Rest Framework ####

Coming soon.

## Contribute

`django-constants` supports a variety of Python and Django versions. It's best if you test each one of these before committing. Our [Circle CI Integration](https://circleci.com will test these when you push but knowing before you commit prevents from having to do a lot of extra commits to get the build to pass.

### Environment Setup

In order to easily test on all these Pythons and run the exact same thing that Travis CI will execute you'll want to setup [pyenv](https://github.com/yyuu/pyenv) and install the Python versions outlined in [tox.ini](tox.ini).

If you are on the Mac, it's recommended you use [brew](http://brew.sh/). After installing `brew` run:

```
$ brew install pyenv pyenv-virtualenv pyenv-virtualenvwrapper
```

Then:

```
pyenv install -s 2.7.14
pyenv install -s 3.4.7
pyenv install -s 3.5.4
pyenv install -s 3.6.3
pyenv virtualenv 2.7.14
pyenv virtualenv 3.4.7
pyenv virtualenv 3.5.4
pyenv virtualenv 3.6.3
pyenv global 2.7.14 3.4.7 3.5.4 3.6.3
pip install detox
```

To run test suite:

Make sure you are NOT inside a `virtualenv` and then:

```
$ detox
```

This will execute the testing matrix in parallel as defined in the `tox.ini`.
