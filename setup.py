##############################################################################
#    Copyright (c) 2009 Novell, All rights reserved.
#    Portions copyright 2009 Massachusetts Institute of Technology,
#    All rights reserved.
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 2.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
##############################################################################

from setuptools import setup


version = "9.0.0.dev0"

setup(
    name="collective.searchandreplace",
    version=version,
    description="Batch Search and Replace",
    long_description=(open("README.rst").read() + "\n" + open("CHANGES.rst").read()),
    # Get more strings from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: Addon",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="batch search replace",
    author="enPraxis",
    author_email="info@enpraxis.net",
    maintainer="Maurits van Rees",
    maintainer_email="m.van.rees@zestsoftware.nl",
    url="https://github.com/collective/collective.searchandreplace",
    license="GPL",
    # src layout; native (PEP 420) namespace, so no collective/__init__.py.
    # setuptools discovers the packages under src/ (plone.meta switch-to-pep420).
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "Acquisition",
        "plone.api",
        "plone.app.registry",
        "plone.app.textfield",
        "plone.autoform",
        "plone.base",
        "plone.dexterity",
        "plone.registry",
        "plone.resource",
        "plone.z3cform",
        "Products.CMFCore",
        "Products.CMFPlone>=6.2",
        "Products.GenericSetup",
        "Products.statusmessages",
        "Zope",
        "z3c.form",
        "zope.component",
        "zope.contentprovider",
        "zope.i18n",
        "zope.i18nmessageid",
        "zope.interface",
        "zope.publisher",
        "zope.schema",
    ],
    extras_require=dict(
        test=[
            "plone.app.contenttypes",
            "plone.app.testing",
            "plone.testing",
            "pytest",
            "zope.pytestlayer",
        ],
    ),
    entry_points="""
    [plone.autoinclude.plugin]
    target = plone
    module = collective.searchandreplace
    """,
)
