# _*_ coding: utf-8 _*_
from .interfaces import IFhirResourceExtractor
from collective.elasticsearch.brain import BrainFactory
from fhirpath.engine.base import EngineResult
from fhirpath.engine.base import EngineResultBody
from fhirpath.engine.base import EngineResultHeader
from fhirpath.engine.base import EngineResultRow
from fhirpath.search import Search
from plone.app.fhirfield import IFhirResourceValue
from Products.ZCatalog.Lazy import LazyMap
from zope.component import queryMultiAdapter

import math


class ElasticResult(object):
    def __init__(self, es, body, **query_params):

        # results are stored in a dictionary, keyed
        # but the start index of the bulk size for the
        # results it holds. This way we can skip around
        # for result data in a result object
        self.es = es
        self.bulk_size = es.get_setting("bulk_size", 50)
        self.sort = body.get("sort", None)
        self.query = body["query"]

        result = es._search(self.query, sort=self.sort, **query_params)["hits"]
        self.results = {0: result["hits"]}
        self.count = result["total"]
        self.query_params = query_params

    def __len__(self):
        return self.count

    def __getitem__(self, key):
        """
        Lazy loading es results with negative index support.
        We store the results in buckets of what the bulk size is.
        This is so you can skip around in the indexes without needing
        to load all the data.
        Example(all zero based indexing here remember):
            (525 results with bulk size 50)
            - self[0]: 0 bucket, 0 item
            - self[10]: 0 bucket, 10 item
            - self[50]: 50 bucket: 0 item
            - self[55]: 50 bucket: 5 item
            - self[352]: 350 bucket: 2 item
            - self[-1]: 500 bucket: 24 item
            - self[-2]: 500 bucket: 23 item
            - self[-55]: 450 bucket: 19 item
        """
        if isinstance(key, slice):
            return [self[i] for i in range(key.start, key.end)]
        else:
            if key + 1 > self.count:
                raise IndexError
            elif key < 0 and abs(key) > self.count:
                raise IndexError

            if key >= 0:
                result_key = int(key / self.bulk_size) * self.bulk_size
                start = result_key
                result_index = key % self.bulk_size  # noqa: S001
            elif key < 0:
                last_key = (
                    int(math.floor(float(self.count) / float(self.bulk_size)))
                    * self.bulk_size
                )
                start = result_key = last_key - (
                    (abs(key) / self.bulk_size) * self.bulk_size
                )
                if last_key == result_key:
                    result_index = key
                else:
                    result_index = (key % self.bulk_size) - (  # noqa: S001
                        self.bulk_size - (self.count % last_key)
                    )

            if result_key not in self.results:
                self.results[result_key] = self.es._search(
                    self.query,
                    sort=self.sort,
                    start=start,
                    **self.query_params,
                )["hits"]["hits"]

            return self.results[result_key][result_index]


def build_engine_result(lazy_maps):
    """ """
    total = 0
    body = EngineResultBody()

    for brain in lazy_maps:
        row = EngineResultRow()
        extractor = queryMultiAdapter((brain.getObject(),), IFhirResourceExtractor)
        assert extractor
        val = extractor()
        if IFhirResourceValue.providedBy(val):
            val = val.foreground_origin()
        row.append(val)
        body.append(row)
        total += 1

    result = EngineResult(header=EngineResultHeader(total=total), body=body)
    return result


def zcatalog_fhir_search(
    context, query_string=None, params=None, bundle_response=False, bundle_as_dict=False
):
    """ """
    query_result = Search(
        context=context, query_string=query_string, params=params
    ).build()

    query_copy = query_result._query.clone()
    if context.unrestricted is False:
        context.engine.build_security_query(query_copy)

    params = {
        "query": query_copy,
        "calculate_field_index_name": context.engine.calculate_field_index_name,
        "get_mapping": context.engine.get_mapping,
    }

    compiled = context.engine.dialect.compile(**params)
    if "from" in compiled:
        del compiled["from"]
    if "scroll" in compiled:
        del compiled["scroll"]
    if "_source" in compiled:
        del compiled["_source"]
    if "size" in compiled:
        del compiled["size"]

    query_params = {"stored_fields": "path.path"}
    result = ElasticResult(context.engine.es_catalog, compiled, **query_params)
    factory = BrainFactory(context.engine.es_catalog.catalog)
    lazy_maps = LazyMap(factory, result, result.count)

    if bundle_response is False:
        return lazy_maps

    engine_result = build_engine_result(lazy_maps)

    return context.engine.wrapped_with_bundle(engine_result, as_json=bundle_as_dict)
