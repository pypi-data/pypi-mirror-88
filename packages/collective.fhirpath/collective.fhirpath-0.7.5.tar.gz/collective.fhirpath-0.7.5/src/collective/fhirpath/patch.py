# -*- coding: utf-8 -*-
from collective.elasticsearch.mapping import MappingAdapter
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import warnings


__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


def MappingAdapter_get_index_creation_body(self):
    """Per index based settings
    https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html
    https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html#mapping-limit-settings
    """
    registry = getUtility(IRegistry)
    settings = dict()

    try:
        settings["index"] = {
            "mapping": {
                "total_fields": {
                    "limit": registry["fhirpath.es.index.mapping.total_fields.limit"]
                },
                "depth": {"limit": registry["fhirpath.es.index.mapping.depth.limit"]},
                "nested_fields": {
                    "limit": registry["fhirpath.es.index.mapping.nested_fields.limit"]
                },
            }
        }
        # removed from ES 7.1.x
        settings["index.mapper.dynamic"] = False

    except KeyError:
        msg = """
            Plone registry records ("
            fhirpath.es.index.mapping.total_fields.limit,
            fhirpath.es.index.mapping.depth.limit,
            fhirpath.es.index.mapping.nested_fields.limit")
            are not created.\n May be collective.fhirpath is not installed!\n
            Either install collective.fhirpath or create records from other addon.
        """
        warnings.warn(msg, UserWarning)

    settings["analysis"] = {
        "analyzer": {
            "fhir_reference_analyzer": {
                "tokenizer": "keyword",
                "filter": ["fhir_reference_filter"],
            },
        },
        "filter": {
            "fhir_reference_filter": {
                "type": "pattern_capture",
                "preserve_original": True,
                "patterns": [r"(?:\w+\/)?(https?\:\/\/.*|[a-zA-Z0-9_-]+)"],
            },
        },
        "char_filter": {},
        "tokenizer": {},
    }
    return dict(settings=settings)


# *** Monkey Patch ***
def do():
    """ """
    if getattr(MappingAdapter_get_index_creation_body, "__patched__", None) is None:

        setattr(MappingAdapter_get_index_creation_body, "__patched__", True)

        setattr(
            MappingAdapter,
            "get_index_creation_body",
            MappingAdapter_get_index_creation_body,
        )
