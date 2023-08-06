r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["ErrorResponses", "ErrorResponsesSchema"]
__pdoc__ = {
    "ErrorResponsesSchema.resource": False,
    "ErrorResponses": False,
}


class ErrorResponsesSchema(ResourceSchema):
    """The fields of the ErrorResponses object"""

    errors = fields.List(fields.Nested("netapp_ontap.models.error.ErrorSchema", unknown=EXCLUDE), data_key="errors")
    r""" The errors field of the error_responses. """

    @property
    def resource(self):
        return ErrorResponses

    gettable_fields = [
        "errors",
    ]
    """errors,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ErrorResponses(Resource):

    _schema = ErrorResponsesSchema
