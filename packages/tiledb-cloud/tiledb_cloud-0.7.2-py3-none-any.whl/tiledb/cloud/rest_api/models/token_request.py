# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.1.1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud.rest_api.configuration import Configuration


class TokenRequest(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {"expires": "datetime", "name": "str", "scope": "str"}

    attribute_map = {"expires": "expires", "name": "name", "scope": "scope"}

    def __init__(
        self, expires=None, name=None, scope="*", local_vars_configuration=None
    ):  # noqa: E501
        """TokenRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._expires = None
        self._name = None
        self._scope = None
        self.discriminator = None

        if expires is not None:
            self.expires = expires
        if name is not None:
            self.name = name
        if scope is not None:
            self.scope = scope

    @property
    def expires(self):
        """Gets the expires of this TokenRequest.  # noqa: E501

        Expiration date for token, if empty token defaults to 30 minutes  # noqa: E501

        :return: The expires of this TokenRequest.  # noqa: E501
        :rtype: datetime
        """
        return self._expires

    @expires.setter
    def expires(self, expires):
        """Sets the expires of this TokenRequest.

        Expiration date for token, if empty token defaults to 30 minutes  # noqa: E501

        :param expires: The expires of this TokenRequest.  # noqa: E501
        :type: datetime
        """

        self._expires = expires

    @property
    def name(self):
        """Gets the name of this TokenRequest.  # noqa: E501

        Optional name for token, if the name already exists for the user it will be auto incremented (i.e. myToken-1)  # noqa: E501

        :return: The name of this TokenRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this TokenRequest.

        Optional name for token, if the name already exists for the user it will be auto incremented (i.e. myToken-1)  # noqa: E501

        :param name: The name of this TokenRequest.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def scope(self):
        """Gets the scope of this TokenRequest.  # noqa: E501

        Optional scope to limit token, defaults to all permissions, current supported values are password_reset or *  # noqa: E501

        :return: The scope of this TokenRequest.  # noqa: E501
        :rtype: str
        """
        return self._scope

    @scope.setter
    def scope(self, scope):
        """Sets the scope of this TokenRequest.

        Optional scope to limit token, defaults to all permissions, current supported values are password_reset or *  # noqa: E501

        :param scope: The scope of this TokenRequest.  # noqa: E501
        :type: str
        """

        self._scope = scope

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, TokenRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TokenRequest):
            return True

        return self.to_dict() != other.to_dict()
