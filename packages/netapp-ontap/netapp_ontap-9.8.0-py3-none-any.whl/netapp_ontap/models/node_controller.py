r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["NodeController", "NodeControllerSchema"]
__pdoc__ = {
    "NodeControllerSchema.resource": False,
    "NodeController": False,
}


class NodeControllerSchema(ResourceSchema):
    """The fields of the NodeController object"""

    flash_cache = fields.List(fields.Nested("netapp_ontap.models.node_controller_flash_cache.NodeControllerFlashCacheSchema", unknown=EXCLUDE), data_key="flash_cache")
    r""" A list of Flash-Cache devices. Only returned when requested by name. """

    frus = fields.List(fields.Nested("netapp_ontap.models.node_controller_frus.NodeControllerFrusSchema", unknown=EXCLUDE), data_key="frus")
    r""" List of FRUs on the node. Only returned when requested by name. """

    over_temperature = fields.Str(data_key="over_temperature")
    r""" Specifies whether the hardware is currently operating outside of its recommended temperature range. The hardware shuts down if the temperature exceeds critical thresholds.

Valid choices:

* over
* normal """

    @property
    def resource(self):
        return NodeController

    gettable_fields = [
        "flash_cache",
        "frus",
        "over_temperature",
    ]
    """flash_cache,frus,over_temperature,"""

    patchable_fields = [
        "frus",
    ]
    """frus,"""

    postable_fields = [
        "frus",
    ]
    """frus,"""


class NodeController(Resource):

    _schema = NodeControllerSchema
