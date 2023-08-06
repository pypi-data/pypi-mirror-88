r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["LunIgroup", "LunIgroupSchema"]
__pdoc__ = {
    "LunIgroupSchema.resource": False,
    "LunIgroup": False,
}


class LunIgroupSchema(ResourceSchema):
    """The fields of the LunIgroup object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the lun_igroup. """

    name = fields.Str(data_key="name")
    r""" The name of the initiator group.


Example: igroup1 """

    uuid = fields.Str(data_key="uuid")
    r""" The unique identifier of the initiator group.


Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return LunIgroup

    gettable_fields = [
        "links",
        "name",
        "uuid",
    ]
    """links,name,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class LunIgroup(Resource):

    _schema = LunIgroupSchema
