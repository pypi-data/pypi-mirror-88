#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
    Polyaxon SDKs and REST API specification.

    Polyaxon SDKs and REST API specification.  # noqa: E501

    The version of the OpenAPI document: 1.4.0
    Contact: contact@polyaxon.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from polyaxon_sdk.configuration import Configuration


class V1ConnectionResponse(object):
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
        'uuid': 'str',
        'name': 'str',
        'agent': 'str',
        'description': 'str',
        'tags': 'list[str]',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'live_state': 'int',
        'kind': 'V1ConnectionKind'
    }

    attribute_map = {
        'uuid': 'uuid',
        'name': 'name',
        'agent': 'agent',
        'description': 'description',
        'tags': 'tags',
        'created_at': 'created_at',
        'updated_at': 'updated_at',
        'live_state': 'live_state',
        'kind': 'kind'
    }

    def __init__(self, uuid=None, name=None, agent=None, description=None, tags=None, created_at=None, updated_at=None, live_state=None, kind=None, local_vars_configuration=None):  # noqa: E501
        """V1ConnectionResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._uuid = None
        self._name = None
        self._agent = None
        self._description = None
        self._tags = None
        self._created_at = None
        self._updated_at = None
        self._live_state = None
        self._kind = None
        self.discriminator = None

        if uuid is not None:
            self.uuid = uuid
        if name is not None:
            self.name = name
        if agent is not None:
            self.agent = agent
        if description is not None:
            self.description = description
        if tags is not None:
            self.tags = tags
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if live_state is not None:
            self.live_state = live_state
        if kind is not None:
            self.kind = kind

    @property
    def uuid(self):
        """Gets the uuid of this V1ConnectionResponse.  # noqa: E501


        :return: The uuid of this V1ConnectionResponse.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this V1ConnectionResponse.


        :param uuid: The uuid of this V1ConnectionResponse.  # noqa: E501
        :type: str
        """

        self._uuid = uuid

    @property
    def name(self):
        """Gets the name of this V1ConnectionResponse.  # noqa: E501


        :return: The name of this V1ConnectionResponse.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this V1ConnectionResponse.


        :param name: The name of this V1ConnectionResponse.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def agent(self):
        """Gets the agent of this V1ConnectionResponse.  # noqa: E501


        :return: The agent of this V1ConnectionResponse.  # noqa: E501
        :rtype: str
        """
        return self._agent

    @agent.setter
    def agent(self, agent):
        """Sets the agent of this V1ConnectionResponse.


        :param agent: The agent of this V1ConnectionResponse.  # noqa: E501
        :type: str
        """

        self._agent = agent

    @property
    def description(self):
        """Gets the description of this V1ConnectionResponse.  # noqa: E501


        :return: The description of this V1ConnectionResponse.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this V1ConnectionResponse.


        :param description: The description of this V1ConnectionResponse.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def tags(self):
        """Gets the tags of this V1ConnectionResponse.  # noqa: E501


        :return: The tags of this V1ConnectionResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this V1ConnectionResponse.


        :param tags: The tags of this V1ConnectionResponse.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def created_at(self):
        """Gets the created_at of this V1ConnectionResponse.  # noqa: E501


        :return: The created_at of this V1ConnectionResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this V1ConnectionResponse.


        :param created_at: The created_at of this V1ConnectionResponse.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this V1ConnectionResponse.  # noqa: E501


        :return: The updated_at of this V1ConnectionResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this V1ConnectionResponse.


        :param updated_at: The updated_at of this V1ConnectionResponse.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def live_state(self):
        """Gets the live_state of this V1ConnectionResponse.  # noqa: E501


        :return: The live_state of this V1ConnectionResponse.  # noqa: E501
        :rtype: int
        """
        return self._live_state

    @live_state.setter
    def live_state(self, live_state):
        """Sets the live_state of this V1ConnectionResponse.


        :param live_state: The live_state of this V1ConnectionResponse.  # noqa: E501
        :type: int
        """

        self._live_state = live_state

    @property
    def kind(self):
        """Gets the kind of this V1ConnectionResponse.  # noqa: E501


        :return: The kind of this V1ConnectionResponse.  # noqa: E501
        :rtype: V1ConnectionKind
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """Sets the kind of this V1ConnectionResponse.


        :param kind: The kind of this V1ConnectionResponse.  # noqa: E501
        :type: V1ConnectionKind
        """

        self._kind = kind

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
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
        if not isinstance(other, V1ConnectionResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1ConnectionResponse):
            return True

        return self.to_dict() != other.to_dict()
