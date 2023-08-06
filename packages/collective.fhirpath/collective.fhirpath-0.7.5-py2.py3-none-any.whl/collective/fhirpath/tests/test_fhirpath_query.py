# _*_ coding: utf-8 _*_
from .base import BaseFunctionalTesting
from collective.elasticsearch.es import ElasticSearchCatalog
from collective.fhirpath.testing import COLLECTIVE_FHIRPATH_FUNCTIONAL_TESTING
from fhirpath.enums import FHIR_VERSION
from fhirpath.enums import SortOrderType
from fhirpath.exceptions import MultipleResultsFound
from fhirpath.fql import not_
from fhirpath.fql import sort_
from fhirpath.fql import T_
from fhirpath.interfaces import IElasticsearchEngineFactory
from fhirpath.query import Q_
from plone import api
from zope.component import queryMultiAdapter


__author__ = "Md Nazrul Islam <email2nazrul@gmail.com>"


class FhirPathPloneQueryFunctionalTest(BaseFunctionalTesting):
    """ """

    layer = COLLECTIVE_FHIRPATH_FUNCTIONAL_TESTING

    def get_es_catalog(self):
        """ """
        return ElasticSearchCatalog(api.portal.get_tool("portal_catalog"))

    def get_engine(self):
        """ """
        factory = queryMultiAdapter(
            (self.get_es_catalog(),), IElasticsearchEngineFactory
        )
        engine = factory(fhir_release=FHIR_VERSION.STU3)
        return engine

    def test_iter_result(self):
        """ """
        self.load_contents()
        engine = self.get_engine()
        builder = Q_(resource="Organization", engine=engine)
        builder = builder.where(
            T_("Organization.meta.profile", "http://hl7.org/fhir/Organization")
        ).sort(sort_("Organization.meta.lastUpdated", SortOrderType.DESC))
        count = 0

        for resource in builder(async_result=False, unrestricted=True):
            count += 1

            assert resource.__class__.__name__ == "Organization"

        self.assertEqual(count, 2)

    def test_fetchall(self):
        """ """
        self.load_contents()

        engine = self.get_engine()
        builder = Q_(resource="Organization", engine=engine)
        builder = builder.where(
            T_("Organization.meta.profile", "http://hl7.org/fhir/Organization")
        ).sort(sort_("Organization.meta.lastUpdated", SortOrderType.DESC))
        result = builder(async_result=False, unrestricted=True).fetchall()

        self.assertEqual(result.header.total, 2)

        # Test
        builder = Q_(resource="Task", engine=engine)
        builder = builder.where(T_("Task.status", "ready"))
        result = builder(async_result=False, unrestricted=True).fetchall()
        self.assertEqual(result.header.total, 2)

        # Search with part-of
        # should be two sub tasks
        builder = Q_(resource="Task", engine=engine)
        builder = builder.where(
            T_("Task.partOf.reference", "Task/5df31190-0ed4-45ba-8b16-3c689fc2e686")
        )
        result = builder(async_result=False, unrestricted=True).fetchall()
        self.assertEqual(result.header.total, 2)

    def test_negetive_query(self):
        """ """
        self.load_contents()

        engine = self.get_engine()

        builder = Q_(resource="Task", engine=engine)
        builder = builder.where(
            not_(
                T_(
                    "Task.owner.reference",
                    "Practitioner/fake-ac0-821d-46d9-9d40-a61f2578cadf",
                )
            )
        )

        result = builder(async_result=False, unrestricted=True).fetchall()
        self.assertEqual(result.header.total, 3)

    def test_single_query(self):
        """ """
        self.load_contents()

        engine = self.get_engine()
        builder = Q_(resource="Organization", engine=engine)
        builder = builder.where(T_("Organization.id", "f001"))
        result_query = builder(async_result=False, unrestricted=True)
        self.assertIsNotNone(result_query.single())

        builder = Q_(resource="Organization", engine=engine)
        builder = builder.where(
            T_("Organization.meta.profile", "http://hl7.org/fhir/Organization")
        )
        result_query = builder(async_result=False, unrestricted=True)
        try:
            result_query.single()
            raise AssertionError(
                "Code should not come here, as multiple resources should in result"
            )
        except MultipleResultsFound:
            pass

    def test_first_query(self):
        """ """
        self.load_contents()

        engine = self.get_engine()
        builder = Q_(resource="Organization", engine=engine)
        builder = builder.where(
            T_("Organization.meta.profile", "http://hl7.org/fhir/Organization")
        )
        result_query = builder(async_result=False, unrestricted=True)
        result = result_query.first()
        self.assertEqual(
            result[0]["resourceType"], result_query._query.get_from()[0][0]
        )
