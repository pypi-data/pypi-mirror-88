r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Updating storage aggregates
The PATCH operation is used to modify properties of the aggregate. There are several properties that can be modified on an aggregate. Only one property can be modified for each PATCH request.
PATCH operations on the aggregate's disk count will be blocked while one or more nodes in the cluster are simulating or implementing automatic aggregate creation.</br>
The following is a list of properties that can be modified using the PATCH operation including a brief description for each:

* name - This property can be changed to rename the aggregate.
* node.name and node.uuid - Either property can be updated in order to relocate the aggregate to a different node in the cluster.
* block_storage.mirror.enabled - This property can be changed from 'false' to 'true' in order to mirror the aggregate, if the system is capable of doing so.
* block_storage.primary.disk_count - This property can be updated to increase the number of disks in an aggregate.
* block_storage.primary.raid_size - This property can be updated to set the desired RAID size.
* block_storage.primary.raid_type - This property can be updated to set the desired RAID type.
* cloud_storage.tiering_fullness_threshold - This property can be updated to set the desired tiering fullness threshold if using FabricPool.
* data_encryption.software_encryption_enabled - This property enables or disables NAE on the aggregate.
### Aggregate expansion
The PATCH operation also supports automatically expanding an aggregate based on the spare disks which are present within the system. Running PATCH with the query "auto_provision_policy" set to "expand" starts the recommended expansion job. In order to see the expected change in capacity before starting the job, call GET on an aggregate instance with the query "auto_provision_policy" set to "expand".
### Manual simulated aggregate expansion
The PATCH operation also supports simulated manual expansion of an aggregate.
Running PATCH with the query "simulate" set to "true" and "block_storage.primary.disk_count" set to the final disk count will start running the prechecks associated with expanding the aggregate to the proposed size.
The response body will include information on how many disks the aggregate can be expanded to, any associated warnings, along with the proposed final size of the aggregate.
## Deleting storage aggregates
If volumes exist on an aggregate, they must be deleted or moved before the aggregate can be deleted.
See the /storage/volumes API for details on moving or deleting volumes.
---
## Examples
### Retrieving a specific aggregate from the cluster
The following example shows the response of the requested aggregate. If there is no aggregate with the requested UUID, an error is returned.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="870dd9f2-bdfa-4167-b692-57d1cec874d4")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
Aggregate(
    {
        "data_encryption": {
            "drive_protection_enabled": False,
            "software_encryption_enabled": False,
        },
        "block_storage": {
            "plexes": [{"name": "plex0"}],
            "mirror": {"enabled": False, "state": "unmirrored"},
            "primary": {
                "disk_type": "ssd",
                "raid_size": 24,
                "checksum_style": "block",
                "disk_class": "solid_state",
                "raid_type": "raid_dp",
                "disk_count": 6,
            },
            "hybrid_cache": {"enabled": False},
        },
        "cloud_storage": {"attach_eligible": False},
        "home_node": {"uuid": "caf95bec-f801-11e8-8af9-005056bbe5c1", "name": "node-1"},
        "node": {"uuid": "caf95bec-f801-11e8-8af9-005056bbe5c1", "name": "node-1"},
        "snaplock_type": "non_snaplock",
        "space": {
            "efficiency_without_snapshots": {
                "logical_used": 737280,
                "ratio": 1.0,
                "savings": 0,
            },
            "block_storage": {
                "available": 191942656,
                "size": 235003904,
                "used": 43061248,
                "full_threshold_percent": 98,
            },
            "cloud_storage": {"used": 0},
            "efficiency": {
                "logical_used": 1646350,
                "ratio": 6.908119720880661,
                "savings": 1408029,
            },
        },
        "state": "online",
        "name": "test1",
        "create_time": "2018-12-04T15:40:38-05:00",
        "uuid": "19425837-f2fa-4a9f-8f01-712f626c983c",
    }
)

```
</div>
</div>

### Retrieving statistics and metric for an aggregate
In this example, the API returns the "statistics" and "metric" properties for the aggregate requested.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="538bf337-1b2c-11e8-bad0-005056b48388")
    resource.get(fields="statistics,metric")
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
Aggregate(
    {
        "statistics": {
            "status": "ok",
            "iops_raw": {
                "write": 1137230,
                "total": 3052032,
                "other": 1586535,
                "read": 328267,
            },
            "throughput_raw": {
                "write": 63771742208,
                "total": 213063348224,
                "other": 146185560064,
                "read": 3106045952,
            },
            "timestamp": "2019-07-08T22:17:09+00:00",
            "latency_raw": {
                "write": 313354426,
                "total": 844628724,
                "other": 477201985,
                "read": 54072313,
            },
        },
        "name": "aggr4",
        "metric": {
            "duration": "PT15S",
            "latency": {"write": 230, "total": 124, "other": 123, "read": 149},
            "status": "ok",
            "throughput": {
                "write": 840226,
                "total": 194141115,
                "other": 193293789,
                "read": 7099,
            },
            "iops": {"write": 17, "total": 11682, "other": 11663, "read": 1},
            "timestamp": "2019-07-08T22:16:45+00:00",
        },
        "uuid": "538bf337-1b2c-11e8-bad0-005056b48388",
    }
)

```
</div>
</div>

For more information and examples on viewing historical performance metrics for any given aggregate, see [`DOC /storage/aggregates/{uuid}/metrics`](#docs-storage-storage_aggregates_{uuid}_metrics)
### Simulating aggregate expansion
The following example shows the response for a simulated data aggregate expansion based on the values of the 'block_storage.primary.disk_count' attribute passed in.
The query does not modify the existing aggregate but returns how the aggregate will look after the expansion along with any associated warnings.
Simulated data aggregate expansion will be blocked while one or more nodes in the cluster are simulating or implementing automatic aggregate creation.
This will be reflected in the following attributes:

* space.block_storage.size - Total usable space in bytes, not including WAFL reserve and aggregate Snapshot copy reserve.
* block_storage.primary.disk_count - Number of disks that could be used to create the aggregate.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="cae60cfe-deae-42bd-babb-ef437d118314")
    resource.block_storage.primary.disk_count = 14
    resource.patch(hydrate=True, simulate=True)

```

### Retrieving a recommendation for an aggregate expansion
The following example shows the response with the recommended data aggregate expansion based on what disks are present within the system.
The query does not modify the existing aggregate but returns how the aggregate will look after the expansion. The recommendation will be reflected in the attributes - 'space.block_storage.size' and 'block_storage.primary.disk_count'.
Recommended data aggregate expansion will be blocked while one or more nodes in the cluster are simulating or implementing automatic aggregate creation.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="cae60cfe-deae-42bd-babb-ef437d118314")
    resource.get(auto_provision_policy="expand")
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
Aggregate(
    {
        "block_storage": {
            "mirror": {"enabled": False},
            "primary": {
                "disk_type": "ssd",
                "disk_class": "solid_state",
                "raid_type": "raid_dp",
                "disk_count": 23,
            },
            "hybrid_cache": {"enabled": False},
        },
        "node": {
            "uuid": "4046dda8-f802-11e8-8f6d-005056bb2030",
            "name": "node-2",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/4046dda8-f802-11e8-8f6d-005056bb2030"
                }
            },
        },
        "space": {"block_storage": {"size": 1116180480}},
        "_links": {
            "self": {
                "href": "/api/storage/aggregates/cae60cfe-deae-42bd-babb-ef437d118314"
            }
        },
        "name": "node_2_SSD_1",
        "uuid": "cae60cfe-deae-42bd-babb-ef437d118314",
    }
)

```
</div>
</div>

### Updating an aggregate in the cluster
The following example shows the workflow of adding disks to the aggregate.<br>
Step 1: Check the current disk count on the aggregate.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="19425837-f2fa-4a9f-8f01-712f626c983c")
    resource.get(fields="block_storage.primary.disk_count")
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
Aggregate(
    {
        "block_storage": {"primary": {"disk_count": 6}},
        "name": "test1",
        "uuid": "19425837-f2fa-4a9f-8f01-712f626c983c",
    }
)

```
</div>
</div>

Step 2: Update the aggregate with the new disk count in 'block_storage.primary.disk_count'. The response to PATCH is a job unless the request is invalid.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="19425837-f2fa-4a9f-8f01-712f626c983c")
    resource.block_storage.primary.disk_count = 8
    resource.patch()

```

Step 3: Wait for the job to finish, then call GET to see the reflected change.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="19425837-f2fa-4a9f-8f01-712f626c983c")
    resource.get(fields="block_storage.primary.disk_count")
    print(resource)

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
Aggregate(
    {
        "block_storage": {"primary": {"disk_count": 8}},
        "name": "test1",
        "uuid": "19425837-f2fa-4a9f-8f01-712f626c983c",
    }
)

```
</div>
</div>

The following example shows the workflow to enable software encryption on an aggregate.<br>
Step 1: Check the current software encryption status of the aggregate.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="f3aafdc6-be35-4d93-9590-5a402bffbe4b")
    resource.get(fields="data_encryption.software_encryption_enabled")
    print(resource)

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
Aggregate(
    {
        "data_encryption": {"software_encryption_enabled": False},
        "name": "aggr5",
        "uuid": "f3aafdc6-be35-4d93-9590-5a402bffbe4b",
    }
)

```
</div>
</div>

Step 2: Update the aggregate with the encryption status in 'data_encryption.software_encryption_enabled'. The response to PATCH is a job unless the request is invalid.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="f3aafdc6-be35-4d93-9590-5a402bffbe4b")
    resource.data_encryption.software_encryption_enabled = True
    resource.patch()

```

Step 3: Wait for the job to finish, then call GET to see the reflected change.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Aggregate(uuid="f3aafdc6-be35-4d93-9590-5a402bffbe4b")
    resource.get(fields="data_encryption.software_encryption_enabled")
    print(resource)

```
<div class="try_it_out">
<input id="example9_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example9_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example9_result" class="try_it_out_content">
```
Aggregate(
    {
        "data_encryption": {"software_encryption_enabled": True},
        "name": "aggr5",
        "uuid": "f3aafdc6-be35-4d93-9590-5a402bffbe4b",
    }
)

```
</div>
</div>

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


__all__ = ["Aggregate", "AggregateSchema"]
__pdoc__ = {
    "AggregateSchema.resource": False,
    "Aggregate.aggregate_show": False,
    "Aggregate.aggregate_create": False,
    "Aggregate.aggregate_modify": False,
    "Aggregate.aggregate_delete": False,
}


class AggregateSchema(ResourceSchema):
    """The fields of the Aggregate object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the aggregate. """

    block_storage = fields.Nested("netapp_ontap.models.aggregate_block_storage.AggregateBlockStorageSchema", data_key="block_storage", unknown=EXCLUDE)
    r""" The block_storage field of the aggregate. """

    cloud_storage = fields.Nested("netapp_ontap.models.aggregate_cloud_storage.AggregateCloudStorageSchema", data_key="cloud_storage", unknown=EXCLUDE)
    r""" The cloud_storage field of the aggregate. """

    create_time = fields.Str(
        data_key="create_time",
    )
    r""" Timestamp of aggregate creation

Example: 2018-01-01T16:00:00.000+0000 """

    data_encryption = fields.Nested("netapp_ontap.models.aggregate_data_encryption.AggregateDataEncryptionSchema", data_key="data_encryption", unknown=EXCLUDE)
    r""" The data_encryption field of the aggregate. """

    dr_home_node = fields.Nested("netapp_ontap.models.dr_node.DrNodeSchema", data_key="dr_home_node", unknown=EXCLUDE)
    r""" The dr_home_node field of the aggregate. """

    home_node = fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="home_node", unknown=EXCLUDE)
    r""" The home_node field of the aggregate. """

    inactive_data_reporting = fields.Nested("netapp_ontap.models.aggregate_inactive_data_reporting.AggregateInactiveDataReportingSchema", data_key="inactive_data_reporting", unknown=EXCLUDE)
    r""" The inactive_data_reporting field of the aggregate. """

    metric = fields.Nested("netapp_ontap.resources.performance_metric.PerformanceMetricSchema", data_key="metric", unknown=EXCLUDE)
    r""" The metric field of the aggregate. """

    name = fields.Str(
        data_key="name",
    )
    r""" Aggregate name

Example: node1_aggr_1 """

    node = fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE)
    r""" The node field of the aggregate. """

    snaplock_type = fields.Str(
        data_key="snaplock_type",
        validate=enum_validation(['non_snaplock', 'compliance', 'enterprise']),
    )
    r""" SnapLock type

Valid choices:

* non_snaplock
* compliance
* enterprise """

    space = fields.Nested("netapp_ontap.models.aggregate_space.AggregateSpaceSchema", data_key="space", unknown=EXCLUDE)
    r""" The space field of the aggregate. """

    state = fields.Str(
        data_key="state",
        validate=enum_validation(['online', 'onlining', 'offline', 'offlining', 'relocating', 'unmounted', 'restricted', 'inconsistent', 'failed', 'unknown']),
    )
    r""" Operational state of the aggregate

Valid choices:

* online
* onlining
* offline
* offlining
* relocating
* unmounted
* restricted
* inconsistent
* failed
* unknown """

    statistics = fields.Nested("netapp_ontap.models.performance_metric_raw.PerformanceMetricRawSchema", data_key="statistics", unknown=EXCLUDE)
    r""" The statistics field of the aggregate. """

    uuid = fields.Str(
        data_key="uuid",
    )
    r""" Aggregate UUID """

    @property
    def resource(self):
        return Aggregate

    gettable_fields = [
        "links",
        "block_storage",
        "create_time",
        "data_encryption",
        "dr_home_node.name",
        "dr_home_node.uuid",
        "home_node.links",
        "home_node.name",
        "home_node.uuid",
        "inactive_data_reporting",
        "metric",
        "name",
        "node.links",
        "node.name",
        "node.uuid",
        "snaplock_type",
        "space",
        "state",
        "statistics.iops_raw",
        "statistics.latency_raw",
        "statistics.status",
        "statistics.throughput_raw",
        "statistics.timestamp",
        "uuid",
    ]
    """links,block_storage,create_time,data_encryption,dr_home_node.name,dr_home_node.uuid,home_node.links,home_node.name,home_node.uuid,inactive_data_reporting,metric,name,node.links,node.name,node.uuid,snaplock_type,space,state,statistics.iops_raw,statistics.latency_raw,statistics.status,statistics.throughput_raw,statistics.timestamp,uuid,"""

    patchable_fields = [
        "block_storage",
        "cloud_storage",
        "data_encryption",
        "dr_home_node.name",
        "dr_home_node.uuid",
        "home_node.name",
        "home_node.uuid",
        "inactive_data_reporting",
        "name",
        "node.name",
        "node.uuid",
        "space",
    ]
    """block_storage,cloud_storage,data_encryption,dr_home_node.name,dr_home_node.uuid,home_node.name,home_node.uuid,inactive_data_reporting,name,node.name,node.uuid,space,"""

    postable_fields = [
        "block_storage",
        "data_encryption",
        "dr_home_node.name",
        "dr_home_node.uuid",
        "home_node.name",
        "home_node.uuid",
        "inactive_data_reporting",
        "name",
        "node.name",
        "node.uuid",
        "snaplock_type",
        "space",
    ]
    """block_storage,data_encryption,dr_home_node.name,dr_home_node.uuid,home_node.name,home_node.uuid,inactive_data_reporting,name,node.name,node.uuid,snaplock_type,space,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in Aggregate.get_collection(fields=field)]
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
            raise NetAppRestError("Aggregate modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class Aggregate(Resource):
    """Allows interaction with Aggregate objects on the host"""

    _schema = AggregateSchema
    _path = "/api/storage/aggregates"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the collection of aggregates for the entire cluster.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `metric.*`
* `space.block_storage.inactive_user_data`
* `space.footprint`
* `statistics.*`
### Related ONTAP commands
* `storage aggregate show`

### Learn more
* [`DOC /storage/aggregates`](#docs-storage-storage_aggregates)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="aggregate show")
        def aggregate_show(
            create_time: Choices.define(_get_field_list("create_time"), cache_choices=True, inexact=True)=None,
            name: Choices.define(_get_field_list("name"), cache_choices=True, inexact=True)=None,
            snaplock_type: Choices.define(_get_field_list("snaplock_type"), cache_choices=True, inexact=True)=None,
            state: Choices.define(_get_field_list("state"), cache_choices=True, inexact=True)=None,
            uuid: Choices.define(_get_field_list("uuid"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["create_time", "name", "snaplock_type", "state", "uuid", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of Aggregate resources

            Args:
                create_time: Timestamp of aggregate creation
                name: Aggregate name
                snaplock_type: SnapLock type
                state: Operational state of the aggregate
                uuid: Aggregate UUID
            """

            kwargs = {}
            if create_time is not None:
                kwargs["create_time"] = create_time
            if name is not None:
                kwargs["name"] = name
            if snaplock_type is not None:
                kwargs["snaplock_type"] = snaplock_type
            if state is not None:
                kwargs["state"] = state
            if uuid is not None:
                kwargs["uuid"] = uuid
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return Aggregate.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves the collection of aggregates for the entire cluster.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `metric.*`
* `space.block_storage.inactive_user_data`
* `space.footprint`
* `statistics.*`
### Related ONTAP commands
* `storage aggregate show`

### Learn more
* [`DOC /storage/aggregates`](#docs-storage-storage_aggregates)"""
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
        r"""Updates the aggregate specified by the UUID with the properties in the body. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate add-disks`
* `storage aggregate mirror`
* `storage aggregate modify`
* `storage aggregate relocation start`
* `storage aggregate rename`

### Learn more
* [`DOC /storage/aggregates/{uuid}`](#docs-storage-storage_aggregates_{uuid})"""
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
        r"""Deletes the aggregate specified by the UUID. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate delete`

### Learn more
* [`DOC /storage/aggregates/{uuid}`](#docs-storage-storage_aggregates_{uuid})"""
        return super()._delete_collection(*args, body=body, connection=connection, **kwargs)

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the collection of aggregates for the entire cluster.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `metric.*`
* `space.block_storage.inactive_user_data`
* `space.footprint`
* `statistics.*`
### Related ONTAP commands
* `storage aggregate show`

### Learn more
* [`DOC /storage/aggregates`](#docs-storage-storage_aggregates)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the aggregate specified by the UUID. The recommend query cannot be used for this operation.
### Expensive properties
There is an added cost to retrieving values for these properties. They are not included by default in GET results and must be explicitly requested using the `fields` query parameter. See [`Requesting specific fields`](#Requesting_specific_fields) to learn more.
* `metric.*`
* `space.block_storage.inactive_user_data`
* `space.footprint`
* `statistics.*`
### Related ONTAP commands
* `storage aggregate show`

### Learn more
* [`DOC /storage/aggregates/{uuid}`](#docs-storage-storage_aggregates_{uuid})"""
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
        r"""Automatically creates aggregates based on an optimal layout recommended by the system. Alternatively, properties can be provided to create an aggregate according to the requested specification. This request starts a job and returns a link to that job.
POST operations will be blocked while one or more nodes in the cluster are simulating or implementing automatic aggregate creation.
### Required properties
Properties are not required for this API. The following properties are only required if you want to specify properties for aggregate creation:
* `name` - Name of the aggregate.
* `node.name` or `node.uuid` - Node on which the aggregate will be created.
* `block_storage.primary.disk_count` - Number of disks to be used to create the aggregate.
### Default values
If not specified in POST, the following default values are assigned. The remaining unspecified properties will receive system dependent default values.
* `block_storage.mirror.enabled` - _false_
* `snaplock_type` - _non_snaplock_
### Related ONTAP commands
* `storage aggregate auto-provision`
* `storage aggregate create`
### Example:
```
POST /api/storage/aggregates {"node": {"name": "node1"}, "name": "test", "block_storage": {"primary": {"disk_count": "10"}}}
```

### Learn more
* [`DOC /storage/aggregates`](#docs-storage-storage_aggregates)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="aggregate create")
        async def aggregate_create(
            links: dict = None,
            block_storage: dict = None,
            cloud_storage: dict = None,
            create_time: str = None,
            data_encryption: dict = None,
            dr_home_node: dict = None,
            home_node: dict = None,
            inactive_data_reporting: dict = None,
            metric: dict = None,
            name: str = None,
            node: dict = None,
            snaplock_type: str = None,
            space: dict = None,
            state: str = None,
            statistics: dict = None,
            uuid: str = None,
        ) -> ResourceTable:
            """Create an instance of a Aggregate resource

            Args:
                links: 
                block_storage: 
                cloud_storage: 
                create_time: Timestamp of aggregate creation
                data_encryption: 
                dr_home_node: 
                home_node: 
                inactive_data_reporting: 
                metric: 
                name: Aggregate name
                node: 
                snaplock_type: SnapLock type
                space: 
                state: Operational state of the aggregate
                statistics: 
                uuid: Aggregate UUID
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if block_storage is not None:
                kwargs["block_storage"] = block_storage
            if cloud_storage is not None:
                kwargs["cloud_storage"] = cloud_storage
            if create_time is not None:
                kwargs["create_time"] = create_time
            if data_encryption is not None:
                kwargs["data_encryption"] = data_encryption
            if dr_home_node is not None:
                kwargs["dr_home_node"] = dr_home_node
            if home_node is not None:
                kwargs["home_node"] = home_node
            if inactive_data_reporting is not None:
                kwargs["inactive_data_reporting"] = inactive_data_reporting
            if metric is not None:
                kwargs["metric"] = metric
            if name is not None:
                kwargs["name"] = name
            if node is not None:
                kwargs["node"] = node
            if snaplock_type is not None:
                kwargs["snaplock_type"] = snaplock_type
            if space is not None:
                kwargs["space"] = space
            if state is not None:
                kwargs["state"] = state
            if statistics is not None:
                kwargs["statistics"] = statistics
            if uuid is not None:
                kwargs["uuid"] = uuid

            resource = Aggregate(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to create Aggregate: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the aggregate specified by the UUID with the properties in the body. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate add-disks`
* `storage aggregate mirror`
* `storage aggregate modify`
* `storage aggregate relocation start`
* `storage aggregate rename`

### Learn more
* [`DOC /storage/aggregates/{uuid}`](#docs-storage-storage_aggregates_{uuid})"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="aggregate modify")
        async def aggregate_modify(
            create_time: str = None,
            query_create_time: str = None,
            name: str = None,
            query_name: str = None,
            snaplock_type: str = None,
            query_snaplock_type: str = None,
            state: str = None,
            query_state: str = None,
            uuid: str = None,
            query_uuid: str = None,
        ) -> ResourceTable:
            """Modify an instance of a Aggregate resource

            Args:
                create_time: Timestamp of aggregate creation
                query_create_time: Timestamp of aggregate creation
                name: Aggregate name
                query_name: Aggregate name
                snaplock_type: SnapLock type
                query_snaplock_type: SnapLock type
                state: Operational state of the aggregate
                query_state: Operational state of the aggregate
                uuid: Aggregate UUID
                query_uuid: Aggregate UUID
            """

            kwargs = {}
            changes = {}
            if query_create_time is not None:
                kwargs["create_time"] = query_create_time
            if query_name is not None:
                kwargs["name"] = query_name
            if query_snaplock_type is not None:
                kwargs["snaplock_type"] = query_snaplock_type
            if query_state is not None:
                kwargs["state"] = query_state
            if query_uuid is not None:
                kwargs["uuid"] = query_uuid

            if create_time is not None:
                changes["create_time"] = create_time
            if name is not None:
                changes["name"] = name
            if snaplock_type is not None:
                changes["snaplock_type"] = snaplock_type
            if state is not None:
                changes["state"] = state
            if uuid is not None:
                changes["uuid"] = uuid

            if hasattr(Aggregate, "find"):
                resource = Aggregate.find(
                    **kwargs
                )
            else:
                resource = Aggregate()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to modify Aggregate: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes the aggregate specified by the UUID. This request starts a job and returns a link to that job.
### Related ONTAP commands
* `storage aggregate delete`

### Learn more
* [`DOC /storage/aggregates/{uuid}`](#docs-storage-storage_aggregates_{uuid})"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="aggregate delete")
        async def aggregate_delete(
            create_time: str = None,
            name: str = None,
            snaplock_type: str = None,
            state: str = None,
            uuid: str = None,
        ) -> None:
            """Delete an instance of a Aggregate resource

            Args:
                create_time: Timestamp of aggregate creation
                name: Aggregate name
                snaplock_type: SnapLock type
                state: Operational state of the aggregate
                uuid: Aggregate UUID
            """

            kwargs = {}
            if create_time is not None:
                kwargs["create_time"] = create_time
            if name is not None:
                kwargs["name"] = name
            if snaplock_type is not None:
                kwargs["snaplock_type"] = snaplock_type
            if state is not None:
                kwargs["state"] = state
            if uuid is not None:
                kwargs["uuid"] = uuid

            if hasattr(Aggregate, "find"):
                resource = Aggregate.find(
                    **kwargs
                )
            else:
                resource = Aggregate()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to delete Aggregate: %s" % err)


