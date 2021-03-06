#
#    Copyright 2018 EPAM Systems
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
"""
K8SBaseHook module
"""
import os
import yaml
from airflow.hooks.base_hook import BaseHook
from airflow.models import Connection
from airflow.utils.log.logging_mixin import LoggingMixin
from legion.k8s import K8SSecretStorage


class K8SBaseHook(BaseHook):
    """
    A hook to work with k8s secret storage as a first default source
    of connections. Retrieves connection via BaseHook parent method
    upon failure to retrieve from k8s.
    """

    STORAGE_NAME_PREFIX = 'airflow-credentials'

    @classmethod
    def get_connection(cls, conn_id):
        """
        Try to get connection from k8 and if failed - invoke parent method.

        :param conn_id: connection id
        :type conn_id: str
        """
        try:
            return cls._get_conn_from_k8s(conn_id)
        except Exception as e:
            LoggingMixin().log.warning(
                'Failed to retrieve connection {} from k8s secret. The error message is {} '
                'retrieving from env/db'.format(conn_id, e),
                exc_info=True, stack_info=True
            )
        return super().get_connection(conn_id)

    @classmethod
    def _get_conn_from_k8s(cls, conn_id):
        """
        Retrieve connection config from k8s secrets and initialize connection

        :param conn_id: connection id
        :type conn_id: str
        """
        config_map = K8SSecretStorage.retrive(
            storage_name=cls.STORAGE_NAME_PREFIX,
            k8s_namespace=os.environ['NAMESPACE']
        )
        if conn_id not in config_map.data:
            raise Exception("Doesn't have {} value in k8s secret".format(conn_id))

        connection_data = yaml.load(config_map.data[conn_id])
        return Connection(**connection_data)
