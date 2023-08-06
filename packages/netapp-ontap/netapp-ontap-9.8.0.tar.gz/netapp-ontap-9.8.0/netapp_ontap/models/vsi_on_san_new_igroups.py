r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["VsiOnSanNewIgroups", "VsiOnSanNewIgroupsSchema"]
__pdoc__ = {
    "VsiOnSanNewIgroupsSchema.resource": False,
    "VsiOnSanNewIgroups": False,
}


class VsiOnSanNewIgroupsSchema(ResourceSchema):
    """The fields of the VsiOnSanNewIgroups object"""

    initiators = fields.List(fields.Str, data_key="initiators")
    r""" The initiators field of the vsi_on_san_new_igroups. """

    name = fields.Str(data_key="name")
    r""" The name of the new initiator group. """

    protocol = fields.Str(data_key="protocol")
    r""" The protocol of the new initiator group.

Valid choices:

* fcp
* iscsi
* mixed """

    @property
    def resource(self):
        return VsiOnSanNewIgroups

    gettable_fields = [
        "initiators",
    ]
    """initiators,"""

    patchable_fields = [
        "initiators",
        "name",
        "protocol",
    ]
    """initiators,name,protocol,"""

    postable_fields = [
        "initiators",
        "name",
        "protocol",
    ]
    """initiators,name,protocol,"""


class VsiOnSanNewIgroups(Resource):

    _schema = VsiOnSanNewIgroupsSchema
