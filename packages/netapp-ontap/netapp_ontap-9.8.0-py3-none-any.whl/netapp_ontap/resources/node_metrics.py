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


__all__ = ["NodeMetrics", "NodeMetricsSchema"]
__pdoc__ = {
    "NodeMetricsSchema.resource": False,
    "NodeMetrics.node_metrics_show": False,
    "NodeMetrics.node_metrics_create": False,
    "NodeMetrics.node_metrics_modify": False,
    "NodeMetrics.node_metrics_delete": False,
}


class NodeMetricsSchema(ResourceSchema):
    """The fields of the NodeMetrics object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the node_metrics. """

    duration = fields.Str(
        data_key="duration",
        validate=enum_validation(['PT15S', 'PT5M', 'PT30M', 'PT2H', 'P1D']),
    )
    r""" The duration over which this sample is calculated. The time durations are represented in the ISO-8601 standard format. Samples can be calculated over the following durations:


Valid choices:

* PT15S
* PT5M
* PT30M
* PT2H
* P1D """

    processor_utilization = Size(
        data_key="processor_utilization",
    )
    r""" Average CPU Utilization for the node

Example: 13 """

    status = fields.Str(
        data_key="status",
        validate=enum_validation(['ok', 'error', 'partial_no_data', 'partial_no_uuid', 'partial_no_response', 'partial_other_error', 'negative_delta', 'backfilled_data', 'inconsistent_delta_time', 'inconsistent_old_data']),
    )
    r""" Errors associated with the sample. For example, if the aggregation of data over multiple nodes fails, then any partial errors might return "ok" on success or "error" on an internal uncategorized failure. Whenever a sample collection is missed but done at a later time, it is back filled to the previous 15 second timestamp and tagged with "backfilled_data". "inconsistent_delta_time" is encountered when the time between two collections is not the same for all nodes. Therefore, the aggregated value might be over or under inflated. "Negative_delta" is returned when an expected monotonically increasing value has decreased in value. "inconsistent_old_data" is returned when one or more nodes do not have the latest data.

Valid choices:

* ok
* error
* partial_no_data
* partial_no_uuid
* partial_no_response
* partial_other_error
* negative_delta
* backfilled_data
* inconsistent_delta_time
* inconsistent_old_data """

    timestamp = ImpreciseDateTime(
        data_key="timestamp",
    )
    r""" The timestamp of the performance data.

Example: 2017-01-25T11:20:13.000+0000 """

    @property
    def resource(self):
        return NodeMetrics

    gettable_fields = [
        "links",
        "duration",
        "processor_utilization",
        "status",
        "timestamp",
    ]
    """links,duration,processor_utilization,status,timestamp,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in NodeMetrics.get_collection(fields=field)]
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
            raise NetAppRestError("NodeMetrics modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class NodeMetrics(Resource):
    r""" CPU performance for the nodes. """

    _schema = NodeMetricsSchema
    _path = "/api/cluster/nodes/{node[uuid]}/metrics"
    _keys = ["node.uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves historical performance metrics for a node."""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="node metrics show")
        def node_metrics_show(
            uuid,
            duration: Choices.define(_get_field_list("duration"), cache_choices=True, inexact=True)=None,
            processor_utilization: Choices.define(_get_field_list("processor_utilization"), cache_choices=True, inexact=True)=None,
            status: Choices.define(_get_field_list("status"), cache_choices=True, inexact=True)=None,
            timestamp: Choices.define(_get_field_list("timestamp"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["duration", "processor_utilization", "status", "timestamp", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of NodeMetrics resources

            Args:
                duration: The duration over which this sample is calculated. The time durations are represented in the ISO-8601 standard format. Samples can be calculated over the following durations: 
                processor_utilization: Average CPU Utilization for the node
                status: Errors associated with the sample. For example, if the aggregation of data over multiple nodes fails, then any partial errors might return \"ok\" on success or \"error\" on an internal uncategorized failure. Whenever a sample collection is missed but done at a later time, it is back filled to the previous 15 second timestamp and tagged with \"backfilled_data\". \"inconsistent_delta_time\" is encountered when the time between two collections is not the same for all nodes. Therefore, the aggregated value might be over or under inflated. \"Negative_delta\" is returned when an expected monotonically increasing value has decreased in value. \"inconsistent_old_data\" is returned when one or more nodes do not have the latest data.
                timestamp: The timestamp of the performance data.
            """

            kwargs = {}
            if duration is not None:
                kwargs["duration"] = duration
            if processor_utilization is not None:
                kwargs["processor_utilization"] = processor_utilization
            if status is not None:
                kwargs["status"] = status
            if timestamp is not None:
                kwargs["timestamp"] = timestamp
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return NodeMetrics.get_collection(
                uuid,
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves historical performance metrics for a node."""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)



    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves historical performance metrics for a node."""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)






