r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Retrieving storage port information
The storage port GET API retrieves all of the storage ports in the cluster.
<br/>
---
## Examples
### 1) Retrieve a list of storage ports from the cluster
#### The following example shows the response with a list of storage ports in the cluster:
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StoragePort

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(StoragePort.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    StoragePort(
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
            "name": "0a",
        }
    ),
    StoragePort(
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
            "name": "0b",
        }
    ),
    StoragePort(
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
            "name": "0c",
        }
    ),
    StoragePort(
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
            "name": "0d",
        }
    ),
    StoragePort(
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
        }
    ),
    StoragePort(
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
            "name": "0f",
        }
    ),
    StoragePort(
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
        }
    ),
]

```
</div>
</div>

---
### 2) Retrieve a specific storage port from the cluster
#### The following example shows the response of the requested storage port. If there is no storage port with the requested node uuid and name, an error is returned.
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import StoragePort

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = StoragePort(
        name="0a", **{"node.uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
StoragePort(
    {
        "cable": {
            "identifier": "500a0980066e2c01-500a098003633df0",
            "serial_number": "629230774",
            "length": "0.5m",
            "part_number": "112-00429+A0",
        },
        "node": {
            "uuid": "0530d6c1-8c6d-11e8-907f-00a0985a72ee",
            "name": "node-1",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/0530d6c1-8c6d-11e8-907f-00a0985a72ee"
                }
            },
        },
        "state": "online",
        "name": "0a",
        "wwn": "500a098003633df0",
        "description": "SAS Host Adapter 0a (PMC-Sierra PM8001 rev. C)",
        "speed": 6.0,
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


__all__ = ["StoragePort", "StoragePortSchema"]
__pdoc__ = {
    "StoragePortSchema.resource": False,
    "StoragePort.storage_port_show": False,
    "StoragePort.storage_port_create": False,
    "StoragePort.storage_port_modify": False,
    "StoragePort.storage_port_delete": False,
}


class StoragePortSchema(ResourceSchema):
    """The fields of the StoragePort object"""

    board_name = fields.Str(
        data_key="board_name",
    )
    r""" The board_name field of the storage_port. """

    cable = fields.Nested("netapp_ontap.models.shelf_cable.ShelfCableSchema", data_key="cable", unknown=EXCLUDE)
    r""" The cable field of the storage_port. """

    description = fields.Str(
        data_key="description",
    )
    r""" The description field of the storage_port.

Example: SAS Host Adapter 2a (PMC-Sierra PM8072 rev. C) """

    error = fields.Nested("netapp_ontap.models.storage_port_error.StoragePortErrorSchema", data_key="error", unknown=EXCLUDE)
    r""" The error field of the storage_port. """

    mac_address = fields.Str(
        data_key="mac_address",
    )
    r""" The mac_address field of the storage_port. """

    mode = fields.Str(
        data_key="mode",
        validate=enum_validation(['network', 'storage']),
    )
    r""" Operational mode of a non-dedicated Ethernet port

Valid choices:

* network
* storage """

    name = fields.Str(
        data_key="name",
    )
    r""" The name field of the storage_port.

Example: 2a """

    node = fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE)
    r""" The node field of the storage_port. """

    part_number = fields.Str(
        data_key="part_number",
    )
    r""" The part_number field of the storage_port.

Example: 111-03801 """

    serial_number = fields.Str(
        data_key="serial_number",
    )
    r""" The serial_number field of the storage_port.

Example: 7A2463CC45B """

    speed = fields.Number(
        data_key="speed",
    )
    r""" Operational port speed in Gbps

Example: 6.0 """

    state = fields.Str(
        data_key="state",
        validate=enum_validation(['online', 'offline', 'error']),
    )
    r""" The state field of the storage_port.

Valid choices:

* online
* offline
* error """

    wwn = fields.Str(
        data_key="wwn",
    )
    r""" World Wide Name

Example: 50000d1703544b80 """

    @property
    def resource(self):
        return StoragePort

    gettable_fields = [
        "board_name",
        "cable",
        "description",
        "error",
        "mac_address",
        "mode",
        "name",
        "node.links",
        "node.name",
        "node.uuid",
        "part_number",
        "serial_number",
        "speed",
        "state",
        "wwn",
    ]
    """board_name,cable,description,error,mac_address,mode,name,node.links,node.name,node.uuid,part_number,serial_number,speed,state,wwn,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in StoragePort.get_collection(fields=field)]
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
            raise NetAppRestError("StoragePort modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class StoragePort(Resource):
    """Allows interaction with StoragePort objects on the host"""

    _schema = StoragePortSchema
    _path = "/api/storage/ports"
    _keys = ["node.uuid", "name"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of storage ports.
### Related ONTAP commands
* `storage port show`
### Learn more
* [`DOC /storage/ports`](#docs-storage-storage_ports)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="storage port show")
        def storage_port_show(
            board_name: Choices.define(_get_field_list("board_name"), cache_choices=True, inexact=True)=None,
            description: Choices.define(_get_field_list("description"), cache_choices=True, inexact=True)=None,
            mac_address: Choices.define(_get_field_list("mac_address"), cache_choices=True, inexact=True)=None,
            mode: Choices.define(_get_field_list("mode"), cache_choices=True, inexact=True)=None,
            name: Choices.define(_get_field_list("name"), cache_choices=True, inexact=True)=None,
            part_number: Choices.define(_get_field_list("part_number"), cache_choices=True, inexact=True)=None,
            serial_number: Choices.define(_get_field_list("serial_number"), cache_choices=True, inexact=True)=None,
            speed: Choices.define(_get_field_list("speed"), cache_choices=True, inexact=True)=None,
            state: Choices.define(_get_field_list("state"), cache_choices=True, inexact=True)=None,
            wwn: Choices.define(_get_field_list("wwn"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["board_name", "description", "mac_address", "mode", "name", "part_number", "serial_number", "speed", "state", "wwn", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of StoragePort resources

            Args:
                board_name: 
                description: 
                mac_address: 
                mode: Operational mode of a non-dedicated Ethernet port
                name: 
                part_number: 
                serial_number: 
                speed: Operational port speed in Gbps
                state: 
                wwn: World Wide Name
            """

            kwargs = {}
            if board_name is not None:
                kwargs["board_name"] = board_name
            if description is not None:
                kwargs["description"] = description
            if mac_address is not None:
                kwargs["mac_address"] = mac_address
            if mode is not None:
                kwargs["mode"] = mode
            if name is not None:
                kwargs["name"] = name
            if part_number is not None:
                kwargs["part_number"] = part_number
            if serial_number is not None:
                kwargs["serial_number"] = serial_number
            if speed is not None:
                kwargs["speed"] = speed
            if state is not None:
                kwargs["state"] = state
            if wwn is not None:
                kwargs["wwn"] = wwn
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return StoragePort.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves a collection of storage ports.
### Related ONTAP commands
* `storage port show`
### Learn more
* [`DOC /storage/ports`](#docs-storage-storage_ports)
"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of storage ports.
### Related ONTAP commands
* `storage port show`
### Learn more
* [`DOC /storage/ports`](#docs-storage-storage_ports)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific storage port.
### Related ONTAP commands
* `storage port show`
### Learn more
* [`DOC /storage/ports`](#docs-storage-storage_ports)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





