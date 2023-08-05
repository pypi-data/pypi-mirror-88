# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.1.1
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import rest_api
from tiledb.cloud.rest_api.models.invitation import Invitation  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestInvitation(unittest.TestCase):
    """Invitation unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Invitation
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.invitation.Invitation()  # noqa: E501
        if include_optional:
            return Invitation(
                id="00000000-0000-0000-0000-000000000000",
                invitation_type="ARRAY_SHARE",
                owner_namespace_uuid="00000000-0000-0000-0000-000000000000",
                user_namespace_uuid="00000000-0000-0000-0000-000000000000",
                organization_user_uuid="00000000-0000-0000-0000-000000000000",
                organization_name="organization_name",
                organization_role="owner",
                array_uuid="00000000-0000-0000-0000-000000000000",
                array_name="array_name",
                email="jane@doe.com",
                actions="read,write",
                status="PENDING",
                created_at=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                expires_at=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                accepted_at=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
            )
        else:
            return Invitation()

    def testInvitation(self):
        """Test Invitation"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
