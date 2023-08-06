r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

##  Overview
Cluster peering allows administrators of ONTAP systems to establish relationships between two or more independent clusters. When a relationship exists between two clusters, the clusters can exchange user data and configuration information, and coordinate operations. The /cluster/peers endpoint supports create, get, modify, and delete operations using GET, PATCH, POST and DELETE HTTP requests.
## Create a cluster peer
You can set up a new cluster peer relationship by issuing a POST request to /cluster/peers. Parameters in the POST body define the settings of the peering relationship. A successful POST request that succeeds in creating a peer returns HTTP status code "201", along with the details of the created peer, such as peer UUID, name, and authentication information. A failed POST request returns an HTTP error code along with a message indicating the reason for the error. This can include malformed requests and invalid operations.
### Sample request
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterPeer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterPeer()
    resource.authentication.expiry_time = "12/25/2018 12:34:56"
    resource.authentication.generate_passphrase = True
    resource.post(hydrate=True)
    print(resource)

```

### Examples
```
# Create - no params
body = {}
# Creating with a peer address and a passphrase
body =
{
    "remote":
      {
          "ip_addresses":["1.2.3.4"]
      }
}
# Creating with a peer name and a generated passphrase that is true
body =
{
    "name":"cp_xyz123",
    "authentication":
      {
          "generate_passphrase":true
      }
}
# Creating with a name, a peer address, and a passphrase
body =
{
    "name":"cp_xyz123",
    "remote":
      {
          "ip_addresses": ["1.2.3.4"]
      },
    "authentication":
      {
          "passphrase":"xyz12345"
      }
 }
# Creating with a proposed encryption protocol
body =
{
    "encryption":
      {
          "proposed":"tls-psk"
      }
}
```
---
## Create local intercluster LIFs
The local cluster must have an intercluster LIF on each node for the correct operation of cluster peering.
If no local intercluster LIFs exist, you can optionally specify LIFs to be created for each node in the local cluster.
These local interfaces, if specified, are created on each node before proceeding with the creation of the cluster peering relationship. Cluster peering relationships are not established if there is an error preventing the LIFs from being created.
After local interfaces have been created, do not specify them for subsequent cluster peering relationships.
### Local LIF creation fields

* local_network.ip_addresses - List of IP addresses to assign, one per node in the local cluster.
* local_network.netmask - IPv4 mask or subnet mask length.
* local_network.broadcast_domain - Broadcast domain that is in use within the IPspace.
* local_network.gateway - The IPv4 or IPv6 address of the default router.
### Additional information on network routes
When creating LIFs, the network route discovery mechanism might take additional time (1-5 seconds) to become visible in the network outside of the cluster. This delay in publishing the routes might cause an initial cluster peer "create" request to fail. This error disappears with a retry of the same request.
### Example
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterPeer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterPeer()
    resource.local_network.interfaces = [
        {"ip_address": "1.2.3.4"},
        {"ip_address": "1.2.3.5"},
        {"ip_address": "1.2.3.6"},
    ]
    resource.local_network.netmask = "255.255.0.0"
    resource.local_network.broadcast_domain = "Default"
    resource.local_network.gateway = "1.2.0.1"
    resource.remote.ip_addresses = ["1.2.9.9"]
    resource.authentication.passphrase = "xyz12345"
    resource.post(hydrate=True)
    print(resource)

```

Note that "<mgmt-ip>" is replaced by the IP address of the cluster management interface, and the body is read from the specified text file containing the fields for the new peering relationship and local interfaces.
---
## Retrieve a cluster peer
You can retrieve peers in a cluster by issuing a GET request to /cluster/peers. It is also possible to retrieve a specific peer when qualified by its UUID to /cluster/peers/{uuid}.
A GET request might have no query parameters or a valid cluster UUID. The former retrieves all records while the latter retrieves the record for the cluster peer with that UUID.
The following fields are used for retrieving a cluster peer.
### Required fields
There are no required fields for GET requests.
### Optional fields
The following fields are optional for GET requests

* UUID - UUID of the cluster peer.
### Examples
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterPeer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(ClusterPeer.get_collection()))

```

```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterPeer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterPeer(uuid="{uuid}")
    resource.get()
    print(resource)

```

```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterPeer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterPeer(uuid="{uuid}")
    resource.get(fields="*")
    print(resource)

```

---
## Update a cluster peer
You can update a cluster peer relationship by issuing a PATCH request to /cluster/peers/{uuid}. As in the CLI mode, you can toggle the proposed encryption protocol, update the passphrase, or specify a new set of stable addresses.  All PATCH requests take the parameters that are to be updated in the request body. If the generate_passphrase is "true", the passphrase is returned in the PATCH response.
This following fields highlight the parameters that control the modification of an existing cluster peering relationship.
### Required fields
A PATCH request with an empty body has no effect on the cluster peer instance. All other fields and the combinations in which they are valid are indicated below:

* `encryption_proposed` - Toggle the proposed encryption protocol (from "none" to "tls-psk" or otherwise). Authentication must be "true" and a passphrase must be present in body.
* `passphrase`
* `passphrase` or `generate passphrase`
* `remote.ip_addresses`
### Optional fields

* `expiration time` - Set the expiration time of the passphrase.
### Examples
```
# Updating with an empty body
body = {}
# Updating the proposed encryption protocol from tls-psk to none
body =
{
    "authentication":
      {
          "passphrase":"xyz12345",
          "in_use":"ok"
      },
    "encryption":
      {
          "proposed":"none"
      }
}
# Updating the passphrase
body =
{
    "authentication":
     {
         "passphrase":"xyz12345",
         "in_use":"ok"
     }
}
# Setting an auto-generated passphrase
body =
{
    "authentication":
     {
         "generate_passphrase": true,
         "in_use":"ok"
     }
}
# Updating remote IP addresses
body =
{
    "remote":
      {
          "ip_addresses":["10.224.65.30"]
      }
}
```
### Sample requests
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterPeer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterPeer(uuid="73123071-d0b9-11e8-a686-005056a7179a")
    resource.authentication.passphrase = "xyz12345"
    resource.authentication.in_use = "ok"
    resource.patch()

```

---
## Delete a cluster peer
You can delete a cluster peer using the HTTP DELETE request.
### Required fields
Perform all delete operations on a valid peer UUID. Deleting an invalid peer returns "HTTP 404", which indicates an error.
### Optional fields
The DELETE operation has no optional fields.
### Request format
DELETE "https://<mgmt-ip>/api/cluster/peers/{uuid}"
### Example
The following request deletes a peer with peer UUID "8becc0d4-c12c-11e8-9ceb-005056bbd143".
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import ClusterPeer

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = ClusterPeer(uuid="8becc0d4-c12c-11e8-9ceb-005056bbd143")
    resource.delete()

```

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


__all__ = ["ClusterPeer", "ClusterPeerSchema"]
__pdoc__ = {
    "ClusterPeerSchema.resource": False,
    "ClusterPeer.cluster_peer_show": False,
    "ClusterPeer.cluster_peer_create": False,
    "ClusterPeer.cluster_peer_modify": False,
    "ClusterPeer.cluster_peer_delete": False,
}


class ClusterPeerSchema(ResourceSchema):
    """The fields of the ClusterPeer object"""

    links = fields.Nested("netapp_ontap.models.cluster_peer_links.ClusterPeerLinksSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the cluster_peer. """

    authentication = fields.Nested("netapp_ontap.models.cluster_peer_authentication.ClusterPeerAuthenticationSchema", data_key="authentication", unknown=EXCLUDE)
    r""" The authentication field of the cluster_peer. """

    encryption = fields.Nested("netapp_ontap.models.cluster_peer_encryption.ClusterPeerEncryptionSchema", data_key="encryption", unknown=EXCLUDE)
    r""" The encryption field of the cluster_peer. """

    initial_allowed_svms = fields.List(fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE), data_key="initial_allowed_svms")
    r""" The local SVMs allowed to peer with the peer cluster's SVMs. This list can be modified until the remote cluster accepts this cluster peering relationship. """

    ipspace = fields.Nested("netapp_ontap.resources.ipspace.IpspaceSchema", data_key="ipspace", unknown=EXCLUDE)
    r""" The ipspace field of the cluster_peer. """

    local_network = fields.Nested("netapp_ontap.models.cluster_peer_local_network.ClusterPeerLocalNetworkSchema", data_key="local_network", unknown=EXCLUDE)
    r""" The local_network field of the cluster_peer. """

    name = fields.Str(
        data_key="name",
    )
    r""" Optional name for the cluster peer relationship. By default, it is the name of the remote cluster.

Example: cluster2 """

    peer_applications = fields.List(fields.Str, data_key="peer_applications")
    r""" Peering applications against which allowed SVMs are configured.

Example: ["snapmirror","flexcache"] """

    remote = fields.Nested("netapp_ontap.models.cluster_peer_remote.ClusterPeerRemoteSchema", data_key="remote", unknown=EXCLUDE)
    r""" The remote field of the cluster_peer. """

    status = fields.Nested("netapp_ontap.models.cluster_peer_status.ClusterPeerStatusSchema", data_key="status", unknown=EXCLUDE)
    r""" The status field of the cluster_peer. """

    uuid = fields.Str(
        data_key="uuid",
    )
    r""" UUID of the cluster peer relationship. For anonymous cluster peer offers, the UUID will change when the remote cluster accepts the relationship.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    version = fields.Nested("netapp_ontap.models.version.VersionSchema", data_key="version", unknown=EXCLUDE)
    r""" The version field of the cluster_peer. """

    @property
    def resource(self):
        return ClusterPeer

    gettable_fields = [
        "links",
        "authentication",
        "encryption",
        "initial_allowed_svms.links",
        "initial_allowed_svms.name",
        "initial_allowed_svms.uuid",
        "ipspace.links",
        "ipspace.name",
        "ipspace.uuid",
        "name",
        "peer_applications",
        "remote",
        "status",
        "uuid",
        "version",
    ]
    """links,authentication,encryption,initial_allowed_svms.links,initial_allowed_svms.name,initial_allowed_svms.uuid,ipspace.links,ipspace.name,ipspace.uuid,name,peer_applications,remote,status,uuid,version,"""

    patchable_fields = [
        "links",
        "authentication",
        "encryption",
        "initial_allowed_svms.name",
        "initial_allowed_svms.uuid",
        "ipspace.name",
        "ipspace.uuid",
        "name",
        "peer_applications",
        "remote",
        "status",
    ]
    """links,authentication,encryption,initial_allowed_svms.name,initial_allowed_svms.uuid,ipspace.name,ipspace.uuid,name,peer_applications,remote,status,"""

    postable_fields = [
        "links",
        "authentication",
        "encryption",
        "initial_allowed_svms.name",
        "initial_allowed_svms.uuid",
        "ipspace.name",
        "ipspace.uuid",
        "local_network",
        "name",
        "peer_applications",
        "remote",
        "status",
    ]
    """links,authentication,encryption,initial_allowed_svms.name,initial_allowed_svms.uuid,ipspace.name,ipspace.uuid,local_network,name,peer_applications,remote,status,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in ClusterPeer.get_collection(fields=field)]
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
            raise NetAppRestError("ClusterPeer modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class ClusterPeer(Resource):
    """Allows interaction with ClusterPeer objects on the host"""

    _schema = ClusterPeerSchema
    _path = "/api/cluster/peers"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the collection of cluster peers.
### Learn more
* [`DOC /cluster/peers`](#docs-cluster-cluster_peers)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="cluster peer show")
        def cluster_peer_show(
            name: Choices.define(_get_field_list("name"), cache_choices=True, inexact=True)=None,
            peer_applications: Choices.define(_get_field_list("peer_applications"), cache_choices=True, inexact=True)=None,
            uuid: Choices.define(_get_field_list("uuid"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["name", "peer_applications", "uuid", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of ClusterPeer resources

            Args:
                name: Optional name for the cluster peer relationship. By default, it is the name of the remote cluster.
                peer_applications: Peering applications against which allowed SVMs are configured.
                uuid: UUID of the cluster peer relationship. For anonymous cluster peer offers, the UUID will change when the remote cluster accepts the relationship.
            """

            kwargs = {}
            if name is not None:
                kwargs["name"] = name
            if peer_applications is not None:
                kwargs["peer_applications"] = peer_applications
            if uuid is not None:
                kwargs["uuid"] = uuid
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return ClusterPeer.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves the collection of cluster peers.
### Learn more
* [`DOC /cluster/peers`](#docs-cluster-cluster_peers)"""
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
        r"""Updates a cluster peer instance.
### Learn more
* [`DOC /cluster/peers`](#docs-cluster-cluster_peers)"""
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
        r"""Deletes a cluster peer.
### Learn more
* [`DOC /cluster/peers`](#docs-cluster-cluster_peers)"""
        return super()._delete_collection(*args, body=body, connection=connection, **kwargs)

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the collection of cluster peers.
### Learn more
* [`DOC /cluster/peers`](#docs-cluster-cluster_peers)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves a specific cluster peer instance.
### Learn more
* [`DOC /cluster/peers`](#docs-cluster-cluster_peers)"""
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
        r"""Creates a peering relationship and, optionally, the IP interfaces it will use. There are two methods used to create a peering relationship:
* Provide a remote IP address - Used when creating a new cluster peer relationship with a specific remote cluster. This requires at least one remote intercluster IP address from the remote cluster.
* Do not provide a remote IP address - Used when the remote IP address is not provided and when the storage system is ready to accept peering requests from foreign clusters.
### Required properties
* `remote.ip_addresses` - Addresses of the remote peers. The local peer must be able to reach and connect to these addresses for the request to succeed in creating a peer. Only required when creating a peering relationship by providing a remote IP address.
* Either set `generate_passphrase` to "true" or provide a passphrase in the body of the request. Only one of these options is required.
### Recommended optional properties
* `name` - Name of the peering relationship or name of the remote peer.
* `passphrase` - User generated passphrase for use in authentication.
* `generate_passphrase` (true/false) - When "true", ONTAP automatically generates a passphrase to authenticate cluster peers.
* `ipspace` - IPspace of the local intercluster LIFs. Assumes Default IPspace if not provided.
* `initial_allowed_svms` - Local SVMs allowed to peer with the peer cluster's SVMs. Can be modified until the remote cluster accepts this cluster peering relationship.
* `local_network` - Fields to create a local intercluster LIF.
* `expiry_time` - Duration in ISO 8601 format for which the user-supplied or auto-generated passphrase is valid. Expiration time must not be greater than seven days into the future. ISO 8601 duration format is "PnDTnHnMnS" or "PnW" where n is a positive integer. The "nD", "nH", "nM" and "nS" fields can be dropped if zero. "P" must always be present and "T" must be present if there are any hours, minutes, or seconds fields.
* `encryption_proposed` (none/tls-psk) - Encryption mechanism of the communication channel between the two peers.
* `peer_applications` - SVM peering applications (SnapMirror, FlexCache or both) for which the SVM peering relationship is set up.
### Additional information
As with creating a cluster peer through the CLI, the combinations of options must be valid in order for the create operation to succeed. The following list shows the combinations that will succeed and those that will fail:
* A passphrase only (fail)
* A peer IP address (fail)
* A passphrase with an expiration time > 7 days into the future (fail)
* A peer IP address and a passphrase (OK)
* generate_passphrase=true (OK)
* Any proposed encryption protocol (OK)
* An IPspace name or UUID (OK)
* A passphrase, peer IP address, and any proposed encryption protocol (OK)
* A non empty list of initial allowed SVM peer names or UUIDs. (OK)

### Learn more
* [`DOC /cluster/peers`](#docs-cluster-cluster_peers)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="cluster peer create")
        async def cluster_peer_create(
            links: dict = None,
            authentication: dict = None,
            encryption: dict = None,
            initial_allowed_svms: dict = None,
            ipspace: dict = None,
            local_network: dict = None,
            name: str = None,
            peer_applications: List[str] = None,
            remote: dict = None,
            status: dict = None,
            uuid: str = None,
            version: dict = None,
        ) -> ResourceTable:
            """Create an instance of a ClusterPeer resource

            Args:
                links: 
                authentication: 
                encryption: 
                initial_allowed_svms: The local SVMs allowed to peer with the peer cluster's SVMs. This list can be modified until the remote cluster accepts this cluster peering relationship.
                ipspace: 
                local_network: 
                name: Optional name for the cluster peer relationship. By default, it is the name of the remote cluster.
                peer_applications: Peering applications against which allowed SVMs are configured.
                remote: 
                status: 
                uuid: UUID of the cluster peer relationship. For anonymous cluster peer offers, the UUID will change when the remote cluster accepts the relationship.
                version: 
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if authentication is not None:
                kwargs["authentication"] = authentication
            if encryption is not None:
                kwargs["encryption"] = encryption
            if initial_allowed_svms is not None:
                kwargs["initial_allowed_svms"] = initial_allowed_svms
            if ipspace is not None:
                kwargs["ipspace"] = ipspace
            if local_network is not None:
                kwargs["local_network"] = local_network
            if name is not None:
                kwargs["name"] = name
            if peer_applications is not None:
                kwargs["peer_applications"] = peer_applications
            if remote is not None:
                kwargs["remote"] = remote
            if status is not None:
                kwargs["status"] = status
            if uuid is not None:
                kwargs["uuid"] = uuid
            if version is not None:
                kwargs["version"] = version

            resource = ClusterPeer(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to create ClusterPeer: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a cluster peer instance.
### Learn more
* [`DOC /cluster/peers`](#docs-cluster-cluster_peers)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="cluster peer modify")
        async def cluster_peer_modify(
            name: str = None,
            query_name: str = None,
            peer_applications: List[str] = None,
            query_peer_applications: List[str] = None,
            uuid: str = None,
            query_uuid: str = None,
        ) -> ResourceTable:
            """Modify an instance of a ClusterPeer resource

            Args:
                name: Optional name for the cluster peer relationship. By default, it is the name of the remote cluster.
                query_name: Optional name for the cluster peer relationship. By default, it is the name of the remote cluster.
                peer_applications: Peering applications against which allowed SVMs are configured.
                query_peer_applications: Peering applications against which allowed SVMs are configured.
                uuid: UUID of the cluster peer relationship. For anonymous cluster peer offers, the UUID will change when the remote cluster accepts the relationship.
                query_uuid: UUID of the cluster peer relationship. For anonymous cluster peer offers, the UUID will change when the remote cluster accepts the relationship.
            """

            kwargs = {}
            changes = {}
            if query_name is not None:
                kwargs["name"] = query_name
            if query_peer_applications is not None:
                kwargs["peer_applications"] = query_peer_applications
            if query_uuid is not None:
                kwargs["uuid"] = query_uuid

            if name is not None:
                changes["name"] = name
            if peer_applications is not None:
                changes["peer_applications"] = peer_applications
            if uuid is not None:
                changes["uuid"] = uuid

            if hasattr(ClusterPeer, "find"):
                resource = ClusterPeer.find(
                    **kwargs
                )
            else:
                resource = ClusterPeer()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to modify ClusterPeer: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a cluster peer.
### Learn more
* [`DOC /cluster/peers`](#docs-cluster-cluster_peers)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="cluster peer delete")
        async def cluster_peer_delete(
            name: str = None,
            peer_applications: List[str] = None,
            uuid: str = None,
        ) -> None:
            """Delete an instance of a ClusterPeer resource

            Args:
                name: Optional name for the cluster peer relationship. By default, it is the name of the remote cluster.
                peer_applications: Peering applications against which allowed SVMs are configured.
                uuid: UUID of the cluster peer relationship. For anonymous cluster peer offers, the UUID will change when the remote cluster accepts the relationship.
            """

            kwargs = {}
            if name is not None:
                kwargs["name"] = name
            if peer_applications is not None:
                kwargs["peer_applications"] = peer_applications
            if uuid is not None:
                kwargs["uuid"] = uuid

            if hasattr(ClusterPeer, "find"):
                resource = ClusterPeer.find(
                    **kwargs
                )
            else:
                resource = ClusterPeer()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to delete ClusterPeer: %s" % err)


