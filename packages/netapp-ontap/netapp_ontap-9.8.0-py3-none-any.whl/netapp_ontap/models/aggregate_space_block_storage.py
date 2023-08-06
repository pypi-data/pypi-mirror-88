r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["AggregateSpaceBlockStorage", "AggregateSpaceBlockStorageSchema"]
__pdoc__ = {
    "AggregateSpaceBlockStorageSchema.resource": False,
    "AggregateSpaceBlockStorage": False,
}


class AggregateSpaceBlockStorageSchema(ResourceSchema):
    """The fields of the AggregateSpaceBlockStorage object"""

    available = Size(data_key="available")
    r""" Space available in bytes.

Example: 10156560384 """

    full_threshold_percent = Size(data_key="full_threshold_percent")
    r""" The aggregate used percentage at which 'monitor.volume.full' EMS is generated. """

    inactive_user_data = Size(data_key="inactive_user_data")
    r""" The size that is physically used in the block storage and has a cold temperature, in bytes. This property is only supported if the aggregate is either attached to a cloud store or can be attached to a cloud store.
This is an advanced property; there is an added cost to retrieving its value. The field is not populated for either a collection GET or an instance GET unless it is explicitly requested using the <i>fields</i> query parameter containing either block_storage.inactive_user_data or **.


Example: 304448 """

    size = Size(data_key="size")
    r""" Total usable space in bytes, not including WAFL reserve and aggregate Snapshot copy reserve.

Example: 10156769280 """

    used = Size(data_key="used")
    r""" Space used or reserved in bytes. Includes volume guarantees and aggregate metadata.

Example: 2088960 """

    @property
    def resource(self):
        return AggregateSpaceBlockStorage

    gettable_fields = [
        "available",
        "full_threshold_percent",
        "inactive_user_data",
        "size",
        "used",
    ]
    """available,full_threshold_percent,inactive_user_data,size,used,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class AggregateSpaceBlockStorage(Resource):

    _schema = AggregateSpaceBlockStorageSchema
