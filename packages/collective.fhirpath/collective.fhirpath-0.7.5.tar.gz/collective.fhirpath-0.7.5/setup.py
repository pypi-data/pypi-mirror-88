# -*- coding: utf-8 -*-
"""Installer for the collective.fhirpath package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("RESTAPI.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)

install_requires = [
    "setuptools",
    # -*- Extra requirements: -*-
    "z3c.jbot",
    "plone.restapi",
    "plone.app.dexterity",
    "collective.elasticsearch>=3.0.4",
    "plone.app.fhirfield>=4.2.0,<5.0.0",
    "fhirpath>=0.10.5",
    "fhir.resources[orjson]>=6.0.0"
]

test_requires = [
    "plone.app.testing",
    "plone.app.contenttypes",
    "plone.app.robotframework[debug]",
    "collective.MockMailHost"
]

docs_requirements = [
    "sphinx",
    "sphinx-rtd-theme",
    "sphinxcontrib-httpdomain",
    "sphinxcontrib-httpexample",
]


setup(
    name="collective.fhirpath",
    version="0.7.5",
    description="Plone powered provider for fhirpath",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Development Status :: 4 - Beta",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 5.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone FHIR Healthcare HL7",
    author="Md Nazrul Islam",
    author_email="email2nazru@gmail.com",
    url="https://github.com/nazrulworld/collective.fhirpath",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/collective.fhirpath",
        "Source": "https://github.com/nazrulworld/collective.fhirpath",
        "Tracker": "https://github.com/nazrulworld/collective.fhirpath/issues",
        'Documentation': 'https://collective-fhirpath.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require={
        "test": test_requires + docs_requirements,
        "docs": docs_requirements,
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = collective.fhirpath.locales.update:update_locale
    """,
)
