r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["NvmeSubsystemNamespace", "NvmeSubsystemNamespaceSchema"]
__pdoc__ = {
    "NvmeSubsystemNamespaceSchema.resource": False,
    "NvmeSubsystemNamespace": False,
}


class NvmeSubsystemNamespaceSchema(ResourceSchema):
    """The fields of the NvmeSubsystemNamespace object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the nvme_subsystem_namespace. """

    name = fields.Str(data_key="name")
    r""" The name of the NVMe namespace.


Example: /vol/vol1/namespace1 """

    uuid = fields.Str(data_key="uuid")
    r""" The unique identifier of the NVMe namespace.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return NvmeSubsystemNamespace

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


class NvmeSubsystemNamespace(Resource):

    _schema = NvmeSubsystemNamespaceSchema
