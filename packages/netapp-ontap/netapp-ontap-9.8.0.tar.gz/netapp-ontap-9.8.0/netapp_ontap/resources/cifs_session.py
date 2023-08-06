r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
ONTAP CIFS sessions `show` functionality is used to provide a list of currently established CIFS sessions.<p/>
The following lists the fields retrieved using the CIFS sessions GET API:<p/>
**node.name:** Node name hosting this record; basically the node hosting the "server_ip".
**node.uuid:** Node UUID hosting this record; basically the node hosting the "server_ip".
**svm.name:** Svm name to which the "server_ip" belongs to.
**svm.uuid:** Svm uuid to which the "server_ip" belongs to.
**server_ip:** All clients connected to this interface are displayed in rows.
**client_ip:** IP address of the client connected to the interface.
**identifier:** Unique identifier used to represent each SMB session.
**connection_id:** Unique identifier used to represent each SMB Connection.
**authentication:** Type of authentication supported by the server when a client accesses a SMB share.
**user:** Username for the Windows client.
**mapped_unix_user:** Mapped UNIX user name.
**open_shares:** Number of shares opened by the client on a specific SVM.
**open_files:** Number of files opened by the client on a specific SVM.
**open_others:** Number of other files opened by the client on a specific SVM.
**connected_duration:** Time elapsed since the first request was sent by the client for this SMB session.
**idle_duration:** Time elapsed since the last request was sent by the client for this SMB session.
**protocol:** SMB protocol dialects over which the client accesses the SMB share.
**availability:** Level of continuous availabilty of protection provided to the files from the SMB share
**smb_signing:** Specifies whether SMB signing is enabled.
**smb_encryption:** Specifies the SMB session encryption status.
**large_mtu:** Specifies whether the SMB session's large MTU is enabled.
**connection_count:** Counter used to track requests that are sent to the volumes to the node.
**volumes.name:** Name of the active volumes the client is accessing.
**volumes.uuid:** UUID of the active volumes the client is accessing.
## Example
### Retrieves established sessions information
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import CifsSession

with HostConnection(
    "<cluster-mgmt-ip>", username="admin", password="password", verify=False
):
    print(list(CifsSession.get_collection(return_timeout=15)))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    CifsSession(
        {
            "connection_id": 91842,
            "identifier": 625718873227788300,
            "svm": {"uuid": "fc824aa8-4e60-11ea-afb1-0050568ec4e4", "name": "vs1"},
            "connection_count": 1,
            "node": {
                "uuid": "85d46998-4e5d-11ea-afb1-0050568ec4e4",
                "name": "bkalyan-vsim1",
            },
        }
    ),
    CifsSession(
        {
            "connection_id": 92080,
            "identifier": 625718873227788500,
            "svm": {"uuid": "fc824aa8-4e60-11ea-afb1-0050568ec4e4", "name": "vs1"},
            "connection_count": 1,
            "node": {
                "uuid": "85d46998-4e5d-11ea-afb1-0050568ec4e4",
                "name": "bkalyan-vsim1",
            },
        }
    ),
]

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


__all__ = ["CifsSession", "CifsSessionSchema"]
__pdoc__ = {
    "CifsSessionSchema.resource": False,
    "CifsSession.cifs_session_show": False,
    "CifsSession.cifs_session_create": False,
    "CifsSession.cifs_session_modify": False,
    "CifsSession.cifs_session_delete": False,
}


class CifsSessionSchema(ResourceSchema):
    """The fields of the CifsSession object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the cifs_session. """

    authentication = fields.Str(
        data_key="authentication",
        validate=enum_validation(['none', 'ntlmv1', 'ntlmv2', 'kerberos', 'anonymous']),
    )
    r""" SMB authentication over which the client accesses the share. The following values are supported:

* none - No authentication
* ntlmv1 - Ntlm version 1 mechanism
* ntlmv2 - Ntlm version 2 mechanism
* kerberos - Kerberos authentication
* anonymous - Anonymous mechanism


Valid choices:

* none
* ntlmv1
* ntlmv2
* kerberos
* anonymous """

    client_ip = fields.Str(
        data_key="client_ip",
    )
    r""" Specifies IP address of the client.


Example: 10.74.7.182 """

    connected_duration = fields.Str(
        data_key="connected_duration",
    )
    r""" Specifies an ISO-8601 format of date and time used to retrieve the connected time duration in hours, minutes, and seconds format.


Example: P4DT84H30M5S """

    connection_count = Size(
        data_key="connection_count",
    )
    r""" A counter used to track requests that are sent to the volumes to the node.


Example: 0 """

    connection_id = Size(
        data_key="connection_id",
    )
    r""" A unique identifier used to represent each SMB connection.


Example: 22802 """

    continuous_availability = fields.Str(
        data_key="continuous_availability",
        validate=enum_validation(['unavailable', 'available', 'partial']),
    )
    r""" The level of continuous availabilty protection provided to the SMB sessions and/or files.

* unavailable - Open file is not continuously available. For sessions, it contains one or more open files but none of them are continuously available.
* available - open file is continuously available. For sessions, it contains one or more open files and all of them are continuously available.
* partial - Sessions only. Contains at least one continuously available open file with other files open but not continuously available.


Valid choices:

* unavailable
* available
* partial """

    identifier = Size(
        data_key="identifier",
    )
    r""" A unique identifier used to represent each SMB session.


Example: 4622663542519103507 """

    idle_duration = fields.Str(
        data_key="idle_duration",
    )
    r""" Specifies an ISO-8601 format of date and time used to retrieve the idle time duration in hours, minutes, and seconds format.


Example: P4DT84H30M5S """

    large_mtu = fields.Boolean(
        data_key="large_mtu",
    )
    r""" Specifies whether or not a large MTU is enabled for an SMB session.


Example: true """

    mapped_unix_user = fields.Str(
        data_key="mapped_unix_user",
    )
    r""" Indicated that a mapped UNIX user has logged in.


Example: root """

    node = fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE)
    r""" The node field of the cifs_session. """

    open_files = Size(
        data_key="open_files",
    )
    r""" Number of files the SMB session has opened. """

    open_other = Size(
        data_key="open_other",
    )
    r""" Number of other files the SMB session has opened. """

    open_shares = Size(
        data_key="open_shares",
    )
    r""" Number of shares the SMB session has opened. """

    protocol = fields.Str(
        data_key="protocol",
        validate=enum_validation(['smb1', 'smb2', 'smb2_1', 'smb3', 'smb3_1']),
    )
    r""" The SMB protocol version over which the client accesses the volumes. The following values are supported:

* smb1 - SMB version 1
* smb2 - SMB version 2
* smb2_1 - SMB version 2 minor version 1
* smb3 - SMB version 3
* smb3_1 - SMB version 3 minor version 1


Valid choices:

* smb1
* smb2
* smb2_1
* smb3
* smb3_1 """

    server_ip = fields.Str(
        data_key="server_ip",
    )
    r""" Specifies the IP address of the SVM.


Example: 10.140.78.248 """

    smb_encryption = fields.Str(
        data_key="smb_encryption",
        validate=enum_validation(['unencrypted', 'encrypted', 'partially_encrypted']),
    )
    r""" Indicates an SMB encryption state. The following values are supported:

* unencrypted - SMB session is not encrypted
* encrypted - SMB session is fully encrypted. SVM level encryption is enabled and encryption occurs for the entire session.
* partially_encrypted - SMB session is partially encrypted. Share level encryption is enabled and encryption is initiated when the tree-connect occurs.


Valid choices:

* unencrypted
* encrypted
* partially_encrypted """

    smb_signing = fields.Boolean(
        data_key="smb_signing",
    )
    r""" Specifies whether or not SMB signing is enabled.

Example: false """

    svm = fields.Nested("netapp_ontap.resources.svm.SvmSchema", data_key="svm", unknown=EXCLUDE)
    r""" The svm field of the cifs_session. """

    user = fields.Str(
        data_key="user",
    )
    r""" Indicates that a Windows user has logged in.


Example: NBCIFSQA2\administrator """

    volumes = fields.List(fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE), data_key="volumes")
    r""" A group of volumes, the client is accessing. """

    @property
    def resource(self):
        return CifsSession

    gettable_fields = [
        "links",
        "authentication",
        "client_ip",
        "connected_duration",
        "connection_count",
        "connection_id",
        "continuous_availability",
        "identifier",
        "idle_duration",
        "large_mtu",
        "mapped_unix_user",
        "node.links",
        "node.name",
        "node.uuid",
        "open_files",
        "open_other",
        "open_shares",
        "protocol",
        "server_ip",
        "smb_encryption",
        "smb_signing",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "user",
        "volumes.links",
        "volumes.name",
        "volumes.uuid",
    ]
    """links,authentication,client_ip,connected_duration,connection_count,connection_id,continuous_availability,identifier,idle_duration,large_mtu,mapped_unix_user,node.links,node.name,node.uuid,open_files,open_other,open_shares,protocol,server_ip,smb_encryption,smb_signing,svm.links,svm.name,svm.uuid,user,volumes.links,volumes.name,volumes.uuid,"""

    patchable_fields = [
        "node.name",
        "node.uuid",
        "svm.name",
        "svm.uuid",
        "volumes.name",
        "volumes.uuid",
    ]
    """node.name,node.uuid,svm.name,svm.uuid,volumes.name,volumes.uuid,"""

    postable_fields = [
        "node.name",
        "node.uuid",
        "svm.name",
        "svm.uuid",
        "volumes.name",
        "volumes.uuid",
    ]
    """node.name,node.uuid,svm.name,svm.uuid,volumes.name,volumes.uuid,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in CifsSession.get_collection(fields=field)]
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
            raise NetAppRestError("CifsSession modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class CifsSession(Resource):
    """Allows interaction with CifsSession objects on the host"""

    _schema = CifsSessionSchema
    _path = "/api/protocols/cifs/sessions"
    _keys = ["node.uuid", "svm.uuid", "identifier", "connection_id"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves the CIFS sessions information for all SVMs.
### Related ONTAP commands
  * `vserver cifs session show -active-volumes`

### Learn more
* [`DOC /protocols/cifs/sessions`](#docs-NAS-protocols_cifs_sessions)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="cifs session show")
        def cifs_session_show(
            authentication: Choices.define(_get_field_list("authentication"), cache_choices=True, inexact=True)=None,
            client_ip: Choices.define(_get_field_list("client_ip"), cache_choices=True, inexact=True)=None,
            connected_duration: Choices.define(_get_field_list("connected_duration"), cache_choices=True, inexact=True)=None,
            connection_count: Choices.define(_get_field_list("connection_count"), cache_choices=True, inexact=True)=None,
            connection_id: Choices.define(_get_field_list("connection_id"), cache_choices=True, inexact=True)=None,
            continuous_availability: Choices.define(_get_field_list("continuous_availability"), cache_choices=True, inexact=True)=None,
            identifier: Choices.define(_get_field_list("identifier"), cache_choices=True, inexact=True)=None,
            idle_duration: Choices.define(_get_field_list("idle_duration"), cache_choices=True, inexact=True)=None,
            large_mtu: Choices.define(_get_field_list("large_mtu"), cache_choices=True, inexact=True)=None,
            mapped_unix_user: Choices.define(_get_field_list("mapped_unix_user"), cache_choices=True, inexact=True)=None,
            open_files: Choices.define(_get_field_list("open_files"), cache_choices=True, inexact=True)=None,
            open_other: Choices.define(_get_field_list("open_other"), cache_choices=True, inexact=True)=None,
            open_shares: Choices.define(_get_field_list("open_shares"), cache_choices=True, inexact=True)=None,
            protocol: Choices.define(_get_field_list("protocol"), cache_choices=True, inexact=True)=None,
            server_ip: Choices.define(_get_field_list("server_ip"), cache_choices=True, inexact=True)=None,
            smb_encryption: Choices.define(_get_field_list("smb_encryption"), cache_choices=True, inexact=True)=None,
            smb_signing: Choices.define(_get_field_list("smb_signing"), cache_choices=True, inexact=True)=None,
            user: Choices.define(_get_field_list("user"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["authentication", "client_ip", "connected_duration", "connection_count", "connection_id", "continuous_availability", "identifier", "idle_duration", "large_mtu", "mapped_unix_user", "open_files", "open_other", "open_shares", "protocol", "server_ip", "smb_encryption", "smb_signing", "user", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of CifsSession resources

            Args:
                authentication: SMB authentication over which the client accesses the share. The following values are supported: * none - No authentication * ntlmv1 - Ntlm version 1 mechanism * ntlmv2 - Ntlm version 2 mechanism * kerberos - Kerberos authentication * anonymous - Anonymous mechanism 
                client_ip: Specifies IP address of the client. 
                connected_duration: Specifies an ISO-8601 format of date and time used to retrieve the connected time duration in hours, minutes, and seconds format. 
                connection_count: A counter used to track requests that are sent to the volumes to the node. 
                connection_id: A unique identifier used to represent each SMB connection. 
                continuous_availability: The level of continuous availabilty protection provided to the SMB sessions and/or files. * unavailable - Open file is not continuously available. For sessions, it contains one or more open files but none of them are continuously available. * available - open file is continuously available. For sessions, it contains one or more open files and all of them are continuously available. * partial - Sessions only. Contains at least one continuously available open file with other files open but not continuously available. 
                identifier: A unique identifier used to represent each SMB session. 
                idle_duration: Specifies an ISO-8601 format of date and time used to retrieve the idle time duration in hours, minutes, and seconds format. 
                large_mtu: Specifies whether or not a large MTU is enabled for an SMB session. 
                mapped_unix_user: Indicated that a mapped UNIX user has logged in. 
                open_files: Number of files the SMB session has opened. 
                open_other: Number of other files the SMB session has opened. 
                open_shares: Number of shares the SMB session has opened. 
                protocol: The SMB protocol version over which the client accesses the volumes. The following values are supported: * smb1 - SMB version 1 * smb2 - SMB version 2 * smb2_1 - SMB version 2 minor version 1 * smb3 - SMB version 3 * smb3_1 - SMB version 3 minor version 1 
                server_ip: Specifies the IP address of the SVM. 
                smb_encryption: Indicates an SMB encryption state. The following values are supported: * unencrypted - SMB session is not encrypted * encrypted - SMB session is fully encrypted. SVM level encryption is enabled and encryption occurs for the entire session. * partially_encrypted - SMB session is partially encrypted. Share level encryption is enabled and encryption is initiated when the tree-connect occurs. 
                smb_signing: Specifies whether or not SMB signing is enabled.
                user: Indicates that a Windows user has logged in. 
            """

            kwargs = {}
            if authentication is not None:
                kwargs["authentication"] = authentication
            if client_ip is not None:
                kwargs["client_ip"] = client_ip
            if connected_duration is not None:
                kwargs["connected_duration"] = connected_duration
            if connection_count is not None:
                kwargs["connection_count"] = connection_count
            if connection_id is not None:
                kwargs["connection_id"] = connection_id
            if continuous_availability is not None:
                kwargs["continuous_availability"] = continuous_availability
            if identifier is not None:
                kwargs["identifier"] = identifier
            if idle_duration is not None:
                kwargs["idle_duration"] = idle_duration
            if large_mtu is not None:
                kwargs["large_mtu"] = large_mtu
            if mapped_unix_user is not None:
                kwargs["mapped_unix_user"] = mapped_unix_user
            if open_files is not None:
                kwargs["open_files"] = open_files
            if open_other is not None:
                kwargs["open_other"] = open_other
            if open_shares is not None:
                kwargs["open_shares"] = open_shares
            if protocol is not None:
                kwargs["protocol"] = protocol
            if server_ip is not None:
                kwargs["server_ip"] = server_ip
            if smb_encryption is not None:
                kwargs["smb_encryption"] = smb_encryption
            if smb_signing is not None:
                kwargs["smb_signing"] = smb_signing
            if user is not None:
                kwargs["user"] = user
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return CifsSession.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves the CIFS sessions information for all SVMs.
### Related ONTAP commands
  * `vserver cifs session show -active-volumes`

### Learn more
* [`DOC /protocols/cifs/sessions`](#docs-NAS-protocols_cifs_sessions)"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves the CIFS sessions information for all SVMs.
### Related ONTAP commands
  * `vserver cifs session show -active-volumes`

### Learn more
* [`DOC /protocols/cifs/sessions`](#docs-NAS-protocols_cifs_sessions)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves SMB session information for a specific SMB connection of a SVM in a node.
### Learn more
* [`DOC /protocols/cifs/sessions`](#docs-NAS-protocols_cifs_sessions)
"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)





