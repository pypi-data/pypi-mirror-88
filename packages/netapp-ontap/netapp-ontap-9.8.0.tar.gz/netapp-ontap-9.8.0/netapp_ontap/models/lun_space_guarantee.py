r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["LunSpaceGuarantee", "LunSpaceGuaranteeSchema"]
__pdoc__ = {
    "LunSpaceGuaranteeSchema.resource": False,
    "LunSpaceGuarantee": False,
}


class LunSpaceGuaranteeSchema(ResourceSchema):
    """The fields of the LunSpaceGuarantee object"""

    requested = fields.Boolean(data_key="requested")
    r""" The requested space reservation policy for the LUN. If _true_, a space reservation is requested for the LUN; if _false_, the LUN is thin provisioned. Guaranteeing a space reservation request for a LUN requires that the volume in which the LUN resides is also space reserved and that the fractional reserve for the volume is 100%. Valid in POST and PATCH. """

    reserved = fields.Boolean(data_key="reserved")
    r""" Reports if the LUN is space guaranteed.<br/>
If _true_, a space guarantee is requested and the containing volume and aggregate support the request. If _false_, a space guarantee is not requested or a space guarantee is requested and either the containing volume or aggregate do not support the request. """

    @property
    def resource(self):
        return LunSpaceGuarantee

    gettable_fields = [
        "requested",
        "reserved",
    ]
    """requested,reserved,"""

    patchable_fields = [
        "requested",
    ]
    """requested,"""

    postable_fields = [
        "requested",
    ]
    """requested,"""


class LunSpaceGuarantee(Resource):

    _schema = LunSpaceGuaranteeSchema
