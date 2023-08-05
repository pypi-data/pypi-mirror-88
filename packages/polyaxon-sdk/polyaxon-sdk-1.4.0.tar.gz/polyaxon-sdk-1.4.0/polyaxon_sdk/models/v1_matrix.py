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


class V1Matrix(object):
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
        'random': 'V1RandomSearch',
        'grid': 'V1GridSearch',
        'hyperband': 'V1Hyperband',
        'bayes': 'V1Bayes',
        'hyperopt': 'V1Hyperopt',
        'iterative': 'V1Iterative',
        'mapping': 'V1Mapping'
    }

    attribute_map = {
        'random': 'random',
        'grid': 'grid',
        'hyperband': 'hyperband',
        'bayes': 'bayes',
        'hyperopt': 'hyperopt',
        'iterative': 'iterative',
        'mapping': 'mapping'
    }

    def __init__(self, random=None, grid=None, hyperband=None, bayes=None, hyperopt=None, iterative=None, mapping=None, local_vars_configuration=None):  # noqa: E501
        """V1Matrix - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._random = None
        self._grid = None
        self._hyperband = None
        self._bayes = None
        self._hyperopt = None
        self._iterative = None
        self._mapping = None
        self.discriminator = None

        if random is not None:
            self.random = random
        if grid is not None:
            self.grid = grid
        if hyperband is not None:
            self.hyperband = hyperband
        if bayes is not None:
            self.bayes = bayes
        if hyperopt is not None:
            self.hyperopt = hyperopt
        if iterative is not None:
            self.iterative = iterative
        if mapping is not None:
            self.mapping = mapping

    @property
    def random(self):
        """Gets the random of this V1Matrix.  # noqa: E501


        :return: The random of this V1Matrix.  # noqa: E501
        :rtype: V1RandomSearch
        """
        return self._random

    @random.setter
    def random(self, random):
        """Sets the random of this V1Matrix.


        :param random: The random of this V1Matrix.  # noqa: E501
        :type: V1RandomSearch
        """

        self._random = random

    @property
    def grid(self):
        """Gets the grid of this V1Matrix.  # noqa: E501


        :return: The grid of this V1Matrix.  # noqa: E501
        :rtype: V1GridSearch
        """
        return self._grid

    @grid.setter
    def grid(self, grid):
        """Sets the grid of this V1Matrix.


        :param grid: The grid of this V1Matrix.  # noqa: E501
        :type: V1GridSearch
        """

        self._grid = grid

    @property
    def hyperband(self):
        """Gets the hyperband of this V1Matrix.  # noqa: E501


        :return: The hyperband of this V1Matrix.  # noqa: E501
        :rtype: V1Hyperband
        """
        return self._hyperband

    @hyperband.setter
    def hyperband(self, hyperband):
        """Sets the hyperband of this V1Matrix.


        :param hyperband: The hyperband of this V1Matrix.  # noqa: E501
        :type: V1Hyperband
        """

        self._hyperband = hyperband

    @property
    def bayes(self):
        """Gets the bayes of this V1Matrix.  # noqa: E501


        :return: The bayes of this V1Matrix.  # noqa: E501
        :rtype: V1Bayes
        """
        return self._bayes

    @bayes.setter
    def bayes(self, bayes):
        """Sets the bayes of this V1Matrix.


        :param bayes: The bayes of this V1Matrix.  # noqa: E501
        :type: V1Bayes
        """

        self._bayes = bayes

    @property
    def hyperopt(self):
        """Gets the hyperopt of this V1Matrix.  # noqa: E501


        :return: The hyperopt of this V1Matrix.  # noqa: E501
        :rtype: V1Hyperopt
        """
        return self._hyperopt

    @hyperopt.setter
    def hyperopt(self, hyperopt):
        """Sets the hyperopt of this V1Matrix.


        :param hyperopt: The hyperopt of this V1Matrix.  # noqa: E501
        :type: V1Hyperopt
        """

        self._hyperopt = hyperopt

    @property
    def iterative(self):
        """Gets the iterative of this V1Matrix.  # noqa: E501


        :return: The iterative of this V1Matrix.  # noqa: E501
        :rtype: V1Iterative
        """
        return self._iterative

    @iterative.setter
    def iterative(self, iterative):
        """Sets the iterative of this V1Matrix.


        :param iterative: The iterative of this V1Matrix.  # noqa: E501
        :type: V1Iterative
        """

        self._iterative = iterative

    @property
    def mapping(self):
        """Gets the mapping of this V1Matrix.  # noqa: E501


        :return: The mapping of this V1Matrix.  # noqa: E501
        :rtype: V1Mapping
        """
        return self._mapping

    @mapping.setter
    def mapping(self, mapping):
        """Sets the mapping of this V1Matrix.


        :param mapping: The mapping of this V1Matrix.  # noqa: E501
        :type: V1Mapping
        """

        self._mapping = mapping

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
        if not isinstance(other, V1Matrix):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1Matrix):
            return True

        return self.to_dict() != other.to_dict()
