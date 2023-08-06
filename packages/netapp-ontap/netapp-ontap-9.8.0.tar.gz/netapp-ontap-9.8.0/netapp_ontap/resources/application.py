r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union

try:
    CLICHE_INSTALLED = False
    import cliche
    from cliche.arg_types.choices import Choices
    from cliche.commands import ClicheCommandError
    from netapp_ontap.resource_table import ResourceTable
    CLICHE_INSTALLED = True
except ImportError:
    pass

from marshmallow import fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size
from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["Application", "ApplicationSchema"]
__pdoc__ = {
    "ApplicationSchema.resource": False,
    "Application.application_show": False,
    "Application.application_create": False,
    "Application.application_modify": False,
    "Application.application_delete": False,
}


class ApplicationSchema(ResourceSchema):
    """The fields of the Application object"""

    links = fields.Nested("netapp_ontap.models.application_links.ApplicationLinksSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the application. """

    creation_timestamp = fields.Str(
        data_key="creation_timestamp",
    )
    r""" The time when the application was created. """

    delete_data = fields.Boolean(
        data_key="delete_data",
    )
    r""" Should application storage elements be deleted? An application is considered to use storage elements from a shared storage pool. Possible values are 'true' and 'false'. If the value is 'true', the application will be deleted in its entirety. If the value is 'false', the storage elements will be disassociated from the application and preserved. The application will then be deleted. """

    generation = Size(
        data_key="generation",
    )
    r""" The generation number of the application. This indicates which features are supported on the application. For example, generation 1 applications do not support Snapshot copies. Support for Snapshot copies was added at generation 2. Any future generation numbers and their feature set will be documented. """

    maxdata_on_san = fields.Nested("netapp_ontap.models.maxdata_on_san.MaxdataOnSanSchema", data_key="maxdata_on_san", unknown=EXCLUDE)
    r""" The maxdata_on_san field of the application. """

    mongo_db_on_san = fields.Nested("netapp_ontap.models.mongo_db_on_san.MongoDbOnSanSchema", data_key="mongo_db_on_san", unknown=EXCLUDE)
    r""" The mongo_db_on_san field of the application. """

    name = fields.Str(
        data_key="name",
    )
    r""" Application Name. This field is user supplied when the application is created. """

    nas = fields.Nested("netapp_ontap.models.nas.NasSchema", data_key="nas", unknown=EXCLUDE)
    r""" The nas field of the application. """

    nvme = fields.Nested("netapp_ontap.models.zapp_nvme.ZappNvmeSchema", data_key="nvme", unknown=EXCLUDE)
    r""" The nvme field of the application. """

    oracle_on_nfs = fields.Nested("netapp_ontap.models.oracle_on_nfs.OracleOnNfsSchema", data_key="oracle_on_nfs", unknown=EXCLUDE)
    r""" The oracle_on_nfs field of the application. """

    oracle_on_san = fields.Nested("netapp_ontap.models.oracle_on_san.OracleOnSanSchema", data_key="oracle_on_san", unknown=EXCLUDE)
    r""" The oracle_on_san field of the application. """

    oracle_rac_on_nfs = fields.Nested("netapp_ontap.models.oracle_rac_on_nfs.OracleRacOnNfsSchema", data_key="oracle_rac_on_nfs", unknown=EXCLUDE)
    r""" The oracle_rac_on_nfs field of the application. """

    oracle_rac_on_san = fields.Nested("netapp_ontap.models.oracle_rac_on_san.OracleRacOnSanSchema", data_key="oracle_rac_on_san", unknown=EXCLUDE)
    r""" The oracle_rac_on_san field of the application. """

    protection_granularity = fields.Str(
        data_key="protection_granularity",
        validate=enum_validation(['application', 'component']),
    )
    r""" Protection granularity determines the scope of Snapshot copy operations for the application. Possible values are "application" and "component". If the value is "application", Snapshot copy operations are performed on the entire application. If the value is "component", Snapshot copy operations are performed separately on the application components.

Valid choices:

* application
* component """

    rpo = fields.Nested("netapp_ontap.models.application_rpo.ApplicationRpoSchema", data_key="rpo", unknown=EXCLUDE)
    r""" The rpo field of the application. """

    s3_bucket = fields.Nested("netapp_ontap.models.zapp_s3_bucket.ZappS3BucketSchema", data_key="s3_bucket", unknown=EXCLUDE)
    r""" The s3_bucket field of the application. """

    san = fields.Nested("netapp_ontap.models.san.SanSchema", data_key="san", unknown=EXCLUDE)
    r""" The san field of the application. """

    smart_container = fields.Boolean(
        data_key="smart_container",
    )
    r""" Identifies if this is a smart container or not. """

    sql_on_san = fields.Nested("netapp_ontap.models.sql_on_san.SqlOnSanSchema", data_key="sql_on_san", unknown=EXCLUDE)
    r""" The sql_on_san field of the application. """

    sql_on_smb = fields.Nested("netapp_ontap.models.sql_on_smb.SqlOnSmbSchema", data_key="sql_on_smb", unknown=EXCLUDE)
    r""" The sql_on_smb field of the application. """

    state = fields.Str(
        data_key="state",
        validate=enum_validation(['creating', 'deleting', 'modifying', 'online', 'restoring']),
    )
    r""" The state of the application. For full functionality, applications must be in the online state. Other states indicate that the application is in a transient state and not all operations are supported.

Valid choices:

* creating
* deleting
* modifying
* online
* restoring """

    statistics = fields.Nested("netapp_ontap.models.application_statistics.ApplicationStatisticsSchema", data_key="statistics", unknown=EXCLUDE)
    r""" The statistics field of the application. """

    svm = fields.Nested("netapp_ontap.models.application_svm.ApplicationSvmSchema", data_key="svm", unknown=EXCLUDE)
    r""" The svm field of the application. """

    template = fields.Nested("netapp_ontap.models.application_template1.ApplicationTemplate1Schema", data_key="template", unknown=EXCLUDE)
    r""" The template field of the application. """

    uuid = fields.Str(
        data_key="uuid",
    )
    r""" Application UUID. This field is generated when the application is created. """

    vdi_on_nas = fields.Nested("netapp_ontap.models.vdi_on_nas.VdiOnNasSchema", data_key="vdi_on_nas", unknown=EXCLUDE)
    r""" The vdi_on_nas field of the application. """

    vdi_on_san = fields.Nested("netapp_ontap.models.vdi_on_san.VdiOnSanSchema", data_key="vdi_on_san", unknown=EXCLUDE)
    r""" The vdi_on_san field of the application. """

    vsi_on_nas = fields.Nested("netapp_ontap.models.vsi_on_nas.VsiOnNasSchema", data_key="vsi_on_nas", unknown=EXCLUDE)
    r""" The vsi_on_nas field of the application. """

    vsi_on_san = fields.Nested("netapp_ontap.models.vsi_on_san.VsiOnSanSchema", data_key="vsi_on_san", unknown=EXCLUDE)
    r""" The vsi_on_san field of the application. """

    @property
    def resource(self):
        return Application

    gettable_fields = [
        "links",
        "creation_timestamp",
        "generation",
        "maxdata_on_san",
        "mongo_db_on_san",
        "name",
        "nas",
        "nvme",
        "oracle_on_nfs",
        "oracle_on_san",
        "oracle_rac_on_nfs",
        "oracle_rac_on_san",
        "protection_granularity",
        "rpo",
        "s3_bucket",
        "san",
        "smart_container",
        "sql_on_san",
        "sql_on_smb",
        "state",
        "statistics",
        "svm",
        "template",
        "uuid",
        "vdi_on_nas",
        "vdi_on_san",
        "vsi_on_nas",
        "vsi_on_san",
    ]
    """links,creation_timestamp,generation,maxdata_on_san,mongo_db_on_san,name,nas,nvme,oracle_on_nfs,oracle_on_san,oracle_rac_on_nfs,oracle_rac_on_san,protection_granularity,rpo,s3_bucket,san,smart_container,sql_on_san,sql_on_smb,state,statistics,svm,template,uuid,vdi_on_nas,vdi_on_san,vsi_on_nas,vsi_on_san,"""

    patchable_fields = [
        "links",
        "maxdata_on_san",
        "mongo_db_on_san",
        "nas",
        "nvme",
        "oracle_on_nfs",
        "oracle_on_san",
        "oracle_rac_on_nfs",
        "oracle_rac_on_san",
        "rpo",
        "s3_bucket",
        "san",
        "sql_on_san",
        "sql_on_smb",
        "statistics",
        "template",
        "vdi_on_nas",
        "vdi_on_san",
        "vsi_on_nas",
        "vsi_on_san",
    ]
    """links,maxdata_on_san,mongo_db_on_san,nas,nvme,oracle_on_nfs,oracle_on_san,oracle_rac_on_nfs,oracle_rac_on_san,rpo,s3_bucket,san,sql_on_san,sql_on_smb,statistics,template,vdi_on_nas,vdi_on_san,vsi_on_nas,vsi_on_san,"""

    postable_fields = [
        "links",
        "delete_data",
        "maxdata_on_san",
        "mongo_db_on_san",
        "name",
        "nas",
        "nvme",
        "oracle_on_nfs",
        "oracle_on_san",
        "oracle_rac_on_nfs",
        "oracle_rac_on_san",
        "rpo",
        "s3_bucket",
        "san",
        "smart_container",
        "sql_on_san",
        "sql_on_smb",
        "statistics",
        "svm",
        "template",
        "vdi_on_nas",
        "vdi_on_san",
        "vsi_on_nas",
        "vsi_on_san",
    ]
    """links,delete_data,maxdata_on_san,mongo_db_on_san,name,nas,nvme,oracle_on_nfs,oracle_on_san,oracle_rac_on_nfs,oracle_rac_on_san,rpo,s3_bucket,san,smart_container,sql_on_san,sql_on_smb,statistics,svm,template,vdi_on_nas,vdi_on_san,vsi_on_nas,vsi_on_san,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in Application.get_collection(fields=field)]
    return getter

async def _wait_for_job(response: NetAppResponse) -> None:
    """Examine the given response. If it is a job, asynchronously wait for it to
    complete. While polling, prints the current status message of the job.
    """

    if not response.is_job:
        return
    from netapp_ontap.resources import Job
    job = Job(**response.http_response.json()["job"])
    while True:
        job.get(fields="state,message")
        if hasattr(job, "message"):
            print("[%s]: %s" % (job.state, job.message))
        if job.state == "failure":
            raise NetAppRestError("Application modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class Application(Resource):
    r""" Applications """

    _schema = ApplicationSchema
    _path = "/api/application/applications"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves applications.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `<template>` the property corresponding to the `template.name` of the application
### Query examples
Numerous queries are available for classifying and sorting applications:
1. Return a list of applications sorted by name.
    ```
    GET /application/applications?order_by=name
    ```
    <br/>
2. Return a list of applications for a specific SVM.
    ```
    GET /application/applications?svm.name=<name>
    ```
    <br/>
3. Return a list of all SQL applications.
    ```
    GET /application/applications?template.name=sql*
    ```
    <br/>
4. Return a list of all applications that can be accessed via SAN.<br/>
    ```
    GET /application/applications?template.protocol=san
    ```
    <br/>
5. Return the top five applications consuming the most IOPS.<br/>
    ```
    GET /application/applications?order_by=statistics.iops.total desc&max_records=5
    ```
<br/>The above examples are not comprehensive. There are many more properties available for queries. Also, multiple queries can be mixed and matched with other query parameters for a large variety of requests. See the per-property documentation below for the full list of supported query parameters.
### Learn more
* [`DOC /application`](#docs-application-overview)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="application show")
        def application_show(
            creation_timestamp: Choices.define(_get_field_list("creation_timestamp"), cache_choices=True, inexact=True)=None,
            delete_data: Choices.define(_get_field_list("delete_data"), cache_choices=True, inexact=True)=None,
            generation: Choices.define(_get_field_list("generation"), cache_choices=True, inexact=True)=None,
            name: Choices.define(_get_field_list("name"), cache_choices=True, inexact=True)=None,
            protection_granularity: Choices.define(_get_field_list("protection_granularity"), cache_choices=True, inexact=True)=None,
            smart_container: Choices.define(_get_field_list("smart_container"), cache_choices=True, inexact=True)=None,
            state: Choices.define(_get_field_list("state"), cache_choices=True, inexact=True)=None,
            uuid: Choices.define(_get_field_list("uuid"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["creation_timestamp", "delete_data", "generation", "name", "protection_granularity", "smart_container", "state", "uuid", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of Application resources

            Args:
                creation_timestamp: The time when the application was created.
                delete_data: Should application storage elements be deleted? An application is considered to use storage elements from a shared storage pool. Possible values are 'true' and 'false'. If the value is 'true', the application will be deleted in its entirety. If the value is 'false', the storage elements will be disassociated from the application and preserved. The application will then be deleted.
                generation: The generation number of the application. This indicates which features are supported on the application. For example, generation 1 applications do not support Snapshot copies. Support for Snapshot copies was added at generation 2. Any future generation numbers and their feature set will be documented.
                name: Application Name. This field is user supplied when the application is created.
                protection_granularity: Protection granularity determines the scope of Snapshot copy operations for the application. Possible values are \"application\" and \"component\". If the value is \"application\", Snapshot copy operations are performed on the entire application. If the value is \"component\", Snapshot copy operations are performed separately on the application components.
                smart_container: Identifies if this is a smart container or not.
                state: The state of the application. For full functionality, applications must be in the online state. Other states indicate that the application is in a transient state and not all operations are supported.
                uuid: Application UUID. This field is generated when the application is created.
            """

            kwargs = {}
            if creation_timestamp is not None:
                kwargs["creation_timestamp"] = creation_timestamp
            if delete_data is not None:
                kwargs["delete_data"] = delete_data
            if generation is not None:
                kwargs["generation"] = generation
            if name is not None:
                kwargs["name"] = name
            if protection_granularity is not None:
                kwargs["protection_granularity"] = protection_granularity
            if smart_container is not None:
                kwargs["smart_container"] = smart_container
            if state is not None:
                kwargs["state"] = state
            if uuid is not None:
                kwargs["uuid"] = uuid
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return Application.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves applications.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `<template>` the property corresponding to the `template.name` of the application
### Query examples
Numerous queries are available for classifying and sorting applications:
1. Return a list of applications sorted by name.
    ```
    GET /application/applications?order_by=name
    ```
    <br/>
2. Return a list of applications for a specific SVM.
    ```
    GET /application/applications?svm.name=<name>
    ```
    <br/>
3. Return a list of all SQL applications.
    ```
    GET /application/applications?template.name=sql*
    ```
    <br/>
4. Return a list of all applications that can be accessed via SAN.<br/>
    ```
    GET /application/applications?template.protocol=san
    ```
    <br/>
5. Return the top five applications consuming the most IOPS.<br/>
    ```
    GET /application/applications?order_by=statistics.iops.total desc&max_records=5
    ```
<br/>The above examples are not comprehensive. There are many more properties available for queries. Also, multiple queries can be mixed and matched with other query parameters for a large variety of requests. See the per-property documentation below for the full list of supported query parameters.
### Learn more
* [`DOC /application`](#docs-application-overview)
"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the properties of an application.
### Overview
Similar to creating an application, modification is done using the template properties of an application. The `storage_service`, `size`, and `igroup_name` of an application may be modified.
### `storage_service`
Storage service modifications are processed in place, meaning that the storage can not be moved to a location with more performance headroom to accommodate the request. If the current backing storage of the application is in a location that can support increased performance, the QoS policies associated with the application will be modified to allow it. If not, an error will be returned. A storage service modification to a lower tier of performance is always allowed, but the reverse modification may not be supported if the cluster is over provisioned and the cluster is unlikely to be able to fulfil the original storage service.
### `size`
Size modifications are processed in a variety of ways depending on the type of application. For NAS applications, volumes are grown or new volumes are added. For SAN applications, LUNs are grown, new LUNs are added to existing volumes, or new LUNs are added to new volumes. If new storage elements are created, they can be found using the [`GET /application/applications/{application.uuid}/components`](#operations-application-application_component_collection_get) interface. The creation time of each storage object is included, and the newly created objects will use the same naming scheme as the previous objects. Resize follows the best practices associated with the type of application being expanded. Reducing the size of an application is not supported.
### `igroup_name`
Modification of the igroup name allows an entire application to be mapped from one initiator group to another. Data access will be interrupted as the LUNs are unmapped from the original igroup and remapped to the new one.
### Application state
During a modification, the `state` property of the application updates to indicate `modifying`. In `modifying` state, statistics are not available and Snapshot copy operations are not allowed. If the modification fails, it is possible for the application to be left in an inconsistent state, with the underlying ONTAP storage elements not matching across a component. When this occurs, the application is left in the `modifying` state until the command is either retried and succeeds or a call to restore the original state is successful.
### Examples
1. Change the storage service of the database of the Oracle application to _extreme_ and resize the redo logs to _100GB_.
    ```
    {
      "oracle_on_nfs": {
        "db": {
          "storage_service": {
            "name": "extreme"
          }
        },
        "redo_log": {
          "size": "100GB"
        }
      }
    }
    ```
    <br/>
2. Change the storage service, size, and igroup of a generic application by component name.
    ```
    {
      "san": {
        "application_components": [
          {
            "name": "component1",
            "storage_service": {
              "name": "value"
            }
          },
          {
            "name": "component2",
            "size": "200GB"
          },
          {
            "name": "component3",
            "igroup_name": "igroup5"
          }
        ]
      }
    }
    ```
    <br/>
### Learn more
* [`DOC /application`](#docs-application-overview)
* [`Asynchronous operations`](#Synchronous_and_asynchronous_operations)
"""
        return super()._patch_collection(body, *args, connection=connection, **kwargs)

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        body: Union[Resource, dict] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an application and all associated data.
### Warning - this deletes it all, including your data
This deletes everything created with the application, including any volumes, LUNs, NFS export policies, CIFS shares, and initiator groups. Initiator groups are only destroyed if they were created as part of an application and are no longer in use by other applications.
### Learn more
* [`DOC /application`](#docs-application-overview)
* [`Asynchronous operations`](#Synchronous_and_asynchronous_operations)
"""
        return super()._delete_collection(*args, body=body, connection=connection, **kwargs)

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves applications.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `<template>` the property corresponding to the `template.name` of the application
### Query examples
Numerous queries are available for classifying and sorting applications:
1. Return a list of applications sorted by name.
    ```
    GET /application/applications?order_by=name
    ```
    <br/>
2. Return a list of applications for a specific SVM.
    ```
    GET /application/applications?svm.name=<name>
    ```
    <br/>
3. Return a list of all SQL applications.
    ```
    GET /application/applications?template.name=sql*
    ```
    <br/>
4. Return a list of all applications that can be accessed via SAN.<br/>
    ```
    GET /application/applications?template.protocol=san
    ```
    <br/>
5. Return the top five applications consuming the most IOPS.<br/>
    ```
    GET /application/applications?order_by=statistics.iops.total desc&max_records=5
    ```
<br/>The above examples are not comprehensive. There are many more properties available for queries. Also, multiple queries can be mixed and matched with other query parameters for a large variety of requests. See the per-property documentation below for the full list of supported query parameters.
### Learn more
* [`DOC /application`](#docs-application-overview)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an application
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `<template>` the property corresponding to the `template.name` of the application
### Property overview
An application includes three main groups or properties.
* Generic properties - such as the `name`, `template.name`, and `state` of the application. These properties are all inexpensive to retrieve and their meaning is consistent for every type of application.
* `statistics.*` - application statistics report live usage data about the application and its components. Various space and IOPS details are included at both the application level and at a per component level. The application model includes a detailed description of each property. These properties are slightly more expensive than the generic properties because live data must be collected from every storage element in the application.
* `<template>` - the property corresponding to the value of the `template.name` returns the contents of the application in the same layout that was used to provision the application. This information is very expensive to retrieve because it requires collecting information about all the storage and access settings for every element of the application. There are a few notable limitations to what can be returned in the `<template>` section:
  * The `new_igroups` array of many SAN templates is not returned by GET. This property allows igroup creation in the same call that creates an application, but is not a property of the application itself. The `new_igroups` array is allowed during PATCH operations, but that does not modify the `new_igroups` of the application. It is another way to allow igroup creation while updating the application to use a different igroup.
  * The `vdi_on_san` and `vdi_on_nas` `desktops.count` property is rounded to the nearest 1000 during creation, and is reported with that rounding applied.
  * The `mongo_db_on_san` `dataset.element_count` property is rounded up to an even number, and is reported with that rounding applied.
  * The `sql_on_san` and `sql_on_smb` `server_cores_count` property is limited to 8 for GET operations. Higher values are accepted by POST, but the impact of the `server_cores_count` property on the application layout currently reaches its limit at 8.
### Learn more
* [`DOC /application`](#docs-application-overview)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Creates an application.
### Template properties
The application APIs appear to be complex and long in this documentation because we document every possible template, of which there are currently 14. When creating an application, only a single template is used, so it is best to focus only on the template of interest. Other than the properties for the chosen template, only the `name` and `svm` of the application must be provided. The following three sections provided guidelines on using the properties of the templates, but the whole idea behind the templates is to automatically follow the best practices of the given application, so the only way to determine the exact list of required properties and default values is to dig in to the model section of the template. The templates are all top level properties of the application object with names matching the values returned by [`GET /application/templates`](#operations-application-application_template_collection_get).
### Required properties
* `svm.uuid` or `svm.name` - The existing SVM in which to create the application.
* `name` - The name for the application.
* `<template>` - Properties for one template must be provided. In general, the following properties are required, however the naming of these may vary slightly from template to template.
  * `name` - The generic templates require names for the components of the application. Other templates name the components automatically.
  * `size` - This generally refers to the size of an application component, which may be spread across multiple underlying storage objects (volumes, LUNs, etc...).
  * One of the following must be specified:
      * `nfs_access` or an identifier (name or id) of an existing `export-policy`.
      * `cifs_access`
      * `igroup_name`
  * `os_type` - All SAN applications require an os_type to be specified in some way. Some templates refer to this as the `hypervisor`.
### Recommended optional properties
* `<template>` - The following properties are available in some templates.
  * `new_igroups.*` - SAN applications can use existing initiator groups or create new ones. When creating new initiator groups, `new_igroups.name` is required and the other properties may be used to fully specify the new initiator group.
### Default property values
If not specified in POST, the follow default property values are assigned. It is recommended that most of these properties be provided explicitly rather than relying upon the defaults. The defaults are intended to make it as easy as possible to provision and connect to an application.
* `template.name` - Defaults to match the `<template>` provided. If specified, the value of this property must match the provided template properties.
* `<template>` - The majority of template properties have default values. The defaults may vary from template to template. See the model of each template for complete details. In general the following patterns are common across all template properties. The location of these properties varies from template to template.
  * `storage_service.name` - _value_
  * `protection_type.local_rpo` - _hourly_ (Hourly Snapshot copies)
  * `protection_type.remote_rpo` - _none_ (Not MetroCluster)
  * `new_igroups.os_type` - Defaults to match the `os_type` provided for the application, but may need to be provided explicitly when using virtualization.
### Optional components
A common pattern across many templates are objects that are optional, but once any property in the object is specified, other properties within the object become required. Many applications have optional components. For example, provisioning a database without a component to store the logs is supported. If the properties related to the logs are omitted, no storage will be provisioned for logs. But when the additional component is desired, the size is required. Specifying any other property of a component without specifying the size is not supported. In the model of each template, the required components are indicated with a red '*'. When a `size` property is listed as optional, that means the component itself is optional, and the size should be specified to include that component in the application.
### POST body examples
1. Create a generic SAN application that exposes four LUNs to an existing initiator group, _igroup_1_.<br/>
    ```
    {
      "name": "app1",
      "svm": { "name": "svm1" },
      "san": {
        "os_type": "linux",
        "application_components": [
          { "name": "component1", "total_size": "10GB", "lun_count": 4, "igroup_name": "igroup_1" }
        ]
      }
    }
    ```
    <br/>
2. Create an SQL application that can be accessed via initiator _iqn.2017-01.com.example:foo_ from a new initiator group, _igroup_2_.<br/>
    ```
    {
      "name": "app2",
      "svm": { "name": "svm1" },
      "sql_on_san": {
        "db": { "size": "5GB" },
        "log": { "size": "1GB" },
        "temp_db": { "size": "2GB" },
        "igroup_name": "igroup_2",
        "new_igroups": [
          { "name": "igroup_2", "initiators": [ "iqn.2017-01.com.example:foo" ] }
        ]
      }
    }
    ```
    <br/>
3. The following body creates the exact same SQL application, but manually provides all the defaults that were excluded from the previous call. Note: The model of a _sql_on_san_ application documents all these default values.<br/>
    ```
    {
      "name": "app3",
      "svm": { "name": "svm1" },
      "template": { "name": "sql_on_san" },
      "sql_on_san": {
        "os_type": "windows_2008",
        "server_cores_count": 8,
        "db": { "size": "5GB", "storage_service": { "name": "value" } },
        "log": { "size": "1GB", "storage_service": { "name": "value" } },
        "temp_db": { "size": "2GB", "storage_service": { "name": "value" } },
        "igroup_name": "igroup_2",
        "new_igroups": [
          {
            "name": "igroup_2",
            "protocol": "mixed",
            "os_type": "windows",
            "initiators": [ "iqn.a.new.initiator" ]
          }
        ],
        "protection_type": { "local_rpo": "none" }
      }
    }
    ```
### Learn more
* [`DOC /application`](#docs-application-overview)
* [`Asynchronous operations`](#Synchronous_and_asynchronous_operations)
"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="application create")
        async def application_create(
            links: dict = None,
            creation_timestamp: str = None,
            delete_data: bool = None,
            generation: Size = None,
            maxdata_on_san: dict = None,
            mongo_db_on_san: dict = None,
            name: str = None,
            nas: dict = None,
            nvme: dict = None,
            oracle_on_nfs: dict = None,
            oracle_on_san: dict = None,
            oracle_rac_on_nfs: dict = None,
            oracle_rac_on_san: dict = None,
            protection_granularity: str = None,
            rpo: dict = None,
            s3_bucket: dict = None,
            san: dict = None,
            smart_container: bool = None,
            sql_on_san: dict = None,
            sql_on_smb: dict = None,
            state: str = None,
            statistics: dict = None,
            svm: dict = None,
            template: dict = None,
            uuid: str = None,
            vdi_on_nas: dict = None,
            vdi_on_san: dict = None,
            vsi_on_nas: dict = None,
            vsi_on_san: dict = None,
        ) -> ResourceTable:
            """Create an instance of a Application resource

            Args:
                links: 
                creation_timestamp: The time when the application was created.
                delete_data: Should application storage elements be deleted? An application is considered to use storage elements from a shared storage pool. Possible values are 'true' and 'false'. If the value is 'true', the application will be deleted in its entirety. If the value is 'false', the storage elements will be disassociated from the application and preserved. The application will then be deleted.
                generation: The generation number of the application. This indicates which features are supported on the application. For example, generation 1 applications do not support Snapshot copies. Support for Snapshot copies was added at generation 2. Any future generation numbers and their feature set will be documented.
                maxdata_on_san: 
                mongo_db_on_san: 
                name: Application Name. This field is user supplied when the application is created.
                nas: 
                nvme: 
                oracle_on_nfs: 
                oracle_on_san: 
                oracle_rac_on_nfs: 
                oracle_rac_on_san: 
                protection_granularity: Protection granularity determines the scope of Snapshot copy operations for the application. Possible values are \"application\" and \"component\". If the value is \"application\", Snapshot copy operations are performed on the entire application. If the value is \"component\", Snapshot copy operations are performed separately on the application components.
                rpo: 
                s3_bucket: 
                san: 
                smart_container: Identifies if this is a smart container or not.
                sql_on_san: 
                sql_on_smb: 
                state: The state of the application. For full functionality, applications must be in the online state. Other states indicate that the application is in a transient state and not all operations are supported.
                statistics: 
                svm: 
                template: 
                uuid: Application UUID. This field is generated when the application is created.
                vdi_on_nas: 
                vdi_on_san: 
                vsi_on_nas: 
                vsi_on_san: 
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if creation_timestamp is not None:
                kwargs["creation_timestamp"] = creation_timestamp
            if delete_data is not None:
                kwargs["delete_data"] = delete_data
            if generation is not None:
                kwargs["generation"] = generation
            if maxdata_on_san is not None:
                kwargs["maxdata_on_san"] = maxdata_on_san
            if mongo_db_on_san is not None:
                kwargs["mongo_db_on_san"] = mongo_db_on_san
            if name is not None:
                kwargs["name"] = name
            if nas is not None:
                kwargs["nas"] = nas
            if nvme is not None:
                kwargs["nvme"] = nvme
            if oracle_on_nfs is not None:
                kwargs["oracle_on_nfs"] = oracle_on_nfs
            if oracle_on_san is not None:
                kwargs["oracle_on_san"] = oracle_on_san
            if oracle_rac_on_nfs is not None:
                kwargs["oracle_rac_on_nfs"] = oracle_rac_on_nfs
            if oracle_rac_on_san is not None:
                kwargs["oracle_rac_on_san"] = oracle_rac_on_san
            if protection_granularity is not None:
                kwargs["protection_granularity"] = protection_granularity
            if rpo is not None:
                kwargs["rpo"] = rpo
            if s3_bucket is not None:
                kwargs["s3_bucket"] = s3_bucket
            if san is not None:
                kwargs["san"] = san
            if smart_container is not None:
                kwargs["smart_container"] = smart_container
            if sql_on_san is not None:
                kwargs["sql_on_san"] = sql_on_san
            if sql_on_smb is not None:
                kwargs["sql_on_smb"] = sql_on_smb
            if state is not None:
                kwargs["state"] = state
            if statistics is not None:
                kwargs["statistics"] = statistics
            if svm is not None:
                kwargs["svm"] = svm
            if template is not None:
                kwargs["template"] = template
            if uuid is not None:
                kwargs["uuid"] = uuid
            if vdi_on_nas is not None:
                kwargs["vdi_on_nas"] = vdi_on_nas
            if vdi_on_san is not None:
                kwargs["vdi_on_san"] = vdi_on_san
            if vsi_on_nas is not None:
                kwargs["vsi_on_nas"] = vsi_on_nas
            if vsi_on_san is not None:
                kwargs["vsi_on_san"] = vsi_on_san

            resource = Application(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to create Application: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the properties of an application.
### Overview
Similar to creating an application, modification is done using the template properties of an application. The `storage_service`, `size`, and `igroup_name` of an application may be modified.
### `storage_service`
Storage service modifications are processed in place, meaning that the storage can not be moved to a location with more performance headroom to accommodate the request. If the current backing storage of the application is in a location that can support increased performance, the QoS policies associated with the application will be modified to allow it. If not, an error will be returned. A storage service modification to a lower tier of performance is always allowed, but the reverse modification may not be supported if the cluster is over provisioned and the cluster is unlikely to be able to fulfil the original storage service.
### `size`
Size modifications are processed in a variety of ways depending on the type of application. For NAS applications, volumes are grown or new volumes are added. For SAN applications, LUNs are grown, new LUNs are added to existing volumes, or new LUNs are added to new volumes. If new storage elements are created, they can be found using the [`GET /application/applications/{application.uuid}/components`](#operations-application-application_component_collection_get) interface. The creation time of each storage object is included, and the newly created objects will use the same naming scheme as the previous objects. Resize follows the best practices associated with the type of application being expanded. Reducing the size of an application is not supported.
### `igroup_name`
Modification of the igroup name allows an entire application to be mapped from one initiator group to another. Data access will be interrupted as the LUNs are unmapped from the original igroup and remapped to the new one.
### Application state
During a modification, the `state` property of the application updates to indicate `modifying`. In `modifying` state, statistics are not available and Snapshot copy operations are not allowed. If the modification fails, it is possible for the application to be left in an inconsistent state, with the underlying ONTAP storage elements not matching across a component. When this occurs, the application is left in the `modifying` state until the command is either retried and succeeds or a call to restore the original state is successful.
### Examples
1. Change the storage service of the database of the Oracle application to _extreme_ and resize the redo logs to _100GB_.
    ```
    {
      "oracle_on_nfs": {
        "db": {
          "storage_service": {
            "name": "extreme"
          }
        },
        "redo_log": {
          "size": "100GB"
        }
      }
    }
    ```
    <br/>
2. Change the storage service, size, and igroup of a generic application by component name.
    ```
    {
      "san": {
        "application_components": [
          {
            "name": "component1",
            "storage_service": {
              "name": "value"
            }
          },
          {
            "name": "component2",
            "size": "200GB"
          },
          {
            "name": "component3",
            "igroup_name": "igroup5"
          }
        ]
      }
    }
    ```
    <br/>
### Learn more
* [`DOC /application`](#docs-application-overview)
* [`Asynchronous operations`](#Synchronous_and_asynchronous_operations)
"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="application modify")
        async def application_modify(
            creation_timestamp: str = None,
            query_creation_timestamp: str = None,
            delete_data: bool = None,
            query_delete_data: bool = None,
            generation: Size = None,
            query_generation: Size = None,
            name: str = None,
            query_name: str = None,
            protection_granularity: str = None,
            query_protection_granularity: str = None,
            smart_container: bool = None,
            query_smart_container: bool = None,
            state: str = None,
            query_state: str = None,
            uuid: str = None,
            query_uuid: str = None,
        ) -> ResourceTable:
            """Modify an instance of a Application resource

            Args:
                creation_timestamp: The time when the application was created.
                query_creation_timestamp: The time when the application was created.
                delete_data: Should application storage elements be deleted? An application is considered to use storage elements from a shared storage pool. Possible values are 'true' and 'false'. If the value is 'true', the application will be deleted in its entirety. If the value is 'false', the storage elements will be disassociated from the application and preserved. The application will then be deleted.
                query_delete_data: Should application storage elements be deleted? An application is considered to use storage elements from a shared storage pool. Possible values are 'true' and 'false'. If the value is 'true', the application will be deleted in its entirety. If the value is 'false', the storage elements will be disassociated from the application and preserved. The application will then be deleted.
                generation: The generation number of the application. This indicates which features are supported on the application. For example, generation 1 applications do not support Snapshot copies. Support for Snapshot copies was added at generation 2. Any future generation numbers and their feature set will be documented.
                query_generation: The generation number of the application. This indicates which features are supported on the application. For example, generation 1 applications do not support Snapshot copies. Support for Snapshot copies was added at generation 2. Any future generation numbers and their feature set will be documented.
                name: Application Name. This field is user supplied when the application is created.
                query_name: Application Name. This field is user supplied when the application is created.
                protection_granularity: Protection granularity determines the scope of Snapshot copy operations for the application. Possible values are \"application\" and \"component\". If the value is \"application\", Snapshot copy operations are performed on the entire application. If the value is \"component\", Snapshot copy operations are performed separately on the application components.
                query_protection_granularity: Protection granularity determines the scope of Snapshot copy operations for the application. Possible values are \"application\" and \"component\". If the value is \"application\", Snapshot copy operations are performed on the entire application. If the value is \"component\", Snapshot copy operations are performed separately on the application components.
                smart_container: Identifies if this is a smart container or not.
                query_smart_container: Identifies if this is a smart container or not.
                state: The state of the application. For full functionality, applications must be in the online state. Other states indicate that the application is in a transient state and not all operations are supported.
                query_state: The state of the application. For full functionality, applications must be in the online state. Other states indicate that the application is in a transient state and not all operations are supported.
                uuid: Application UUID. This field is generated when the application is created.
                query_uuid: Application UUID. This field is generated when the application is created.
            """

            kwargs = {}
            changes = {}
            if query_creation_timestamp is not None:
                kwargs["creation_timestamp"] = query_creation_timestamp
            if query_delete_data is not None:
                kwargs["delete_data"] = query_delete_data
            if query_generation is not None:
                kwargs["generation"] = query_generation
            if query_name is not None:
                kwargs["name"] = query_name
            if query_protection_granularity is not None:
                kwargs["protection_granularity"] = query_protection_granularity
            if query_smart_container is not None:
                kwargs["smart_container"] = query_smart_container
            if query_state is not None:
                kwargs["state"] = query_state
            if query_uuid is not None:
                kwargs["uuid"] = query_uuid

            if creation_timestamp is not None:
                changes["creation_timestamp"] = creation_timestamp
            if delete_data is not None:
                changes["delete_data"] = delete_data
            if generation is not None:
                changes["generation"] = generation
            if name is not None:
                changes["name"] = name
            if protection_granularity is not None:
                changes["protection_granularity"] = protection_granularity
            if smart_container is not None:
                changes["smart_container"] = smart_container
            if state is not None:
                changes["state"] = state
            if uuid is not None:
                changes["uuid"] = uuid

            if hasattr(Application, "find"):
                resource = Application.find(
                    **kwargs
                )
            else:
                resource = Application()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to modify Application: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an application and all associated data.
### Warning - this deletes it all, including your data
This deletes everything created with the application, including any volumes, LUNs, NFS export policies, CIFS shares, and initiator groups. Initiator groups are only destroyed if they were created as part of an application and are no longer in use by other applications.
### Learn more
* [`DOC /application`](#docs-application-overview)
* [`Asynchronous operations`](#Synchronous_and_asynchronous_operations)
"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="application delete")
        async def application_delete(
            creation_timestamp: str = None,
            delete_data: bool = None,
            generation: Size = None,
            name: str = None,
            protection_granularity: str = None,
            smart_container: bool = None,
            state: str = None,
            uuid: str = None,
        ) -> None:
            """Delete an instance of a Application resource

            Args:
                creation_timestamp: The time when the application was created.
                delete_data: Should application storage elements be deleted? An application is considered to use storage elements from a shared storage pool. Possible values are 'true' and 'false'. If the value is 'true', the application will be deleted in its entirety. If the value is 'false', the storage elements will be disassociated from the application and preserved. The application will then be deleted.
                generation: The generation number of the application. This indicates which features are supported on the application. For example, generation 1 applications do not support Snapshot copies. Support for Snapshot copies was added at generation 2. Any future generation numbers and their feature set will be documented.
                name: Application Name. This field is user supplied when the application is created.
                protection_granularity: Protection granularity determines the scope of Snapshot copy operations for the application. Possible values are \"application\" and \"component\". If the value is \"application\", Snapshot copy operations are performed on the entire application. If the value is \"component\", Snapshot copy operations are performed separately on the application components.
                smart_container: Identifies if this is a smart container or not.
                state: The state of the application. For full functionality, applications must be in the online state. Other states indicate that the application is in a transient state and not all operations are supported.
                uuid: Application UUID. This field is generated when the application is created.
            """

            kwargs = {}
            if creation_timestamp is not None:
                kwargs["creation_timestamp"] = creation_timestamp
            if delete_data is not None:
                kwargs["delete_data"] = delete_data
            if generation is not None:
                kwargs["generation"] = generation
            if name is not None:
                kwargs["name"] = name
            if protection_granularity is not None:
                kwargs["protection_granularity"] = protection_granularity
            if smart_container is not None:
                kwargs["smart_container"] = smart_container
            if state is not None:
                kwargs["state"] = state
            if uuid is not None:
                kwargs["uuid"] = uuid

            if hasattr(Application, "find"):
                resource = Application.find(
                    **kwargs
                )
            else:
                resource = Application()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to delete Application: %s" % err)


