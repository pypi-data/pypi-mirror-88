r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Retrieving storage shelf information
The storage shelf GET API retrieves all of the shelves in the cluster.
<br/>
---
## Examples
### 1) Retrieve a list of shelves from the cluster
#### The following example shows the response with a list of shelves in the cluster:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Shelf

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Shelf.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    Shelf({"uid": "3109174803597886800"}),
    Shelf({"uid": "9237728366621690448"}),
    Shelf({"uid": "9946762738829886800"}),
    Shelf({"uid": "10318311901725526608"}),
    Shelf({"uid": "13477584846688355664"}),
]

```
</div>
</div>

---
### 2) Retrieve a specific shelf from the cluster
#### The following example shows the response of the requested shelf. If there is no shelf with the requested uid, an error is returned.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Shelf

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Shelf(uid=3109174803597886800)
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
Shelf(
    {
        "id": "10",
        "module_type": "iom6",
        "internal": False,
        "paths": [
            {
                "node": {
                    "uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee",
                    "name": "node-1",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/0530d6c1-8c6d-11e8-907f-00a0985a72ee"
                        }
                    },
                },
                "name": "0e",
            },
            {
                "node": {
                    "uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee",
                    "name": "node-1",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/0530d6c1-8c6d-11e8-907f-00a0985a72ee"
                        }
                    },
                },
                "name": "0g",
            },
        ],
        "ports": [
            {
                "id": 0,
                "remote": {"phy": "08", "wwn": "5001086000702488"},
                "cable": {
                    "identifier": "5001086000702488-500a098000c9edbf",
                    "serial_number": "APF16510229807",
                    "length": "2m",
                    "part_number": "112-00430+A0",
                },
                "state": "connected",
                "wwn": "500A098000C9EDBF",
                "module_id": "a",
                "designator": "square",
                "internal": False,
            },
            {
                "id": 1,
                "remote": {"phy": "00", "wwn": "500A098000D5C4BF"},
                "cable": {
                    "identifier": "500a098000d5c4bf-500a098000c9edbf",
                    "serial_number": "APF133917610YT",
                    "length": "0.5-1.0m",
                    "part_number": "112-00176+A0",
                },
                "state": "connected",
                "wwn": "500A098000C9EDBF",
                "module_id": "a",
                "designator": "circle",
                "internal": False,
            },
            {
                "id": 2,
                "remote": {"phy": "08", "wwn": "5001086000702648"},
                "cable": {
                    "identifier": "5001086000702648-500a098004f208bf",
                    "serial_number": "APF16510229540",
                    "length": "2m",
                    "part_number": "112-00430+A0",
                },
                "state": "connected",
                "wwn": "500A098004F208BF",
                "module_id": "b",
                "designator": "square",
                "internal": False,
            },
            {
                "id": 3,
                "remote": {"phy": "00", "wwn": "500A0980062BA33F"},
                "cable": {
                    "identifier": "500a0980062ba33f-500a098004f208bf",
                    "serial_number": "832210017",
                    "length": "0.5-1.0m",
                    "part_number": "112-00176+20",
                },
                "state": "connected",
                "wwn": "500A098004F208BF",
                "module_id": "b",
                "designator": "circle",
                "internal": False,
            },
        ],
        "serial_number": "SHU0954292N0HAH",
        "connection_type": "sas",
        "local": True,
        "state": "ok",
        "model": "DS4246",
        "name": "6.10",
        "uid": "3109174803597886800",
        "bays": [
            {"id": 0, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 1, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 2, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 3, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 4, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 5, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 6, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 7, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 8, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 9, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 10, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 11, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 12, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 13, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 14, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 15, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 16, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 17, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 18, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 19, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 20, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 21, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 22, "state": "ok", "has_disk": True, "type": "single_disk"},
            {"id": 23, "state": "ok", "has_disk": True, "type": "single_disk"},
        ],
        "frus": [
            {
                "type": "module",
                "id": 0,
                "firmware_version": "0191",
                "serial_number": "8001900099",
                "part_number": "111-00690+B2",
                "state": "ok",
            },
            {
                "type": "module",
                "id": 1,
                "firmware_version": "0191",
                "serial_number": "7903785183",
                "part_number": "111-00190+B0",
                "state": "ok",
            },
            {
                "type": "psu",
                "id": 1,
                "firmware_version": "0311",
                "serial_number": "PMW82562007513E",
                "part_number": "0082562-12",
                "state": "ok",
            },
            {
                "type": "psu",
                "id": 2,
                "firmware_version": "0311",
                "serial_number": "PMW825620075138",
                "part_number": "0082562-12",
                "state": "ok",
            },
            {
                "type": "psu",
                "id": 3,
                "firmware_version": "0311",
                "serial_number": "PMW8256200750BA",
                "part_number": "0082562-12",
                "state": "ok",
            },
            {
                "type": "psu",
                "id": 4,
                "firmware_version": "0311",
                "serial_number": "PMW8256200750A2",
                "part_number": "0082562-12",
                "state": "ok",
            },
        ],
        "disk_count": 24,
    }
)

```
</div>
</div>

---
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


__all__ = ["Shelf", "ShelfSchema"]
__pdoc__ = {
    "ShelfSchema.resource": False,
    "Shelf.shelf_show": False,
    "Shelf.shelf_create": False,
    "Shelf.shelf_modify": False,
    "Shelf.shelf_delete": False,
}


class ShelfSchema(ResourceSchema):
    """The fields of the Shelf object"""

    bays = fields.List(fields.Nested("netapp_ontap.models.shelf_bays.ShelfBaysSchema", unknown=EXCLUDE), data_key="bays")
    r""" The bays field of the shelf. """

    connection_type = fields.Str(
        data_key="connection_type",
        validate=enum_validation(['unknown', 'fc', 'sas', 'nvme']),
    )
    r""" The connection_type field of the shelf.

Valid choices:

* unknown
* fc
* sas
* nvme """

    disk_count = Size(
        data_key="disk_count",
    )
    r""" The disk_count field of the shelf.

Example: 12 """

    drawers = fields.List(fields.Nested("netapp_ontap.models.shelf_drawers.ShelfDrawersSchema", unknown=EXCLUDE), data_key="drawers")
    r""" The drawers field of the shelf. """

    frus = fields.List(fields.Nested("netapp_ontap.models.shelf_frus.ShelfFrusSchema", unknown=EXCLUDE), data_key="frus")
    r""" The frus field of the shelf. """

    id = fields.Str(
        data_key="id",
    )
    r""" The id field of the shelf.

Example: 1 """

    internal = fields.Boolean(
        data_key="internal",
    )
    r""" The internal field of the shelf. """

    local = fields.Boolean(
        data_key="local",
    )
    r""" The local field of the shelf. """

    model = fields.Str(
        data_key="model",
    )
    r""" The model field of the shelf.

Example: DS2246 """

    module_type = fields.Str(
        data_key="module_type",
        validate=enum_validation(['unknown', 'iom6', 'iom6e', 'iom12', 'iom12e', 'iom12f', 'nsm100', 'psm3e']),
    )
    r""" The module_type field of the shelf.

Valid choices:

* unknown
* iom6
* iom6e
* iom12
* iom12e
* iom12f
* nsm100
* psm3e """

    name = fields.Str(
        data_key="name",
    )
    r""" The name field of the shelf.

Example: 1.1 """

    paths = fields.List(fields.Nested("netapp_ontap.resources.storage_port.StoragePortSchema", unknown=EXCLUDE), data_key="paths")
    r""" The paths field of the shelf. """

    ports = fields.List(fields.Nested("netapp_ontap.models.shelf_ports.ShelfPortsSchema", unknown=EXCLUDE), data_key="ports")
    r""" The ports field of the shelf. """

    serial_number = fields.Str(
        data_key="serial_number",
    )
    r""" The serial_number field of the shelf.

Example: SHFMS1514000895 """

    state = fields.Str(
        data_key="state",
        validate=enum_validation(['unknown', 'ok', 'error']),
    )
    r""" The state field of the shelf.

Valid choices:

* unknown
* ok
* error """

    uid = fields.Str(
        data_key="uid",
    )
    r""" The uid field of the shelf.

Example: 7777841915827391056 """

    vendor = fields.Nested("netapp_ontap.models.shelf_vendor.ShelfVendorSchema", data_key="vendor", unknown=EXCLUDE)
    r""" The vendor field of the shelf. """

    @property
    def resource(self):
        return Shelf

    gettable_fields = [
        "bays",
        "connection_type",
        "disk_count",
        "drawers",
        "frus",
        "id",
        "internal",
        "local",
        "model",
        "module_type",
        "name",
        "paths.links",
        "paths.name",
        "paths.node",
        "ports",
        "serial_number",
        "state",
        "uid",
        "vendor",
    ]
    """bays,connection_type,disk_count,drawers,frus,id,internal,local,model,module_type,name,paths.links,paths.name,paths.node,ports,serial_number,state,uid,vendor,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in Shelf.get_collection(fields=field)]
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
            raise NetAppRestError("Shelf modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class Shelf(Resource):
    """Allows interaction with Shelf objects on the host"""

    _schema = ShelfSchema
    _path = "/api/storage/shelves"
    _keys = ["uid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of shelves.
### Related ONTAP commands
* `storage shelf show`
* `storage shelf port show`
* `storage shelf drawer show`
### Learn more
* [`DOC /storage/shelves`](#docs-storage-storage_shelves)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="shelf show")
        def shelf_show(
            connection_type: Choices.define(_get_field_list("connection_type"), cache_choices=True, inexact=True)=None,
            disk_count: Choices.define(_get_field_list("disk_count"), cache_choices=True, inexact=True)=None,
            id: Choices.define(_get_field_list("id"), cache_choices=True, inexact=True)=None,
            internal: Choices.define(_get_field_list("internal"), cache_choices=True, inexact=True)=None,
            local: Choices.define(_get_field_list("local"), cache_choices=True, inexact=True)=None,
            model: Choices.define(_get_field_list("model"), cache_choices=True, inexact=True)=None,
            module_type: Choices.define(_get_field_list("module_type"), cache_choices=True, inexact=True)=None,
            name: Choices.define(_get_field_list("name"), cache_choices=True, inexact=True)=None,
            serial_number: Choices.define(_get_field_list("serial_number"), cache_choices=True, inexact=True)=None,
            state: Choices.define(_get_field_list("state"), cache_choices=True, inexact=True)=None,
            uid: Choices.define(_get_field_list("uid"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["connection_type", "disk_count", "id", "internal", "local", "model", "module_type", "name", "serial_number", "state", "uid", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of Shelf resources

            Args:
                connection_type: 
                disk_count: 
                id: 
                internal: 
                local: 
                model: 
                module_type: 
                name: 
                serial_number: 
                state: 
                uid: 
            """

            kwargs = {}
            if connection_type is not None:
                kwargs["connection_type"] = connection_type
            if disk_count is not None:
                kwargs["disk_count"] = disk_count
            if id is not None:
                kwargs["id"] = id
            if internal is not None:
                kwargs["internal"] = internal
            if local is not None:
                kwargs["local"] = local
            if model is not None:
                kwargs["model"] = model
            if module_type is not None:
                kwargs["module_type"] = module_type
            if name is not None:
                kwargs["name"] = name
            if serial_number is not None:
                kwargs["serial_number"] = serial_number
            if state is not None:
                kwargs["state"] = state
            if uid is not None:
                kwargs["uid"] = uid
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return Shelf.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves a collection of shelves.
### Related ONTAP commands
* `storage shelf show`
* `storage shelf port show`
* `storage shelf drawer show`
### Learn more
* [`DOC /storage/shelves`](#docs-storage-storage_shelves)
"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of shelves.
### Related ONTAP commands
* `storage shelf show`
* `storage shelf port show`
* `storage shelf drawer show`
### Learn more
* [`DOC /storage/shelves`](#docs-storage-storage_shelves)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific shelf.
### Related ONTAP commands
* `storage shelf show`
* `storage shelf port show`
* `storage shelf drawer show`
### Learn more
* [`DOC /storage/shelves`](#docs-storage-storage_shelves)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





