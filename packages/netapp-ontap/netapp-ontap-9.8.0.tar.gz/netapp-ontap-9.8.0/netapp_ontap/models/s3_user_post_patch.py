r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["S3UserPostPatch", "S3UserPostPatchSchema"]
__pdoc__ = {
    "S3UserPostPatchSchema.resource": False,
    "S3UserPostPatch": False,
}


class S3UserPostPatchSchema(ResourceSchema):
    """The fields of the S3UserPostPatch object"""

    num_records = Size(data_key="num_records")
    r""" Number of records """

    records = fields.List(fields.Nested("netapp_ontap.models.s3_service_user_post_response.S3ServiceUserPostSchema", unknown=EXCLUDE), data_key="records")
    r""" The records field of the s3_user_post_patch. """

    @property
    def resource(self):
        return S3UserPostPatch

    gettable_fields = [
        "num_records",
        "records",
    ]
    """num_records,records,"""

    patchable_fields = [
        "num_records",
        "records",
    ]
    """num_records,records,"""

    postable_fields = [
        "num_records",
        "records",
    ]
    """num_records,records,"""


class S3UserPostPatch(Resource):

    _schema = S3UserPostPatchSchema
