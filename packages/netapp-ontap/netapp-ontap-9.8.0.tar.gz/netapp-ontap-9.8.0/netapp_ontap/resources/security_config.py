r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
You can use this API for various cluster-wide security-related operations.
## "onboard_key_manager_configurable_status" object
Use this API to retrieve details of whether or not the Onboard Key Manager can be configured on the cluster.

* GET    /api/security
* GET    /api/security?fields=onboard_key_manager_configurable_status
## "software_data_encryption" object
Contains software data encryption related information.<br/>
  The following APIs can be used to enable or disable and obtain default software data at rest encryption values:

  * PATCH  /api/security -d '{ "software_data_encryption.disabled_by_default" : true }'
  * PATCH  /api/security -d '{ "software_data_encryption.disabled_by_default" : false }'
  * GET    /api/security
  * GET    /api/security?fields=software_data_encryption <br/>
A PATCH request on this API using the parameter "software_data_encryption.conversion_enabled" triggers the  conversion of all non-encrypted metadata volumes to encrypted metadata volumes and all non-NAE aggregates to NAE aggregates. For the conversion to start, the cluster must have either an Onboard or an external key manager set up and the aggregates should either be empty or have only metadata volumes. No data volumes should be present in any of the aggregates. For MetroCluster configurations, the PATCH request will fail if the cluster is in the switchover state.<br/>
The following API can be used to initiate software data encryption conversion.

* PATCH  /api/security -d '{ "software_data_encryption.conversion_enabled" : true }'
## "fips" object
Contains FIPS mode information.<br/>
A PATCH request on this API using the parameter "fips.enabled" switches the system from using the default cryptographic module software implementations to validated ones or vice versa, where applicable. If the value of the parameter is "true" and unapproved algorithms are configured as permitted in relevant subsystems, those algorithms will be disabled in the relevant subsystem configurations. If "false", there will be no implied change to the relevant subsystem configurations.

* GET    /api/security
* GET    /api/security?fields=fips
* PATCH  /api/security -d '{ "fips.enabled" : true }'
* PATCH  /api/security -d '{ "fips.enabled" : false }'
## GET Examples
### Retrieving information about the security configured on the cluster
The following example shows how to retrieve the configuration of the cluster.
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import SecurityConfig

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = SecurityConfig()
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
SecurityConfig(
    {
        "onboard_key_manager_configurable_status": {
            "supported": False,
            "message": "Onboard Key Manager cannot be configured on the cluster. There are no self-encrypting disks in the cluster, and the following nodes do not support volume granular encryption: ntap-vsim2.",
            "code": 65537300,
        },
        "fips": {"enabled": False},
    }
)

```
</div>
</div>

---
```
---
## PATCH Examples
### Enabling software encryption conversion in the cluster
The following example shows how to convert all the aggregates and metadata volumes in the cluster from non-encrypted to encrypted.
# The API:
PATCH /api/security
# The call
curl -X PATCH "https://<mgmt_ip>/api/security" -d '{ "software_data_encryption.conversion_enabled" : true }'
# The response:
{
   "job": {
       "uuid": "ebcbd82d-1cd4-11ea-8f75-005056ac4adc",
       "_links": {
           "self": {
               "href": "/api/cluster/jobs/ebcbd82d-1cd4-11ea-8f75-005056ac4adc"
           }
       }
   }
}
This will return a job UUID. A subsequent GET for this job should return the details of the job.
# The call
curl -X GET "https://<mgmt_ip>/api/cluster/jobs/ebcbd82d-1cd4-11ea-8f75-005056ac4adc"
# The response:
{
  "uuid": "ebcbd82d-1cd4-11ea-8f75-005056ac4adc",
  "description": "PATCH /api/security",
  "state": "success",
  "message": "success",
  "code": 0,
  "start_time": "2019-12-12T06:45:40-05:00",
  "end_time": "2019-12-12T06:45:40-05:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/ebcbd82d-1cd4-11ea-8f75-005056ac4adc"
    }
  }
}
### Enabling FIPS mode in the cluster
The following example shows how to enable FIPS mode in the cluster.
# The API:
PATCH /api/security
# The call
curl -X PATCH "https://<mgmt_ip>/api/security" -d '{ "fips.enabled" : true }'
# The response:
{
   "job": {
       "uuid": "8e7f59ee-a9c4-4faa-9513-bef689bbf2c2",
       "_links": {
           "self": {
               "href": "/api/cluster/jobs/8e7f59ee-a9c4-4faa-9513-bef689bbf2c2"
           }
       }
   }
}
This will return a job UUID. A subsequent GET for this job UUID should return the details of the job.
# The call
curl -X GET "https://<mgmt_ip>/api/cluster/jobs/8e7f59ee-a9c4-4faa-9513-bef689bbf2c2"
# The response:
{
  "uuid": "8e7f59ee-a9c4-4faa-9513-bef689bbf2c2",
  "description": "PATCH /api/security",
  "state": "success",
  "message": "success",
  "code": 0,
  "start_time": "2020-04-28T06:55:40-05:00",
  "end_time": "2020-04-28T06:55:41-05:00",
  "_links": {
    "self": {
      "href": "/api/cluster/jobs/8e7f59ee-a9c4-4faa-9513-bef689bbf2c2"
    }
  }
}
---
"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union

try:
    CLICHE_INSTALLED = False
    import cliche
    from cliche.arg_types.choices import Choices
    from cliche.commands import ClicheCommandError
    from netapp_ontap.resource_table import ResourceTable
    CLICHE_INSTALLED = True
except ImportError:
    pass

from marshmallow import fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size
from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["SecurityConfig", "SecurityConfigSchema"]
__pdoc__ = {
    "SecurityConfigSchema.resource": False,
    "SecurityConfig.security_config_show": False,
    "SecurityConfig.security_config_create": False,
    "SecurityConfig.security_config_modify": False,
    "SecurityConfig.security_config_delete": False,
}


class SecurityConfigSchema(ResourceSchema):
    """The fields of the SecurityConfig object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the security_config. """

    fips = fields.Nested("netapp_ontap.models.fips.FipsSchema", data_key="fips", unknown=EXCLUDE)
    r""" The fips field of the security_config. """

    onboard_key_manager_configurable_status = fields.Nested("netapp_ontap.models.onboard_key_manager_configurable_status.OnboardKeyManagerConfigurableStatusSchema", data_key="onboard_key_manager_configurable_status", unknown=EXCLUDE)
    r""" The onboard_key_manager_configurable_status field of the security_config. """

    software_data_encryption = fields.Nested("netapp_ontap.models.software_data_encryption.SoftwareDataEncryptionSchema", data_key="software_data_encryption", unknown=EXCLUDE)
    r""" The software_data_encryption field of the security_config. """

    @property
    def resource(self):
        return SecurityConfig

    gettable_fields = [
        "links",
        "fips",
        "onboard_key_manager_configurable_status",
        "software_data_encryption",
    ]
    """links,fips,onboard_key_manager_configurable_status,software_data_encryption,"""

    patchable_fields = [
        "fips",
        "software_data_encryption",
    ]
    """fips,software_data_encryption,"""

    postable_fields = [
        "fips",
        "software_data_encryption",
    ]
    """fips,software_data_encryption,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in SecurityConfig.get_collection(fields=field)]
    return getter

async def _wait_for_job(response: NetAppResponse) -> None:
    """Examine the given response. If it is a job, asynchronously wait for it to
    complete. While polling, prints the current status message of the job.
    """

    if not response.is_job:
        return
    from netapp_ontap.resources import Job
    job = Job(**response.http_response.json()["job"])
    while True:
        job.get(fields="state,message")
        if hasattr(job, "message"):
            print("[%s]: %s" % (job.state, job.message))
        if job.state == "failure":
            raise NetAppRestError("SecurityConfig modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class SecurityConfig(Resource):
    """Allows interaction with SecurityConfig objects on the host"""

    _schema = SecurityConfigSchema
    _path = "/api/security"
    _action_form_data_parameters = { 'file':'file', }






    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves information about the security configured on the cluster.

### Learn more
* [`DOC /security`](#docs-security-security)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="security config show")
        def security_config_show(
            fields: List[str] = None,
        ) -> ResourceTable:
            """Fetch a single SecurityConfig resource

            Args:
            """

            kwargs = {}
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            resource = SecurityConfig(
                **kwargs
            )
            resource.get()
            return [resource]


    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates the software FIPS mode or enables conversion of non-encrypted metadata volumes to encrypted metadata volumes and non-NAE aggregates to NAE aggregates.

### Learn more
* [`DOC /security`](#docs-security-security)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="security config modify")
        async def security_config_modify(
        ) -> ResourceTable:
            """Modify an instance of a SecurityConfig resource

            Args:
            """

            kwargs = {}
            changes = {}


            if hasattr(SecurityConfig, "find"):
                resource = SecurityConfig.find(
                    **kwargs
                )
            else:
                resource = SecurityConfig()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to modify SecurityConfig: %s" % err)


    def certificate_signing_request(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""This API generates a Certificate Signing Request(CSR) and a private key pair. A CSR is a message sent securely to a certificate authority (CA) via any electronic media to apply for a digital identity certificate. This is a general utility API for users to generate a CSR.
### Recommended optional properties
* `subject_name` - Subject details of the certificate.
* `security_strength` - Key size of the certificate in bits. Specifying a stronger security strength in bits is recommended when creating a certificate.
* `hash_function` -  Hashing function.
* `algorithm` - Asymmetric algorithm. Algorithm used to generate a public/private key pair when creating a certificate.
* `subject_alternatives` - Subject Alternate name extensions.
### Default property values
If not specified in POST, the following default property values are assigned:
* `security_strength` - _112_
* `hash_function` - _sha256_
* `algorithm` - _rsa_
### Related ONTAP commands
* `security certificate generate-csr`
"""
        return super()._action(
            "certificate_signing_request", body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    certificate_signing_request.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._action.__doc__)

