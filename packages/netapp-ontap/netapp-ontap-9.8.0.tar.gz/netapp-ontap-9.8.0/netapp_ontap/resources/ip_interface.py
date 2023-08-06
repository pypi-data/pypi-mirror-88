r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
The following operations are supported:

* Creation: POST network/ip/interfaces
* Collection Get: GET network/ip/interfaces
* Instance Get: GET network/ip/interfaces/{uuid}
* Instance Patch: PATCH network/ip/interfaces/{uuid}
* Instance Delete: DELETE network/ip/interfaces/{uuid}
## Retrieving network interface information
The IP interfaces GET API retrieves and displays relevant information pertaining to the interfaces configured in the cluster. The response can contain a list of multiple interfaces or a specific interface. The fields returned in the response vary for different interfaces and configurations.
## Examples
### Retrieving all interfaces in the cluster
The following example shows the list of all interfaces configured in a cluster.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(IpInterface.get_collection()))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    IpInterface(
        {
            "_links": {
                "self": {
                    "href": "/api/network/ip/interfaces/14531286-59fc-11e8-ba55-005056b4340f"
                }
            },
            "name": "user-cluster-01_mgmt1",
            "uuid": "14531286-59fc-11e8-ba55-005056b4340f",
        }
    ),
    IpInterface(
        {
            "_links": {
                "self": {
                    "href": "/api/network/ip/interfaces/145318ba-59fc-11e8-ba55-005056b4340f"
                }
            },
            "name": "user-cluster-01_clus2",
            "uuid": "145318ba-59fc-11e8-ba55-005056b4340f",
        }
    ),
    IpInterface(
        {
            "_links": {
                "self": {
                    "href": "/api/network/ip/interfaces/14531e45-59fc-11e8-ba55-005056b4340f"
                }
            },
            "name": "user-cluster-01_clus1",
            "uuid": "14531e45-59fc-11e8-ba55-005056b4340f",
        }
    ),
    IpInterface(
        {
            "_links": {
                "self": {
                    "href": "/api/network/ip/interfaces/245979de-59fc-11e8-ba55-005056b4340f"
                }
            },
            "name": "cluster_mgmt",
            "uuid": "245979de-59fc-11e8-ba55-005056b4340f",
        }
    ),
    IpInterface(
        {
            "_links": {
                "self": {
                    "href": "/api/network/ip/interfaces/c670707c-5a11-11e8-8fcb-005056b4340f"
                }
            },
            "name": "lif1",
            "uuid": "c670707c-5a11-11e8-8fcb-005056b4340f",
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific Cluster-scoped interface
The following example shows the response when a specific Cluster-scoped interface is requested. The system returns an error when there is no interface with the requested UUID. SVM information is not returned for Cluster-scoped interfaces.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpInterface(uuid="245979de-59fc-11e8-ba55-005056b4340f")
    resource.get()
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
IpInterface(
    {
        "vip": False,
        "ip": {"netmask": "18", "family": "ipv4", "address": "10.63.41.6"},
        "services": ["management_core", "management_autosupport", "management_access"],
        "location": {
            "failover": "broadcast_domain_only",
            "auto_revert": False,
            "home_node": {
                "uuid": "c1db2904-1396-11e9-bb7d-005056acfcbb",
                "name": "user-cluster-01-a",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/c1db2904-1396-11e9-bb7d-005056acfcbb"
                    }
                },
            },
            "node": {
                "uuid": "c1db2904-1396-11e9-bb7d-005056acfcbb",
                "name": "user-cluster-01-a",
                "_links": {
                    "self": {
                        "href": "/api/cluster/nodes/c1db2904-1396-11e9-bb7d-005056acfcbb"
                    }
                },
            },
            "port": {
                "node": {"name": "user-cluster-01-a"},
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/ports/c84d5337-1397-11e9-87c2-005056acfcbb"
                    }
                },
                "name": "e0d",
                "uuid": "c84d5337-1397-11e9-87c2-005056acfcbb",
            },
            "is_home": True,
            "home_port": {
                "node": {"name": "user-cluster-01-a"},
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/ports/c84d5337-1397-11e9-87c2-005056acfcbb"
                    }
                },
                "name": "e0d",
                "uuid": "c84d5337-1397-11e9-87c2-005056acfcbb",
            },
        },
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/network/ip/interfaces/245979de-59fc-11e8-ba55-005056b4340f"
            }
        },
        "service_policy": {
            "name": "default-management",
            "uuid": "9e0f4151-141b-11e9-851e-005056ac1ce0",
        },
        "name": "cluster_mgmt",
        "scope": "cluster",
        "state": "up",
        "ipspace": {
            "_links": {
                "self": {
                    "href": "/api/network/ipspaces/114ecfb5-59fc-11e8-ba55-005056b4340f"
                }
            },
            "name": "Default",
            "uuid": "114ecfb5-59fc-11e8-ba55-005056b4340f",
        },
        "uuid": "245979de-59fc-11e8-ba55-005056b4340f",
    }
)

```
</div>
</div>

---
### Retrieving a specific SVM-scoped interface using a filter
The following example shows the response when a specific SVM-scoped interface is requested. The SVM object is only included for SVM-scoped interfaces.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(IpInterface.get_collection(name="lif1", fields="*")))

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
[
    IpInterface(
        {
            "svm": {
                "uuid": "c2134665-5a11-11e8-8fcb-005056b4340f",
                "name": "user_vs0",
                "_links": {
                    "self": {
                        "href": "/api/svm/svms/c2134665-5a11-11e8-8fcb-005056b4340f"
                    }
                },
            },
            "vip": False,
            "ip": {"netmask": "24", "family": "ipv4", "address": "10.10.10.11"},
            "services": ["data_core", "data_nfs", "data_cifs", "data_flexcache"],
            "location": {
                "failover": "broadcast_domain_only",
                "auto_revert": False,
                "home_node": {
                    "uuid": "c1db2904-1396-11e9-bb7d-005056acfcbb",
                    "name": "user-cluster-01-a",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/c1db2904-1396-11e9-bb7d-005056acfcbb"
                        }
                    },
                },
                "node": {
                    "uuid": "c1db2904-1396-11e9-bb7d-005056acfcbb",
                    "name": "user-cluster-01-a",
                    "_links": {
                        "self": {
                            "href": "/api/cluster/nodes/c1db2904-1396-11e9-bb7d-005056acfcbb"
                        }
                    },
                },
                "port": {
                    "node": {"name": "user-cluster-01-a"},
                    "_links": {
                        "self": {
                            "href": "/api/network/ethernet/ports/c84d5337-1397-11e9-87c2-005056acfcbb"
                        }
                    },
                    "name": "e0d",
                    "uuid": "c84d5337-1397-11e9-87c2-005056acfcbb",
                },
                "is_home": True,
                "home_port": {
                    "node": {"name": "user-cluster-01-a"},
                    "_links": {
                        "self": {
                            "href": "/api/network/ethernet/ports/c84d5337-1397-11e9-87c2-005056acfcbb"
                        }
                    },
                    "name": "e0d",
                    "uuid": "c84d5337-1397-11e9-87c2-005056acfcbb",
                },
            },
            "enabled": True,
            "_links": {
                "self": {
                    "href": "/api/network/ip/interfaces/c670707c-5a11-11e8-8fcb-005056b4340f"
                }
            },
            "service_policy": {
                "name": "default-data-files",
                "uuid": "9e53525f-141b-11e9-851e-005056ac1ce0",
            },
            "name": "lif1",
            "scope": "svm",
            "state": "up",
            "ipspace": {
                "_links": {
                    "self": {
                        "href": "/api/network/ipspaces/114ecfb5-59fc-11e8-ba55-005056b4340f"
                    }
                },
                "name": "Default",
                "uuid": "114ecfb5-59fc-11e8-ba55-005056b4340f",
            },
            "uuid": "c670707c-5a11-11e8-8fcb-005056b4340f",
        }
    )
]

```
</div>
</div>

---
### Retrieving specific fields and limiting the output using filters
The following example shows the response when a filter is applied (location.home_port.name=e0a) and only certain fields are requested. Filtered fields are in the output in addition to the default fields and requested fields.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            IpInterface.get_collection(
                fields="location.home_node.name,service_policy.name,ip.address,enabled",
                **{"location.home_port.name": "e0a"}
            )
        )
    )

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
[
    IpInterface(
        {
            "ip": {"address": "192.168.170.24"},
            "location": {
                "home_node": {"name": "user-cluster-01-a"},
                "home_port": {"name": "e0a"},
            },
            "enabled": True,
            "_links": {
                "self": {
                    "href": "/api/network/ip/interfaces/1d1c9dc8-4f17-11e9-9553-005056ac918a"
                }
            },
            "service_policy": {"name": "default-cluster"},
            "name": "user-cluster-01-a_clus1",
            "uuid": "1d1c9dc8-4f17-11e9-9553-005056ac918a",
        }
    ),
    IpInterface(
        {
            "ip": {"address": "192.168.170.22"},
            "location": {
                "home_node": {"name": "user-cluster-01-b"},
                "home_port": {"name": "e0a"},
            },
            "enabled": True,
            "_links": {
                "self": {
                    "href": "/api/network/ip/interfaces/d07782c1-4f16-11e9-86e7-005056ace7ee"
                }
            },
            "service_policy": {"name": "default-cluster"},
            "name": "user-cluster-01-b_clus1",
            "uuid": "d07782c1-4f16-11e9-86e7-005056ace7ee",
        }
    ),
]

```
</div>
</div>

---
## Creating IP interfaces
You can use the IP interfaces POST API to create IP interfaces as shown in the following examples.
<br/>
---
## Examples
### Creating a Cluster-scoped IP interface using names
The following example shows the record returned after the creation of an IP interface on "e0d".
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpInterface()
    resource.name = "cluster_mgmt"
    resource.ip.address = "10.63.41.6"
    resource.ip.netmask = "18"
    resource.enabled = True
    resource.scope = "cluster"
    resource.ipspace.name = "Default"
    resource.location.auto_revert = False
    resource.location.failover = "broadcast_domain_only"
    resource.location.home_port.name = "e0d"
    resource.location.home_port.node.name = "user-cluster-01-a"
    resource.service_policy.name = "default-management"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
IpInterface(
    {
        "ip": {"netmask": "18", "address": "10.63.41.6"},
        "location": {
            "failover": "broadcast_domain_only",
            "auto_revert": False,
            "home_port": {"node": {"name": "user-cluster-01-a"}, "name": "e0d"},
        },
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/network/ip/interfaces/245979de-59fc-11e8-ba55-005056b4340f"
            }
        },
        "service_policy": {"name": "default-management"},
        "name": "cluster_mgmt",
        "scope": "cluster",
        "ipspace": {"name": "Default"},
        "uuid": "245979de-59fc-11e8-ba55-005056b4340f",
    }
)

```
</div>
</div>

---
### Creating a SVM-scoped IP interface using a mix of parameter types
The following example shows the record returned after the creation of a IP interface by specifying a broadcast domain as the location.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpInterface()
    resource.name = "Data1"
    resource.ip.address = "10.234.101.116"
    resource.ip.netmask = "255.255.240.0"
    resource.enabled = True
    resource.scope = "svm"
    resource.svm.uuid = "137f3618-1e89-11e9-803e-005056a7646a"
    resource.location.auto_revert = True
    resource.location.broadcast_domain.name = "Default"
    resource.service_policy.name = "default-data-files"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
IpInterface(
    {
        "svm": {
            "uuid": "137f3618-1e89-11e9-803e-005056a7646a",
            "name": "vs0",
            "_links": {
                "self": {"href": "/api/svm/svms/137f3618-1e89-11e9-803e-005056a7646a"}
            },
        },
        "ip": {"netmask": "20", "address": "10.234.101.116"},
        "location": {"auto_revert": True},
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/network/ip/interfaces/80d271c9-1f43-11e9-803e-005056a7646a"
            }
        },
        "service_policy": {"name": "default-data-files"},
        "name": "Data1",
        "scope": "svm",
        "uuid": "80d271c9-1f43-11e9-803e-005056a7646a",
    }
)

```
</div>
</div>

---
### Creating a Cluster-scoped IP interface without specifying the scope parameter
The following example shows the record returned after creating an IP interface on "e0d" without specifying the scope parameter. The scope is "cluster" if an "svm" is not specified.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpInterface()
    resource.name = "cluster_mgmt"
    resource.ip.address = "10.63.41.6"
    resource.ip.netmask = "18"
    resource.enabled = True
    resource.ipspace.name = "Default"
    resource.location.auto_revert = False
    resource.location.home_port.name = "e0d"
    resource.location.home_port.node.name = "user-cluster-01-a"
    resource.service_policy.name = "default-management"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
IpInterface(
    {
        "ip": {"netmask": "18", "address": "10.63.41.6"},
        "location": {
            "auto_revert": False,
            "home_port": {"node": {"name": "user-cluster-01-a"}, "name": "e0d"},
        },
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/network/ip/interfaces/245979de-59fc-11e8-ba55-005056b4340f"
            }
        },
        "service_policy": {"name": "default-management"},
        "name": "cluster_mgmt",
        "scope": "cluster",
        "ipspace": {"name": "Default"},
        "uuid": "245979de-59fc-11e8-ba55-005056b4340f",
    }
)

```
</div>
</div>

---
### Creating an SVM-scoped IP interface without specifying the scope parameter
The following example shows the record returned after creating an IP interface on "e0d" without specifying the scope parameter. The scope is "svm" if the "svm" field is specified.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpInterface()
    resource.name = "Data1"
    resource.ip.address = "10.234.101.116"
    resource.ip.netmask = "255.255.240.0"
    resource.enabled = True
    resource.svm.uuid = "137f3618-1e89-11e9-803e-005056a7646a"
    resource.location.auto_revert = True
    resource.location.broadcast_domain.name = "Default"
    resource.service_policy.name = "default-data-files"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
IpInterface(
    {
        "svm": {
            "uuid": "137f3618-1e89-11e9-803e-005056a7646a",
            "name": "vs0",
            "_links": {
                "self": {"href": "/api/svms/137f3618-1e89-11e9-803e-005056a7646a"}
            },
        },
        "ip": {"netmask": "20", "address": "10.234.101.116"},
        "location": {"auto_revert": True},
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/network/ip/interfaces/80d271c9-1f43-11e9-803e-005056a7646a"
            }
        },
        "service_policy": {"name": "default-data-files"},
        "name": "Data1",
        "scope": "svm",
        "uuid": "80d271c9-1f43-11e9-803e-005056a7646a",
    }
)

```
</div>
</div>

---
## Updating IP interfaces
You can use the IP interfaces PATCH API to update the attributes of an IP interface.
<br/>
---
## Examples
### Updating the auto revert flag of an IP interface
The following example shows how the PATCH request changes the auto revert flag to 'false'.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpInterface(uuid="80d271c9-1f43-11e9-803e-005056a7646a")
    resource.location.auto_revert = False
    resource.patch()

```

---
### Updating the service policy of an IP interface
The following example shows how the PATCH request changes the service policy to 'default-management'.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpInterface(uuid="80d271c9-1f43-11e9-803e-005056a7646a")
    resource.service_policy.name = "default-management"
    resource.patch()

```

---
## Deleting IP interfaces
You can use the IP interfaces DELETE API to delete an IP interface in the cluster.
<br/>
---
## Example
### Deleting an IP Interface
The following DELETE request deletes a network IP interface.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import IpInterface

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = IpInterface(uuid="80d271c9-1f43-11e9-803e-005056a7646a")
    resource.delete()

```

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


__all__ = ["IpInterface", "IpInterfaceSchema"]
__pdoc__ = {
    "IpInterfaceSchema.resource": False,
    "IpInterface.ip_interface_show": False,
    "IpInterface.ip_interface_create": False,
    "IpInterface.ip_interface_modify": False,
    "IpInterface.ip_interface_delete": False,
}


class IpInterfaceSchema(ResourceSchema):
    """The fields of the IpInterface object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the ip_interface. """

    enabled = fields.Boolean(
        data_key="enabled",
    )
    r""" The administrative state of the interface. """

    ip = fields.Nested("netapp_ontap.models.ip_info.IpInfoSchema", data_key="ip", unknown=EXCLUDE)
    r""" The ip field of the ip_interface. """

    ipspace = fields.Nested("netapp_ontap.resources.ipspace.IpspaceSchema", data_key="ipspace", unknown=EXCLUDE)
    r""" The ipspace field of the ip_interface. """

    location = fields.Nested("netapp_ontap.models.ip_interface_location.IpInterfaceLocationSchema", data_key="location", unknown=EXCLUDE)
    r""" The location field of the ip_interface. """

    metric = fields.Nested("netapp_ontap.resources.interface_metrics.InterfaceMetricsSchema", data_key="metric", unknown=EXCLUDE)
    r""" The metric field of the ip_interface. """

    name = fields.Str(
        data_key="name",
    )
    r""" Interface name

Example: dataLif1 """

    scope = fields.Str(
        data_key="scope",
        validate=enum_validation(['svm', 'cluster']),
    )
    r""" Set to "svm" for interfaces owned by an SVM. Otherwise, set to "cluster".

Valid choices:

* svm
* cluster """

    service_policy = fields.Nested("netapp_ontap.resources.ip_service_policy.IpServicePolicySchema", data_key="service_policy", unknown=EXCLUDE)
    r""" The service_policy field of the ip_interface. """

    services = fields.List(fields.Str, data_key="services")
    r""" The services associated with the interface. """

    state = fields.Str(
        data_key="state",
        validate=enum_validation(['up', 'down']),
    )
    r""" The operational state of the interface.

Valid choices:

* up
* down """

    statistics = fields.Nested("netapp_ontap.models.interface_statistics.InterfaceStatisticsSchema", data_key="statistics", unknown=EXCLUDE)
    r""" The statistics field of the ip_interface. """

    svm = fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE)
    r""" The svm field of the ip_interface. """

    uuid = fields.Str(
        data_key="uuid",
    )
    r""" The UUID that uniquely identifies the interface.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    vip = fields.Boolean(
        data_key="vip",
    )
    r""" True for a VIP interface, whose location is announced via BGP. """

    @property
    def resource(self):
        return IpInterface

    gettable_fields = [
        "links",
        "enabled",
        "ip",
        "ipspace.links",
        "ipspace.name",
        "ipspace.uuid",
        "location",
        "metric",
        "name",
        "scope",
        "service_policy.links",
        "service_policy.name",
        "service_policy.uuid",
        "services",
        "state",
        "statistics",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
        "vip",
    ]
    """links,enabled,ip,ipspace.links,ipspace.name,ipspace.uuid,location,metric,name,scope,service_policy.links,service_policy.name,service_policy.uuid,services,state,statistics,svm.links,svm.name,svm.uuid,uuid,vip,"""

    patchable_fields = [
        "enabled",
        "ip",
        "location",
        "name",
        "service_policy.name",
        "service_policy.uuid",
    ]
    """enabled,ip,location,name,service_policy.name,service_policy.uuid,"""

    postable_fields = [
        "enabled",
        "ip",
        "ipspace.name",
        "ipspace.uuid",
        "location",
        "name",
        "scope",
        "service_policy.name",
        "service_policy.uuid",
        "svm.name",
        "svm.uuid",
        "vip",
    ]
    """enabled,ip,ipspace.name,ipspace.uuid,location,name,scope,service_policy.name,service_policy.uuid,svm.name,svm.uuid,vip,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in IpInterface.get_collection(fields=field)]
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
            raise NetAppRestError("IpInterface modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class IpInterface(Resource):
    """Allows interaction with IpInterface objects on the host"""

    _schema = IpInterfaceSchema
    _path = "/api/network/ip/interfaces"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the details of all IP interfaces.
### Related ONTAP Commands
* `network interface show`

### Learn more
* [`DOC /network/ip/interfaces`](#docs-networking-network_ip_interfaces)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="ip interface show")
        def ip_interface_show(
            enabled: Choices.define(_get_field_list("enabled"), cache_choices=True, inexact=True)=None,
            name: Choices.define(_get_field_list("name"), cache_choices=True, inexact=True)=None,
            scope: Choices.define(_get_field_list("scope"), cache_choices=True, inexact=True)=None,
            services: Choices.define(_get_field_list("services"), cache_choices=True, inexact=True)=None,
            state: Choices.define(_get_field_list("state"), cache_choices=True, inexact=True)=None,
            uuid: Choices.define(_get_field_list("uuid"), cache_choices=True, inexact=True)=None,
            vip: Choices.define(_get_field_list("vip"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["enabled", "name", "scope", "services", "state", "uuid", "vip", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of IpInterface resources

            Args:
                enabled: The administrative state of the interface.
                name: Interface name
                scope: Set to \"svm\" for interfaces owned by an SVM. Otherwise, set to \"cluster\".
                services: The services associated with the interface.
                state: The operational state of the interface.
                uuid: The UUID that uniquely identifies the interface.
                vip: True for a VIP interface, whose location is announced via BGP.
            """

            kwargs = {}
            if enabled is not None:
                kwargs["enabled"] = enabled
            if name is not None:
                kwargs["name"] = name
            if scope is not None:
                kwargs["scope"] = scope
            if services is not None:
                kwargs["services"] = services
            if state is not None:
                kwargs["state"] = state
            if uuid is not None:
                kwargs["uuid"] = uuid
            if vip is not None:
                kwargs["vip"] = vip
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return IpInterface.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves the details of all IP interfaces.
### Related ONTAP Commands
* `network interface show`

### Learn more
* [`DOC /network/ip/interfaces`](#docs-networking-network_ip_interfaces)"""
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
        r"""Updates an IP interface.
### Related ONTAP commands
* `network interface migrate`
* `network interface modify`
* `network interface rename`
* `network interface revert`

### Learn more
* [`DOC /network/ip/interfaces`](#docs-networking-network_ip_interfaces)"""
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
        r"""Deletes an IP interface.
### Related ONTAP commands
* `network interface delete`

### Learn more
* [`DOC /network/ip/interfaces`](#docs-networking-network_ip_interfaces)"""
        return super()._delete_collection(*args, body=body, connection=connection, **kwargs)

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the details of all IP interfaces.
### Related ONTAP Commands
* `network interface show`

### Learn more
* [`DOC /network/ip/interfaces`](#docs-networking-network_ip_interfaces)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves details for a specific IP interface.
### Related ONTAP commands
* `network interface show`

### Learn more
* [`DOC /network/ip/interfaces`](#docs-networking-network_ip_interfaces)"""
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
        r"""Creates a new Cluster-scoped or SVM-scoped interface.<br/>
### Required properties
* `name` - Name of the interface to create.
* `ip.address` - IP address for the interface.
* `ip.netmask` - IP subnet of the interface.
* `ipspace.name` or `ipspace.uuid`
  * Required for Cluster-scoped interfaces.
  * Optional for SVM-scoped interfaces.
* `svm.name` or `svm.uuid`
  * Required for an SVM-scoped interface.
  * Invalid for a Cluster-scoped interface.
* `location.home_port` or `location.home_node` or `location.broadcast_domain` - One of these properties must be set to a value to define where the interface will be located.
### Recommended property values
* `service_policy`
  * `for SVM scoped interfaces`
    * _default-data-files_ for interfaces carrying file-oriented NAS data traffic
    * _default-data-blocks_ for interfaces carrying block-oriented SAN data traffic
    * _default-management_ for interfaces carrying SVM management requests
  * `for Cluster scoped interfaces`
    * _default-intercluster_ for interfaces carrying cluster peering traffic
    * _default-management_ for interfaces carrying system management requests
    * _default-route-announce_ for interfaces carrying BGP peer connections
### Default property values
If not specified in POST, the following default property values are assigned:
* `scope`
  * _svm_ if svm parameter is specified.
  * _cluster_ if svm parameter is not specified
* `enabled` - _true_
* `location.auto_revert` - _true_
* `service_policy`
  * _default-data-files_ if scope is `svm`
  * _default-management_ if scope is `cluster` and IPspace is not `Cluster`
  * _default-cluster_ if scope is `svm` and IPspace is `Cluster`
* `failover` - Selects the least restrictive failover policy supported by all the services in the service policy.
### Related ONTAP commands
* `network interface create`

### Learn more
* [`DOC /network/ip/interfaces`](#docs-networking-network_ip_interfaces)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="ip interface create")
        async def ip_interface_create(
            links: dict = None,
            enabled: bool = None,
            ip: dict = None,
            ipspace: dict = None,
            location: dict = None,
            metric: dict = None,
            name: str = None,
            scope: str = None,
            service_policy: dict = None,
            services: List[str] = None,
            state: str = None,
            statistics: dict = None,
            svm: dict = None,
            uuid: str = None,
            vip: bool = None,
        ) -> ResourceTable:
            """Create an instance of a IpInterface resource

            Args:
                links: 
                enabled: The administrative state of the interface.
                ip: 
                ipspace: 
                location: 
                metric: 
                name: Interface name
                scope: Set to \"svm\" for interfaces owned by an SVM. Otherwise, set to \"cluster\".
                service_policy: 
                services: The services associated with the interface.
                state: The operational state of the interface.
                statistics: 
                svm: 
                uuid: The UUID that uniquely identifies the interface.
                vip: True for a VIP interface, whose location is announced via BGP.
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if enabled is not None:
                kwargs["enabled"] = enabled
            if ip is not None:
                kwargs["ip"] = ip
            if ipspace is not None:
                kwargs["ipspace"] = ipspace
            if location is not None:
                kwargs["location"] = location
            if metric is not None:
                kwargs["metric"] = metric
            if name is not None:
                kwargs["name"] = name
            if scope is not None:
                kwargs["scope"] = scope
            if service_policy is not None:
                kwargs["service_policy"] = service_policy
            if services is not None:
                kwargs["services"] = services
            if state is not None:
                kwargs["state"] = state
            if statistics is not None:
                kwargs["statistics"] = statistics
            if svm is not None:
                kwargs["svm"] = svm
            if uuid is not None:
                kwargs["uuid"] = uuid
            if vip is not None:
                kwargs["vip"] = vip

            resource = IpInterface(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to create IpInterface: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates an IP interface.
### Related ONTAP commands
* `network interface migrate`
* `network interface modify`
* `network interface rename`
* `network interface revert`

### Learn more
* [`DOC /network/ip/interfaces`](#docs-networking-network_ip_interfaces)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="ip interface modify")
        async def ip_interface_modify(
            enabled: bool = None,
            query_enabled: bool = None,
            name: str = None,
            query_name: str = None,
            scope: str = None,
            query_scope: str = None,
            services: List[str] = None,
            query_services: List[str] = None,
            state: str = None,
            query_state: str = None,
            uuid: str = None,
            query_uuid: str = None,
            vip: bool = None,
            query_vip: bool = None,
        ) -> ResourceTable:
            """Modify an instance of a IpInterface resource

            Args:
                enabled: The administrative state of the interface.
                query_enabled: The administrative state of the interface.
                name: Interface name
                query_name: Interface name
                scope: Set to \"svm\" for interfaces owned by an SVM. Otherwise, set to \"cluster\".
                query_scope: Set to \"svm\" for interfaces owned by an SVM. Otherwise, set to \"cluster\".
                services: The services associated with the interface.
                query_services: The services associated with the interface.
                state: The operational state of the interface.
                query_state: The operational state of the interface.
                uuid: The UUID that uniquely identifies the interface.
                query_uuid: The UUID that uniquely identifies the interface.
                vip: True for a VIP interface, whose location is announced via BGP.
                query_vip: True for a VIP interface, whose location is announced via BGP.
            """

            kwargs = {}
            changes = {}
            if query_enabled is not None:
                kwargs["enabled"] = query_enabled
            if query_name is not None:
                kwargs["name"] = query_name
            if query_scope is not None:
                kwargs["scope"] = query_scope
            if query_services is not None:
                kwargs["services"] = query_services
            if query_state is not None:
                kwargs["state"] = query_state
            if query_uuid is not None:
                kwargs["uuid"] = query_uuid
            if query_vip is not None:
                kwargs["vip"] = query_vip

            if enabled is not None:
                changes["enabled"] = enabled
            if name is not None:
                changes["name"] = name
            if scope is not None:
                changes["scope"] = scope
            if services is not None:
                changes["services"] = services
            if state is not None:
                changes["state"] = state
            if uuid is not None:
                changes["uuid"] = uuid
            if vip is not None:
                changes["vip"] = vip

            if hasattr(IpInterface, "find"):
                resource = IpInterface.find(
                    **kwargs
                )
            else:
                resource = IpInterface()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to modify IpInterface: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes an IP interface.
### Related ONTAP commands
* `network interface delete`

### Learn more
* [`DOC /network/ip/interfaces`](#docs-networking-network_ip_interfaces)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="ip interface delete")
        async def ip_interface_delete(
            enabled: bool = None,
            name: str = None,
            scope: str = None,
            services: List[str] = None,
            state: str = None,
            uuid: str = None,
            vip: bool = None,
        ) -> None:
            """Delete an instance of a IpInterface resource

            Args:
                enabled: The administrative state of the interface.
                name: Interface name
                scope: Set to \"svm\" for interfaces owned by an SVM. Otherwise, set to \"cluster\".
                services: The services associated with the interface.
                state: The operational state of the interface.
                uuid: The UUID that uniquely identifies the interface.
                vip: True for a VIP interface, whose location is announced via BGP.
            """

            kwargs = {}
            if enabled is not None:
                kwargs["enabled"] = enabled
            if name is not None:
                kwargs["name"] = name
            if scope is not None:
                kwargs["scope"] = scope
            if services is not None:
                kwargs["services"] = services
            if state is not None:
                kwargs["state"] = state
            if uuid is not None:
                kwargs["uuid"] = uuid
            if vip is not None:
                kwargs["vip"] = vip

            if hasattr(IpInterface, "find"):
                resource = IpInterface.find(
                    **kwargs
                )
            else:
                resource = IpInterface()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to delete IpInterface: %s" % err)


