# _*_ coding: utf-8 _*_
from fhirpath.enums import FHIR_VERSION
from fhirpath.json import json_dumps
from fhirpath.json import json_loads
from fhirpath.storage import MemoryStorage
from plone import api
from plone.app.fhirfield.interfaces import IFhirResource
from plone.app.fhirfield.interfaces import IFhirResourceValue
from plone.behavior.interfaces import IBehavior
from plone.restapi.exceptions import DeserializationError
from plone.restapi.services import _no_content_marker
from pydantic import BaseModel
from zope.component import getUtility
from zope.schema import getFields

import os


__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"

FHIR_ES_MAPPINGS_CACHE = MemoryStorage()
releases = [member.name for member in FHIR_VERSION if member.name != "DEFAULT"]
for release in releases:
    if not FHIR_ES_MAPPINGS_CACHE.exists(release):
        FHIR_ES_MAPPINGS_CACHE.insert(release, MemoryStorage())
del releases

FHIRFIELD_NAMES_MAP = MemoryStorage()


def get_elasticsearch_mapping(
    resource, fhir_release="R4", mapping_dir=None, cache=True
):
    """Elastic search mapping for FHIR resources"""
    fhir_release = FHIR_VERSION[fhir_release].name
    if mapping_dir is None:
        mapping_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "browser",
            "static",
            "ES_MAPPINGS",
            fhir_release,
        )
    storage = FHIR_ES_MAPPINGS_CACHE.get(fhir_release)

    if resource not in storage or cache is False:
        file_location = None
        expected_filename = "{0}.mapping.json".format(resource)
        for root, dirs, files in os.walk(mapping_dir, topdown=True):
            for filename in files:
                if filename == expected_filename:
                    file_location = os.path.join(root, filename)
                    break

        if file_location is None:
            raise LookupError(
                "Mapping files {0}/{1} doesn't exists.".format(
                    mapping_dir, expected_filename
                )
            )

        with open(os.path.join(root, file_location), "rb") as f:
            content = json_loads(f.read())
            assert filename.split(".")[0] == content["resourceType"]

            storage[resource] = content

    return storage[resource]["mapping"]


def find_fhirfield_by_name(fieldname):
    """  """
    if fieldname in FHIRFIELD_NAMES_MAP:
        return FHIRFIELD_NAMES_MAP.get(fieldname)

    types_tool = api.portal.get_tool("portal_types")
    field_ = None

    def _from_schema(schema):
        for name, field in getFields(schema).items():
            if IFhirResource.providedBy(field) and name == fieldname:
                return field

    def _from_factory(factory):
        schema = factory.lookupSchema() or factory.lookupModel().schema
        field = _from_schema(schema)
        if field:
            return field
        for behavior in factory.behaviors:
            schema = getUtility(IBehavior, name=behavior).interface
            if schema is None:
                continue
            field = _from_schema(schema)
            if field:
                return field

    for type_name in types_tool.listContentTypes():
        factory = types_tool.getTypeInfo(type_name)
        if factory.meta_type != "Dexterity FTI":
            continue
        field_ = _from_factory(factory)
        if field_ is not None:
            break
    if field_:
        FHIRFIELD_NAMES_MAP.insert(fieldname, field_)
    return field_


def json_body(request):
    try:
        data = json_loads(request.get("BODY") or b"{}")
    except ValueError:
        raise DeserializationError("No JSON object could be decoded")
    if not isinstance(data, dict):
        raise DeserializationError("Malformed body")
    return data


class FHIRModelServiceMixin:
    """This is performance optimized plone.restapi service's render mixin class
    for FHIRModel (fhir.resources) content. Avoiding redundant json serilization
    and deserialization.
    User it with your Service Class::
    >>> from collective.fhirpath.utils import FHIRModelServiceMixin
    >>> from plone.restapi.services import Service
    >>> class MyAwesomeService(FHIRModelServiceMixin, Service):
    >>> .... pass
    """

    def render(self):
        """ """
        self.check_permission()
        content = self.reply()
        if content is _no_content_marker or content is None:
            return

        pretty = self.request.get("_pretty", "false") == "true"
        dumps_params = {"return_bytes": True}
        if pretty:
            dumps_params["indent"] = 2
            dumps_params["sort_keys"] = True

        self.request.response.setHeader("Content-Type", self.content_type)

        if IFhirResourceValue.providedBy(content):
            value = content.foreground_origin()
            if value:
                content = value
            else:
                return _no_content_marker

        if isinstance(content, BaseModel):
            return content.json(**dumps_params)

        return json_dumps(content, **dumps_params)
