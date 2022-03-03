from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="django_partial_datetime",
    version="1.0.1",
    description="Django custom model field for partial datetimes with the form YYYY, YYYY-MM, YYYY-MM-DD, YYYY-MM-DD HH(?) and YYYY-MM-DD HH:mm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ktowen/django_partial_date",
    author="jamesbisese",
    author_email="jimmy@jimmyandjanie.com",
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Experimenting",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    keywords=["fields", "django", "dates", "datetimes", "partial"],
    packages=["partial_datetime"],
    install_requires=["six", "django"],
)
