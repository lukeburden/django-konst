from setuptools import find_packages
from setuptools import setup


name = "django-konst"
description = "Convenient constants fields for Django"
author = "Luke Burden"
author_email = "lukeburden@gmail.com"
url = "https://github.com/lukeburden/django-konst"

with open("README.md", "r") as fh:
    long_description = fh.read()

tests_require = ["pytest", "pytest-django", "djangorestframework>=3.4.7"]

setup(
    name=name,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="1.0.1",
    license="MIT",
    url=url,
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
    install_requires=["django>=1.8"],
    test_suite="runtests.runtests",
    tests_require=tests_require,
    zip_safe=False,
)
