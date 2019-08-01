from setuptools import find_packages
from setuptools import setup


NAME = "django-konst"
DESCRIPTION = "Convenient constants fields for Django"
AUTHOR = "Luke Burden"
AUTHOR_EMAIL = "lukeburden@gmail.com"
URL = "https://github.com/lukeburden/django-konst"
LONG_DESCRIPTION = """
============
Django Constants
============
.. image:: https://img.shields.io/travis/lukeburden/django-konst.svg
    :target: https://travis-ci.org/lukeburden/django-konst
.. image:: https://img.shields.io/codecov/c/github/lukeburden/django-konst.svg
    :target: https://codecov.io/gh/lukeburden/django-konst
.. image:: https://img.shields.io/pypi/dm/django-konst.svg
    :target:  https://pypi.python.org/pypi/django-konst/
.. image:: https://img.shields.io/pypi/v/django-konst.svg
    :target:  https://pypi.python.org/pypi/django-konst/
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target:  https://pypi.python.org/pypi/django-konst/

This app provides convenient constants fields to improve readability
and consistency of code and templates.
"""

tests_require = ["pytest", "pytest-django", "djangorestframework>=3.4.7"]

setup(
    name=NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    version="1.0.1",
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
        "django>=1.8"
    ],
    test_suite="runtests.runtests",
    tests_require=tests_require,
    zip_safe=False,
)
