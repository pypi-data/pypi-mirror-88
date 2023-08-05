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


class SubarrayPartitioner(object):
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
    openapi_types = {
        "subarray": "Subarray",
        "budget": "list[AttributeBufferSize]",
        "current": "SubarrayPartitionerCurrent",
        "state": "SubarrayPartitionerState",
        "memory_budget": "int",
        "memory_budget_var": "int",
    }

    attribute_map = {
        "subarray": "subarray",
        "budget": "budget",
        "current": "current",
        "state": "state",
        "memory_budget": "memoryBudget",
        "memory_budget_var": "memoryBudgetVar",
    }

    def __init__(
        self,
        subarray=None,
        budget=None,
        current=None,
        state=None,
        memory_budget=None,
        memory_budget_var=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """SubarrayPartitioner - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._subarray = None
        self._budget = None
        self._current = None
        self._state = None
        self._memory_budget = None
        self._memory_budget_var = None
        self.discriminator = None

        if subarray is not None:
            self.subarray = subarray
        if budget is not None:
            self.budget = budget
        if current is not None:
            self.current = current
        if state is not None:
            self.state = state
        if memory_budget is not None:
            self.memory_budget = memory_budget
        if memory_budget_var is not None:
            self.memory_budget_var = memory_budget_var

    @property
    def subarray(self):
        """Gets the subarray of this SubarrayPartitioner.  # noqa: E501


        :return: The subarray of this SubarrayPartitioner.  # noqa: E501
        :rtype: Subarray
        """
        return self._subarray

    @subarray.setter
    def subarray(self, subarray):
        """Sets the subarray of this SubarrayPartitioner.


        :param subarray: The subarray of this SubarrayPartitioner.  # noqa: E501
        :type: Subarray
        """

        self._subarray = subarray

    @property
    def budget(self):
        """Gets the budget of this SubarrayPartitioner.  # noqa: E501

        Result size budget (in bytes) for all attributes.  # noqa: E501

        :return: The budget of this SubarrayPartitioner.  # noqa: E501
        :rtype: list[AttributeBufferSize]
        """
        return self._budget

    @budget.setter
    def budget(self, budget):
        """Sets the budget of this SubarrayPartitioner.

        Result size budget (in bytes) for all attributes.  # noqa: E501

        :param budget: The budget of this SubarrayPartitioner.  # noqa: E501
        :type: list[AttributeBufferSize]
        """

        self._budget = budget

    @property
    def current(self):
        """Gets the current of this SubarrayPartitioner.  # noqa: E501


        :return: The current of this SubarrayPartitioner.  # noqa: E501
        :rtype: SubarrayPartitionerCurrent
        """
        return self._current

    @current.setter
    def current(self, current):
        """Sets the current of this SubarrayPartitioner.


        :param current: The current of this SubarrayPartitioner.  # noqa: E501
        :type: SubarrayPartitionerCurrent
        """

        self._current = current

    @property
    def state(self):
        """Gets the state of this SubarrayPartitioner.  # noqa: E501


        :return: The state of this SubarrayPartitioner.  # noqa: E501
        :rtype: SubarrayPartitionerState
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this SubarrayPartitioner.


        :param state: The state of this SubarrayPartitioner.  # noqa: E501
        :type: SubarrayPartitionerState
        """

        self._state = state

    @property
    def memory_budget(self):
        """Gets the memory_budget of this SubarrayPartitioner.  # noqa: E501

        The memory budget for the fixed-sized attributes and the offsets of the var-sized attributes  # noqa: E501

        :return: The memory_budget of this SubarrayPartitioner.  # noqa: E501
        :rtype: int
        """
        return self._memory_budget

    @memory_budget.setter
    def memory_budget(self, memory_budget):
        """Sets the memory_budget of this SubarrayPartitioner.

        The memory budget for the fixed-sized attributes and the offsets of the var-sized attributes  # noqa: E501

        :param memory_budget: The memory_budget of this SubarrayPartitioner.  # noqa: E501
        :type: int
        """

        self._memory_budget = memory_budget

    @property
    def memory_budget_var(self):
        """Gets the memory_budget_var of this SubarrayPartitioner.  # noqa: E501

        The memory budget for the var-sized attributes  # noqa: E501

        :return: The memory_budget_var of this SubarrayPartitioner.  # noqa: E501
        :rtype: int
        """
        return self._memory_budget_var

    @memory_budget_var.setter
    def memory_budget_var(self, memory_budget_var):
        """Sets the memory_budget_var of this SubarrayPartitioner.

        The memory budget for the var-sized attributes  # noqa: E501

        :param memory_budget_var: The memory_budget_var of this SubarrayPartitioner.  # noqa: E501
        :type: int
        """

        self._memory_budget_var = memory_budget_var

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
        if not isinstance(other, SubarrayPartitioner):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SubarrayPartitioner):
            return True

        return self.to_dict() != other.to_dict()
