.. image:: https://img.shields.io/pypi/status/plone.app.fhirfield.svg
    :target: https://pypi.python.org/pypi/plone.app.fhirfield/
    :alt: Egg Status

.. image:: https://img.shields.io/travis/nazrulworld/collective.fhirpath/master.svg
    :target: http://travis-ci.org/nazrulworld/collective.fhirpath
    :alt: Travis Build Status

.. image:: https://coveralls.io/repos/github/nazrulworld/collective.fhirpath/badge.svg?branch=master
    :target: https://coveralls.io/github/nazrulworld/collective.fhirpath?branch=master
    :alt: Test Coverage

.. image:: https://img.shields.io/pypi/pyversions/collective.fhirpath.svg
    :target: https://pypi.python.org/pypi/collective.fhirpath/
    :alt: Python Versions

.. image:: https://img.shields.io/pypi/v/collective.fhirpath.svg
    :target: https://pypi.python.org/pypi/collective.fhirpath/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/l/collective.fhirpath.svg
    :target: https://pypi.python.org/pypi/collective.fhirpath/
    :alt: License

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black


Background (collective.fhirpath)
================================

`fhirpath`_ implementation in Plone, essential battery included, ready to use.


Installation
------------

Install collective.fhirpath by adding it to your buildout::

    [buildout]
    ...
    eggs +=
        collective.fhirpath


and then running ``bin/buildout``

From Plone controlpanel in the addon settings, install ``collective.fhirpath``.

How It Works
------------

**``FhirResource`` the fhirfield**

Make sure this specialized field is used properly according to `plone.app.fhirfield`_ documentation.

**Make field indexable**

A specilized Catalog PluginIndexes is named ``FhirFieldIndex`` is available, you will use it as like other catalog indexes.

Example::

    <?xml version="1.0"?>
    <object name="portal_catalog" meta_type="Plone Catalog Tool">
        <index name="organization_resource" meta_type="FhirFieldIndex">
            <indexed_attr value="organization_resource"/>
        </index>
    </object>

**Elasticsearch settings**

Make sure elasticsearch has been configured accourding to `collective.elasticsearch`_ docs.


Usages
~~~~~~

FHIR Search::
    >>> from fhirpath.interfaces import IElasticsearchEngineFactory
    >>> from fhirpath.interfaces import IFhirSearch
    >>> from fhirpath.interfaces import ISearchContextFactory
    >>> from plone import api
    >>> from collective.elasticsearch.es import ElasticSearchCatalog
    >>> from zope.component import queryMultiAdapter

    >>> es_catalog = ElasticSearchCatalog(api.portal.get_tool("portal_catalog"))
    >>> factory = queryMultiAdapter(
    ....        (es_catalog,), IElasticsearchEngineFactory
    .... )
    >>> engine = factory(fhir_release="STU3")
    >>> search_context = queryMultiAdapter((engine,), ISearchContextFactory)(
    .... resource_type, unrestricted=False)
    >>> search_factory = queryMultiAdapter((search_context,), IFhirSearch)

    >>> params = (
    ....        ("_profile", "http://hl7.org/fhir/Organization"),
    ....        ("identifier", "urn:oid:2.16.528.1|91654"),
    ....        ("type", "http://hl7.org/fhir/organization-type|prov"),
    ....        ("address-postalcode", "9100 AA"),
    ....        ("address", "Den Burg"),
    ....    )
    >>> bundle = search_factory(params)
    >>> len(bundle.entry)
    2
    >>> # with query string.
    >>> # query_string = self.request["QUERY_STRING]
    >>> query_string = "_profile=http://hl7.org/fhir/Organization&identifier=urn:oid:2.16.528.1|91654&type=http://hl7.org/fhir/organization-type|prov&address-postalcode=9100+AA"
    >>> bundle = search_factory(query_string=query_string)
    >>> len(bundle.entry)
    2

ZCatlog FHIR Search::
    >>> from collective.fhirpath.interfaces import IZCatalogFhirSearch
    >>> zcatalog_factory = queryMultiAdapter((search_context,), IZCatalogFhirSearch)

    >>> # with query string.
    >>> # query_string = self.request["QUERY_STRING]
    >>> query_string = "_profile=http://hl7.org/fhir/Organization&identifier=urn:oid:2.16.528.1|91654&type=http://hl7.org/fhir/organization-type|prov&address-postalcode=9100+AA"
    >>> brains = zcatalog_factory(query_string=query_string)
    >>> len(brains)
    2

FHIR Query::
    >>> from fhirpath.interfaces import IElasticsearchEngineFactory
    >>> from fhirpath.interfaces import IFhirSearch
    >>> from fhirpath.interfaces import ISearchContextFactory
    >>> from plone import api
    >>> from collective.elasticsearch.es import ElasticSearchCatalog
    >>> from zope.component import queryMultiAdapter
    >>> from fhirpath.query import Q_
    >>> from fhirpath.fql import T_
    >>> from fhirpath.fql import sort_
    >>> from fhirpath.enums import SortOrderType

    >>> es_catalog = ElasticSearchCatalog(api.portal.get_tool("portal_catalog"))
    >>> factory = queryMultiAdapter(
    ....        (es_catalog,), IElasticsearchEngineFactory
    .... )
    >>> engine = factory(fhir_release="STU3")
    >>> query_builder = Q_(resource="Organization", engine=engine)
    ....    query_builder = query_builder.where(
    ....        T_("Organization.meta.profile", "http://hl7.org/fhir/Organization")
    ....    ).sort(sort_("Organization.meta.lastUpdated", SortOrderType.DESC))

    >>> result = query_builder(async_result=False, unrestricted=True).fetchall()
    >>> result.header.total
    2
    >>> query_result = query_builder(async_result=False, unrestricted=True)
    >>> for resource in query_result:
    ....        count += 1
    ....        assert resource.__class__.__name__ == "Organization"

    >>> query_builder = Q_(resource="Organization", engine=engine)
    >>> query_builder = query_builder.where(T_("Organization.id", "f001"))
    >>> result_query = query_builder(async_result=False, unrestricted=True)
    >>> resource = result_query.single()
    >>> resource is not None
    True

    >>> query_builder = Q_(resource="Organization", engine=engine)
    >>> query_builder = query_builder.where(
    ....        T_("Organization.meta.profile", "http://hl7.org/fhir/Organization")
    ....    )
    >>> result_query = builder(async_result=False, unrestricted=True)
    >>> result = result_query.first()
    >>> isinstance(result, result_query._query.get_from()[0][1])
    True



Use ``FHIRModelServiceMixin``
-----------------------------

For better performance optimization, you should use ``FHIRModelServiceMixin`` to response ``FHIRModel``, ``FhirFieldValue`` object efficiently.

Example 1::

    >>> from plone.restapi.services import Service
    >>> from collective.fhirpath.utils import FHIRModelServiceMixin
    >>> class MyFHIRGetService(FHIRModelServiceMixin, Service):
    ....     """ """
    ....     def reply(self):
    ....        # do return bellow's types of data
    ....        # could be ``dict`` type data
    ....        # could be instance of ``FHIRAbstractModel`` derrived class.
    ....        # could be instance of ``plone.app.fhirfield.FhirResourceValue`` derrived class.
    ....        # or self.reply_no_content()



configuration
-------------

This product provides three plone registry based records ``fhirpath.es.index.mapping.nested_fields.limit``, ``fhirpath.es.index.mapping.depth.limit``, ``fhirpath.es.index.mapping.total_fields.limit``. Those are related to ElasticSearch index mapping setup, if you aware about it, then you have option to modify from plone control panel (Registry).


Documentation
-------------

Full documentation for end users can be found in the "docs" folder,
and is also available online at https://collective-fhirpath.readthedocs.io/



Contribute
----------

- Issue Tracker: https://github.com/nazrulworld/collective.fhirpath/issues
- Source Code: https://github.com/nazrulworld/collective.fhirpath
- Documentation: https://collective-fhirpath.readthedocs.io/


Support
-------

If you are having issues, please let us know at: Md Nazrul Islam<email2nazrul@gmail.com>


License
-------

The project is licensed under the GPLv2.

.. _`elasticsearch`: https://www.elastic.co/products/elasticsearch
.. _`fhirpath`: https://pypi.org/project/fhirpath/
.. _`PostgreSQL`: https://www.postgresql.org/
.. _`plone.app.fhirfield`: https://pypi.org/project/plone.app.fhirfield/
.. _`collective.elasticsearch`: https://pypi.org/project/collective.elasticsearch/
