r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["LunLocation", "LunLocationSchema"]
__pdoc__ = {
    "LunLocationSchema.resource": False,
    "LunLocation": False,
}


class LunLocationSchema(ResourceSchema):
    """The fields of the LunLocation object"""

    logical_unit = fields.Str(data_key="logical_unit")
    r""" The base name component of the LUN. Valid in POST and PATCH.<br/>
If properties `name` and `location.logical_unit` are specified in the same request, they must refer to the base name.<br/>
A PATCH that modifies the base name of the LUN is considered a rename operation.


Example: lun1 """

    qtree = fields.Nested("netapp_ontap.resources.qtree.QtreeSchema", unknown=EXCLUDE, data_key="qtree")
    r""" The qtree field of the lun_location. """

    volume = fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, data_key="volume")
    r""" The volume field of the lun_location. """

    @property
    def resource(self):
        return LunLocation

    gettable_fields = [
        "logical_unit",
        "qtree.links",
        "qtree.id",
        "qtree.name",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """logical_unit,qtree.links,qtree.id,qtree.name,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "logical_unit",
        "qtree.id",
        "qtree.name",
        "volume.name",
        "volume.uuid",
    ]
    """logical_unit,qtree.id,qtree.name,volume.name,volume.uuid,"""

    postable_fields = [
        "logical_unit",
        "qtree.id",
        "qtree.name",
        "volume.name",
        "volume.uuid",
    ]
    """logical_unit,qtree.id,qtree.name,volume.name,volume.uuid,"""


class LunLocation(Resource):

    _schema = LunLocationSchema
