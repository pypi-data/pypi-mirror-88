r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
Queries a live collection of observed events on the system.
Note: The `filter.name` parameter is used to pass a filter to be applied to the event collection returned. To retrieve the list of available filters, refer to [/support/ems/filters](#/docs/support/ems_filter_collection_get)
## Example
### Querying for the latest event received by EMS
```JSON
# API
GET /api/support/ems/events?fields=message.name&max_records=1
# Response
200 OK
# JSON Body
{
  "records": [
    {
      "node": {
        "name": "node1",
        "uuid": "f087b8e3-99ac-11e8-b5a5-005056bb4ec7",
        "_links": {
          "self": {
            "href": "/api/cluster/nodes/f087b8e3-99ac-11e8-b5a5-005056bb4ec7"
          }
        }
      },
      "index": 661,
      "message": {
        "name": "raid.aggr.log.CP.count"
      },
      "_links": {
        "self": {
          "href": "/api/support/ems/events/node1/661"
        }
      }
    }
  ],
  "num_records": 1,
  "_links": {
    "self": {
      "href": "/api/support/ems/events?fields=message.name&max_records=1"
    },
  }
}
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


__all__ = ["EmsEvent", "EmsEventSchema"]
__pdoc__ = {
    "EmsEventSchema.resource": False,
    "EmsEvent.ems_event_show": False,
    "EmsEvent.ems_event_create": False,
    "EmsEvent.ems_event_modify": False,
    "EmsEvent.ems_event_delete": False,
}


class EmsEventSchema(ResourceSchema):
    """The fields of the EmsEvent object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the ems_event. """

    index = Size(
        data_key="index",
    )
    r""" Index of the event. Returned by default.

Example: 1 """

    log_message = fields.Str(
        data_key="log_message",
    )
    r""" A formatted text string populated with parameter details. Returned by default. """

    message = fields.Nested("netapp_ontap.models.ems_event_message.EmsEventMessageSchema", data_key="message", unknown=EXCLUDE)
    r""" The message field of the ems_event. """

    node = fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE)
    r""" The node field of the ems_event. """

    parameters = fields.List(fields.Nested("netapp_ontap.models.ems_event_parameter.EmsEventParameterSchema", unknown=EXCLUDE), data_key="parameters")
    r""" A list of parameters provided with the EMS event. """

    source = fields.Str(
        data_key="source",
    )
    r""" Source """

    time = ImpreciseDateTime(
        data_key="time",
    )
    r""" Timestamp of the event. Returned by default. """

    @property
    def resource(self):
        return EmsEvent

    gettable_fields = [
        "links",
        "index",
        "log_message",
        "message",
        "node.links",
        "node.name",
        "node.uuid",
        "parameters",
        "source",
        "time",
    ]
    """links,index,log_message,message,node.links,node.name,node.uuid,parameters,source,time,"""

    patchable_fields = [
        "message",
        "node.name",
        "node.uuid",
        "parameters",
    ]
    """message,node.name,node.uuid,parameters,"""

    postable_fields = [
        "message",
        "node.name",
        "node.uuid",
        "parameters",
    ]
    """message,node.name,node.uuid,parameters,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in EmsEvent.get_collection(fields=field)]
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
            raise NetAppRestError("EmsEvent modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class EmsEvent(Resource):
    """Allows interaction with EmsEvent objects on the host"""

    _schema = EmsEventSchema
    _path = "/api/support/ems/events"

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of observed events.
### Related ONTAP commands
* `event log show`

### Learn more
* [`DOC /support/ems/events`](#docs-support-support_ems_events)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="ems event show")
        def ems_event_show(
            index: Choices.define(_get_field_list("index"), cache_choices=True, inexact=True)=None,
            log_message: Choices.define(_get_field_list("log_message"), cache_choices=True, inexact=True)=None,
            source: Choices.define(_get_field_list("source"), cache_choices=True, inexact=True)=None,
            time: Choices.define(_get_field_list("time"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["index", "log_message", "source", "time", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of EmsEvent resources

            Args:
                index: Index of the event. Returned by default.
                log_message: A formatted text string populated with parameter details. Returned by default.
                source: Source
                time: Timestamp of the event. Returned by default.
            """

            kwargs = {}
            if index is not None:
                kwargs["index"] = index
            if log_message is not None:
                kwargs["log_message"] = log_message
            if source is not None:
                kwargs["source"] = source
            if time is not None:
                kwargs["time"] = time
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return EmsEvent.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves a collection of observed events.
### Related ONTAP commands
* `event log show`

### Learn more
* [`DOC /support/ems/events`](#docs-support-support_ems_events)"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of observed events.
### Related ONTAP commands
* `event log show`

### Learn more
* [`DOC /support/ems/events`](#docs-support-support_ems_events)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






