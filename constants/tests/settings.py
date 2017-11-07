# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

import django

DEBUG = True
USE_TZ = True
TIME_ZONE = "UTC"
DATABASES = {
    "default": {
        "ENGINE": os.environ.get(
            "CONSTANTS_DATABASE_ENGINE", "django.db.backends.sqlite3"
        ),
        "HOST": os.environ.get("CONSTANTS_DATABASE_HOST", "127.0.0.1"),
        "NAME": os.environ.get("CONSTANTS_DATABASE_NAME", "constants"),
        "USER": os.environ.get("CONSTANTS_DATABASE_USER", ""),
    }
}
MIDDLEWARE = []  # from 2.0 onwards, only MIDDLEWARE is used

if django.VERSION < (1, 10):
    MIDDLEWARE_CLASSES = MIDDLEWARE
ROOT_URLCONF = "constants.tests.urls"
INSTALLED_APPS = [
    "constants",
    "constants.tests",
    "rest_framework"
]
SITE_ID = 1

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [
        "constants/tests/templates"
    ],
    "APP_DIRS": True,
    "OPTIONS": {
        "debug": True,
        "context_processors": [
            "django.contrib.auth.context_processors.auth",
            "django.template.context_processors.debug",
            "django.template.context_processors.i18n",
            "django.template.context_processors.media",
            "django.template.context_processors.static",
            "django.template.context_processors.tz",
            "django.template.context_processors.request",
        ],
    },
}]
SECRET_KEY = "constants-secret-key"
