from rest_framework.fields import Field
from rest_framework.fields import IntegerField
from django.utils import six
from django.utils.translation import ugettext_lazy as _


class ConstantChoiceField(Field):
    """
    Variant of rest_framework.fields.ChoiceField that allows us to expose and receive
    string values for our constants.
    """

    default_error_messages = {
        'invalid_choice': _('"{input}" is not a valid choice.')
    }

    def __init__(self, constants, **kwargs):
        self.choice_values_to_strings = constants.by_value
        self.choice_strings_to_values = dict([
            (k, v) for v, k in constants.by_value.items()
        ])
        self.allow_blank = kwargs.pop('allow_blank', False)
        super(ConstantChoiceField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        """ Given a string, try convert to an integer value """
        if data == '' and self.allow_blank:
            return ''
        try:
            return self.choice_strings_to_values[six.text_type(data)]
        except KeyError:
            self.fail('invalid_choice', input=data)

    def to_representation(self, value):
        """ Given a value, convert to the string representation """
        if value in ('', None):
            return value
        # if the value is not mappable in our constants file then we've mucked up and
        # removed a constant choice while leaving rows in our db with the removed
        # value. Rather than fail catastrophically, we indicate a current value of null
        # in this case
        return self.choice_values_to_strings.get(value, None)


