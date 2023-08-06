r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["MaxdataOnSanApplicationComponentsTiering", "MaxdataOnSanApplicationComponentsTieringSchema"]
__pdoc__ = {
    "MaxdataOnSanApplicationComponentsTieringSchema.resource": False,
    "MaxdataOnSanApplicationComponentsTiering": False,
}


class MaxdataOnSanApplicationComponentsTieringSchema(ResourceSchema):
    """The fields of the MaxdataOnSanApplicationComponentsTiering object"""

    control = fields.Str(data_key="control")
    r""" Storage tiering placement rules for the container(s)

Valid choices:

* best_effort
* disallowed """

    object_stores = fields.List(fields.Nested("netapp_ontap.models.maxdata_on_san_application_components_tiering_object_stores.MaxdataOnSanApplicationComponentsTieringObjectStoresSchema", unknown=EXCLUDE), data_key="object_stores")
    r""" The object_stores field of the maxdata_on_san_application_components_tiering. """

    policy = fields.Str(data_key="policy")
    r""" The storage tiering type of the application component.

Valid choices:

* none
* snapshot_only """

    @property
    def resource(self):
        return MaxdataOnSanApplicationComponentsTiering

    gettable_fields = [
        "policy",
    ]
    """policy,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "control",
        "object_stores",
        "policy",
    ]
    """control,object_stores,policy,"""


class MaxdataOnSanApplicationComponentsTiering(Resource):

    _schema = MaxdataOnSanApplicationComponentsTieringSchema
