r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["VolumeMovement", "VolumeMovementSchema"]
__pdoc__ = {
    "VolumeMovementSchema.resource": False,
    "VolumeMovement": False,
}


class VolumeMovementSchema(ResourceSchema):
    """The fields of the VolumeMovement object"""

    cutover_window = Size(data_key="cutover_window")
    r""" Time window in seconds for cutover. The allowed range is between 30 to 300 seconds.

Example: 30 """

    destination_aggregate = fields.Nested("netapp_ontap.resources.aggregate.AggregateSchema", unknown=EXCLUDE, data_key="destination_aggregate")
    r""" The destination_aggregate field of the volume_movement. """

    percent_complete = Size(data_key="percent_complete")
    r""" Completion percentage """

    state = fields.Str(data_key="state")
    r""" State of volume move operation. PATCH the state to "aborted" to abort the move operation. PATCH the state to "cutover" to trigger cutover. PATCH the state to "paused" to pause the volume move operation in progress. PATCH the state to "replicating" to resume the paused volume move operation. PATCH the state to "cutover_wait" to go into cutover manually. When volume move operation is waiting to go into "cutover" state, this is indicated by the "cutover_pending" state. A change of state is only supported if volume movement is in progress.

Valid choices:

* aborted
* cutover
* cutover_wait
* cutover_pending
* failed
* paused
* queued
* replicating
* success """

    tiering_policy = fields.Str(data_key="tiering_policy")
    r""" Tiering policy for FabricPool

Valid choices:

* all
* auto
* backup
* none
* snapshot_only """

    @property
    def resource(self):
        return VolumeMovement

    gettable_fields = [
        "cutover_window",
        "destination_aggregate.links",
        "destination_aggregate.name",
        "destination_aggregate.uuid",
        "percent_complete",
        "state",
    ]
    """cutover_window,destination_aggregate.links,destination_aggregate.name,destination_aggregate.uuid,percent_complete,state,"""

    patchable_fields = [
        "cutover_window",
        "destination_aggregate.name",
        "destination_aggregate.uuid",
        "state",
        "tiering_policy",
    ]
    """cutover_window,destination_aggregate.name,destination_aggregate.uuid,state,tiering_policy,"""

    postable_fields = [
        "cutover_window",
        "destination_aggregate.name",
        "destination_aggregate.uuid",
        "state",
    ]
    """cutover_window,destination_aggregate.name,destination_aggregate.uuid,state,"""


class VolumeMovement(Resource):

    _schema = VolumeMovementSchema
