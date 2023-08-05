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


class V1Schemas(object):
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
        'operation_cond': 'V1OperationCond',
        'early_stopping': 'V1EarlyStopping',
        'matrix': 'V1Matrix',
        'run': 'V1RunSchema',
        'operation': 'V1Operation',
        'compiled_operation': 'V1CompiledOperation',
        'schedule': 'V1Schedule',
        'connection_schema': 'V1ConnectionSchema',
        'hp_params': 'V1HpParams',
        'reference': 'V1Reference',
        'artifacts_mount': 'V1ArtifactsMount',
        'polyaxon_sidecar_container': 'V1PolyaxonSidecarContainer',
        'polyaxon_init_container': 'V1PolyaxonInitContainer',
        'artifacs': 'V1ArtifactsType',
        'wasb': 'V1WasbType',
        'gcs': 'V1GcsType',
        's3': 'V1S3Type',
        'autg': 'V1AuthType',
        'dockerfile': 'V1DockerfileType',
        'git': 'V1GitType',
        'uri': 'V1UriType',
        'k8s_resource': 'V1K8sResourceType',
        'connection': 'V1ConnectionType',
        'event_type': 'V1EventType',
        'matrix_kind': 'V1MatrixKind',
        'schedule_kind': 'V1ScheduleKind',
        'event': 'V1Event'
    }

    attribute_map = {
        'operation_cond': 'operation_cond',
        'early_stopping': 'early_stopping',
        'matrix': 'matrix',
        'run': 'run',
        'operation': 'operation',
        'compiled_operation': 'compiled_operation',
        'schedule': 'schedule',
        'connection_schema': 'connection_schema',
        'hp_params': 'hp_params',
        'reference': 'reference',
        'artifacts_mount': 'artifacts_mount',
        'polyaxon_sidecar_container': 'polyaxon_sidecar_container',
        'polyaxon_init_container': 'polyaxon_init_container',
        'artifacs': 'artifacs',
        'wasb': 'wasb',
        'gcs': 'gcs',
        's3': 's3',
        'autg': 'autg',
        'dockerfile': 'dockerfile',
        'git': 'git',
        'uri': 'uri',
        'k8s_resource': 'k8s_resource',
        'connection': 'connection',
        'event_type': 'event_type',
        'matrix_kind': 'matrix_kind',
        'schedule_kind': 'schedule_kind',
        'event': 'event'
    }

    def __init__(self, operation_cond=None, early_stopping=None, matrix=None, run=None, operation=None, compiled_operation=None, schedule=None, connection_schema=None, hp_params=None, reference=None, artifacts_mount=None, polyaxon_sidecar_container=None, polyaxon_init_container=None, artifacs=None, wasb=None, gcs=None, s3=None, autg=None, dockerfile=None, git=None, uri=None, k8s_resource=None, connection=None, event_type=None, matrix_kind=None, schedule_kind=None, event=None, local_vars_configuration=None):  # noqa: E501
        """V1Schemas - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._operation_cond = None
        self._early_stopping = None
        self._matrix = None
        self._run = None
        self._operation = None
        self._compiled_operation = None
        self._schedule = None
        self._connection_schema = None
        self._hp_params = None
        self._reference = None
        self._artifacts_mount = None
        self._polyaxon_sidecar_container = None
        self._polyaxon_init_container = None
        self._artifacs = None
        self._wasb = None
        self._gcs = None
        self._s3 = None
        self._autg = None
        self._dockerfile = None
        self._git = None
        self._uri = None
        self._k8s_resource = None
        self._connection = None
        self._event_type = None
        self._matrix_kind = None
        self._schedule_kind = None
        self._event = None
        self.discriminator = None

        if operation_cond is not None:
            self.operation_cond = operation_cond
        if early_stopping is not None:
            self.early_stopping = early_stopping
        if matrix is not None:
            self.matrix = matrix
        if run is not None:
            self.run = run
        if operation is not None:
            self.operation = operation
        if compiled_operation is not None:
            self.compiled_operation = compiled_operation
        if schedule is not None:
            self.schedule = schedule
        if connection_schema is not None:
            self.connection_schema = connection_schema
        if hp_params is not None:
            self.hp_params = hp_params
        if reference is not None:
            self.reference = reference
        if artifacts_mount is not None:
            self.artifacts_mount = artifacts_mount
        if polyaxon_sidecar_container is not None:
            self.polyaxon_sidecar_container = polyaxon_sidecar_container
        if polyaxon_init_container is not None:
            self.polyaxon_init_container = polyaxon_init_container
        if artifacs is not None:
            self.artifacs = artifacs
        if wasb is not None:
            self.wasb = wasb
        if gcs is not None:
            self.gcs = gcs
        if s3 is not None:
            self.s3 = s3
        if autg is not None:
            self.autg = autg
        if dockerfile is not None:
            self.dockerfile = dockerfile
        if git is not None:
            self.git = git
        if uri is not None:
            self.uri = uri
        if k8s_resource is not None:
            self.k8s_resource = k8s_resource
        if connection is not None:
            self.connection = connection
        if event_type is not None:
            self.event_type = event_type
        if matrix_kind is not None:
            self.matrix_kind = matrix_kind
        if schedule_kind is not None:
            self.schedule_kind = schedule_kind
        if event is not None:
            self.event = event

    @property
    def operation_cond(self):
        """Gets the operation_cond of this V1Schemas.  # noqa: E501


        :return: The operation_cond of this V1Schemas.  # noqa: E501
        :rtype: V1OperationCond
        """
        return self._operation_cond

    @operation_cond.setter
    def operation_cond(self, operation_cond):
        """Sets the operation_cond of this V1Schemas.


        :param operation_cond: The operation_cond of this V1Schemas.  # noqa: E501
        :type: V1OperationCond
        """

        self._operation_cond = operation_cond

    @property
    def early_stopping(self):
        """Gets the early_stopping of this V1Schemas.  # noqa: E501


        :return: The early_stopping of this V1Schemas.  # noqa: E501
        :rtype: V1EarlyStopping
        """
        return self._early_stopping

    @early_stopping.setter
    def early_stopping(self, early_stopping):
        """Sets the early_stopping of this V1Schemas.


        :param early_stopping: The early_stopping of this V1Schemas.  # noqa: E501
        :type: V1EarlyStopping
        """

        self._early_stopping = early_stopping

    @property
    def matrix(self):
        """Gets the matrix of this V1Schemas.  # noqa: E501


        :return: The matrix of this V1Schemas.  # noqa: E501
        :rtype: V1Matrix
        """
        return self._matrix

    @matrix.setter
    def matrix(self, matrix):
        """Sets the matrix of this V1Schemas.


        :param matrix: The matrix of this V1Schemas.  # noqa: E501
        :type: V1Matrix
        """

        self._matrix = matrix

    @property
    def run(self):
        """Gets the run of this V1Schemas.  # noqa: E501


        :return: The run of this V1Schemas.  # noqa: E501
        :rtype: V1RunSchema
        """
        return self._run

    @run.setter
    def run(self, run):
        """Sets the run of this V1Schemas.


        :param run: The run of this V1Schemas.  # noqa: E501
        :type: V1RunSchema
        """

        self._run = run

    @property
    def operation(self):
        """Gets the operation of this V1Schemas.  # noqa: E501


        :return: The operation of this V1Schemas.  # noqa: E501
        :rtype: V1Operation
        """
        return self._operation

    @operation.setter
    def operation(self, operation):
        """Sets the operation of this V1Schemas.


        :param operation: The operation of this V1Schemas.  # noqa: E501
        :type: V1Operation
        """

        self._operation = operation

    @property
    def compiled_operation(self):
        """Gets the compiled_operation of this V1Schemas.  # noqa: E501


        :return: The compiled_operation of this V1Schemas.  # noqa: E501
        :rtype: V1CompiledOperation
        """
        return self._compiled_operation

    @compiled_operation.setter
    def compiled_operation(self, compiled_operation):
        """Sets the compiled_operation of this V1Schemas.


        :param compiled_operation: The compiled_operation of this V1Schemas.  # noqa: E501
        :type: V1CompiledOperation
        """

        self._compiled_operation = compiled_operation

    @property
    def schedule(self):
        """Gets the schedule of this V1Schemas.  # noqa: E501


        :return: The schedule of this V1Schemas.  # noqa: E501
        :rtype: V1Schedule
        """
        return self._schedule

    @schedule.setter
    def schedule(self, schedule):
        """Sets the schedule of this V1Schemas.


        :param schedule: The schedule of this V1Schemas.  # noqa: E501
        :type: V1Schedule
        """

        self._schedule = schedule

    @property
    def connection_schema(self):
        """Gets the connection_schema of this V1Schemas.  # noqa: E501


        :return: The connection_schema of this V1Schemas.  # noqa: E501
        :rtype: V1ConnectionSchema
        """
        return self._connection_schema

    @connection_schema.setter
    def connection_schema(self, connection_schema):
        """Sets the connection_schema of this V1Schemas.


        :param connection_schema: The connection_schema of this V1Schemas.  # noqa: E501
        :type: V1ConnectionSchema
        """

        self._connection_schema = connection_schema

    @property
    def hp_params(self):
        """Gets the hp_params of this V1Schemas.  # noqa: E501


        :return: The hp_params of this V1Schemas.  # noqa: E501
        :rtype: V1HpParams
        """
        return self._hp_params

    @hp_params.setter
    def hp_params(self, hp_params):
        """Sets the hp_params of this V1Schemas.


        :param hp_params: The hp_params of this V1Schemas.  # noqa: E501
        :type: V1HpParams
        """

        self._hp_params = hp_params

    @property
    def reference(self):
        """Gets the reference of this V1Schemas.  # noqa: E501


        :return: The reference of this V1Schemas.  # noqa: E501
        :rtype: V1Reference
        """
        return self._reference

    @reference.setter
    def reference(self, reference):
        """Sets the reference of this V1Schemas.


        :param reference: The reference of this V1Schemas.  # noqa: E501
        :type: V1Reference
        """

        self._reference = reference

    @property
    def artifacts_mount(self):
        """Gets the artifacts_mount of this V1Schemas.  # noqa: E501


        :return: The artifacts_mount of this V1Schemas.  # noqa: E501
        :rtype: V1ArtifactsMount
        """
        return self._artifacts_mount

    @artifacts_mount.setter
    def artifacts_mount(self, artifacts_mount):
        """Sets the artifacts_mount of this V1Schemas.


        :param artifacts_mount: The artifacts_mount of this V1Schemas.  # noqa: E501
        :type: V1ArtifactsMount
        """

        self._artifacts_mount = artifacts_mount

    @property
    def polyaxon_sidecar_container(self):
        """Gets the polyaxon_sidecar_container of this V1Schemas.  # noqa: E501


        :return: The polyaxon_sidecar_container of this V1Schemas.  # noqa: E501
        :rtype: V1PolyaxonSidecarContainer
        """
        return self._polyaxon_sidecar_container

    @polyaxon_sidecar_container.setter
    def polyaxon_sidecar_container(self, polyaxon_sidecar_container):
        """Sets the polyaxon_sidecar_container of this V1Schemas.


        :param polyaxon_sidecar_container: The polyaxon_sidecar_container of this V1Schemas.  # noqa: E501
        :type: V1PolyaxonSidecarContainer
        """

        self._polyaxon_sidecar_container = polyaxon_sidecar_container

    @property
    def polyaxon_init_container(self):
        """Gets the polyaxon_init_container of this V1Schemas.  # noqa: E501


        :return: The polyaxon_init_container of this V1Schemas.  # noqa: E501
        :rtype: V1PolyaxonInitContainer
        """
        return self._polyaxon_init_container

    @polyaxon_init_container.setter
    def polyaxon_init_container(self, polyaxon_init_container):
        """Sets the polyaxon_init_container of this V1Schemas.


        :param polyaxon_init_container: The polyaxon_init_container of this V1Schemas.  # noqa: E501
        :type: V1PolyaxonInitContainer
        """

        self._polyaxon_init_container = polyaxon_init_container

    @property
    def artifacs(self):
        """Gets the artifacs of this V1Schemas.  # noqa: E501


        :return: The artifacs of this V1Schemas.  # noqa: E501
        :rtype: V1ArtifactsType
        """
        return self._artifacs

    @artifacs.setter
    def artifacs(self, artifacs):
        """Sets the artifacs of this V1Schemas.


        :param artifacs: The artifacs of this V1Schemas.  # noqa: E501
        :type: V1ArtifactsType
        """

        self._artifacs = artifacs

    @property
    def wasb(self):
        """Gets the wasb of this V1Schemas.  # noqa: E501


        :return: The wasb of this V1Schemas.  # noqa: E501
        :rtype: V1WasbType
        """
        return self._wasb

    @wasb.setter
    def wasb(self, wasb):
        """Sets the wasb of this V1Schemas.


        :param wasb: The wasb of this V1Schemas.  # noqa: E501
        :type: V1WasbType
        """

        self._wasb = wasb

    @property
    def gcs(self):
        """Gets the gcs of this V1Schemas.  # noqa: E501


        :return: The gcs of this V1Schemas.  # noqa: E501
        :rtype: V1GcsType
        """
        return self._gcs

    @gcs.setter
    def gcs(self, gcs):
        """Sets the gcs of this V1Schemas.


        :param gcs: The gcs of this V1Schemas.  # noqa: E501
        :type: V1GcsType
        """

        self._gcs = gcs

    @property
    def s3(self):
        """Gets the s3 of this V1Schemas.  # noqa: E501


        :return: The s3 of this V1Schemas.  # noqa: E501
        :rtype: V1S3Type
        """
        return self._s3

    @s3.setter
    def s3(self, s3):
        """Sets the s3 of this V1Schemas.


        :param s3: The s3 of this V1Schemas.  # noqa: E501
        :type: V1S3Type
        """

        self._s3 = s3

    @property
    def autg(self):
        """Gets the autg of this V1Schemas.  # noqa: E501


        :return: The autg of this V1Schemas.  # noqa: E501
        :rtype: V1AuthType
        """
        return self._autg

    @autg.setter
    def autg(self, autg):
        """Sets the autg of this V1Schemas.


        :param autg: The autg of this V1Schemas.  # noqa: E501
        :type: V1AuthType
        """

        self._autg = autg

    @property
    def dockerfile(self):
        """Gets the dockerfile of this V1Schemas.  # noqa: E501


        :return: The dockerfile of this V1Schemas.  # noqa: E501
        :rtype: V1DockerfileType
        """
        return self._dockerfile

    @dockerfile.setter
    def dockerfile(self, dockerfile):
        """Sets the dockerfile of this V1Schemas.


        :param dockerfile: The dockerfile of this V1Schemas.  # noqa: E501
        :type: V1DockerfileType
        """

        self._dockerfile = dockerfile

    @property
    def git(self):
        """Gets the git of this V1Schemas.  # noqa: E501


        :return: The git of this V1Schemas.  # noqa: E501
        :rtype: V1GitType
        """
        return self._git

    @git.setter
    def git(self, git):
        """Sets the git of this V1Schemas.


        :param git: The git of this V1Schemas.  # noqa: E501
        :type: V1GitType
        """

        self._git = git

    @property
    def uri(self):
        """Gets the uri of this V1Schemas.  # noqa: E501


        :return: The uri of this V1Schemas.  # noqa: E501
        :rtype: V1UriType
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this V1Schemas.


        :param uri: The uri of this V1Schemas.  # noqa: E501
        :type: V1UriType
        """

        self._uri = uri

    @property
    def k8s_resource(self):
        """Gets the k8s_resource of this V1Schemas.  # noqa: E501


        :return: The k8s_resource of this V1Schemas.  # noqa: E501
        :rtype: V1K8sResourceType
        """
        return self._k8s_resource

    @k8s_resource.setter
    def k8s_resource(self, k8s_resource):
        """Sets the k8s_resource of this V1Schemas.


        :param k8s_resource: The k8s_resource of this V1Schemas.  # noqa: E501
        :type: V1K8sResourceType
        """

        self._k8s_resource = k8s_resource

    @property
    def connection(self):
        """Gets the connection of this V1Schemas.  # noqa: E501


        :return: The connection of this V1Schemas.  # noqa: E501
        :rtype: V1ConnectionType
        """
        return self._connection

    @connection.setter
    def connection(self, connection):
        """Sets the connection of this V1Schemas.


        :param connection: The connection of this V1Schemas.  # noqa: E501
        :type: V1ConnectionType
        """

        self._connection = connection

    @property
    def event_type(self):
        """Gets the event_type of this V1Schemas.  # noqa: E501


        :return: The event_type of this V1Schemas.  # noqa: E501
        :rtype: V1EventType
        """
        return self._event_type

    @event_type.setter
    def event_type(self, event_type):
        """Sets the event_type of this V1Schemas.


        :param event_type: The event_type of this V1Schemas.  # noqa: E501
        :type: V1EventType
        """

        self._event_type = event_type

    @property
    def matrix_kind(self):
        """Gets the matrix_kind of this V1Schemas.  # noqa: E501


        :return: The matrix_kind of this V1Schemas.  # noqa: E501
        :rtype: V1MatrixKind
        """
        return self._matrix_kind

    @matrix_kind.setter
    def matrix_kind(self, matrix_kind):
        """Sets the matrix_kind of this V1Schemas.


        :param matrix_kind: The matrix_kind of this V1Schemas.  # noqa: E501
        :type: V1MatrixKind
        """

        self._matrix_kind = matrix_kind

    @property
    def schedule_kind(self):
        """Gets the schedule_kind of this V1Schemas.  # noqa: E501


        :return: The schedule_kind of this V1Schemas.  # noqa: E501
        :rtype: V1ScheduleKind
        """
        return self._schedule_kind

    @schedule_kind.setter
    def schedule_kind(self, schedule_kind):
        """Sets the schedule_kind of this V1Schemas.


        :param schedule_kind: The schedule_kind of this V1Schemas.  # noqa: E501
        :type: V1ScheduleKind
        """

        self._schedule_kind = schedule_kind

    @property
    def event(self):
        """Gets the event of this V1Schemas.  # noqa: E501


        :return: The event of this V1Schemas.  # noqa: E501
        :rtype: V1Event
        """
        return self._event

    @event.setter
    def event(self, event):
        """Sets the event of this V1Schemas.


        :param event: The event of this V1Schemas.  # noqa: E501
        :type: V1Event
        """

        self._event = event

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
        if not isinstance(other, V1Schemas):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1Schemas):
            return True

        return self.to_dict() != other.to_dict()
