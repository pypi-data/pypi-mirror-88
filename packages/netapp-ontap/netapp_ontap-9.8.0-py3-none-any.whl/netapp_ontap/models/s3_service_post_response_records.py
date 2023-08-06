r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["S3ServicePostResponseRecords", "S3ServicePostResponseRecordsSchema"]
__pdoc__ = {
    "S3ServicePostResponseRecordsSchema.resource": False,
    "S3ServicePostResponseRecords": False,
}


class S3ServicePostResponseRecordsSchema(ResourceSchema):
    """The fields of the S3ServicePostResponseRecords object"""

    links = fields.Nested("netapp_ontap.models.collection_links.CollectionLinksSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the s3_service_post_response_records. """

    job = fields.Nested("netapp_ontap.models.job_link.JobLinkSchema", unknown=EXCLUDE, data_key="job")
    r""" The job field of the s3_service_post_response_records. """

    users = fields.List(fields.Nested("netapp_ontap.models.s3_service_user_post_response.S3ServiceUserPostSchema", unknown=EXCLUDE), data_key="users")
    r""" The users field of the s3_service_post_response_records. """

    @property
    def resource(self):
        return S3ServicePostResponseRecords

    gettable_fields = [
        "links",
        "job",
        "users",
    ]
    """links,job,users,"""

    patchable_fields = [
        "job",
        "users",
    ]
    """job,users,"""

    postable_fields = [
        "job",
        "users",
    ]
    """job,users,"""


class S3ServicePostResponseRecords(Resource):

    _schema = S3ServicePostResponseRecordsSchema
