from setuptools import find_packages
from setuptools import setup


NAME = "django-constants"
DESCRIPTION = "Convenient constants fields for Django"
AUTHOR = "Luke Burden"
AUTHOR_EMAIL = "lukeburden@gmail.com"
URL = "https://github.com/lukeburden/django-constants"
LONG_DESCRIPTION = """
============
Django Constants
============
.. image:: https://img.shields.io/travis/lukeburden/django-constants.svg
    :target: https://travis-ci.org/lukeburden/django-constants
.. image:: https://img.shields.io/codecov/c/github/lukeburden/django-constants.svg
    :target: https://codecov.io/gh/lukeburden/django-constants
.. image:: https://img.shields.io/pypi/dm/django-constants.svg
    :target:  https://pypi.python.org/pypi/django-constants/
.. image:: https://img.shields.io/pypi/v/django-constants.svg
    :target:  https://pypi.python.org/pypi/django-constants/
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target:  https://pypi.python.org/pypi/django-constants/

This app provides convenient constants fields to improve readability
and consistency of code and templates.
"""

tests_require = [
    "mock",
]

setup(
    name=NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    version="1.0.0",
    license="MIT",
    url=URL,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Framework :: Django",
    ],
    install_requires=[
        "django-appconf>=1.0.1",
        "django>=1.8",
        "six"
    ],
    extras_require={
        "pytest": ["pytest", "pytest-django"] + tests_require,
    },
    test_suite="runtests.runtests",
    tests_require=tests_require,
    zip_safe=False,
)
