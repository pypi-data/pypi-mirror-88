#!/usr/bin/env python
import os
from setuptools import find_packages, setup

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
README = open(os.path.join(ROOT_DIR, "README.md")).read()
VERSION = open(os.path.join(ROOT_DIR, "version.txt")).read()

setup(
    name="django-aid",
    version=VERSION,
    description="Helper module used in general django applications",
    long_description=README,
    long_description_content_type="text/markdown",
    author="lhy",
    author_email="dev@lhy.kr",
    license="MIT",
    packages=find_packages(exclude=["test*", "sample", "demo"]),
    install_requires=[
        "django",
        "djangorestframework",
        "drf-yasg",
    ],
    python_requires=">=3.7",
    url="https://github.com/LeeHanYeong/django-aid",
    zip_safe=True,
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
