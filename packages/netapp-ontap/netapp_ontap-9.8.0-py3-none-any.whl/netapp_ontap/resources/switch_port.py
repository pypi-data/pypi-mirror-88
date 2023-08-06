r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
This API can be used to get the port information for an ethernet switch used in a cluster or storage networks. This API supports GET only. The GET operation returns a list of ports with status and configuration information.
## Examples
### Retrieving the ports for ethernet switches
The following example retrieves the ethernet switch ports for all the ethernet switches used for cluster and/or storage networks.
Note that if the <i>fields=*</i> parameter is not specified, the fields in-octets, in-errors, in-discards, out-octets, out-errors, out-discards, interface-number, unique-name, mac-address are not returned.
Filters can be added on the fields to limit the results.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SwitchPort

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(SwitchPort.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    SwitchPort(
        {
            "vlan_id": [1, 17, 18, 92],
            "identity": {"number": 1, "index": 436207616, "name": "Ethernet1/1"},
            "speed": 100000,
            "statistics": {
                "transmit_raw": {"errors": 0, "discards": 0, "packets": 206717534},
                "receive_raw": {"errors": 0, "discards": 0, "packets": 1616467751},
            },
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/switch/ports/RTP-CS01-510R11%28FOC22092K12%29/Ethernet1%2F1/436207616"
                }
            },
            "state": "up",
            "duplex_type": "full_duplex",
            "mtu": 9216,
            "mac_address": "00:be:75:ae:2a:d4",
            "remote_port": {
                "name": "e3a",
                "device": {
                    "node": {
                        "uuid": "54c0f036-8a3a-11ea-893d-00a098fd726d",
                        "name": "stiA400-311",
                        "_links": {
                            "self": {
                                "href": "/api/cluster/nodes/54c0f036-8a3a-11ea-893d-00a098fd726d"
                            }
                        },
                    }
                },
                "mtu": 9000,
            },
            "switch": {
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/switches/RTP-CS01-510R11(FOC22092K12)"
                    }
                },
                "name": "RTP-CS01-510R11(FOC22092K12)",
            },
            "isl": False,
            "configured": "up",
        }
    ),
    SwitchPort(
        {
            "vlan_id": [1, 17, 18, 92],
            "identity": {"number": 11, "index": 436212736, "name": "Ethernet1/11"},
            "speed": 100000,
            "statistics": {
                "transmit_raw": {"errors": 0, "discards": 0, "packets": 0},
                "receive_raw": {"errors": 0, "discards": 0, "packets": 0},
            },
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/switch/ports/RTP-CS01-510R11%28FOC22092K12%29/Ethernet1%2F11/436212736"
                }
            },
            "state": "down",
            "duplex_type": "unknown",
            "mtu": 9216,
            "mac_address": "00be75ae2afc",
            "switch": {
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/switches/RTP-CS01-510R11(FOC22092K12)"
                    }
                },
                "name": "RTP-CS01-510R11(FOC22092K12)",
            },
            "isl": False,
            "configured": "up",
        }
    ),
    SwitchPort(
        {
            "vlan_id": [1, 30],
            "identity": {"number": 10, "index": 436212224, "name": "Ethernet1/10"},
            "speed": 100000,
            "statistics": {
                "transmit_raw": {"errors": 0, "discards": 0, "packets": 2429595607},
                "receive_raw": {"errors": 0, "discards": 0, "packets": 332013844},
            },
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/switch/ports/RTP-SS01-510R10%28FOC22170DFR%29/Ethernet1%2F10/436212224"
                }
            },
            "state": "up",
            "duplex_type": "full_duplex",
            "mtu": 9216,
            "mac_address": "00fcbaead548",
            "remote_port": {
                "name": "e0a",
                "device": {
                    "shelf": {
                        "name": "SHFFG1828000004:B",
                        "uid": "12439000444923584512",
                    }
                },
                "mtu": 9000,
            },
            "switch": {
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/switches/RTP-SS01-510R10(FOC22170DFR)"
                    }
                },
                "name": "RTP-SS01-510R10(FOC22170DFR)",
            },
            "isl": False,
            "configured": "up",
        }
    ),
]

```
</div>
</div>

---
### Retrieving a ports on an ethernet switch
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SwitchPort

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SwitchPort(
        switch="RTP-SS02-510R10(FOC22131U6T)",
        **{"identity.index": "436211712", "identity.name": "Ethernet1/9"}
    )
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
SwitchPort(
    {
        "vlan_id": [1, 30],
        "identity": {"number": 9, "index": 436211712, "name": "Ethernet1/9"},
        "speed": 100000,
        "statistics": {
            "transmit_raw": {"errors": 0, "discards": 0, "packets": 337898026},
            "receive_raw": {"errors": 0, "discards": 0, "packets": 4012559315},
        },
        "_links": {
            "self": {
                "href": "/api/network/ethernet/switch/ports/RTP-SS02-510R10%28FOC22131U6T%29/Ethernet1%2F9/436211712"
            }
        },
        "state": "up",
        "duplex_type": "full_duplex",
        "mtu": 9216,
        "mac_address": "00fcbaea7228",
        "remote_port": {
            "name": "e0b",
            "device": {
                "shelf": {"name": "SHFFG1828000004:A", "uid": "12439000444923584512"}
            },
            "mtu": 9000,
        },
        "switch": {
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/switches/RTP-SS02-510R10(FOC22131U6T)"
                }
            },
            "name": "RTP-SS02-510R10(FOC22131U6T)",
        },
        "isl": False,
        "configured": "up",
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


__all__ = ["SwitchPort", "SwitchPortSchema"]
__pdoc__ = {
    "SwitchPortSchema.resource": False,
    "SwitchPort.switch_port_show": False,
    "SwitchPort.switch_port_create": False,
    "SwitchPort.switch_port_modify": False,
    "SwitchPort.switch_port_delete": False,
}


class SwitchPortSchema(ResourceSchema):
    """The fields of the SwitchPort object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the switch_port. """

    configured = fields.Str(
        data_key="configured",
        validate=enum_validation(['down', 'testing', 'up']),
    )
    r""" Administrative Status.

Valid choices:

* down
* testing
* up """

    duplex_type = fields.Str(
        data_key="duplex_type",
        validate=enum_validation(['full_duplex', 'half_duplex', 'unknown']),
    )
    r""" Duplex Settings.

Valid choices:

* full_duplex
* half_duplex
* unknown """

    identity = fields.Nested("netapp_ontap.models.switch_port_identity.SwitchPortIdentitySchema", data_key="identity", unknown=EXCLUDE)
    r""" The identity field of the switch_port. """

    isl = fields.Boolean(
        data_key="isl",
    )
    r""" Is configured as an ISL link. """

    mac_address = fields.Str(
        data_key="mac_address",
    )
    r""" MAC Address. """

    mtu = Size(
        data_key="mtu",
    )
    r""" MTU. """

    remote_port = fields.Nested("netapp_ontap.models.switch_port_remote_port.SwitchPortRemotePortSchema", data_key="remote_port", unknown=EXCLUDE)
    r""" The remote_port field of the switch_port. """

    speed = Size(
        data_key="speed",
    )
    r""" Interface Speed(Mbps) """

    state = fields.Str(
        data_key="state",
        validate=enum_validation(['dormant', 'down', 'lower_layer_down', 'not_present', 'testing', 'unknown', 'up']),
    )
    r""" Operational Status.

Valid choices:

* dormant
* down
* lower_layer_down
* not_present
* testing
* unknown
* up """

    statistics = fields.Nested("netapp_ontap.models.switch_port_statistics.SwitchPortStatisticsSchema", data_key="statistics", unknown=EXCLUDE)
    r""" The statistics field of the switch_port. """

    switch = fields.Nested("netapp_ontap.resources.switch.SwitchSchema", data_key="switch", unknown=EXCLUDE)
    r""" The switch field of the switch_port. """

    type = fields.Str(
        data_key="type",
        validate=enum_validation(['ethernetcsmacd', 'fastetherfx', 'fibrechannel', 'gigabitethernet', 'ieee8023adlag', 'other', 'propvirtual', 'softwareloopback', 'tunnel']),
    )
    r""" Interface Type.

Valid choices:

* ethernetcsmacd
* fastetherfx
* fibrechannel
* gigabitethernet
* ieee8023adlag
* other
* propvirtual
* softwareloopback
* tunnel """

    vlan_id = fields.List(Size, data_key="vlan_id")
    r""" The vlan_id field of the switch_port. """

    @property
    def resource(self):
        return SwitchPort

    gettable_fields = [
        "links",
        "configured",
        "duplex_type",
        "identity",
        "isl",
        "mac_address",
        "mtu",
        "remote_port",
        "speed",
        "state",
        "statistics",
        "switch.links",
        "switch.name",
        "type",
        "vlan_id",
    ]
    """links,configured,duplex_type,identity,isl,mac_address,mtu,remote_port,speed,state,statistics,switch.links,switch.name,type,vlan_id,"""

    patchable_fields = [
        "identity",
        "remote_port",
        "switch.links",
        "switch.name",
        "vlan_id",
    ]
    """identity,remote_port,switch.links,switch.name,vlan_id,"""

    postable_fields = [
        "identity",
        "remote_port",
        "switch.links",
        "switch.name",
        "vlan_id",
    ]
    """identity,remote_port,switch.links,switch.name,vlan_id,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in SwitchPort.get_collection(fields=field)]
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
            raise NetAppRestError("SwitchPort modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class SwitchPort(Resource):
    r""" Ethernet Switch Port REST API """

    _schema = SwitchPortSchema
    _path = "/api/network/ethernet/switch/ports"
    _keys = ["switch", "identity.name", "identity.index"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the ethernet switch ports.
### Related ONTAP commands
* `system switch ethernet interface show`
### Learn more
* [`DOC /network/ethernet/switch/ports`](#docs-networking-network_ethernet_switch_ports)
"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="switch port show")
        def switch_port_show(
            configured: Choices.define(_get_field_list("configured"), cache_choices=True, inexact=True)=None,
            duplex_type: Choices.define(_get_field_list("duplex_type"), cache_choices=True, inexact=True)=None,
            isl: Choices.define(_get_field_list("isl"), cache_choices=True, inexact=True)=None,
            mac_address: Choices.define(_get_field_list("mac_address"), cache_choices=True, inexact=True)=None,
            mtu: Choices.define(_get_field_list("mtu"), cache_choices=True, inexact=True)=None,
            speed: Choices.define(_get_field_list("speed"), cache_choices=True, inexact=True)=None,
            state: Choices.define(_get_field_list("state"), cache_choices=True, inexact=True)=None,
            type: Choices.define(_get_field_list("type"), cache_choices=True, inexact=True)=None,
            vlan_id: Choices.define(_get_field_list("vlan_id"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["configured", "duplex_type", "isl", "mac_address", "mtu", "speed", "state", "type", "vlan_id", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of SwitchPort resources

            Args:
                configured: Administrative Status.
                duplex_type: Duplex Settings.
                isl: Is configured as an ISL link.
                mac_address: MAC Address.
                mtu: MTU.
                speed: Interface Speed(Mbps)
                state: Operational Status.
                type: Interface Type.
                vlan_id: 
            """

            kwargs = {}
            if configured is not None:
                kwargs["configured"] = configured
            if duplex_type is not None:
                kwargs["duplex_type"] = duplex_type
            if isl is not None:
                kwargs["isl"] = isl
            if mac_address is not None:
                kwargs["mac_address"] = mac_address
            if mtu is not None:
                kwargs["mtu"] = mtu
            if speed is not None:
                kwargs["speed"] = speed
            if state is not None:
                kwargs["state"] = state
            if type is not None:
                kwargs["type"] = type
            if vlan_id is not None:
                kwargs["vlan_id"] = vlan_id
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return SwitchPort.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves the ethernet switch ports.
### Related ONTAP commands
* `system switch ethernet interface show`
### Learn more
* [`DOC /network/ethernet/switch/ports`](#docs-networking-network_ethernet_switch_ports)
"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the ethernet switch ports.
### Related ONTAP commands
* `system switch ethernet interface show`
### Learn more
* [`DOC /network/ethernet/switch/ports`](#docs-networking-network_ethernet_switch_ports)
"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves an ethernet switch port.
### Related ONTAP commands
* `system switch ethernet interface show`

### Learn more
* [`DOC /network/ethernet/switch/ports`](#docs-networking-network_ethernet_switch_ports)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





