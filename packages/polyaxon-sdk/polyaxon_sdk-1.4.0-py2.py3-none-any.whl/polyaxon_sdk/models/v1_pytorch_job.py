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


class V1PytorchJob(object):
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
        'kind': 'str',
        'clean_pod_policy': 'V1CleanPodPolicy',
        'master': 'V1KFReplica',
        'worker': 'V1KFReplica'
    }

    attribute_map = {
        'kind': 'kind',
        'clean_pod_policy': 'cleanPodPolicy',
        'master': 'master',
        'worker': 'worker'
    }

    def __init__(self, kind='pytorch_job', clean_pod_policy=None, master=None, worker=None, local_vars_configuration=None):  # noqa: E501
        """V1PytorchJob - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._kind = None
        self._clean_pod_policy = None
        self._master = None
        self._worker = None
        self.discriminator = None

        if kind is not None:
            self.kind = kind
        if clean_pod_policy is not None:
            self.clean_pod_policy = clean_pod_policy
        if master is not None:
            self.master = master
        if worker is not None:
            self.worker = worker

    @property
    def kind(self):
        """Gets the kind of this V1PytorchJob.  # noqa: E501


        :return: The kind of this V1PytorchJob.  # noqa: E501
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """Sets the kind of this V1PytorchJob.


        :param kind: The kind of this V1PytorchJob.  # noqa: E501
        :type: str
        """

        self._kind = kind

    @property
    def clean_pod_policy(self):
        """Gets the clean_pod_policy of this V1PytorchJob.  # noqa: E501


        :return: The clean_pod_policy of this V1PytorchJob.  # noqa: E501
        :rtype: V1CleanPodPolicy
        """
        return self._clean_pod_policy

    @clean_pod_policy.setter
    def clean_pod_policy(self, clean_pod_policy):
        """Sets the clean_pod_policy of this V1PytorchJob.


        :param clean_pod_policy: The clean_pod_policy of this V1PytorchJob.  # noqa: E501
        :type: V1CleanPodPolicy
        """

        self._clean_pod_policy = clean_pod_policy

    @property
    def master(self):
        """Gets the master of this V1PytorchJob.  # noqa: E501


        :return: The master of this V1PytorchJob.  # noqa: E501
        :rtype: V1KFReplica
        """
        return self._master

    @master.setter
    def master(self, master):
        """Sets the master of this V1PytorchJob.


        :param master: The master of this V1PytorchJob.  # noqa: E501
        :type: V1KFReplica
        """

        self._master = master

    @property
    def worker(self):
        """Gets the worker of this V1PytorchJob.  # noqa: E501


        :return: The worker of this V1PytorchJob.  # noqa: E501
        :rtype: V1KFReplica
        """
        return self._worker

    @worker.setter
    def worker(self, worker):
        """Sets the worker of this V1PytorchJob.


        :param worker: The worker of this V1PytorchJob.  # noqa: E501
        :type: V1KFReplica
        """

        self._worker = worker

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
        if not isinstance(other, V1PytorchJob):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1PytorchJob):
            return True

        return self.to_dict() != other.to_dict()
