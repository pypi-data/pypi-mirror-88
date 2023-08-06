r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size


__all__ = ["KeyManagerState", "KeyManagerStateSchema"]
__pdoc__ = {
    "KeyManagerStateSchema.resource": False,
    "KeyManagerState": False,
}


class KeyManagerStateSchema(ResourceSchema):
    """The fields of the KeyManagerState object"""

    code = Size(data_key="code")
    r""" Code corresponding to the status message. Returns 0 if the setup is complete. This is an advanced property; there is an added cost to retrieving its value. The property is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter or GET for all advanced properties is enabled.

Example: 346758 """

    message = fields.Str(data_key="message")
    r""" Current state of the key manager indicating any additional steps to perform to finish the setup. This is an advanced property; there is an added cost to retrieving its value. The property is not populated for either a collection GET or an instance GET unless it is explicitly requested using the `fields` query parameter or GET for all advanced properties is enabled.

Example: This cluster is part of a MetroCluster configuration. Use the REST API POST method security/key_managers/ with the synchronize option and the same passphrase on the partner cluster before proceeding with any key manager operations.  Failure to do so could lead to switchover or switchback failure. """

    @property
    def resource(self):
        return KeyManagerState

    gettable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class KeyManagerState(Resource):

    _schema = KeyManagerStateSchema
