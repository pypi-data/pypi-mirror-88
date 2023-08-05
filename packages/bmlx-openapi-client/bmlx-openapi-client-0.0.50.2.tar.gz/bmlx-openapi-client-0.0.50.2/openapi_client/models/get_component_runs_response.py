# coding: utf-8

"""
    bmlx api-server.

    Documentation of bmlx api-server apis. To find more info about generating spec from source, please refer to https://goswagger.io/use/spec.html  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


import inspect
import pprint
import re  # noqa: F401
import six

from openapi_client.configuration import Configuration


class GetComponentRunsResponse(object):
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
        'component_runs': 'list[ComponentRun]',
        'next_page_token': 'str'
    }

    attribute_map = {
        'component_runs': 'component_runs',
        'next_page_token': 'next_page_token'
    }

    def __init__(self, component_runs=None, next_page_token=None, local_vars_configuration=None):  # noqa: E501
        """GetComponentRunsResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._component_runs = None
        self._next_page_token = None
        self.discriminator = None

        if component_runs is not None:
            self.component_runs = component_runs
        if next_page_token is not None:
            self.next_page_token = next_page_token

    @property
    def component_runs(self):
        """Gets the component_runs of this GetComponentRunsResponse.  # noqa: E501


        :return: The component_runs of this GetComponentRunsResponse.  # noqa: E501
        :rtype: list[ComponentRun]
        """
        return self._component_runs

    @component_runs.setter
    def component_runs(self, component_runs):
        """Sets the component_runs of this GetComponentRunsResponse.


        :param component_runs: The component_runs of this GetComponentRunsResponse.  # noqa: E501
        :type component_runs: list[ComponentRun]
        """

        self._component_runs = component_runs

    @property
    def next_page_token(self):
        """Gets the next_page_token of this GetComponentRunsResponse.  # noqa: E501


        :return: The next_page_token of this GetComponentRunsResponse.  # noqa: E501
        :rtype: str
        """
        return self._next_page_token

    @next_page_token.setter
    def next_page_token(self, next_page_token):
        """Sets the next_page_token of this GetComponentRunsResponse.


        :param next_page_token: The next_page_token of this GetComponentRunsResponse.  # noqa: E501
        :type next_page_token: str
        """

        self._next_page_token = next_page_token

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = inspect.getargsspec(x.to_dict)
                if len(args) == 1:
                    return x.to_dict()
                elif len(args) == 2:
                    return x.to_dict(serialize)
                else:
                    raise ValueError("Invalid argument size of to_dict")
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, GetComponentRunsResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GetComponentRunsResponse):
            return True

        return self.to_dict() != other.to_dict()
