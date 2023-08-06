Changelog
=========


0.7.5 (2020-12-17)
------------------

- minimum ``fhir.resources`` version is now ``6.0.0``, see it's associated changes at https://pypi.org/project/fhir.resources/6.0.0/.

- minimum ``fhirpath``version is now ``0.10.5``, see it's associated improvements and bug fixes at https://pypi.org/project/fhirpath/0.10.4/

- minimum ``plone.app.fhirfield``version is now ``4.2.0``, see it's associated improvements and bug fixes at https://pypi.org/project/plone.app.fhirfield/4.2.0/

0.7.4 (2020-11-19)
------------------

- Minimum required ``fhirpath`` version is now ``0.10.4`` (see it's changes log) and added compabilities.


0.7.3 (2020-10-24)
------------------

- new helper function ``json_body`` has been created, which is using ``orjson`` deserializer.

- ``FHIRModelServiceMixin`` is now more performance optimized.


0.7.2 (2020-10-06)
------------------

- Bundle resposne as ``dict`` option enable in ZCatalog based search.


0.7.1 (2020-10-05)
------------------

- ``fhirpath``minimum version has been updated, which includes minimum ``fhir.resources`` version ``6.0.0b5``.

- Improvements for ``FHIRModelServiceMixin`` as orjson serializer used.


0.7.0 (2020-09-25)
------------------

Improvements

- Issue #2 `ZCatalog based search should have option to return bundle type alongside as LazyBrain <https://github.com/nazrulworld/collective.fhirpath/issues/2>`_

- Supports all features from ``fhirpath`` 0.8.0.

- Elasticsearch Mappings JSON files are updated.

Fixes

- ``utils.FHIRModelServiceMixin`` can now handle ``list`` type data in response.


0.6.1 (2020-09-09)
------------------

- ``plone.app.fhirfield:default``has been added in dependency, so no need separete install of ``plone.app.fhirfield``.


0.6.0 (2020-09-09)
------------------


Improvements

- ``FHIRModelServiceMixin`` class has been available under ``utils`` module, which can be used with your ``plone.restapi``
  services to response type as ``FhirModel`` aka pydantic's ``BaseModel`` or ``plone.app.fhirfield.FhirFieldValue`` object with the best possible effecient way.


0.5.0 (2020-08-18)
------------------

Improvements

- Supports the revolutionary version of `fhir.resources <https://pypi.org/project/fhir.resources/>`_ via `fhirpath <https://pypi.org/project/fhirpath/>`_
  we may expect some refactor on your existing codebase because of some breaking changes, please see changes at ``fhir.resources``, ``plone.app.fhirfield`` and ``fhirpath``.

- Brings back support for Python version 3.6

- Three configurations (``fhirpath.es.index.mapping.nested_fields.limit``, ``fhirpath.es.index.mapping.depth.limit``, ``fhirpath.es.index.mapping.total_fields.limit``) based on plone registry has now been available.


0.4.0 (2020-05-15)
------------------

Breakings

- As a part of supporting latest ``fhirpath`` version (from ``0.6.1``), drop python version later than ``3.7.0``.

-  ``ElasticsearchEngineFactory.__call__``'s argument name ``fhir_version`` changed to ``fhir_release``.


0.3.0 (2019-11-10)
------------------

Improvements

- ZCatalog featured fhir search added, from which you will get ZCatalog´s brain feature.

- ``FhirFieldIndex`` named PluginIndex is now available.

- FHIR ``STU3``and ``R4`` search mapping is now available.

- Others improvements that make able to use in production project (of course without guarantee.)


0.2.0 (2019-09-16)
------------------

- first working versions, with lots of improvements.


0.1.0 (2019-09-06)
------------------

- Initial release.
  [nazrulworld]
