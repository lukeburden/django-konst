# -*- coding: utf-8 -*-
from __future__ import absolute_import

import copy
import pickle
import sys

from django.core.management import call_command
from django.test import TestCase
from django.utils.encoding import force_text

from rest_framework import serializers

from konst import Constant, ConstantGroup, Constants, json
from konst.extras.drf.fields import ConstantChoiceField as DRFConstantChoiceField
from konst.tests.models import Apple


try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class ConstantTestCase(TestCase):
    def test_repr(self):
        self.assertEqual(repr(Apple.purposes.cooking), u"cooking (0)")
        self.assertEqual(repr(Apple.colours.red), u"red (FF0000)")

    def test_str(self):
        self.assertEqual(str(Apple.purposes.cooking), u"0")
        self.assertEqual(str(Apple.colours.red), u"FF0000")

    def test_comparison_with_int(self):
        self.assertEqual(Apple.purposes.cooking, 0)
        self.assertNotEqual(Apple.purposes.cooking, 1)

    def test_comparison_with_char(self):
        self.assertEqual(Apple.colours.red, u"FF0000")
        self.assertNotEqual(Apple.colours.red, u"FF0001")

    def test_comparison_with_constant(self):
        self.assertEqual(Apple.purposes.cooking, Apple.purposes.cooking)
        self.assertNotEqual(Apple.purposes.cooking, Apple.purposes.eating)
        self.assertEqual(Apple.colours.red, Apple.colours.red)
        self.assertNotEqual(Apple.colours.red, Apple.colours.green)

    def test_constant_in_group(self):
        self.assertEqual(
            Apple.purposes.culinary,
            set(
                [Apple.purposes.eating, Apple.purposes.cooking, Apple.purposes.juicing]
            ),
        )

    def test_two_groups_defined(self):
        pets = Constants(
            Constant(husky="husky"),
            Constant(poodle="poodle"),
            Constant(burmese="burmese"),
            Constant(ginger="ginger"),
            ConstantGroup("cat", ("burmese", "ginger")),
            ConstantGroup("dog", ("husky", "poodle")),
        )
        self.assertTrue(pets.husky.dog)
        self.assertFalse(pets.husky.cat)
        self.assertTrue(pets.poodle.dog)
        self.assertFalse(pets.poodle.cat)
        self.assertTrue(pets.burmese.cat)
        self.assertFalse(pets.burmese.dog)
        self.assertTrue(pets.ginger.cat)
        self.assertFalse(pets.ginger.dog)
        self.assertEqual(pets.dog, set([pets.husky, pets.poodle]))
        self.assertEqual(pets.cat, set([pets.burmese, pets.ginger]))


class ConstantChoiceFieldTestCase(TestCase):

    fixtures = ["test_apples"]

    def setUp(self):
        self.instance = Apple.objects.first()

    def test_create_and_save(self):
        gala = Apple.objects.create(
            name=u"Gala", colour=Apple.colours.red, purpose=Apple.purposes.eating
        )
        self.assertTrue(isinstance(gala.colour, Constant))
        self.assertTrue(isinstance(gala.purpose, Constant))
        self.assertEqual(gala.colour, Apple.colours.red)
        self.assertTrue(gala.colour.red)

    def test_from_db(self):
        instance = Apple.objects.all().first()
        self.assertTrue(isinstance(instance.colour, Constant))
        self.assertTrue(isinstance(instance.purpose, Constant))
        self.assertTrue(instance.colour.green)
        self.assertTrue(instance.purpose.cooking)

    def test_widget_force_text(self):
        self.assertEqual(
            force_text(self.instance.colour), u"{}".format(self.instance.colour.v)
        )
        self.assertEqual(
            force_text(self.instance.purpose), u"{}".format(self.instance.purpose.v)
        )

    def test_getattr_equality_check(self):
        self.assertTrue(self.instance.colour.green)
        self.assertFalse(self.instance.colour.red)
        self.assertTrue(self.instance.purpose.cooking)
        self.assertFalse(self.instance.purpose.eating)

    def test_getattr_equality_check_missing_attr(self):
        with self.assertRaises(AttributeError):
            self.instance.colour.donkey
        with self.assertRaises(AttributeError):
            self.instance.purposes.donkey

    def test_loaddata(self):
        # if the grannysmith exists we"re good
        # as the tests have already loaded the fixture
        instance = Apple.objects.all().first()
        self.assertEqual(instance.name, u"Granny Smith")
        self.assertTrue(instance.colour.green)
        self.assertTrue(instance.purpose.cooking)

    def test_dumpdata(self):
        """Dump our users, load as JSON and inspect."""
        sysout = sys.stdout
        sys.stdout = StringIO()
        call_command("dumpdata", "tests.apple")
        dumped_data = json.loads(sys.stdout.getvalue())
        sys.stdout = sysout
        self.assertEqual(
            dumped_data[0]["fields"]["colour"], u"{}".format(Apple.colours.green)
        )

    def test_copy(self):
        # https://nedbatchelder.com/blog/201010/surprising_getattr_recursion.html
        def f(*args, **kw):
            pass

        sys.settrace(f)
        self.assertEqual(sys.gettrace(), f)
        colour = Apple.colours.red
        self.assertTrue(colour.red)
        self.assertFalse(colour.green)
        colour_2 = copy.copy(colour)
        self.assertNotEqual(sys.gettrace(), None)
        self.assertTrue(colour_2.red)
        self.assertFalse(colour_2.green)

    def test_pickle(self):
        # very similar to the test_copy above
        c = pickle.dumps(Apple.colours.red)
        try:
            colour = pickle.loads(c)
        except RuntimeError as r:
            self.fail("Loading pickled constant raised RuntimeError: {}".format(r))
        else:
            self.assertTrue(colour.red)
            self.assertFalse(colour.green)

    def test_group_in_filter(self):
        self.assertEqual(
            Apple.objects.filter(purpose__in=Apple.purposes.culinary).count(), 1
        )
        instance = Apple.objects.filter(purpose__in=Apple.purposes.culinary).first()
        self.assertEqual(self.instance, instance)
        self.assertTrue(instance.purpose.culinary)


class ConstantJSONSerializerTestCase(TestCase):

    # Can"t make it serializable by default .. use our custom encoder
    def test_json_serializable(self):
        data = {
            # "colour": Apple.colours.red,
            "purpose": Apple.purposes.cooking
        }
        self.assertEqual(json.loads(json.dumps(data)), data)


class AppleSerializer(serializers.ModelSerializer):

    purpose = DRFConstantChoiceField(Apple.purposes)
    colour = DRFConstantChoiceField(Apple.colours)

    class Meta:
        model = Apple
        fields = ("name", "purpose", "colour")


class DRFConstantChoiceFieldTestCase(TestCase):

    fixtures = ["test_apples"]

    def setUp(self):
        self.purposes = DRFConstantChoiceField(Apple.purposes)
        self.colours = DRFConstantChoiceField(Apple.colours)

    def test_to_representation_int_backed(self):
        self.assertEqual(
            self.purposes.to_representation(Apple.purposes.cooking), u"cooking"
        )

    def test_to_representation_string_backed(self):
        self.assertEqual(
            self.colours.to_representation(Apple.colours.yellow), u"yellow"
        )

    def test_to_internal_value_int_backed(self):
        self.assertEqual(
            self.purposes.to_internal_value("eating"), Apple.purposes.eating
        )

    def test_to_internal_value_string_backed(self):
        self.assertEqual(self.colours.to_internal_value("red"), Apple.colours.red)

    def test_to_internal_value_not_a_valid_option_int_backed(self):
        with self.assertRaises(serializers.ValidationError) as e:
            self.colours.to_internal_value("purple")
        self.assertEqual(e.exception.detail, [u'"purple" is not a valid choice.'])

    def test_to_internal_value_not_a_valid_option_string_backed(self):
        with self.assertRaises(serializers.ValidationError) as e:
            self.purposes.to_internal_value("mincing")
        self.assertEqual(e.exception.detail, [u'"mincing" is not a valid choice.'])

    def test_in_serializer_output(self):
        instance = Apple.objects.all().first()
        serializer = AppleSerializer(instance=instance)
        self.assertEqual(
            serializer.data,
            {"name": "Granny Smith", "colour": "green", "purpose": "cooking"},
        )

    def test_in_serializer_input_bad(self):
        data = {"name": "Fuji", "colour": "blue", "purpose": "dicing"}
        serializer = AppleSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors,
            {
                "colour": [u'"blue" is not a valid choice.'],
                "purpose": [u'"dicing" is not a valid choice.'],
            },
        )

    def test_in_serializer_input_good(self):
        data = {"name": "Fuji", "colour": "red", "purpose": "eating"}
        serializer = AppleSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertTrue(instance.colour.red)
        self.assertTrue(instance.purpose.eating)
        self.assertTrue(instance.purpose.culinary)
