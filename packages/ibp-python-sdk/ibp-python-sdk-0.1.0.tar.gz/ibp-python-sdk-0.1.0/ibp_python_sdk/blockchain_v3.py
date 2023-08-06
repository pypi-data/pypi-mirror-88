# coding: utf-8

# (C) Copyright IBM Corp. 2020.
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

# IBM OpenAPI SDK Code Generator Version: 3.19.0-be3b4618-20201113-200858
 
"""
This doc lists APIs that you can use to interact with your IBM Blockchain Platform console
(IBP console)
"""

from enum import Enum
from typing import Dict, List
import json

from ibm_cloud_sdk_core import BaseService, DetailedResponse
from ibm_cloud_sdk_core.authenticators.authenticator import Authenticator
from ibm_cloud_sdk_core.get_authenticator import get_authenticator_from_environment
from ibm_cloud_sdk_core.utils import convert_model

from .common import get_sdk_headers

##############################################################################
# Service
##############################################################################

class BlockchainV3(BaseService):
    """The blockchain V3 service."""

    DEFAULT_SERVICE_URL = None
    DEFAULT_SERVICE_NAME = 'blockchain'

    @classmethod
    def new_instance(cls,
                     service_name: str = DEFAULT_SERVICE_NAME,
                    ) -> 'BlockchainV3':
        """
        Return a new client for the blockchain service using the specified
               parameters and external configuration.
        """
        authenticator = get_authenticator_from_environment(service_name)
        service = cls(
            authenticator
            )
        service.configure_service(service_name)
        return service

    def __init__(self,
                 authenticator: Authenticator = None,
                ) -> None:
        """
        Construct a new client for the blockchain service.

        :param Authenticator authenticator: The authenticator specifies the authentication mechanism.
               Get up to date information from https://github.com/IBM/python-sdk-core/blob/master/README.md
               about initializing the authenticator of your choice.
        """
        BaseService.__init__(self,
                             service_url=self.DEFAULT_SERVICE_URL,
                             authenticator=authenticator)


    #########################
    # Manage component
    #########################


    def get_component(self,
        id: str,
        *,
        deployment_attrs: str = None,
        parsed_certs: str = None,
        cache: str = None,
        ca_attrs: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get component data.

        Get the IBP console's data on a component (peer, CA, orderer, or MSP). The
        component might be imported or created.

        :param str id: The `id` of the component to retrieve. Use the [Get all
               components](#list_components) API to determine the component id.
        :param str deployment_attrs: (optional) Set to 'included' if the response
               should include Kubernetes deployment attributes such as 'resources',
               'storage', 'zone', 'region', 'admin_certs', etc. Default responses will not
               include these fields.
               **This parameter will not work on *imported* components.**
               It's recommended to use `cache=skip` as well if up-to-date deployment data
               is needed.
        :param str parsed_certs: (optional) Set to 'included' if the response
               should include parsed PEM data along with base 64 encoded PEM string.
               Parsed certificate data will include fields such as the serial number,
               issuer, expiration, subject, subject alt names, etc. Default responses will
               not include these fields.
        :param str cache: (optional) Set to 'skip' if the response should skip
               local data and fetch live data wherever possible. Expect longer response
               times if the cache is skipped. Default responses will use the cache.
        :param str ca_attrs: (optional) Set to 'included' if the response should
               fetch CA attributes, inspect certificates, and append extra fields to CA
               and MSP component responses.
               - CA components will have fields appended/updated with data fetched from
               the `/cainfo?ca=ca` endpoint of a CA, such as: `ca_name`, `root_cert`,
               `fabric_version`, `issuer_public_key` and `issued_known_msps`. The field
               `issued_known_msps` indicates imported IBP MSPs that this CA has issued.
               Meaning the MSP's root cert contains a signature that is derived from this
               CA's root cert. Only imported MSPs are checked. Default responses will not
               include these fields.
               - MSP components will have the field `issued_by_ca_id` appended. This field
               indicates the id of an IBP console CA that issued this MSP. Meaning the
               MSP's root cert contains a signature that is derived from this CA's root
               cert. Only imported/created CAs are checked. Default responses will not
               include these fields.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `GenericComponentResponse` object
        """

        if id is None:
            raise ValueError('id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='get_component')
        headers.update(sdk_headers)

        params = {
            'deployment_attrs': deployment_attrs,
            'parsed_certs': parsed_certs,
            'cache': cache,
            'ca_attrs': ca_attrs
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['id']
        path_param_values = self.encode_path_vars(id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/components/{id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def remove_component(self,
        id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Remove imported component.

        Remove a single component from the IBP console.
        - Using this api on an **imported** component removes it from the IBP console.
        - Using this api on a **created** component removes it from the IBP console
        **but** it will **not** delete the component from the Kubernetes cluster where it
        resides. Thus it orphans the Kubernetes deployment (if it exists). Instead use the
        [Delete component](#delete-component) API to delete the Kubernetes deployment and
        the IBP console data at once.

        :param str id: The `id` of the imported component to remove. Use the [Get
               all components](#list-components) API to determine the component id.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `DeleteComponentResponse` object
        """

        if id is None:
            raise ValueError('id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='remove_component')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['id']
        path_param_values = self.encode_path_vars(id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/components/{id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def delete_component(self,
        id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete component.

        Removes a single component from the IBP console **and** it deletes the Kubernetes
        deployment.
        - Using this api on an **imported** component will *error out* since its
        Kubernetes deployment is unknown and cannot be removed. Instead use the [Remove
        imported component](#remove-component) API to remove imported components.
        - Using this api on a **created** component removes it from the IBP console
        **and** it will delete the component from the Kubernetes cluster where it resides.
        The Kubernetes delete must succeed before the component will be removed from the
        IBP console.

        :param str id: The `id` of the component to delete. Use the [Get all
               components](#list_components) API to determine the id of the component to
               be deleted.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `DeleteComponentResponse` object
        """

        if id is None:
            raise ValueError('id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='delete_component')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['id']
        path_param_values = self.encode_path_vars(id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/kubernetes/components/{id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def create_ca(self,
        display_name: str,
        config_override: 'CreateCaBodyConfigOverride',
        *,
        resources: 'CreateCaBodyResources' = None,
        storage: 'CreateCaBodyStorage' = None,
        zone: str = None,
        replicas: float = None,
        tags: List[str] = None,
        hsm: 'Hsm' = None,
        region: str = None,
        version: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Create a CA.

        Create a Hyperledger Fabric Certificate Authority (CA) in your Kubernetes cluster.

        :param str display_name: A descriptive name for this CA. The IBP console
               tile displays this name.
        :param CreateCaBodyConfigOverride config_override: Set `config_override` to
               create the root/initial enroll id and enroll secret as well as enabling
               custom CA configurations (such as using postgres). See the [Fabric CA
               configuration
               file](https://hyperledger-fabric-ca.readthedocs.io/en/release-1.4/serverconfig.html)
               for more information about each parameter.
               The field `tlsca` is optional. The IBP console will copy the value of
               `config_override.ca` into `config_override.tlsca` if
               `config_override.tlsca` is omitted (which is recommended).
               *The nested field **names** below are not case-sensitive.*.
        :param CreateCaBodyResources resources: (optional) CPU and memory
               properties. This feature is not available if using a free Kubernetes
               cluster.
        :param CreateCaBodyStorage storage: (optional) Disk space properties. This
               feature is not available if using a free Kubernetes cluster.
        :param str zone: (optional) Specify the Kubernetes zone for the deployment.
               The deployment will use a k8s node in this zone. Find the list of possible
               zones by retrieving your Kubernetes node labels: `kubectl get nodes
               --show-labels`. [More
               information](https://kubernetes.io/docs/setup/best-practices/multiple-zones).
        :param float replicas: (optional) The number of replica pods running at any
               given time.
        :param List[str] tags: (optional)
        :param Hsm hsm: (optional) The connection details of the HSM (Hardware
               Security Module).
        :param str region: (optional) Specify the Kubernetes region for the
               deployment. The deployment will use a k8s node in this region. Find the
               list of possible regions by retrieving your Kubernetes node labels:
               `kubectl get nodes --show-labels`. [More
               info](https://kubernetes.io/docs/setup/best-practices/multiple-zones).
        :param str version: (optional) The Hyperledger Fabric release version to
               use.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `CaResponse` object
        """

        if display_name is None:
            raise ValueError('display_name must be provided')
        if config_override is None:
            raise ValueError('config_override must be provided')
        config_override = convert_model(config_override)
        if resources is not None:
            resources = convert_model(resources)
        if storage is not None:
            storage = convert_model(storage)
        if hsm is not None:
            hsm = convert_model(hsm)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='create_ca')
        headers.update(sdk_headers)

        data = {
            'display_name': display_name,
            'config_override': config_override,
            'resources': resources,
            'storage': storage,
            'zone': zone,
            'replicas': replicas,
            'tags': tags,
            'hsm': hsm,
            'region': region,
            'version': version
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/kubernetes/components/fabric-ca'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def import_ca(self,
        display_name: str,
        api_url: str,
        msp: 'ImportCaBodyMsp',
        *,
        location: str = None,
        operations_url: str = None,
        tags: List[str] = None,
        tls_cert: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Import a CA.

        Import an existing Certificate Authority (CA) to your IBP console. It is
        recommended to only import components that were created by this or another IBP
        console.

        :param str display_name: A descriptive name for this component.
        :param str api_url: The URL for the CA. Typically, client applications
               would send requests to this URL. Include the protocol, hostname/ip and
               port.
        :param ImportCaBodyMsp msp:
        :param str location: (optional) Indicates where the component is running.
        :param str operations_url: (optional) The operations URL for the CA.
               Include the protocol, hostname/ip and port.
        :param List[str] tags: (optional)
        :param str tls_cert: (optional) The TLS certificate as base 64 encoded PEM.
               Certificate is used to secure/validate a TLS connection with this
               component.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `CaResponse` object
        """

        if display_name is None:
            raise ValueError('display_name must be provided')
        if api_url is None:
            raise ValueError('api_url must be provided')
        if msp is None:
            raise ValueError('msp must be provided')
        msp = convert_model(msp)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='import_ca')
        headers.update(sdk_headers)

        data = {
            'display_name': display_name,
            'api_url': api_url,
            'msp': msp,
            'location': location,
            'operations_url': operations_url,
            'tags': tags,
            'tls_cert': tls_cert
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/components/fabric-ca'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def update_ca(self,
        id: str,
        *,
        config_override: 'UpdateCaBodyConfigOverride' = None,
        replicas: float = None,
        resources: 'UpdateCaBodyResources' = None,
        version: str = None,
        zone: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Update a CA.

        Update Kubernetes deployment attributes of a Hyperledger Fabric Certificate
        Authority (CA) in your cluster.

        :param str id: The `id` of the component to modify. Use the [Get all
               components](#list_components) API to determine the component id.
        :param UpdateCaBodyConfigOverride config_override: (optional) Update the
               [Fabric CA configuration
               file](https://hyperledger-fabric-ca.readthedocs.io/en/release-1.4/serverconfig.html)
               if you want use custom attributes to configure advanced CA features. Omit
               if not.
               *The nested field **names** below are not case-sensitive.*
               *The nested fields sent will be merged with the existing settings.*.
        :param float replicas: (optional) The number of replica pods running at any
               given time.
        :param UpdateCaBodyResources resources: (optional) CPU and memory
               properties. This feature is not available if using a free Kubernetes
               cluster.
        :param str version: (optional) The Hyperledger Fabric release version to
               update to.
        :param str zone: (optional) Specify the Kubernetes zone for the deployment.
               The deployment will use a k8s node in this zone. Find the list of possible
               zones by retrieving your Kubernetes node labels: `kubectl get nodes
               --show-labels`. [More
               information](https://kubernetes.io/docs/setup/best-practices/multiple-zones).
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `CaResponse` object
        """

        if id is None:
            raise ValueError('id must be provided')
        if config_override is not None:
            config_override = convert_model(config_override)
        if resources is not None:
            resources = convert_model(resources)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='update_ca')
        headers.update(sdk_headers)

        data = {
            'config_override': config_override,
            'replicas': replicas,
            'resources': resources,
            'version': version,
            'zone': zone
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['id']
        path_param_values = self.encode_path_vars(id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/kubernetes/components/fabric-ca/{id}'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def edit_ca(self,
        id: str,
        *,
        display_name: str = None,
        api_url: str = None,
        operations_url: str = None,
        ca_name: str = None,
        location: str = None,
        tags: List[str] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Edit data about a CA.

        Modify local metadata fields of a Certificate Authority (CA). For example, the
        "display_name" field. This API will **not** change any Kubernetes deployment
        attributes for the CA.

        :param str id: The `id` of the component to modify. Use the [Get all
               components](#list_components) API to determine the component id.
        :param str display_name: (optional) A descriptive name for this CA. The IBP
               console tile displays this name.
        :param str api_url: (optional) The URL for the CA. Typically, client
               applications would send requests to this URL. Include the protocol,
               hostname/ip and port.
        :param str operations_url: (optional) The operations URL for the CA.
               Include the protocol, hostname/ip and port.
        :param str ca_name: (optional) The CA's "CAName" attribute. This name is
               used to distinguish this CA from the TLS CA.
        :param str location: (optional) Indicates where the component is running.
        :param List[str] tags: (optional)
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `CaResponse` object
        """

        if id is None:
            raise ValueError('id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='edit_ca')
        headers.update(sdk_headers)

        data = {
            'display_name': display_name,
            'api_url': api_url,
            'operations_url': operations_url,
            'ca_name': ca_name,
            'location': location,
            'tags': tags
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['id']
        path_param_values = self.encode_path_vars(id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/components/fabric-ca/{id}'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def ca_action(self,
        id: str,
        *,
        restart: bool = None,
        renew: 'ActionRenew' = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Submit action to a CA.

        Submit an action to a Fabric CA component. Actions such as restarting the
        component or certificate operations.

        :param str id: The `id` of the component to modify. Use the [Get all
               components](#list_components) API to determine the component id.
        :param bool restart: (optional) Set to `true` to restart the component.
        :param ActionRenew renew: (optional)
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ActionsResponse` object
        """

        if id is None:
            raise ValueError('id must be provided')
        if renew is not None:
            renew = convert_model(renew)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='ca_action')
        headers.update(sdk_headers)

        data = {
            'restart': restart,
            'renew': renew
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['id']
        path_param_values = self.encode_path_vars(id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/kubernetes/components/fabric-ca/{id}/actions'.format(**path_param_dict)
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def create_peer(self,
        msp_id: str,
        display_name: str,
        crypto: 'CryptoObject',
        *,
        config_override: 'ConfigPeerCreate' = None,
        resources: 'PeerResources' = None,
        storage: 'CreatePeerBodyStorage' = None,
        zone: str = None,
        state_db: str = None,
        tags: List[str] = None,
        hsm: 'Hsm' = None,
        region: str = None,
        version: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Create a peer.

        Create a Hyperledger Fabric peer in your Kubernetes cluster.

        :param str msp_id: The MSP id that is related to this component.
        :param str display_name: A descriptive name for this peer. The IBP console
               tile displays this name.
        :param CryptoObject crypto: See this
               [topic](/docs/blockchain?topic=blockchain-ibp-v2-apis#ibp-v2-apis-config)
               for instructions on how to build a crypto object.
        :param ConfigPeerCreate config_override: (optional) Override the [Fabric
               Peer configuration
               file](https://github.com/hyperledger/fabric/blob/release-1.4/sampleconfig/core.yaml)
               if you want use custom attributes to configure the Peer. Omit if not.
               *The nested field **names** below are not case-sensitive.*.
        :param PeerResources resources: (optional) CPU and memory properties. This
               feature is not available if using a free Kubernetes cluster.
        :param CreatePeerBodyStorage storage: (optional) Disk space properties.
               This feature is not available if using a free Kubernetes cluster.
        :param str zone: (optional) Specify the Kubernetes zone for the deployment.
               The deployment will use a k8s node in this zone. Find the list of possible
               zones by retrieving your Kubernetes node labels: `kubectl get nodes
               --show-labels`. [More
               information](https://kubernetes.io/docs/setup/best-practices/multiple-zones).
        :param str state_db: (optional) Select the state database for the peer. Can
               be either "couchdb" or "leveldb". The default is "couchdb".
        :param List[str] tags: (optional)
        :param Hsm hsm: (optional) The connection details of the HSM (Hardware
               Security Module).
        :param str region: (optional) Specify the Kubernetes region for the
               deployment. The deployment will use a k8s node in this region. Find the
               list of possible regions by retrieving your Kubernetes node labels:
               `kubectl get nodes --show-labels`. [More
               info](https://kubernetes.io/docs/setup/best-practices/multiple-zones).
        :param str version: (optional) The Hyperledger Fabric release version to
               use.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `PeerResponse` object
        """

        if msp_id is None:
            raise ValueError('msp_id must be provided')
        if display_name is None:
            raise ValueError('display_name must be provided')
        if crypto is None:
            raise ValueError('crypto must be provided')
        crypto = convert_model(crypto)
        if config_override is not None:
            config_override = convert_model(config_override)
        if resources is not None:
            resources = convert_model(resources)
        if storage is not None:
            storage = convert_model(storage)
        if hsm is not None:
            hsm = convert_model(hsm)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='create_peer')
        headers.update(sdk_headers)

        data = {
            'msp_id': msp_id,
            'display_name': display_name,
            'crypto': crypto,
            'config_override': config_override,
            'resources': resources,
            'storage': storage,
            'zone': zone,
            'state_db': state_db,
            'tags': tags,
            'hsm': hsm,
            'region': region,
            'version': version
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/kubernetes/components/fabric-peer'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def import_peer(self,
        display_name: str,
        grpcwp_url: str,
        msp: 'MspCryptoField',
        msp_id: str,
        *,
        api_url: str = None,
        location: str = None,
        operations_url: str = None,
        tags: List[str] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Import a peer.

        Import an existing peer into your IBP console. It is recommended to only import
        components that were created by this or another IBP console.

        :param str display_name: A descriptive name for this peer. The IBP console
               tile displays this name.
        :param str grpcwp_url: The gRPC web proxy URL in front of the peer. Include
               the protocol, hostname/ip and port.
        :param MspCryptoField msp: The msp crypto data.
        :param str msp_id: The MSP id that is related to this component.
        :param str api_url: (optional) The gRPC URL for the peer. Typically, client
               applications would send requests to this URL. Include the protocol,
               hostname/ip and port.
        :param str location: (optional) Indicates where the component is running.
        :param str operations_url: (optional) Used by Fabric health checker to
               monitor the health status of this peer. For more information, see [Fabric
               documentation](https://hyperledger-fabric.readthedocs.io/en/release-1.4/operations_service.html).
               Include the protocol, hostname/ip and port.
        :param List[str] tags: (optional)
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `PeerResponse` object
        """

        if display_name is None:
            raise ValueError('display_name must be provided')
        if grpcwp_url is None:
            raise ValueError('grpcwp_url must be provided')
        if msp is None:
            raise ValueError('msp must be provided')
        if msp_id is None:
            raise ValueError('msp_id must be provided')
        msp = convert_model(msp)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='import_peer')
        headers.update(sdk_headers)

        data = {
            'display_name': display_name,
            'grpcwp_url': grpcwp_url,
            'msp': msp,
            'msp_id': msp_id,
            'api_url': api_url,
            'location': location,
            'operations_url': operations_url,
            'tags': tags
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/components/fabric-peer'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def edit_peer(self,
        id: str,
        *,
        display_name: str = None,
        api_url: str = None,
        operations_url: str = None,
        grpcwp_url: str = None,
        msp_id: str = None,
        location: str = None,
        tags: List[str] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Edit data about a peer.

        Modify local metadata fields of a peer. For example, the "display_name" field.
        This API will **not** change any Kubernetes deployment attributes for the peer.

        :param str id: The `id` of the component to modify. Use the [Get all
               components](#list_components) API to determine the component id.
        :param str display_name: (optional) A descriptive name for this peer. The
               IBP console tile displays this name.
        :param str api_url: (optional) The gRPC URL for the peer. Typically, client
               applications would send requests to this URL. Include the protocol,
               hostname/ip and port.
        :param str operations_url: (optional) Used by Fabric health checker to
               monitor the health status of this peer. For more information, see [Fabric
               documentation](https://hyperledger-fabric.readthedocs.io/en/release-1.4/operations_service.html).
               Include the protocol, hostname/ip and port.
        :param str grpcwp_url: (optional) The gRPC web proxy URL in front of the
               peer. Include the protocol, hostname/ip and port.
        :param str msp_id: (optional) The MSP id that is related to this component.
        :param str location: (optional) Indicates where the component is running.
        :param List[str] tags: (optional)
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `PeerResponse` object
        """

        if id is None:
            raise ValueError('id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='edit_peer')
        headers.update(sdk_headers)

        data = {
            'display_name': display_name,
            'api_url': api_url,
            'operations_url': operations_url,
            'grpcwp_url': grpcwp_url,
            'msp_id': msp_id,
            'location': location,
            'tags': tags
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['id']
        path_param_values = self.encode_path_vars(id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/components/fabric-peer/{id}'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def peer_action(self,
        id: str,
        *,
        restart: bool = None,
        reenroll: 'ActionReenroll' = None,
        enroll: 'ActionEnroll' = None,
        upgrade_dbs: bool = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Submit action to a peer.

        Submit an action to a Fabric Peer component. Actions such as restarting the
        component or certificate operations.

        :param str id: The `id` of the component to modify. Use the [Get all
               components](#list_components) API to determine the component id.
        :param bool restart: (optional) Set to `true` to restart the component.
        :param ActionReenroll reenroll: (optional)
        :param ActionEnroll enroll: (optional)
        :param bool upgrade_dbs: (optional) Set to `true` to start the peer's db
               migration.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ActionsResponse` object
        """

        if id is None:
            raise ValueError('id must be provided')
        if reenroll is not None:
            reenroll = convert_model(reenroll)
        if enroll is not None:
            enroll = convert_model(enroll)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='peer_action')
        headers.update(sdk_headers)

        data = {
            'restart': restart,
            'reenroll': reenroll,
            'enroll': enroll,
            'upgrade_dbs': upgrade_dbs
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['id']
        path_param_values = self.encode_path_vars(id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/kubernetes/components/fabric-peer/{id}/actions'.format(**path_param_dict)
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def update_peer(self,
        id: str,
        *,
        admin_certs: List[str] = None,
        config_override: 'ConfigPeerUpdate' = None,
        crypto: 'UpdatePeerBodyCrypto' = None,
        node_ou: 'NodeOu' = None,
        replicas: float = None,
        resources: 'PeerResources' = None,
        version: str = None,
        zone: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Update a peer.

        Update Kubernetes deployment attributes of a Hyperledger Fabric Peer node.

        :param str id: The `id` of the component to modify. Use the [Get all
               components](#list_components) API to determine the component id.
        :param List[str] admin_certs: (optional) An array that contains *all* the
               base 64 encoded PEM identity certificates for administrators of this
               component. Also known as signing certificates of an organization
               administrator.
        :param ConfigPeerUpdate config_override: (optional) Update the [Fabric Peer
               configuration
               file](https://github.com/hyperledger/fabric/blob/release-1.4/sampleconfig/core.yaml)
               if you want use custom attributes to configure the Peer. Omit if not.
               *The nested field **names** below are not case-sensitive.*
               *The nested fields sent will be merged with the existing settings.*.
        :param UpdatePeerBodyCrypto crypto: (optional)
        :param NodeOu node_ou: (optional)
        :param float replicas: (optional) The number of replica pods running at any
               given time.
        :param PeerResources resources: (optional) CPU and memory properties. This
               feature is not available if using a free Kubernetes cluster.
        :param str version: (optional) The Hyperledger Fabric release version to
               update to.
        :param str zone: (optional) Specify the Kubernetes zone for the deployment.
               The deployment will use a k8s node in this zone. Find the list of possible
               zones by retrieving your Kubernetes node labels: `kubectl get nodes
               --show-labels`. [More
               information](https://kubernetes.io/docs/setup/best-practices/multiple-zones).
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `PeerResponse` object
        """

        if id is None:
            raise ValueError('id must be provided')
        if config_override is not None:
            config_override = convert_model(config_override)
        if crypto is not None:
            crypto = convert_model(crypto)
        if node_ou is not None:
            node_ou = convert_model(node_ou)
        if resources is not None:
            resources = convert_model(resources)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='update_peer')
        headers.update(sdk_headers)

        data = {
            'admin_certs': admin_certs,
            'config_override': config_override,
            'crypto': crypto,
            'node_ou': node_ou,
            'replicas': replicas,
            'resources': resources,
            'version': version,
            'zone': zone
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['id']
        path_param_values = self.encode_path_vars(id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/kubernetes/components/fabric-peer/{id}'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def create_orderer(self,
        orderer_type: str,
        msp_id: str,
        display_name: str,
        crypto: List['CryptoObject'],
        *,
        cluster_name: str = None,
        cluster_id: str = None,
        external_append: str = None,
        config_override: List['ConfigOrdererCreate'] = None,
        resources: 'CreateOrdererRaftBodyResources' = None,
        storage: 'CreateOrdererRaftBodyStorage' = None,
        system_channel_id: str = None,
        zone: List[str] = None,
        tags: List[str] = None,
        region: List[str] = None,
        hsm: 'Hsm' = None,
        version: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Create an ordering service.

        Create a Hyperledger Ordering Service (OS) in your Kubernetes cluster. Currently,
        only raft ordering nodes are supported.

        :param str orderer_type: The type of Fabric orderer. Currently, only the
               type `"raft"` is supported.
               [etcd/raft](/docs/blockchain?topic=blockchain-ibp-console-build-network#ibp-console-build-network-ordering-console).
        :param str msp_id: The MSP id that is related to this component.
        :param str display_name: A descriptive base name for each ordering node.
               One or more child IBP console tiles display this name.
        :param List[CryptoObject] crypto: An array of config objects. When creating
               a new OS (Ordering Service) the array must have one object per desired raft
               node. 1 or 5 nodes are recommended.
               **When appending to an existing OS only an array of size 1 is supported.**
               See this
               [topic](/docs/blockchain?topic=blockchain-ibp-v2-apis#ibp-v2-apis-config)
               for instructions on how to build a config object.
        :param str cluster_name: (optional) A descriptive name for an ordering
               service. The parent IBP console tile displays this name.
               This field should only be set if you are creating a new OS cluster or when
               appending to an unknown (external) OS cluster. An unknown/external cluster
               is one that this IBP console has not imported or created.
        :param str cluster_id: (optional) This field should only be set if you are
               appending a new raft node to an **existing** raft cluster. When appending
               to a known (internal) OS cluster set `cluster_id` to the same value used by
               the OS cluster. When appending to an unknown (external) OS cluster set
               `cluster_id` to a unique string.
               Setting this field means the `config` array should be of length 1, since it
               is not possible to add multiple raft nodes at the same time in Fabric.
               If this field is set the orderer will be "pre-created" and start without a
               genesis block. It is effectively dead until it is configured. This is the
               first step to **append** a node to a raft cluster. The next step is to add
               this node as a consenter to the system-channel by using Fabric-APIs. Then,
               init this node by sending the updated system-channel config-block with the
               [Submit config block to orderer](#submit-block) API. The node will not be
               usable until these steps are completed.
        :param str external_append: (optional) Set to `true` only if you are
               appending to an unknown (external) OS cluster. Else set it to `false` or
               omit the field. An unknown/external cluster is one that this IBP console
               has not imported or created.
        :param List[ConfigOrdererCreate] config_override: (optional) An array of
               configuration override objects. 1 object per component. Must be the same
               size as the `config` array.
        :param CreateOrdererRaftBodyResources resources: (optional) CPU and memory
               properties. This feature is not available if using a free Kubernetes
               cluster.
        :param CreateOrdererRaftBodyStorage storage: (optional) Disk space
               properties. This feature is not available if using a free Kubernetes
               cluster.
        :param str system_channel_id: (optional) The name of the system channel.
               Defaults to `testchainid`.
        :param List[str] zone: (optional) An array of Kubernetes zones for the
               deployment. 1 zone per component. Must be the same size as the `config`
               array.
        :param List[str] tags: (optional)
        :param List[str] region: (optional) An array of Kubernetes regions for the
               deployment. One region per component. Must be the same size as the `config`
               array.
        :param Hsm hsm: (optional) The connection details of the HSM (Hardware
               Security Module).
        :param str version: (optional) The Hyperledger Fabric release version to
               use.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `OrdererResponse` object
        """

        if orderer_type is None:
            raise ValueError('orderer_type must be provided')
        if msp_id is None:
            raise ValueError('msp_id must be provided')
        if display_name is None:
            raise ValueError('display_name must be provided')
        if crypto is None:
            raise ValueError('crypto must be provided')
        crypto = [convert_model(x) for x in crypto]
        if config_override is not None:
            config_override = [convert_model(x) for x in config_override]
        if resources is not None:
            resources = convert_model(resources)
        if storage is not None:
            storage = convert_model(storage)
        if hsm is not None:
            hsm = convert_model(hsm)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='create_orderer')
        headers.update(sdk_headers)

        data = {
            'orderer_type': orderer_type,
            'msp_id': msp_id,
            'display_name': display_name,
            'crypto': crypto,
            'cluster_name': cluster_name,
            'cluster_id': cluster_id,
            'external_append': external_append,
            'config_override': config_override,
            'resources': resources,
            'storage': storage,
            'system_channel_id': system_channel_id,
            'zone': zone,
            'tags': tags,
            'region': region,
            'hsm': hsm,
            'version': version
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/kubernetes/components/fabric-orderer'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def import_orderer(self,
        cluster_name: str,
        display_name: str,
        grpcwp_url: str,
        msp: 'MspCryptoField',
        msp_id: str,
        *,
        api_url: str = None,
        cluster_id: str = None,
        location: str = None,
        operations_url: str = None,
        system_channel_id: str = None,
        tags: List[str] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Import an ordering service.

        Import an existing Ordering Service (OS) to your IBP console. It is recommended to
        only import components that were created by this or another IBP console.

        :param str cluster_name: A descriptive name for an ordering service. The
               parent IBP console tile displays this name.
        :param str display_name: A descriptive base name for each ordering node.
               One or more child IBP console tiles display this name.
        :param str grpcwp_url: The gRPC web proxy URL in front of the orderer.
               Include the protocol, hostname/ip and port.
        :param MspCryptoField msp: The msp crypto data.
        :param str msp_id: The MSP id that is related to this component.
        :param str api_url: (optional) The gRPC URL for the orderer. Typically,
               client applications would send requests to this URL. Include the protocol,
               hostname/ip and port.
        :param str cluster_id: (optional) A unique id to identify this rafter
               cluster. Generated if not provided.
        :param str location: (optional) Indicates where the component is running.
        :param str operations_url: (optional) Used by Fabric health checker to
               monitor the health status of this orderer node. For more information, see
               [Fabric
               documentation](https://hyperledger-fabric.readthedocs.io/en/release-1.4/operations_service.html).
               Include the protocol, hostname/ip and port.
        :param str system_channel_id: (optional) The name of the system channel.
               Defaults to `testchainid`.
        :param List[str] tags: (optional)
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `OrdererResponse` object
        """

        if cluster_name is None:
            raise ValueError('cluster_name must be provided')
        if display_name is None:
            raise ValueError('display_name must be provided')
        if grpcwp_url is None:
            raise ValueError('grpcwp_url must be provided')
        if msp is None:
            raise ValueError('msp must be provided')
        if msp_id is None:
            raise ValueError('msp_id must be provided')
        msp = convert_model(msp)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='import_orderer')
        headers.update(sdk_headers)

        data = {
            'cluster_name': cluster_name,
            'display_name': display_name,
            'grpcwp_url': grpcwp_url,
            'msp': msp,
            'msp_id': msp_id,
            'api_url': api_url,
            'cluster_id': cluster_id,
            'location': location,
            'operations_url': operations_url,
            'system_channel_id': system_channel_id,
            'tags': tags
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/components/fabric-orderer'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def edit_orderer(self,
        id: str,
        *,
        cluster_name: str = None,
        display_name: str = None,
        api_url: str = None,
        operations_url: str = None,
        grpcwp_url: str = None,
        msp_id: str = None,
        consenter_proposal_fin: bool = None,
        location: str = None,
        system_channel_id: str = None,
        tags: List[str] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Edit data about an orderer.

        Modify local metadata fields of a single node in an Ordering Service (OS). For
        example, the "display_name" field. This API will **not** change any Kubernetes
        deployment attributes for the node.

        :param str id: The `id` of the component to modify. Use the [Get all
               components](#list_components) API to determine the component id.
        :param str cluster_name: (optional) A descriptive name for an ordering
               service. The parent IBP console tile displays this name.
        :param str display_name: (optional) A descriptive base name for each
               ordering node. One or more child IBP console tiles display this name.
        :param str api_url: (optional) The gRPC URL for the orderer. Typically,
               client applications would send requests to this URL. Include the protocol,
               hostname/ip and port.
        :param str operations_url: (optional) Used by Fabric health checker to
               monitor the health status of this orderer node. For more information, see
               [Fabric
               documentation](https://hyperledger-fabric.readthedocs.io/en/release-1.4/operations_service.html).
               Include the protocol, hostname/ip and port.
        :param str grpcwp_url: (optional) The gRPC web proxy URL in front of the
               orderer. Include the protocol, hostname/ip and port.
        :param str msp_id: (optional) The MSP id that is related to this component.
        :param bool consenter_proposal_fin: (optional) The state of a pre-created
               orderer node. A value of `true` means that the orderer node was added as a
               system channel consenter. This is a manual field. Set it yourself after
               finishing the raft append flow to indicate that this node is ready for use.
               See the [Submit config block to orderer](#submit-block) API description for
               more details about appending raft nodes.
        :param str location: (optional) Indicates where the component is running.
        :param str system_channel_id: (optional) The name of the system channel.
               Defaults to `testchainid`.
        :param List[str] tags: (optional)
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `OrdererResponse` object
        """

        if id is None:
            raise ValueError('id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='edit_orderer')
        headers.update(sdk_headers)

        data = {
            'cluster_name': cluster_name,
            'display_name': display_name,
            'api_url': api_url,
            'operations_url': operations_url,
            'grpcwp_url': grpcwp_url,
            'msp_id': msp_id,
            'consenter_proposal_fin': consenter_proposal_fin,
            'location': location,
            'system_channel_id': system_channel_id,
            'tags': tags
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['id']
        path_param_values = self.encode_path_vars(id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/components/fabric-orderer/{id}'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def orderer_action(self,
        id: str,
        *,
        restart: bool = None,
        reenroll: 'ActionReenroll' = None,
        enroll: 'ActionEnroll' = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Submit action to an orderer.

        Submit an action to a Fabric Orderer component. Actions such as restarting the
        component or certificate operations.

        :param str id: The `id` of the component to modify. Use the [Get all
               components](#list_components) API to determine the component id.
        :param bool restart: (optional) Set to `true` to restart the component.
        :param ActionReenroll reenroll: (optional)
        :param ActionEnroll enroll: (optional)
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ActionsResponse` object
        """

        if id is None:
            raise ValueError('id must be provided')
        if reenroll is not None:
            reenroll = convert_model(reenroll)
        if enroll is not None:
            enroll = convert_model(enroll)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='orderer_action')
        headers.update(sdk_headers)

        data = {
            'restart': restart,
            'reenroll': reenroll,
            'enroll': enroll
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['id']
        path_param_values = self.encode_path_vars(id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/kubernetes/components/fabric-orderer/{id}/actions'.format(**path_param_dict)
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def update_orderer(self,
        id: str,
        *,
        admin_certs: List[str] = None,
        config_override: 'ConfigOrdererUpdate' = None,
        crypto: 'UpdateOrdererBodyCrypto' = None,
        node_ou: 'NodeOu' = None,
        replicas: float = None,
        resources: 'UpdateOrdererBodyResources' = None,
        version: str = None,
        zone: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Update an orderer node.

        Update Kubernetes deployment attributes of a Hyperledger Fabric Ordering node.

        :param str id: The `id` of the component to modify. Use the [Get all
               components](#list_components) API to determine the component id.
        :param List[str] admin_certs: (optional) An array that contains *all* the
               base 64 encoded PEM identity certificates for administrators of this
               component. Also known as signing certificates of an organization
               administrator.
        :param ConfigOrdererUpdate config_override: (optional) Update the [Fabric
               Orderer configuration
               file](https://github.com/hyperledger/fabric/blob/release-1.4/sampleconfig/orderer.yaml)
               if you want use custom attributes to configure the Orderer. Omit if not.
               *The nested field **names** below are not case-sensitive.*
               *The nested fields sent will be merged with the existing settings.*.
        :param UpdateOrdererBodyCrypto crypto: (optional)
        :param NodeOu node_ou: (optional)
        :param float replicas: (optional) The number of replica pods running at any
               given time.
        :param UpdateOrdererBodyResources resources: (optional) CPU and memory
               properties. This feature is not available if using a free Kubernetes
               cluster.
        :param str version: (optional) The Hyperledger Fabric release version to
               update to.
        :param str zone: (optional) Specify the Kubernetes zone for the deployment.
               The deployment will use a k8s node in this zone. Find the list of possible
               zones by retrieving your Kubernetes node labels: `kubectl get nodes
               --show-labels`. [More
               information](https://kubernetes.io/docs/setup/best-practices/multiple-zones).
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `OrdererResponse` object
        """

        if id is None:
            raise ValueError('id must be provided')
        if config_override is not None:
            config_override = convert_model(config_override)
        if crypto is not None:
            crypto = convert_model(crypto)
        if node_ou is not None:
            node_ou = convert_model(node_ou)
        if resources is not None:
            resources = convert_model(resources)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='update_orderer')
        headers.update(sdk_headers)

        data = {
            'admin_certs': admin_certs,
            'config_override': config_override,
            'crypto': crypto,
            'node_ou': node_ou,
            'replicas': replicas,
            'resources': resources,
            'version': version,
            'zone': zone
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['id']
        path_param_values = self.encode_path_vars(id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/kubernetes/components/fabric-orderer/{id}'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def submit_block(self,
        id: str,
        *,
        b64_block: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Submit config block to orderer.

        Send a config block (or genesis block) to a pre-created raft orderer node. Use
        this api to finish the raft-append flow and finalize a pre-created orderer. This
        is the final step to append a node to a raft cluster. The orderer will restart,
        load this block, and connect to the other orderers listed in said block.
        The full flow to append a raft node:
          1. Pre-create the orderer with the [Create an ordering service](#create-orderer)
        API (setting `cluster_id` is how you turn the normal create-orderer api into a
        pre-create-orderer api).
          2. Retrieve the pre-created node's tls cert with the [Get component
        data](#get-component) API (set the `deployment_attrs=included` parameter).
          3. Get the latest config block for the system-channel by using the Fabric API
        (use a Fabric CLI or another Fabric tool).
          4. Edit the config block for the system-channel and add the pre-created
        orderer's tls cert and api url as a consenter.
          5. Create and marshal a Fabric
        [ConfigUpdate](https://github.com/hyperledger/fabric/blob/release-1.4/protos/common/configtx.proto#L78)
        proposal with
        [configtxlator](https://hyperledger-fabric.readthedocs.io/en/release-1.4/commands/configtxlator.html#configtxlator-compute-update)
        using the old and new block.
          6. Sign the `ConfigUpdate` proposal and create a
        [ConfigSignature](https://github.com/hyperledger/fabric/blob/release-1.4/protos/common/configtx.proto#L111).
        Create a set of signatures that will satisfy the system channel's update policy.
          7. Build a
        [SignedProposal](https://github.com/hyperledger/fabric/blob/release-1.4/protos/peer/proposal.proto#L105)
        out of the `ConfigUpdate` & `ConfigSignature`. Submit the `SignedProposal` to an
        existing ordering node (do not use the pre-created node).
          8. After the `SignedProposal` transaction is committed to a block, pull the
        latest config block (for the system-channel) from an existing ordering node (use a
        Fabric CLI or another Fabric tool).
          9. Submit the latest config block to your pre-created node with the 'Submit
        config block to orderer' API (which is this api!)
          10. Use the [Edit data about an orderer](#edit-orderer) API to change the
        pre-created node's field `consenter_proposal_fin` to `true`. This changes the
        status icon on the IBP console.

        :param str id: The `id` of the component to modify. Use the [Get all
               components](#list_components) API to determine the component id.
        :param str b64_block: (optional) The latest config block of the system
               channel. Base 64 encoded. To obtain this block, you must use a **Fabric
               API**. This config block should list this ordering node as a valid
               consenter on the system-channel.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `GenericComponentResponse` object
        """

        if id is None:
            raise ValueError('id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='submit_block')
        headers.update(sdk_headers)

        data = {
            'b64_block': b64_block
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['id']
        path_param_values = self.encode_path_vars(id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/kubernetes/components/{id}/config'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def import_msp(self,
        msp_id: str,
        display_name: str,
        root_certs: List[str],
        *,
        intermediate_certs: List[str] = None,
        admins: List[str] = None,
        tls_root_certs: List[str] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Import an MSP.

        Create or import a Membership Service Provider (MSP) definition into your IBP
        console. This definition represents an organization that controls a peer or OS
        (Ordering Service).

        :param str msp_id: The MSP id that is related to this component.
        :param str display_name: A descriptive name for this MSP. The IBP console
               tile displays this name.
        :param List[str] root_certs: An array that contains one or more base 64
               encoded PEM root certificates for the MSP.
        :param List[str] intermediate_certs: (optional) An array that contains base
               64 encoded PEM intermediate certificates.
        :param List[str] admins: (optional) An array that contains base 64 encoded
               PEM identity certificates for administrators. Also known as signing
               certificates of an organization administrator.
        :param List[str] tls_root_certs: (optional) An array that contains one or
               more base 64 encoded PEM TLS root certificates.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `MspResponse` object
        """

        if msp_id is None:
            raise ValueError('msp_id must be provided')
        if display_name is None:
            raise ValueError('display_name must be provided')
        if root_certs is None:
            raise ValueError('root_certs must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='import_msp')
        headers.update(sdk_headers)

        data = {
            'msp_id': msp_id,
            'display_name': display_name,
            'root_certs': root_certs,
            'intermediate_certs': intermediate_certs,
            'admins': admins,
            'tls_root_certs': tls_root_certs
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/components/msp'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def edit_msp(self,
        id: str,
        *,
        msp_id: str = None,
        display_name: str = None,
        root_certs: List[str] = None,
        intermediate_certs: List[str] = None,
        admins: List[str] = None,
        tls_root_certs: List[str] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Edit an MSP.

        Modify local metadata fields of a Membership Service Provider (MSP) definition.
        For example, the "display_name" property.

        :param str id: The `id` of the component to modify. Use the [Get all
               components](#list_components) API to determine the component id.
        :param str msp_id: (optional) The MSP id that is related to this component.
        :param str display_name: (optional) A descriptive name for this MSP. The
               IBP console tile displays this name.
        :param List[str] root_certs: (optional) An array that contains one or more
               base 64 encoded PEM root certificates for the MSP.
        :param List[str] intermediate_certs: (optional) An array that contains base
               64 encoded PEM intermediate certificates.
        :param List[str] admins: (optional) An array that contains base 64 encoded
               PEM identity certificates for administrators. Also known as signing
               certificates of an organization administrator.
        :param List[str] tls_root_certs: (optional) An array that contains one or
               more base 64 encoded PEM TLS root certificates.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `MspResponse` object
        """

        if id is None:
            raise ValueError('id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='edit_msp')
        headers.update(sdk_headers)

        data = {
            'msp_id': msp_id,
            'display_name': display_name,
            'root_certs': root_certs,
            'intermediate_certs': intermediate_certs,
            'admins': admins,
            'tls_root_certs': tls_root_certs
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['id']
        path_param_values = self.encode_path_vars(id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/components/msp/{id}'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def get_msp_certificate(self,
        msp_id: str,
        *,
        cache: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get MSP's public certificates.

        External IBP consoles can use this API to get the public certificate for your
        given MSP id.

        :param str msp_id: The `msp_id` to fetch.
        :param str cache: (optional) Set to 'skip' if the response should skip
               local data and fetch live data wherever possible. Expect longer response
               times if the cache is skipped. Default responses will use the cache.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `GetMSPCertificateResponse` object
        """

        if msp_id is None:
            raise ValueError('msp_id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='get_msp_certificate')
        headers.update(sdk_headers)

        params = {
            'cache': cache
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['msp_id']
        path_param_values = self.encode_path_vars(msp_id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/components/msps/{msp_id}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def edit_admin_certs(self,
        id: str,
        *,
        append_admin_certs: List[str] = None,
        remove_admin_certs: List[str] = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Edit admin certs on a component.

        This api will append or remove admin certs to the components' file system.
        Certificates will be parsed. If invalid they will be skipped. Duplicate
        certificates will also be skipped. To view existing admin certificate use the [Get
        component data](#get-component) API with the query parameters:
        `?deployment_attrs=included&cache=skip`.
        **This API will not work on *imported* components.**.

        :param str id: The `id` of the component to edit. Use the [Get all
               components](#list_components) API to determine the id of the component.
        :param List[str] append_admin_certs: (optional) The admin certificates to
               add to the file system.
        :param List[str] remove_admin_certs: (optional) The admin certificates to
               remove from the file system. To see the current list run the [Get a
               component](#get-component) API with the `deployment_attrs=included`
               parameter.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `EditAdminCertsResponse` object
        """

        if id is None:
            raise ValueError('id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='edit_admin_certs')
        headers.update(sdk_headers)

        data = {
            'append_admin_certs': append_admin_certs,
            'remove_admin_certs': remove_admin_certs
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['id']
        path_param_values = self.encode_path_vars(id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/kubernetes/components/{id}/certs'.format(**path_param_dict)
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response

    #########################
    # Manage multiple components
    #########################


    def list_components(self,
        *,
        deployment_attrs: str = None,
        parsed_certs: str = None,
        cache: str = None,
        ca_attrs: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get all components.

        Get the IBP console's data on all components (peers, CAs, orderers, and MSPs). The
        component might be imported or created.

        :param str deployment_attrs: (optional) Set to 'included' if the response
               should include Kubernetes deployment attributes such as 'resources',
               'storage', 'zone', 'region', 'admin_certs', etc. Default responses will not
               include these fields.
               **This parameter will not work on *imported* components.**
               It's recommended to use `cache=skip` as well if up-to-date deployment data
               is needed.
        :param str parsed_certs: (optional) Set to 'included' if the response
               should include parsed PEM data along with base 64 encoded PEM string.
               Parsed certificate data will include fields such as the serial number,
               issuer, expiration, subject, subject alt names, etc. Default responses will
               not include these fields.
        :param str cache: (optional) Set to 'skip' if the response should skip
               local data and fetch live data wherever possible. Expect longer response
               times if the cache is skipped. Default responses will use the cache.
        :param str ca_attrs: (optional) Set to 'included' if the response should
               fetch CA attributes, inspect certificates, and append extra fields to CA
               and MSP component responses.
               - CA components will have fields appended/updated with data fetched from
               the `/cainfo?ca=ca` endpoint of a CA, such as: `ca_name`, `root_cert`,
               `fabric_version`, `issuer_public_key` and `issued_known_msps`. The field
               `issued_known_msps` indicates imported IBP MSPs that this CA has issued.
               Meaning the MSP's root cert contains a signature that is derived from this
               CA's root cert. Only imported MSPs are checked. Default responses will not
               include these fields.
               - MSP components will have the field `issued_by_ca_id` appended. This field
               indicates the id of an IBP console CA that issued this MSP. Meaning the
               MSP's root cert contains a signature that is derived from this CA's root
               cert. Only imported/created CAs are checked. Default responses will not
               include these fields.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `GetMultiComponentsResponse` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='list_components')
        headers.update(sdk_headers)

        params = {
            'deployment_attrs': deployment_attrs,
            'parsed_certs': parsed_certs,
            'cache': cache,
            'ca_attrs': ca_attrs
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/components'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def get_components_by_type(self,
        type: str,
        *,
        deployment_attrs: str = None,
        parsed_certs: str = None,
        cache: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get components of a type.

        Get the IBP console's data on components that are a specific type. The component
        might be imported or created.

        :param str type: The type of component to filter components on.
        :param str deployment_attrs: (optional) Set to 'included' if the response
               should include Kubernetes deployment attributes such as 'resources',
               'storage', 'zone', 'region', 'admin_certs', etc. Default responses will not
               include these fields.
               **This parameter will not work on *imported* components.**
               It's recommended to use `cache=skip` as well if up-to-date deployment data
               is needed.
        :param str parsed_certs: (optional) Set to 'included' if the response
               should include parsed PEM data along with base 64 encoded PEM string.
               Parsed certificate data will include fields such as the serial number,
               issuer, expiration, subject, subject alt names, etc. Default responses will
               not include these fields.
        :param str cache: (optional) Set to 'skip' if the response should skip
               local data and fetch live data wherever possible. Expect longer response
               times if the cache is skipped. Default responses will use the cache.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `GetMultiComponentsResponse` object
        """

        if type is None:
            raise ValueError('type must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='get_components_by_type')
        headers.update(sdk_headers)

        params = {
            'deployment_attrs': deployment_attrs,
            'parsed_certs': parsed_certs,
            'cache': cache
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['type']
        path_param_values = self.encode_path_vars(type)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/components/types/{type}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def get_components_by_tag(self,
        tag: str,
        *,
        deployment_attrs: str = None,
        parsed_certs: str = None,
        cache: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get components with tag.

        Get the IBP console's data on components that have a specific tag. The component
        might be imported or created. Tags are not case-sensitive.

        :param str tag: The tag to filter components on. Not case-sensitive.
        :param str deployment_attrs: (optional) Set to 'included' if the response
               should include Kubernetes deployment attributes such as 'resources',
               'storage', 'zone', 'region', 'admin_certs', etc. Default responses will not
               include these fields.
               **This parameter will not work on *imported* components.**
               It's recommended to use `cache=skip` as well if up-to-date deployment data
               is needed.
        :param str parsed_certs: (optional) Set to 'included' if the response
               should include parsed PEM data along with base 64 encoded PEM string.
               Parsed certificate data will include fields such as the serial number,
               issuer, expiration, subject, subject alt names, etc. Default responses will
               not include these fields.
        :param str cache: (optional) Set to 'skip' if the response should skip
               local data and fetch live data wherever possible. Expect longer response
               times if the cache is skipped. Default responses will use the cache.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `GetMultiComponentsResponse` object
        """

        if tag is None:
            raise ValueError('tag must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='get_components_by_tag')
        headers.update(sdk_headers)

        params = {
            'deployment_attrs': deployment_attrs,
            'parsed_certs': parsed_certs,
            'cache': cache
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['tag']
        path_param_values = self.encode_path_vars(tag)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/components/tags/{tag}'.format(**path_param_dict)
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def remove_components_by_tag(self,
        tag: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Remove components with tag.

        Removes components with the matching tag from the IBP console. Tags are not
        case-sensitive.
        - Using this api on **imported** components removes them from the IBP console.
        - Using this api on **created** components removes them from the IBP console
        **but** it will **not** delete the components from the Kubernetes cluster where
        they reside. Thus it orphans the Kubernetes deployments (if it exists). Instead
        use the [Delete components with tag](#delete_components_by_tag) API to delete the
        Kubernetes deployment and the IBP console data at once.

        :param str tag: The tag to filter components on. Not case-sensitive.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `RemoveMultiComponentsResponse` object
        """

        if tag is None:
            raise ValueError('tag must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='remove_components_by_tag')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['tag']
        path_param_values = self.encode_path_vars(tag)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/components/tags/{tag}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def delete_components_by_tag(self,
        tag: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete components with tag.

        Removes components with the matching tag from the IBP console **and** it deletes
        the Kubernetes deployment. Tags are not case-sensitive.
        - Using this api on **imported** components will be skipped over since their
        Kubernetes deployment is unknown and cannot be removed. Instead use the [Remove
        components with tag](#remove_components_by_tag) API to remove imported components
        with a tag.
        - Using this api on **created** components removes them from the IBP console
        **and** it will delete the components from the Kubernetes cluster where they
        reside. The Kubernetes delete must succeed before the component will be removed
        from the IBP console.

        :param str tag: The tag to filter components on. Not case-sensitive.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `DeleteMultiComponentsResponse` object
        """

        if tag is None:
            raise ValueError('tag must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='delete_components_by_tag')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['tag']
        path_param_values = self.encode_path_vars(tag)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/kubernetes/components/tags/{tag}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def delete_all_components(self,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete all components.

        Removes all components from the IBP console **and** their Kubernetes deployments
        (if applicable). Works on imported and created components (peers, CAs, orderers,
        MSPs, and signature collection transactions). This api attempts to effectively
        reset the IBP console to its initial (empty) state (except for logs &
        notifications, those will remain).

        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `DeleteMultiComponentsResponse` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='delete_all_components')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/kubernetes/components/purge'
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response

    #########################
    # Administer the IBP console
    #########################


    def get_settings(self,
        **kwargs
    ) -> DetailedResponse:
        """
        Get public IBP console settings.

        Retrieve all public (non-sensitive) settings for the IBP console. Use this API for
        debugging purposes. It shows what behavior to expect and confirms whether the
        desired settings are active.

        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `GetPublicSettingsResponse` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='get_settings')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/settings'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def edit_settings(self,
        *,
        inactivity_timeouts: 'EditSettingsBodyInactivityTimeouts' = None,
        file_logging: 'EditLogSettingsBody' = None,
        max_req_per_min: float = None,
        max_req_per_min_ak: float = None,
        fabric_get_block_timeout_ms: float = None,
        fabric_instantiate_timeout_ms: float = None,
        fabric_join_channel_timeout_ms: float = None,
        fabric_install_cc_timeout_ms: float = None,
        fabric_lc_install_cc_timeout_ms: float = None,
        fabric_lc_get_cc_timeout_ms: float = None,
        fabric_general_timeout_ms: float = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Change IBP console settings.

        Edit a few IBP console settings (such as the rate limit and timeout settings).
        **Some edits will trigger an automatic server restart.**.

        :param EditSettingsBodyInactivityTimeouts inactivity_timeouts: (optional)
        :param EditLogSettingsBody file_logging: (optional) File system logging
               settings. All body fields are optional (only send the fields that you want
               to change). _Changes to this field will restart the IBP console server(s)_.
        :param float max_req_per_min: (optional) The base limit for the maximum
               number of `/api/*` API requests (aka UI requests) in 1 minute. Defaults
               `25`. [Rate Limits](#rate-limits). _Changes to this field will restart the
               IBP console server(s)_.
        :param float max_req_per_min_ak: (optional) The base limit for the maximum
               number of `/ak/api/*` API requests (aka external api key requests) in 1
               minute. Defaults `25`. [Rate Limits](#rate-limits). _Changes to this field
               will restart the IBP console server(s)_.
        :param float fabric_get_block_timeout_ms: (optional) Maximum time in
               milliseconds to wait for a get-block transaction. Defaults to `10000` ms
               (10 seconds). _Refresh browser after changes_.
        :param float fabric_instantiate_timeout_ms: (optional) Maximum time in
               milliseconds to wait for a instantiate chaincode transaction. Defaults to
               `300000` ms (5 minutes). _Refresh browser after changes_.
        :param float fabric_join_channel_timeout_ms: (optional) Maximum time in
               milliseconds to wait for a join-channel transaction. Defaults to `25000` ms
               (25 seconds). _Refresh browser after changes_.
        :param float fabric_install_cc_timeout_ms: (optional) Maximum time in
               milliseconds to wait for a install chaincode transaction (Fabric v1.x).
               Defaults to `300000` ms (5 minutes). _Refresh browser after changes_.
        :param float fabric_lc_install_cc_timeout_ms: (optional) Maximum time in
               milliseconds to wait for a install chaincode transaction (Fabric v2.x).
               Defaults to `300000` ms (5 minutes). _Refresh browser after changes_.
        :param float fabric_lc_get_cc_timeout_ms: (optional) Maximum time in
               milliseconds to wait for a get-chaincode transaction (Fabric v2.x).
               Defaults to `180000` ms (3 minutes). _Refresh browser after changes_.
        :param float fabric_general_timeout_ms: (optional) Default maximum time in
               milliseconds to wait for a Fabric transaction. Defaults to `10000` ms (10
               seconds). _Refresh browser after changes_.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `GetPublicSettingsResponse` object
        """

        if inactivity_timeouts is not None:
            inactivity_timeouts = convert_model(inactivity_timeouts)
        if file_logging is not None:
            file_logging = convert_model(file_logging)
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='edit_settings')
        headers.update(sdk_headers)

        data = {
            'inactivity_timeouts': inactivity_timeouts,
            'file_logging': file_logging,
            'max_req_per_min': max_req_per_min,
            'max_req_per_min_ak': max_req_per_min_ak,
            'fabric_get_block_timeout_ms': fabric_get_block_timeout_ms,
            'fabric_instantiate_timeout_ms': fabric_instantiate_timeout_ms,
            'fabric_join_channel_timeout_ms': fabric_join_channel_timeout_ms,
            'fabric_install_cc_timeout_ms': fabric_install_cc_timeout_ms,
            'fabric_lc_install_cc_timeout_ms': fabric_lc_install_cc_timeout_ms,
            'fabric_lc_get_cc_timeout_ms': fabric_lc_get_cc_timeout_ms,
            'fabric_general_timeout_ms': fabric_general_timeout_ms
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/settings'
        request = self.prepare_request(method='PUT',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def get_fab_versions(self,
        *,
        cache: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get supported Fabric versions.

        Get list of supported Fabric versions by each component type. These are the Fabric
        versions your IBP console can use when creating or upgrading components.

        :param str cache: (optional) Set to 'skip' if the response should skip
               local data and fetch live data wherever possible. Expect longer response
               times if the cache is skipped. Default responses will use the cache.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `GetFabricVersionsResponse` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='get_fab_versions')
        headers.update(sdk_headers)

        params = {
            'cache': cache
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/kubernetes/fabric/versions'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def get_health(self,
        **kwargs
    ) -> DetailedResponse:
        """
        Get IBP console health stats.

        See statistics of the IBP console process such as memory usage, CPU usage, up
        time, cache, and operating system stats.

        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `GetAthenaHealthStatsResponse` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='get_health')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/health'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def list_notifications(self,
        *,
        limit: float = None,
        skip: float = None,
        component_id: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Get all notifications.

        Retrieve all notifications. This API supports pagination through the query
        parameters. Notifications are generated from actions such as creating a component,
        deleting a component, server restart, and so on.

        :param float limit: (optional) The number of notifications to return. The
               default value is 100.
        :param float skip: (optional) `skip` is used to paginate through a long
               list of sorted entries. For example, if there are 100 notifications, you
               can issue the API with limit=10 and skip=0 to get the first 1-10. To get
               the next 10, you can set limit=10 and skip=10 so that the values of entries
               11-20 are returned.
        :param str component_id: (optional) Filter response to only contain
               notifications for a particular component id. The default response will
               include all notifications.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `GetNotificationsResponse` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='list_notifications')
        headers.update(sdk_headers)

        params = {
            'limit': limit,
            'skip': skip,
            'component_id': component_id
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/notifications'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def delete_sig_tx(self,
        id: str,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete a signature collection tx.

        Delete a signature collection transaction. These transactions involve creating or
        editing Fabric channels & chaincode approvals. This request is not distributed to
        external IBP consoles, thus the signature collection transaction is only deleted
        locally.

        :param str id: The unique transaction ID of this signature collection.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `DeleteSignatureCollectionResponse` object
        """

        if id is None:
            raise ValueError('id must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='delete_sig_tx')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        path_param_keys = ['id']
        path_param_values = self.encode_path_vars(id)
        path_param_dict = dict(zip(path_param_keys, path_param_values))
        url = '/ak/api/v3/signature_collections/{id}'.format(**path_param_dict)
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def archive_notifications(self,
        notification_ids: List[str],
        **kwargs
    ) -> DetailedResponse:
        """
        Archive notifications.

        Archive 1 or more notifications. Archived notifications will no longer appear in
        the default [Get all notifications](#list-notifications) API.

        :param List[str] notification_ids: Array of notification IDs to archive.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `ArchiveResponse` object
        """

        if notification_ids is None:
            raise ValueError('notification_ids must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='archive_notifications')
        headers.update(sdk_headers)

        data = {
            'notification_ids': notification_ids
        }
        data = {k: v for (k, v) in data.items() if v is not None}
        data = json.dumps(data)
        headers['content-type'] = 'application/json'

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/notifications/bulk'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       data=data)

        response = self.send(request)
        return response


    def restart(self,
        **kwargs
    ) -> DetailedResponse:
        """
        Restart the IBP console.

        Restart IBP console processes. This causes a small outage (10 - 30 seconds) which
        is possibly disruptive to active user sessions.

        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `RestartAthenaResponse` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='restart')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/restart'
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def delete_all_sessions(self,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete all IBP console sessions.

        Delete all client sessions in IBP console. Use this API to clear any active logins
        and force everyone to log in again. This API is useful for debugging purposes and
        when changing roles of a user. It forces any role changes to take effect
        immediately. Otherwise, permission or role changes will take effect during the
        user's next login or session expiration.

        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `DeleteAllSessionsResponse` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='delete_all_sessions')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/sessions'
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def delete_all_notifications(self,
        **kwargs
    ) -> DetailedResponse:
        """
        Delete all notifications.

        Delete all notifications. This API is intended for administration.

        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `DeleteAllNotificationsResponse` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='delete_all_notifications')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/notifications/purge'
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


    def clear_caches(self,
        **kwargs
    ) -> DetailedResponse:
        """
        Clear IBP console caches.

        Clear the in-memory caches across all IBP console server processes. No effect on
        caches that are currently disabled.

        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `dict` result representing a `CacheFlushResponse` object
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='clear_caches')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/cache'
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response

    #########################
    # Download examples
    #########################


    def get_postman(self,
        auth_type: str,
        *,
        token: str = None,
        api_key: str = None,
        username: str = None,
        password: str = None,
        **kwargs
    ) -> DetailedResponse:
        """
        Generate Postman collection.

        Generate and download a Postman API Collection. The JSON contains all the APIs
        available in the IBP console. It can be imported to the
        [Postman](https://www.postman.com/downloads) desktop application. **The examples
        in the collection will be pre-populated with authorization credentials.** The
        authorization credentials to use must be provided to this API. See the query
        parameters for available options.
        Choose an auth strategy that matches your environment & concerns:
        - **IAM Bearer Auth** - *[Available on IBM Cloud]* - This is the recommended auth
        strategy. The same bearer token used to authenticate this request will be copied
        into the Postman collection examples. Since the bearer token expires the auth
        embedded in the collection will also expire. At that point the collection might be
        deleted & regenerated, or manually edited to refresh the authorization header
        values. To use this strategy set `auth_type` to `bearer`.
        - **IAM Api Key Auth** - *[Available on IBM Cloud]* - The IAM api key will be
        copied into the Postman collection examples. This means the auth embedded in the
        collection will never expire. To use this strategy set `auth_type` to `api_key`.
        - **Basic Auth** - *[Available on OpenShift & IBM Cloud Private]* - A basic auth
        username and password will be copied into the Postman collection examples. This is
        **not** available for an IBP SaaS instance on IBM Cloud. To use this strategy set
        `auth_type` to `basic`.

        :param str auth_type: - **bearer** - IAM Bearer Auth - *[Available on IBM
               Cloud]* - The same bearer token used to authenticate this request will be
               copied into the Postman collection examples. The query parameter `token`
               must also be set with your IAM bearer/access token value.
               - **api_key** - IAM Api Key Auth - *[Available on IBM Cloud]* - The IAM api
               key will be copied into the Postman collection examples. The query
               parameter `api_key` must also be set with your IAM API Key value.
               - **basic** - Basic Auth - *[Available on OpenShift & IBM Cloud Private]* -
               A basic auth username and password will be copied into the Postman
               collection examples. The query parameters `username` & `password` must also
               be set with your IBP api key credentials. The IBP api key is the username
               and the api secret is the password.
        :param str token: (optional) The IAM access/bearer token to use for auth in
               the collection.
        :param str api_key: (optional) The IAM api key to use for auth in the
               collection.
        :param str username: (optional) The basic auth username to use for auth in
               the collection.
        :param str password: (optional) The basic auth password to use for auth in
               the collection.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if auth_type is None:
            raise ValueError('auth_type must be provided')
        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='get_postman')
        headers.update(sdk_headers)

        params = {
            'auth_type': auth_type,
            'token': token,
            'api_key': api_key,
            'username': username,
            'password': password
        }

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'application/json'

        url = '/ak/api/v3/postman'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response


    def get_swagger(self,
        **kwargs
    ) -> DetailedResponse:
        """
        Download OpenAPI file.

        Download the [OpenAPI](https://swagger.io/specification/) specification YAML file
        (aka swagger file) for the IBP console. This is the same file that was used to
        generate the APIs on this page. This file documents APIs offered by the IBP
        console.

        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `str` result
        """

        headers = {}
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V3',
                                      operation_id='get_swagger')
        headers.update(sdk_headers)

        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        headers['Accept'] = 'text/plain'

        url = '/ak/api/v3/openapi'
        request = self.prepare_request(method='GET',
                                       url=url,
                                       headers=headers)

        response = self.send(request)
        return response


class GetComponentEnums:
    """
    Enums for get_component parameters.
    """

    class DeploymentAttrs(str, Enum):
        """
        Set to 'included' if the response should include Kubernetes deployment attributes
        such as 'resources', 'storage', 'zone', 'region', 'admin_certs', etc. Default
        responses will not include these fields.
        **This parameter will not work on *imported* components.**
        It's recommended to use `cache=skip` as well if up-to-date deployment data is
        needed.
        """
        INCLUDED = 'included'
        OMITTED = 'omitted'
    class ParsedCerts(str, Enum):
        """
        Set to 'included' if the response should include parsed PEM data along with base
        64 encoded PEM string. Parsed certificate data will include fields such as the
        serial number, issuer, expiration, subject, subject alt names, etc. Default
        responses will not include these fields.
        """
        INCLUDED = 'included'
        OMITTED = 'omitted'
    class Cache(str, Enum):
        """
        Set to 'skip' if the response should skip local data and fetch live data wherever
        possible. Expect longer response times if the cache is skipped. Default responses
        will use the cache.
        """
        SKIP = 'skip'
        USE = 'use'
    class CaAttrs(str, Enum):
        """
        Set to 'included' if the response should fetch CA attributes, inspect
        certificates, and append extra fields to CA and MSP component responses.
        - CA components will have fields appended/updated with data fetched from the
        `/cainfo?ca=ca` endpoint of a CA, such as: `ca_name`, `root_cert`,
        `fabric_version`, `issuer_public_key` and `issued_known_msps`. The field
        `issued_known_msps` indicates imported IBP MSPs that this CA has issued. Meaning
        the MSP's root cert contains a signature that is derived from this CA's root cert.
        Only imported MSPs are checked. Default responses will not include these fields.
        - MSP components will have the field `issued_by_ca_id` appended. This field
        indicates the id of an IBP console CA that issued this MSP. Meaning the MSP's root
        cert contains a signature that is derived from this CA's root cert. Only
        imported/created CAs are checked. Default responses will not include these fields.
        """
        INCLUDED = 'included'
        OMITTED = 'omitted'


class GetMspCertificateEnums:
    """
    Enums for get_msp_certificate parameters.
    """

    class Cache(str, Enum):
        """
        Set to 'skip' if the response should skip local data and fetch live data wherever
        possible. Expect longer response times if the cache is skipped. Default responses
        will use the cache.
        """
        SKIP = 'skip'
        USE = 'use'


class ListComponentsEnums:
    """
    Enums for list_components parameters.
    """

    class DeploymentAttrs(str, Enum):
        """
        Set to 'included' if the response should include Kubernetes deployment attributes
        such as 'resources', 'storage', 'zone', 'region', 'admin_certs', etc. Default
        responses will not include these fields.
        **This parameter will not work on *imported* components.**
        It's recommended to use `cache=skip` as well if up-to-date deployment data is
        needed.
        """
        INCLUDED = 'included'
        OMITTED = 'omitted'
    class ParsedCerts(str, Enum):
        """
        Set to 'included' if the response should include parsed PEM data along with base
        64 encoded PEM string. Parsed certificate data will include fields such as the
        serial number, issuer, expiration, subject, subject alt names, etc. Default
        responses will not include these fields.
        """
        INCLUDED = 'included'
        OMITTED = 'omitted'
    class Cache(str, Enum):
        """
        Set to 'skip' if the response should skip local data and fetch live data wherever
        possible. Expect longer response times if the cache is skipped. Default responses
        will use the cache.
        """
        SKIP = 'skip'
        USE = 'use'
    class CaAttrs(str, Enum):
        """
        Set to 'included' if the response should fetch CA attributes, inspect
        certificates, and append extra fields to CA and MSP component responses.
        - CA components will have fields appended/updated with data fetched from the
        `/cainfo?ca=ca` endpoint of a CA, such as: `ca_name`, `root_cert`,
        `fabric_version`, `issuer_public_key` and `issued_known_msps`. The field
        `issued_known_msps` indicates imported IBP MSPs that this CA has issued. Meaning
        the MSP's root cert contains a signature that is derived from this CA's root cert.
        Only imported MSPs are checked. Default responses will not include these fields.
        - MSP components will have the field `issued_by_ca_id` appended. This field
        indicates the id of an IBP console CA that issued this MSP. Meaning the MSP's root
        cert contains a signature that is derived from this CA's root cert. Only
        imported/created CAs are checked. Default responses will not include these fields.
        """
        INCLUDED = 'included'
        OMITTED = 'omitted'


class GetComponentsByTypeEnums:
    """
    Enums for get_components_by_type parameters.
    """

    class Type(str, Enum):
        """
        The type of component to filter components on.
        """
        FABRIC_PEER = 'fabric-peer'
        FABRIC_ORDERER = 'fabric-orderer'
        FABRIC_CA = 'fabric-ca'
        MSP = 'msp'
    class DeploymentAttrs(str, Enum):
        """
        Set to 'included' if the response should include Kubernetes deployment attributes
        such as 'resources', 'storage', 'zone', 'region', 'admin_certs', etc. Default
        responses will not include these fields.
        **This parameter will not work on *imported* components.**
        It's recommended to use `cache=skip` as well if up-to-date deployment data is
        needed.
        """
        INCLUDED = 'included'
        OMITTED = 'omitted'
    class ParsedCerts(str, Enum):
        """
        Set to 'included' if the response should include parsed PEM data along with base
        64 encoded PEM string. Parsed certificate data will include fields such as the
        serial number, issuer, expiration, subject, subject alt names, etc. Default
        responses will not include these fields.
        """
        INCLUDED = 'included'
        OMITTED = 'omitted'
    class Cache(str, Enum):
        """
        Set to 'skip' if the response should skip local data and fetch live data wherever
        possible. Expect longer response times if the cache is skipped. Default responses
        will use the cache.
        """
        SKIP = 'skip'
        USE = 'use'


class GetComponentsByTagEnums:
    """
    Enums for get_components_by_tag parameters.
    """

    class DeploymentAttrs(str, Enum):
        """
        Set to 'included' if the response should include Kubernetes deployment attributes
        such as 'resources', 'storage', 'zone', 'region', 'admin_certs', etc. Default
        responses will not include these fields.
        **This parameter will not work on *imported* components.**
        It's recommended to use `cache=skip` as well if up-to-date deployment data is
        needed.
        """
        INCLUDED = 'included'
        OMITTED = 'omitted'
    class ParsedCerts(str, Enum):
        """
        Set to 'included' if the response should include parsed PEM data along with base
        64 encoded PEM string. Parsed certificate data will include fields such as the
        serial number, issuer, expiration, subject, subject alt names, etc. Default
        responses will not include these fields.
        """
        INCLUDED = 'included'
        OMITTED = 'omitted'
    class Cache(str, Enum):
        """
        Set to 'skip' if the response should skip local data and fetch live data wherever
        possible. Expect longer response times if the cache is skipped. Default responses
        will use the cache.
        """
        SKIP = 'skip'
        USE = 'use'


class GetFabVersionsEnums:
    """
    Enums for get_fab_versions parameters.
    """

    class Cache(str, Enum):
        """
        Set to 'skip' if the response should skip local data and fetch live data wherever
        possible. Expect longer response times if the cache is skipped. Default responses
        will use the cache.
        """
        SKIP = 'skip'
        USE = 'use'


class GetPostmanEnums:
    """
    Enums for get_postman parameters.
    """

    class AuthType(str, Enum):
        """
        - **bearer** - IAM Bearer Auth - *[Available on IBM Cloud]* - The same bearer
        token used to authenticate this request will be copied into the Postman collection
        examples. The query parameter `token` must also be set with your IAM bearer/access
        token value.
        - **api_key** - IAM Api Key Auth - *[Available on IBM Cloud]* - The IAM api key
        will be copied into the Postman collection examples. The query parameter `api_key`
        must also be set with your IAM API Key value.
        - **basic** - Basic Auth - *[Available on OpenShift & IBM Cloud Private]* - A
        basic auth username and password will be copied into the Postman collection
        examples. The query parameters `username` & `password` must also be set with your
        IBP api key credentials. The IBP api key is the username and the api secret is the
        password.
        """
        BEARER = 'bearer'
        API_KEY = 'api_key'
        BASIC = 'basic'


##############################################################################
# Models
##############################################################################


class ActionsResponse():
    """
    ActionsResponse.

    :attr str message: (optional)
    :attr str id: (optional) The id of the component.
    :attr List[str] actions: (optional)
    """

    def __init__(self,
                 *,
                 message: str = None,
                 id: str = None,
                 actions: List[str] = None) -> None:
        """
        Initialize a ActionsResponse object.

        :param str message: (optional)
        :param str id: (optional) The id of the component.
        :param List[str] actions: (optional)
        """
        self.message = message
        self.id = id
        self.actions = actions

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ActionsResponse':
        """Initialize a ActionsResponse object from a json dictionary."""
        args = {}
        if 'message' in _dict:
            args['message'] = _dict.get('message')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'actions' in _dict:
            args['actions'] = _dict.get('actions')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ActionsResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'message') and self.message is not None:
            _dict['message'] = self.message
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'actions') and self.actions is not None:
            _dict['actions'] = self.actions
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ActionsResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ActionsResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ActionsResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ArchiveResponse():
    """
    ArchiveResponse.

    :attr str message: (optional) Response message. "ok" indicates the api completed
          successfully.
    :attr str details: (optional) Text with the number of notifications that were
          archived.
    """

    def __init__(self,
                 *,
                 message: str = None,
                 details: str = None) -> None:
        """
        Initialize a ArchiveResponse object.

        :param str message: (optional) Response message. "ok" indicates the api
               completed successfully.
        :param str details: (optional) Text with the number of notifications that
               were archived.
        """
        self.message = message
        self.details = details

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ArchiveResponse':
        """Initialize a ArchiveResponse object from a json dictionary."""
        args = {}
        if 'message' in _dict:
            args['message'] = _dict.get('message')
        if 'details' in _dict:
            args['details'] = _dict.get('details')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ArchiveResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'message') and self.message is not None:
            _dict['message'] = self.message
        if hasattr(self, 'details') and self.details is not None:
            _dict['details'] = self.details
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ArchiveResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ArchiveResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ArchiveResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class Bccsp():
    """
    Configures the Blockchain Crypto Service Providers (bccsp).

    :attr str default: (optional) The name of the crypto library implementation to
          use for the BlockChain Crypto Service Provider (bccsp). Defaults to `SW`.
    :attr BccspSW sw: (optional) Software based blockchain crypto provider.
    :attr BccspPKCS11 pkc_s11: (optional) Hardware-based blockchain crypto provider.
    """

    def __init__(self,
                 *,
                 default: str = None,
                 sw: 'BccspSW' = None,
                 pkc_s11: 'BccspPKCS11' = None) -> None:
        """
        Initialize a Bccsp object.

        :param str default: (optional) The name of the crypto library
               implementation to use for the BlockChain Crypto Service Provider (bccsp).
               Defaults to `SW`.
        :param BccspSW sw: (optional) Software based blockchain crypto provider.
        :param BccspPKCS11 pkc_s11: (optional) Hardware-based blockchain crypto
               provider.
        """
        self.default = default
        self.sw = sw
        self.pkc_s11 = pkc_s11

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Bccsp':
        """Initialize a Bccsp object from a json dictionary."""
        args = {}
        if 'Default' in _dict:
            args['default'] = _dict.get('Default')
        if 'SW' in _dict:
            args['sw'] = BccspSW.from_dict(_dict.get('SW'))
        if 'PKCS11' in _dict:
            args['pkc_s11'] = BccspPKCS11.from_dict(_dict.get('PKCS11'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Bccsp object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'default') and self.default is not None:
            _dict['Default'] = self.default
        if hasattr(self, 'sw') and self.sw is not None:
            _dict['SW'] = self.sw.to_dict()
        if hasattr(self, 'pkc_s11') and self.pkc_s11 is not None:
            _dict['PKCS11'] = self.pkc_s11.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Bccsp object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Bccsp') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Bccsp') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class DefaultEnum(str, Enum):
        """
        The name of the crypto library implementation to use for the BlockChain Crypto
        Service Provider (bccsp). Defaults to `SW`.
        """
        SW = 'SW'
        PKCS11 = 'PKCS11'


class BccspPKCS11():
    """
    Hardware-based blockchain crypto provider.

    :attr str label: Token Label.
    :attr str pin: The user PIN.
    :attr str hash: (optional) The hash family to use for the BlockChain Crypto
          Service Provider (bccsp).
    :attr float security: (optional) The length of hash to use for the BlockChain
          Crypto Service Provider (bccsp).
    """

    def __init__(self,
                 label: str,
                 pin: str,
                 *,
                 hash: str = None,
                 security: float = None) -> None:
        """
        Initialize a BccspPKCS11 object.

        :param str label: Token Label.
        :param str pin: The user PIN.
        :param str hash: (optional) The hash family to use for the BlockChain
               Crypto Service Provider (bccsp).
        :param float security: (optional) The length of hash to use for the
               BlockChain Crypto Service Provider (bccsp).
        """
        self.label = label
        self.pin = pin
        self.hash = hash
        self.security = security

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'BccspPKCS11':
        """Initialize a BccspPKCS11 object from a json dictionary."""
        args = {}
        if 'Label' in _dict:
            args['label'] = _dict.get('Label')
        else:
            raise ValueError('Required property \'Label\' not present in BccspPKCS11 JSON')
        if 'Pin' in _dict:
            args['pin'] = _dict.get('Pin')
        else:
            raise ValueError('Required property \'Pin\' not present in BccspPKCS11 JSON')
        if 'Hash' in _dict:
            args['hash'] = _dict.get('Hash')
        if 'Security' in _dict:
            args['security'] = _dict.get('Security')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a BccspPKCS11 object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'label') and self.label is not None:
            _dict['Label'] = self.label
        if hasattr(self, 'pin') and self.pin is not None:
            _dict['Pin'] = self.pin
        if hasattr(self, 'hash') and self.hash is not None:
            _dict['Hash'] = self.hash
        if hasattr(self, 'security') and self.security is not None:
            _dict['Security'] = self.security
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this BccspPKCS11 object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'BccspPKCS11') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'BccspPKCS11') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class BccspSW():
    """
    Software based blockchain crypto provider.

    :attr str hash: The hash family to use for the BlockChain Crypto Service
          Provider (bccsp).
    :attr float security: The length of hash to use for the BlockChain Crypto
          Service Provider (bccsp).
    """

    def __init__(self,
                 hash: str,
                 security: float) -> None:
        """
        Initialize a BccspSW object.

        :param str hash: The hash family to use for the BlockChain Crypto Service
               Provider (bccsp).
        :param float security: The length of hash to use for the BlockChain Crypto
               Service Provider (bccsp).
        """
        self.hash = hash
        self.security = security

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'BccspSW':
        """Initialize a BccspSW object from a json dictionary."""
        args = {}
        if 'Hash' in _dict:
            args['hash'] = _dict.get('Hash')
        else:
            raise ValueError('Required property \'Hash\' not present in BccspSW JSON')
        if 'Security' in _dict:
            args['security'] = _dict.get('Security')
        else:
            raise ValueError('Required property \'Security\' not present in BccspSW JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a BccspSW object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'hash') and self.hash is not None:
            _dict['Hash'] = self.hash
        if hasattr(self, 'security') and self.security is not None:
            _dict['Security'] = self.security
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this BccspSW object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'BccspSW') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'BccspSW') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CaResponse():
    """
    Contains the details of a CA.

    :attr str id: (optional) The unique identifier of this component.
    :attr str dep_component_id: (optional) The unique id for the component in
          Kubernetes. Not available if component was imported.
    :attr str display_name: (optional) A descriptive name for this CA. The IBP
          console tile displays this name.
    :attr str api_url: (optional) The gRPC URL for the peer. Typically, client
          applications would send requests to this URL. Include the protocol, hostname/ip
          and port.
    :attr str operations_url: (optional) The operations URL for the CA. Include the
          protocol, hostname/ip and port.
    :attr object config_override: (optional) The **cached** configuration override
          that was set for the Kubernetes deployment. Field does not exist if an override
          was not set of if the component was imported.
    :attr str location: (optional) Indicates where the component is running.
    :attr MspCryptoField msp: (optional) The msp crypto data.
    :attr CaResponseResources resources: (optional) The **cached** Kubernetes
          resource attributes for this component. Not available if CA was imported.
    :attr str scheme_version: (optional) The versioning of the IBP console format of
          this JSON.
    :attr CaResponseStorage storage: (optional) The **cached** Kubernetes storage
          attributes for this component. Not available if CA was imported.
    :attr List[str] tags: (optional)
    :attr float timestamp: (optional) UTC UNIX timestamp of component onboarding to
          the UI. In milliseconds.
    :attr str version: (optional) The cached Hyperledger Fabric release version.
    :attr str zone: (optional) Specify the Kubernetes zone for the deployment. The
          deployment will use a k8s node in this zone. Find the list of possible zones by
          retrieving your Kubernetes node labels: `kubectl get nodes --show-labels`. [More
          information](https://kubernetes.io/docs/setup/best-practices/multiple-zones).
    """

    def __init__(self,
                 *,
                 id: str = None,
                 dep_component_id: str = None,
                 display_name: str = None,
                 api_url: str = None,
                 operations_url: str = None,
                 config_override: object = None,
                 location: str = None,
                 msp: 'MspCryptoField' = None,
                 resources: 'CaResponseResources' = None,
                 scheme_version: str = None,
                 storage: 'CaResponseStorage' = None,
                 tags: List[str] = None,
                 timestamp: float = None,
                 version: str = None,
                 zone: str = None) -> None:
        """
        Initialize a CaResponse object.

        :param str id: (optional) The unique identifier of this component.
        :param str dep_component_id: (optional) The unique id for the component in
               Kubernetes. Not available if component was imported.
        :param str display_name: (optional) A descriptive name for this CA. The IBP
               console tile displays this name.
        :param str api_url: (optional) The gRPC URL for the peer. Typically, client
               applications would send requests to this URL. Include the protocol,
               hostname/ip and port.
        :param str operations_url: (optional) The operations URL for the CA.
               Include the protocol, hostname/ip and port.
        :param object config_override: (optional) The **cached** configuration
               override that was set for the Kubernetes deployment. Field does not exist
               if an override was not set of if the component was imported.
        :param str location: (optional) Indicates where the component is running.
        :param MspCryptoField msp: (optional) The msp crypto data.
        :param CaResponseResources resources: (optional) The **cached** Kubernetes
               resource attributes for this component. Not available if CA was imported.
        :param str scheme_version: (optional) The versioning of the IBP console
               format of this JSON.
        :param CaResponseStorage storage: (optional) The **cached** Kubernetes
               storage attributes for this component. Not available if CA was imported.
        :param List[str] tags: (optional)
        :param float timestamp: (optional) UTC UNIX timestamp of component
               onboarding to the UI. In milliseconds.
        :param str version: (optional) The cached Hyperledger Fabric release
               version.
        :param str zone: (optional) Specify the Kubernetes zone for the deployment.
               The deployment will use a k8s node in this zone. Find the list of possible
               zones by retrieving your Kubernetes node labels: `kubectl get nodes
               --show-labels`. [More
               information](https://kubernetes.io/docs/setup/best-practices/multiple-zones).
        """
        self.id = id
        self.dep_component_id = dep_component_id
        self.display_name = display_name
        self.api_url = api_url
        self.operations_url = operations_url
        self.config_override = config_override
        self.location = location
        self.msp = msp
        self.resources = resources
        self.scheme_version = scheme_version
        self.storage = storage
        self.tags = tags
        self.timestamp = timestamp
        self.version = version
        self.zone = zone

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CaResponse':
        """Initialize a CaResponse object from a json dictionary."""
        args = {}
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'dep_component_id' in _dict:
            args['dep_component_id'] = _dict.get('dep_component_id')
        if 'display_name' in _dict:
            args['display_name'] = _dict.get('display_name')
        if 'api_url' in _dict:
            args['api_url'] = _dict.get('api_url')
        if 'operations_url' in _dict:
            args['operations_url'] = _dict.get('operations_url')
        if 'config_override' in _dict:
            args['config_override'] = _dict.get('config_override')
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'msp' in _dict:
            args['msp'] = MspCryptoField.from_dict(_dict.get('msp'))
        if 'resources' in _dict:
            args['resources'] = CaResponseResources.from_dict(_dict.get('resources'))
        if 'scheme_version' in _dict:
            args['scheme_version'] = _dict.get('scheme_version')
        if 'storage' in _dict:
            args['storage'] = CaResponseStorage.from_dict(_dict.get('storage'))
        if 'tags' in _dict:
            args['tags'] = _dict.get('tags')
        if 'timestamp' in _dict:
            args['timestamp'] = _dict.get('timestamp')
        if 'version' in _dict:
            args['version'] = _dict.get('version')
        if 'zone' in _dict:
            args['zone'] = _dict.get('zone')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CaResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'dep_component_id') and self.dep_component_id is not None:
            _dict['dep_component_id'] = self.dep_component_id
        if hasattr(self, 'display_name') and self.display_name is not None:
            _dict['display_name'] = self.display_name
        if hasattr(self, 'api_url') and self.api_url is not None:
            _dict['api_url'] = self.api_url
        if hasattr(self, 'operations_url') and self.operations_url is not None:
            _dict['operations_url'] = self.operations_url
        if hasattr(self, 'config_override') and self.config_override is not None:
            _dict['config_override'] = self.config_override
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'msp') and self.msp is not None:
            _dict['msp'] = self.msp.to_dict()
        if hasattr(self, 'resources') and self.resources is not None:
            _dict['resources'] = self.resources.to_dict()
        if hasattr(self, 'scheme_version') and self.scheme_version is not None:
            _dict['scheme_version'] = self.scheme_version
        if hasattr(self, 'storage') and self.storage is not None:
            _dict['storage'] = self.storage.to_dict()
        if hasattr(self, 'tags') and self.tags is not None:
            _dict['tags'] = self.tags
        if hasattr(self, 'timestamp') and self.timestamp is not None:
            _dict['timestamp'] = self.timestamp
        if hasattr(self, 'version') and self.version is not None:
            _dict['version'] = self.version
        if hasattr(self, 'zone') and self.zone is not None:
            _dict['zone'] = self.zone
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CaResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CaResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CaResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CaResponseResources():
    """
    The **cached** Kubernetes resource attributes for this component. Not available if CA
    was imported.

    :attr GenericResources ca: (optional)
    """

    def __init__(self,
                 *,
                 ca: 'GenericResources' = None) -> None:
        """
        Initialize a CaResponseResources object.

        :param GenericResources ca: (optional)
        """
        self.ca = ca

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CaResponseResources':
        """Initialize a CaResponseResources object from a json dictionary."""
        args = {}
        if 'ca' in _dict:
            args['ca'] = GenericResources.from_dict(_dict.get('ca'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CaResponseResources object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CaResponseResources object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CaResponseResources') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CaResponseResources') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CaResponseStorage():
    """
    The **cached** Kubernetes storage attributes for this component. Not available if CA
    was imported.

    :attr StorageObject ca: (optional)
    """

    def __init__(self,
                 *,
                 ca: 'StorageObject' = None) -> None:
        """
        Initialize a CaResponseStorage object.

        :param StorageObject ca: (optional)
        """
        self.ca = ca

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CaResponseStorage':
        """Initialize a CaResponseStorage object from a json dictionary."""
        args = {}
        if 'ca' in _dict:
            args['ca'] = StorageObject.from_dict(_dict.get('ca'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CaResponseStorage object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CaResponseStorage object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CaResponseStorage') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CaResponseStorage') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CacheData():
    """
    CacheData.

    :attr float hits: (optional) Number of cache hits.
    :attr float misses: (optional) Number of cache misses.
    :attr float keys: (optional) Number of entries in the cache.
    :attr str cache_size: (optional) Approximate size of the in memory cache.
    """

    def __init__(self,
                 *,
                 hits: float = None,
                 misses: float = None,
                 keys: float = None,
                 cache_size: str = None) -> None:
        """
        Initialize a CacheData object.

        :param float hits: (optional) Number of cache hits.
        :param float misses: (optional) Number of cache misses.
        :param float keys: (optional) Number of entries in the cache.
        :param str cache_size: (optional) Approximate size of the in memory cache.
        """
        self.hits = hits
        self.misses = misses
        self.keys = keys
        self.cache_size = cache_size

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CacheData':
        """Initialize a CacheData object from a json dictionary."""
        args = {}
        if 'hits' in _dict:
            args['hits'] = _dict.get('hits')
        if 'misses' in _dict:
            args['misses'] = _dict.get('misses')
        if 'keys' in _dict:
            args['keys'] = _dict.get('keys')
        if 'cache_size' in _dict:
            args['cache_size'] = _dict.get('cache_size')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CacheData object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'hits') and self.hits is not None:
            _dict['hits'] = self.hits
        if hasattr(self, 'misses') and self.misses is not None:
            _dict['misses'] = self.misses
        if hasattr(self, 'keys') and self.keys is not None:
            _dict['keys'] = self.keys
        if hasattr(self, 'cache_size') and self.cache_size is not None:
            _dict['cache_size'] = self.cache_size
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CacheData object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CacheData') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CacheData') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CacheFlushResponse():
    """
    CacheFlushResponse.

    :attr str message: (optional) Response message. "ok" indicates the api completed
          successfully.
    :attr List[str] flushed: (optional) The name of the caches that were cleared.
    """

    def __init__(self,
                 *,
                 message: str = None,
                 flushed: List[str] = None) -> None:
        """
        Initialize a CacheFlushResponse object.

        :param str message: (optional) Response message. "ok" indicates the api
               completed successfully.
        :param List[str] flushed: (optional) The name of the caches that were
               cleared.
        """
        self.message = message
        self.flushed = flushed

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CacheFlushResponse':
        """Initialize a CacheFlushResponse object from a json dictionary."""
        args = {}
        if 'message' in _dict:
            args['message'] = _dict.get('message')
        if 'flushed' in _dict:
            args['flushed'] = _dict.get('flushed')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CacheFlushResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'message') and self.message is not None:
            _dict['message'] = self.message
        if hasattr(self, 'flushed') and self.flushed is not None:
            _dict['flushed'] = self.flushed
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CacheFlushResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CacheFlushResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CacheFlushResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class FlushedEnum(str, Enum):
        """
        flushed.
        """
        COUCH_CACHE = 'couch_cache'
        IAM_CACHE = 'iam_cache'
        PROXY_CACHE = 'proxy_cache'
        SESSION_CACHE = 'session_cache'


class ConfigCACfgIdentities():
    """
    ConfigCACfgIdentities.

    :attr float passwordattempts: The maximum number of incorrect password attempts
          allowed per identity.
    :attr bool allowremove: (optional) Set to `true` to allow deletion of
          identities. Defaults `false`.
    """

    def __init__(self,
                 passwordattempts: float,
                 *,
                 allowremove: bool = None) -> None:
        """
        Initialize a ConfigCACfgIdentities object.

        :param float passwordattempts: The maximum number of incorrect password
               attempts allowed per identity.
        :param bool allowremove: (optional) Set to `true` to allow deletion of
               identities. Defaults `false`.
        """
        self.passwordattempts = passwordattempts
        self.allowremove = allowremove

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCACfgIdentities':
        """Initialize a ConfigCACfgIdentities object from a json dictionary."""
        args = {}
        if 'passwordattempts' in _dict:
            args['passwordattempts'] = _dict.get('passwordattempts')
        else:
            raise ValueError('Required property \'passwordattempts\' not present in ConfigCACfgIdentities JSON')
        if 'allowremove' in _dict:
            args['allowremove'] = _dict.get('allowremove')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCACfgIdentities object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'passwordattempts') and self.passwordattempts is not None:
            _dict['passwordattempts'] = self.passwordattempts
        if hasattr(self, 'allowremove') and self.allowremove is not None:
            _dict['allowremove'] = self.allowremove
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCACfgIdentities object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCACfgIdentities') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCACfgIdentities') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCACreate():
    """
    ConfigCACreate.

    :attr ConfigCACors cors: (optional)
    :attr bool debug: (optional) Enable debug to debug the CA.
    :attr float crlsizelimit: (optional) Max size of an acceptable CRL in bytes.
    :attr ConfigCATls tls: (optional)
    :attr ConfigCACa ca: (optional)
    :attr ConfigCACrl crl: (optional)
    :attr ConfigCARegistry registry:
    :attr ConfigCADb db: (optional)
    :attr ConfigCAAffiliations affiliations: (optional) Set the keys to the desired
          affiliation parent names. The keys 'org1' and 'org2' are examples.
    :attr ConfigCACsr csr: (optional)
    :attr ConfigCAIdemix idemix: (optional)
    :attr Bccsp bccsp: (optional) Configures the Blockchain Crypto Service Providers
          (bccsp).
    :attr ConfigCAIntermediate intermediate: (optional)
    :attr ConfigCACfg cfg: (optional)
    :attr Metrics metrics: (optional)
    :attr ConfigCASigning signing: (optional)
    """

    def __init__(self,
                 registry: 'ConfigCARegistry',
                 *,
                 cors: 'ConfigCACors' = None,
                 debug: bool = None,
                 crlsizelimit: float = None,
                 tls: 'ConfigCATls' = None,
                 ca: 'ConfigCACa' = None,
                 crl: 'ConfigCACrl' = None,
                 db: 'ConfigCADb' = None,
                 affiliations: 'ConfigCAAffiliations' = None,
                 csr: 'ConfigCACsr' = None,
                 idemix: 'ConfigCAIdemix' = None,
                 bccsp: 'Bccsp' = None,
                 intermediate: 'ConfigCAIntermediate' = None,
                 cfg: 'ConfigCACfg' = None,
                 metrics: 'Metrics' = None,
                 signing: 'ConfigCASigning' = None) -> None:
        """
        Initialize a ConfigCACreate object.

        :param ConfigCARegistry registry:
        :param ConfigCACors cors: (optional)
        :param bool debug: (optional) Enable debug to debug the CA.
        :param float crlsizelimit: (optional) Max size of an acceptable CRL in
               bytes.
        :param ConfigCATls tls: (optional)
        :param ConfigCACa ca: (optional)
        :param ConfigCACrl crl: (optional)
        :param ConfigCADb db: (optional)
        :param ConfigCAAffiliations affiliations: (optional) Set the keys to the
               desired affiliation parent names. The keys 'org1' and 'org2' are examples.
        :param ConfigCACsr csr: (optional)
        :param ConfigCAIdemix idemix: (optional)
        :param Bccsp bccsp: (optional) Configures the Blockchain Crypto Service
               Providers (bccsp).
        :param ConfigCAIntermediate intermediate: (optional)
        :param ConfigCACfg cfg: (optional)
        :param Metrics metrics: (optional)
        :param ConfigCASigning signing: (optional)
        """
        self.cors = cors
        self.debug = debug
        self.crlsizelimit = crlsizelimit
        self.tls = tls
        self.ca = ca
        self.crl = crl
        self.registry = registry
        self.db = db
        self.affiliations = affiliations
        self.csr = csr
        self.idemix = idemix
        self.bccsp = bccsp
        self.intermediate = intermediate
        self.cfg = cfg
        self.metrics = metrics
        self.signing = signing

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCACreate':
        """Initialize a ConfigCACreate object from a json dictionary."""
        args = {}
        if 'cors' in _dict:
            args['cors'] = ConfigCACors.from_dict(_dict.get('cors'))
        if 'debug' in _dict:
            args['debug'] = _dict.get('debug')
        if 'crlsizelimit' in _dict:
            args['crlsizelimit'] = _dict.get('crlsizelimit')
        if 'tls' in _dict:
            args['tls'] = ConfigCATls.from_dict(_dict.get('tls'))
        if 'ca' in _dict:
            args['ca'] = ConfigCACa.from_dict(_dict.get('ca'))
        if 'crl' in _dict:
            args['crl'] = ConfigCACrl.from_dict(_dict.get('crl'))
        if 'registry' in _dict:
            args['registry'] = ConfigCARegistry.from_dict(_dict.get('registry'))
        else:
            raise ValueError('Required property \'registry\' not present in ConfigCACreate JSON')
        if 'db' in _dict:
            args['db'] = ConfigCADb.from_dict(_dict.get('db'))
        if 'affiliations' in _dict:
            args['affiliations'] = ConfigCAAffiliations.from_dict(_dict.get('affiliations'))
        if 'csr' in _dict:
            args['csr'] = ConfigCACsr.from_dict(_dict.get('csr'))
        if 'idemix' in _dict:
            args['idemix'] = ConfigCAIdemix.from_dict(_dict.get('idemix'))
        if 'BCCSP' in _dict:
            args['bccsp'] = Bccsp.from_dict(_dict.get('BCCSP'))
        if 'intermediate' in _dict:
            args['intermediate'] = ConfigCAIntermediate.from_dict(_dict.get('intermediate'))
        if 'cfg' in _dict:
            args['cfg'] = ConfigCACfg.from_dict(_dict.get('cfg'))
        if 'metrics' in _dict:
            args['metrics'] = Metrics.from_dict(_dict.get('metrics'))
        if 'signing' in _dict:
            args['signing'] = ConfigCASigning.from_dict(_dict.get('signing'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCACreate object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'cors') and self.cors is not None:
            _dict['cors'] = self.cors.to_dict()
        if hasattr(self, 'debug') and self.debug is not None:
            _dict['debug'] = self.debug
        if hasattr(self, 'crlsizelimit') and self.crlsizelimit is not None:
            _dict['crlsizelimit'] = self.crlsizelimit
        if hasattr(self, 'tls') and self.tls is not None:
            _dict['tls'] = self.tls.to_dict()
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        if hasattr(self, 'crl') and self.crl is not None:
            _dict['crl'] = self.crl.to_dict()
        if hasattr(self, 'registry') and self.registry is not None:
            _dict['registry'] = self.registry.to_dict()
        if hasattr(self, 'db') and self.db is not None:
            _dict['db'] = self.db.to_dict()
        if hasattr(self, 'affiliations') and self.affiliations is not None:
            _dict['affiliations'] = self.affiliations.to_dict()
        if hasattr(self, 'csr') and self.csr is not None:
            _dict['csr'] = self.csr.to_dict()
        if hasattr(self, 'idemix') and self.idemix is not None:
            _dict['idemix'] = self.idemix.to_dict()
        if hasattr(self, 'bccsp') and self.bccsp is not None:
            _dict['BCCSP'] = self.bccsp.to_dict()
        if hasattr(self, 'intermediate') and self.intermediate is not None:
            _dict['intermediate'] = self.intermediate.to_dict()
        if hasattr(self, 'cfg') and self.cfg is not None:
            _dict['cfg'] = self.cfg.to_dict()
        if hasattr(self, 'metrics') and self.metrics is not None:
            _dict['metrics'] = self.metrics.to_dict()
        if hasattr(self, 'signing') and self.signing is not None:
            _dict['signing'] = self.signing.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCACreate object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCACreate') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCACreate') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCACsrCa():
    """
    ConfigCACsrCa.

    :attr str expiry: (optional) The expiration for the root CA certificate.
    :attr float pathlength: (optional) The pathlength field is used to limit CA
          certificate hierarchy. 0 means that the CA cannot issue CA certs, only entity
          certificates. 1 means that the CA can issue both.
    """

    def __init__(self,
                 *,
                 expiry: str = None,
                 pathlength: float = None) -> None:
        """
        Initialize a ConfigCACsrCa object.

        :param str expiry: (optional) The expiration for the root CA certificate.
        :param float pathlength: (optional) The pathlength field is used to limit
               CA certificate hierarchy. 0 means that the CA cannot issue CA certs, only
               entity certificates. 1 means that the CA can issue both.
        """
        self.expiry = expiry
        self.pathlength = pathlength

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCACsrCa':
        """Initialize a ConfigCACsrCa object from a json dictionary."""
        args = {}
        if 'expiry' in _dict:
            args['expiry'] = _dict.get('expiry')
        if 'pathlength' in _dict:
            args['pathlength'] = _dict.get('pathlength')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCACsrCa object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'expiry') and self.expiry is not None:
            _dict['expiry'] = self.expiry
        if hasattr(self, 'pathlength') and self.pathlength is not None:
            _dict['pathlength'] = self.pathlength
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCACsrCa object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCACsrCa') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCACsrCa') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCACsrKeyrequest():
    """
    ConfigCACsrKeyrequest.

    :attr str algo: The algorithm to use for CSRs.
    :attr float size: The size of the key for CSRs.
    """

    def __init__(self,
                 algo: str,
                 size: float) -> None:
        """
        Initialize a ConfigCACsrKeyrequest object.

        :param str algo: The algorithm to use for CSRs.
        :param float size: The size of the key for CSRs.
        """
        self.algo = algo
        self.size = size

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCACsrKeyrequest':
        """Initialize a ConfigCACsrKeyrequest object from a json dictionary."""
        args = {}
        if 'algo' in _dict:
            args['algo'] = _dict.get('algo')
        else:
            raise ValueError('Required property \'algo\' not present in ConfigCACsrKeyrequest JSON')
        if 'size' in _dict:
            args['size'] = _dict.get('size')
        else:
            raise ValueError('Required property \'size\' not present in ConfigCACsrKeyrequest JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCACsrKeyrequest object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'algo') and self.algo is not None:
            _dict['algo'] = self.algo
        if hasattr(self, 'size') and self.size is not None:
            _dict['size'] = self.size
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCACsrKeyrequest object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCACsrKeyrequest') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCACsrKeyrequest') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCACsrNamesItem():
    """
    ConfigCACsrNamesItem.

    :attr str c:
    :attr str st:
    :attr str l: (optional)
    :attr str o:
    :attr str ou: (optional)
    """

    def __init__(self,
                 c: str,
                 st: str,
                 o: str,
                 *,
                 l: str = None,
                 ou: str = None) -> None:
        """
        Initialize a ConfigCACsrNamesItem object.

        :param str c:
        :param str st:
        :param str o:
        :param str l: (optional)
        :param str ou: (optional)
        """
        self.c = c
        self.st = st
        self.l = l
        self.o = o
        self.ou = ou

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCACsrNamesItem':
        """Initialize a ConfigCACsrNamesItem object from a json dictionary."""
        args = {}
        if 'C' in _dict:
            args['c'] = _dict.get('C')
        else:
            raise ValueError('Required property \'C\' not present in ConfigCACsrNamesItem JSON')
        if 'ST' in _dict:
            args['st'] = _dict.get('ST')
        else:
            raise ValueError('Required property \'ST\' not present in ConfigCACsrNamesItem JSON')
        if 'L' in _dict:
            args['l'] = _dict.get('L')
        if 'O' in _dict:
            args['o'] = _dict.get('O')
        else:
            raise ValueError('Required property \'O\' not present in ConfigCACsrNamesItem JSON')
        if 'OU' in _dict:
            args['ou'] = _dict.get('OU')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCACsrNamesItem object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'c') and self.c is not None:
            _dict['C'] = self.c
        if hasattr(self, 'st') and self.st is not None:
            _dict['ST'] = self.st
        if hasattr(self, 'l') and self.l is not None:
            _dict['L'] = self.l
        if hasattr(self, 'o') and self.o is not None:
            _dict['O'] = self.o
        if hasattr(self, 'ou') and self.ou is not None:
            _dict['OU'] = self.ou
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCACsrNamesItem object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCACsrNamesItem') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCACsrNamesItem') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCADbTls():
    """
    ConfigCADbTls.

    :attr List[str] certfiles: (optional)
    :attr ConfigCADbTlsClient client: (optional)
    :attr bool enabled: (optional) Set to true if TLS is to be used between the CA
          and its database, else false.
    """

    def __init__(self,
                 *,
                 certfiles: List[str] = None,
                 client: 'ConfigCADbTlsClient' = None,
                 enabled: bool = None) -> None:
        """
        Initialize a ConfigCADbTls object.

        :param List[str] certfiles: (optional)
        :param ConfigCADbTlsClient client: (optional)
        :param bool enabled: (optional) Set to true if TLS is to be used between
               the CA and its database, else false.
        """
        self.certfiles = certfiles
        self.client = client
        self.enabled = enabled

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCADbTls':
        """Initialize a ConfigCADbTls object from a json dictionary."""
        args = {}
        if 'certfiles' in _dict:
            args['certfiles'] = _dict.get('certfiles')
        if 'client' in _dict:
            args['client'] = ConfigCADbTlsClient.from_dict(_dict.get('client'))
        if 'enabled' in _dict:
            args['enabled'] = _dict.get('enabled')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCADbTls object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'certfiles') and self.certfiles is not None:
            _dict['certfiles'] = self.certfiles
        if hasattr(self, 'client') and self.client is not None:
            _dict['client'] = self.client.to_dict()
        if hasattr(self, 'enabled') and self.enabled is not None:
            _dict['enabled'] = self.enabled
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCADbTls object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCADbTls') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCADbTls') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCADbTlsClient():
    """
    ConfigCADbTlsClient.

    :attr str certfile: The TLS certificate for client TLS as base 64 encoded PEM.
    :attr str keyfile: The TLS private key for client TLS as base 64 encoded PEM.
    """

    def __init__(self,
                 certfile: str,
                 keyfile: str) -> None:
        """
        Initialize a ConfigCADbTlsClient object.

        :param str certfile: The TLS certificate for client TLS as base 64 encoded
               PEM.
        :param str keyfile: The TLS private key for client TLS as base 64 encoded
               PEM.
        """
        self.certfile = certfile
        self.keyfile = keyfile

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCADbTlsClient':
        """Initialize a ConfigCADbTlsClient object from a json dictionary."""
        args = {}
        if 'certfile' in _dict:
            args['certfile'] = _dict.get('certfile')
        else:
            raise ValueError('Required property \'certfile\' not present in ConfigCADbTlsClient JSON')
        if 'keyfile' in _dict:
            args['keyfile'] = _dict.get('keyfile')
        else:
            raise ValueError('Required property \'keyfile\' not present in ConfigCADbTlsClient JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCADbTlsClient object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'certfile') and self.certfile is not None:
            _dict['certfile'] = self.certfile
        if hasattr(self, 'keyfile') and self.keyfile is not None:
            _dict['keyfile'] = self.keyfile
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCADbTlsClient object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCADbTlsClient') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCADbTlsClient') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCAIntermediateEnrollment():
    """
    ConfigCAIntermediateEnrollment.

    :attr str hosts: Hosts to set when issuing the certificate.
    :attr str profile: Name of the signing profile to use when issuing the
          certificate.
    :attr str label: Label to use in HSM operations.
    """

    def __init__(self,
                 hosts: str,
                 profile: str,
                 label: str) -> None:
        """
        Initialize a ConfigCAIntermediateEnrollment object.

        :param str hosts: Hosts to set when issuing the certificate.
        :param str profile: Name of the signing profile to use when issuing the
               certificate.
        :param str label: Label to use in HSM operations.
        """
        self.hosts = hosts
        self.profile = profile
        self.label = label

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCAIntermediateEnrollment':
        """Initialize a ConfigCAIntermediateEnrollment object from a json dictionary."""
        args = {}
        if 'hosts' in _dict:
            args['hosts'] = _dict.get('hosts')
        else:
            raise ValueError('Required property \'hosts\' not present in ConfigCAIntermediateEnrollment JSON')
        if 'profile' in _dict:
            args['profile'] = _dict.get('profile')
        else:
            raise ValueError('Required property \'profile\' not present in ConfigCAIntermediateEnrollment JSON')
        if 'label' in _dict:
            args['label'] = _dict.get('label')
        else:
            raise ValueError('Required property \'label\' not present in ConfigCAIntermediateEnrollment JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCAIntermediateEnrollment object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'hosts') and self.hosts is not None:
            _dict['hosts'] = self.hosts
        if hasattr(self, 'profile') and self.profile is not None:
            _dict['profile'] = self.profile
        if hasattr(self, 'label') and self.label is not None:
            _dict['label'] = self.label
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCAIntermediateEnrollment object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCAIntermediateEnrollment') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCAIntermediateEnrollment') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCAIntermediateParentserver():
    """
    ConfigCAIntermediateParentserver.

    :attr str url: The url of the parent server. Include the protocol, hostname/ip
          and port.
    :attr str caname: The name of the CA to enroll within the server.
    """

    def __init__(self,
                 url: str,
                 caname: str) -> None:
        """
        Initialize a ConfigCAIntermediateParentserver object.

        :param str url: The url of the parent server. Include the protocol,
               hostname/ip and port.
        :param str caname: The name of the CA to enroll within the server.
        """
        self.url = url
        self.caname = caname

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCAIntermediateParentserver':
        """Initialize a ConfigCAIntermediateParentserver object from a json dictionary."""
        args = {}
        if 'url' in _dict:
            args['url'] = _dict.get('url')
        else:
            raise ValueError('Required property \'url\' not present in ConfigCAIntermediateParentserver JSON')
        if 'caname' in _dict:
            args['caname'] = _dict.get('caname')
        else:
            raise ValueError('Required property \'caname\' not present in ConfigCAIntermediateParentserver JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCAIntermediateParentserver object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'url') and self.url is not None:
            _dict['url'] = self.url
        if hasattr(self, 'caname') and self.caname is not None:
            _dict['caname'] = self.caname
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCAIntermediateParentserver object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCAIntermediateParentserver') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCAIntermediateParentserver') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCAIntermediateTls():
    """
    ConfigCAIntermediateTls.

    :attr List[str] certfiles:
    :attr ConfigCAIntermediateTlsClient client: (optional)
    """

    def __init__(self,
                 certfiles: List[str],
                 *,
                 client: 'ConfigCAIntermediateTlsClient' = None) -> None:
        """
        Initialize a ConfigCAIntermediateTls object.

        :param List[str] certfiles:
        :param ConfigCAIntermediateTlsClient client: (optional)
        """
        self.certfiles = certfiles
        self.client = client

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCAIntermediateTls':
        """Initialize a ConfigCAIntermediateTls object from a json dictionary."""
        args = {}
        if 'certfiles' in _dict:
            args['certfiles'] = _dict.get('certfiles')
        else:
            raise ValueError('Required property \'certfiles\' not present in ConfigCAIntermediateTls JSON')
        if 'client' in _dict:
            args['client'] = ConfigCAIntermediateTlsClient.from_dict(_dict.get('client'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCAIntermediateTls object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'certfiles') and self.certfiles is not None:
            _dict['certfiles'] = self.certfiles
        if hasattr(self, 'client') and self.client is not None:
            _dict['client'] = self.client.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCAIntermediateTls object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCAIntermediateTls') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCAIntermediateTls') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCAIntermediateTlsClient():
    """
    ConfigCAIntermediateTlsClient.

    :attr str certfile: The TLS certificate for client TLS as base 64 encoded PEM.
    :attr str keyfile: The TLS private key for client TLS as base 64 encoded PEM.
    """

    def __init__(self,
                 certfile: str,
                 keyfile: str) -> None:
        """
        Initialize a ConfigCAIntermediateTlsClient object.

        :param str certfile: The TLS certificate for client TLS as base 64 encoded
               PEM.
        :param str keyfile: The TLS private key for client TLS as base 64 encoded
               PEM.
        """
        self.certfile = certfile
        self.keyfile = keyfile

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCAIntermediateTlsClient':
        """Initialize a ConfigCAIntermediateTlsClient object from a json dictionary."""
        args = {}
        if 'certfile' in _dict:
            args['certfile'] = _dict.get('certfile')
        else:
            raise ValueError('Required property \'certfile\' not present in ConfigCAIntermediateTlsClient JSON')
        if 'keyfile' in _dict:
            args['keyfile'] = _dict.get('keyfile')
        else:
            raise ValueError('Required property \'keyfile\' not present in ConfigCAIntermediateTlsClient JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCAIntermediateTlsClient object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'certfile') and self.certfile is not None:
            _dict['certfile'] = self.certfile
        if hasattr(self, 'keyfile') and self.keyfile is not None:
            _dict['keyfile'] = self.keyfile
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCAIntermediateTlsClient object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCAIntermediateTlsClient') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCAIntermediateTlsClient') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCARegistryIdentitiesItem():
    """
    ConfigCARegistryIdentitiesItem.

    :attr str name: The ID for the identity, aka enroll id.
    :attr str pass_: The password for the identity, aka enroll secret.
    :attr str type: The type of identity.
    :attr float maxenrollments: (optional) Maximum number of enrollments for id. Set
          -1 for infinite.
    :attr str affiliation: (optional) The affiliation data for the identity.
    :attr IdentityAttrs attrs: (optional)
    """

    def __init__(self,
                 name: str,
                 pass_: str,
                 type: str,
                 *,
                 maxenrollments: float = None,
                 affiliation: str = None,
                 attrs: 'IdentityAttrs' = None) -> None:
        """
        Initialize a ConfigCARegistryIdentitiesItem object.

        :param str name: The ID for the identity, aka enroll id.
        :param str pass_: The password for the identity, aka enroll secret.
        :param str type: The type of identity.
        :param float maxenrollments: (optional) Maximum number of enrollments for
               id. Set -1 for infinite.
        :param str affiliation: (optional) The affiliation data for the identity.
        :param IdentityAttrs attrs: (optional)
        """
        self.name = name
        self.pass_ = pass_
        self.type = type
        self.maxenrollments = maxenrollments
        self.affiliation = affiliation
        self.attrs = attrs

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCARegistryIdentitiesItem':
        """Initialize a ConfigCARegistryIdentitiesItem object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        else:
            raise ValueError('Required property \'name\' not present in ConfigCARegistryIdentitiesItem JSON')
        if 'pass' in _dict:
            args['pass_'] = _dict.get('pass')
        else:
            raise ValueError('Required property \'pass\' not present in ConfigCARegistryIdentitiesItem JSON')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        else:
            raise ValueError('Required property \'type\' not present in ConfigCARegistryIdentitiesItem JSON')
        if 'maxenrollments' in _dict:
            args['maxenrollments'] = _dict.get('maxenrollments')
        if 'affiliation' in _dict:
            args['affiliation'] = _dict.get('affiliation')
        if 'attrs' in _dict:
            args['attrs'] = IdentityAttrs.from_dict(_dict.get('attrs'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCARegistryIdentitiesItem object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'pass_') and self.pass_ is not None:
            _dict['pass'] = self.pass_
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'maxenrollments') and self.maxenrollments is not None:
            _dict['maxenrollments'] = self.maxenrollments
        if hasattr(self, 'affiliation') and self.affiliation is not None:
            _dict['affiliation'] = self.affiliation
        if hasattr(self, 'attrs') and self.attrs is not None:
            _dict['attrs'] = self.attrs.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCARegistryIdentitiesItem object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCARegistryIdentitiesItem') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCARegistryIdentitiesItem') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class TypeEnum(str, Enum):
        """
        The type of identity.
        """
        CLIENT = 'client'
        PEER = 'peer'
        ORDERER = 'orderer'
        USER = 'user'
        ADMIN = 'admin'


class ConfigCASigningDefault():
    """
    ConfigCASigningDefault.

    :attr List[str] usage: (optional)
    :attr str expiry: (optional) Controls the default expiration for signed
          certificates.
    """

    def __init__(self,
                 *,
                 usage: List[str] = None,
                 expiry: str = None) -> None:
        """
        Initialize a ConfigCASigningDefault object.

        :param List[str] usage: (optional)
        :param str expiry: (optional) Controls the default expiration for signed
               certificates.
        """
        self.usage = usage
        self.expiry = expiry

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCASigningDefault':
        """Initialize a ConfigCASigningDefault object from a json dictionary."""
        args = {}
        if 'usage' in _dict:
            args['usage'] = _dict.get('usage')
        if 'expiry' in _dict:
            args['expiry'] = _dict.get('expiry')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCASigningDefault object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'usage') and self.usage is not None:
            _dict['usage'] = self.usage
        if hasattr(self, 'expiry') and self.expiry is not None:
            _dict['expiry'] = self.expiry
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCASigningDefault object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCASigningDefault') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCASigningDefault') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCASigningProfiles():
    """
    ConfigCASigningProfiles.

    :attr ConfigCASigningProfilesCa ca: (optional) Controls attributes of
          intermediate CA certificates.
    :attr ConfigCASigningProfilesTls tls: (optional) Controls attributes of
          intermediate tls CA certificates.
    """

    def __init__(self,
                 *,
                 ca: 'ConfigCASigningProfilesCa' = None,
                 tls: 'ConfigCASigningProfilesTls' = None) -> None:
        """
        Initialize a ConfigCASigningProfiles object.

        :param ConfigCASigningProfilesCa ca: (optional) Controls attributes of
               intermediate CA certificates.
        :param ConfigCASigningProfilesTls tls: (optional) Controls attributes of
               intermediate tls CA certificates.
        """
        self.ca = ca
        self.tls = tls

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCASigningProfiles':
        """Initialize a ConfigCASigningProfiles object from a json dictionary."""
        args = {}
        if 'ca' in _dict:
            args['ca'] = ConfigCASigningProfilesCa.from_dict(_dict.get('ca'))
        if 'tls' in _dict:
            args['tls'] = ConfigCASigningProfilesTls.from_dict(_dict.get('tls'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCASigningProfiles object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        if hasattr(self, 'tls') and self.tls is not None:
            _dict['tls'] = self.tls.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCASigningProfiles object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCASigningProfiles') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCASigningProfiles') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCASigningProfilesCa():
    """
    Controls attributes of intermediate CA certificates.

    :attr List[str] usage: (optional)
    :attr str expiry: (optional) Controls the expiration for signed intermediate CA
          certificates.
    :attr ConfigCASigningProfilesCaCaconstraint caconstraint: (optional)
    """

    def __init__(self,
                 *,
                 usage: List[str] = None,
                 expiry: str = None,
                 caconstraint: 'ConfigCASigningProfilesCaCaconstraint' = None) -> None:
        """
        Initialize a ConfigCASigningProfilesCa object.

        :param List[str] usage: (optional)
        :param str expiry: (optional) Controls the expiration for signed
               intermediate CA certificates.
        :param ConfigCASigningProfilesCaCaconstraint caconstraint: (optional)
        """
        self.usage = usage
        self.expiry = expiry
        self.caconstraint = caconstraint

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCASigningProfilesCa':
        """Initialize a ConfigCASigningProfilesCa object from a json dictionary."""
        args = {}
        if 'usage' in _dict:
            args['usage'] = _dict.get('usage')
        if 'expiry' in _dict:
            args['expiry'] = _dict.get('expiry')
        if 'caconstraint' in _dict:
            args['caconstraint'] = ConfigCASigningProfilesCaCaconstraint.from_dict(_dict.get('caconstraint'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCASigningProfilesCa object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'usage') and self.usage is not None:
            _dict['usage'] = self.usage
        if hasattr(self, 'expiry') and self.expiry is not None:
            _dict['expiry'] = self.expiry
        if hasattr(self, 'caconstraint') and self.caconstraint is not None:
            _dict['caconstraint'] = self.caconstraint.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCASigningProfilesCa object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCASigningProfilesCa') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCASigningProfilesCa') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCASigningProfilesCaCaconstraint():
    """
    ConfigCASigningProfilesCaCaconstraint.

    :attr bool isca: (optional) Indicates if this certificate is for a CA.
    :attr float maxpathlen: (optional) A value of 0 indicates that this intermediate
          CA cannot issue other intermediate CA certificates.
    :attr bool maxpathlenzero: (optional) To enforce a `maxpathlen` of 0, this field
          must be `true`. If `maxpathlen` should be ignored or if it is greater than 0 set
          this to `false`.
    """

    def __init__(self,
                 *,
                 isca: bool = None,
                 maxpathlen: float = None,
                 maxpathlenzero: bool = None) -> None:
        """
        Initialize a ConfigCASigningProfilesCaCaconstraint object.

        :param bool isca: (optional) Indicates if this certificate is for a CA.
        :param float maxpathlen: (optional) A value of 0 indicates that this
               intermediate CA cannot issue other intermediate CA certificates.
        :param bool maxpathlenzero: (optional) To enforce a `maxpathlen` of 0, this
               field must be `true`. If `maxpathlen` should be ignored or if it is greater
               than 0 set this to `false`.
        """
        self.isca = isca
        self.maxpathlen = maxpathlen
        self.maxpathlenzero = maxpathlenzero

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCASigningProfilesCaCaconstraint':
        """Initialize a ConfigCASigningProfilesCaCaconstraint object from a json dictionary."""
        args = {}
        if 'isca' in _dict:
            args['isca'] = _dict.get('isca')
        if 'maxpathlen' in _dict:
            args['maxpathlen'] = _dict.get('maxpathlen')
        if 'maxpathlenzero' in _dict:
            args['maxpathlenzero'] = _dict.get('maxpathlenzero')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCASigningProfilesCaCaconstraint object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'isca') and self.isca is not None:
            _dict['isca'] = self.isca
        if hasattr(self, 'maxpathlen') and self.maxpathlen is not None:
            _dict['maxpathlen'] = self.maxpathlen
        if hasattr(self, 'maxpathlenzero') and self.maxpathlenzero is not None:
            _dict['maxpathlenzero'] = self.maxpathlenzero
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCASigningProfilesCaCaconstraint object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCASigningProfilesCaCaconstraint') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCASigningProfilesCaCaconstraint') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCASigningProfilesTls():
    """
    Controls attributes of intermediate tls CA certificates.

    :attr List[str] usage: (optional)
    :attr str expiry: (optional) Controls the expiration for signed tls intermediate
          CA certificates.
    """

    def __init__(self,
                 *,
                 usage: List[str] = None,
                 expiry: str = None) -> None:
        """
        Initialize a ConfigCASigningProfilesTls object.

        :param List[str] usage: (optional)
        :param str expiry: (optional) Controls the expiration for signed tls
               intermediate CA certificates.
        """
        self.usage = usage
        self.expiry = expiry

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCASigningProfilesTls':
        """Initialize a ConfigCASigningProfilesTls object from a json dictionary."""
        args = {}
        if 'usage' in _dict:
            args['usage'] = _dict.get('usage')
        if 'expiry' in _dict:
            args['expiry'] = _dict.get('expiry')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCASigningProfilesTls object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'usage') and self.usage is not None:
            _dict['usage'] = self.usage
        if hasattr(self, 'expiry') and self.expiry is not None:
            _dict['expiry'] = self.expiry
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCASigningProfilesTls object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCASigningProfilesTls') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCASigningProfilesTls') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCATlsClientauth():
    """
    ConfigCATlsClientauth.

    :attr str type:
    :attr List[str] certfiles:
    """

    def __init__(self,
                 type: str,
                 certfiles: List[str]) -> None:
        """
        Initialize a ConfigCATlsClientauth object.

        :param str type:
        :param List[str] certfiles:
        """
        self.type = type
        self.certfiles = certfiles

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCATlsClientauth':
        """Initialize a ConfigCATlsClientauth object from a json dictionary."""
        args = {}
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        else:
            raise ValueError('Required property \'type\' not present in ConfigCATlsClientauth JSON')
        if 'certfiles' in _dict:
            args['certfiles'] = _dict.get('certfiles')
        else:
            raise ValueError('Required property \'certfiles\' not present in ConfigCATlsClientauth JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCATlsClientauth object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'certfiles') and self.certfiles is not None:
            _dict['certfiles'] = self.certfiles
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCATlsClientauth object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCATlsClientauth') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCATlsClientauth') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCAUpdate():
    """
    ConfigCAUpdate.

    :attr ConfigCACors cors: (optional)
    :attr bool debug: (optional) Enable debug to debug the CA.
    :attr float crlsizelimit: (optional) Max size of an acceptable CRL in bytes.
    :attr ConfigCATls tls: (optional)
    :attr ConfigCACa ca: (optional)
    :attr ConfigCACrl crl: (optional)
    :attr ConfigCARegistry registry: (optional)
    :attr ConfigCADb db: (optional)
    :attr ConfigCAAffiliations affiliations: (optional) Set the keys to the desired
          affiliation parent names. The keys 'org1' and 'org2' are examples.
    :attr ConfigCACsr csr: (optional)
    :attr ConfigCAIdemix idemix: (optional)
    :attr Bccsp bccsp: (optional) Configures the Blockchain Crypto Service Providers
          (bccsp).
    :attr ConfigCAIntermediate intermediate: (optional)
    :attr ConfigCACfg cfg: (optional)
    :attr Metrics metrics: (optional)
    """

    def __init__(self,
                 *,
                 cors: 'ConfigCACors' = None,
                 debug: bool = None,
                 crlsizelimit: float = None,
                 tls: 'ConfigCATls' = None,
                 ca: 'ConfigCACa' = None,
                 crl: 'ConfigCACrl' = None,
                 registry: 'ConfigCARegistry' = None,
                 db: 'ConfigCADb' = None,
                 affiliations: 'ConfigCAAffiliations' = None,
                 csr: 'ConfigCACsr' = None,
                 idemix: 'ConfigCAIdemix' = None,
                 bccsp: 'Bccsp' = None,
                 intermediate: 'ConfigCAIntermediate' = None,
                 cfg: 'ConfigCACfg' = None,
                 metrics: 'Metrics' = None) -> None:
        """
        Initialize a ConfigCAUpdate object.

        :param ConfigCACors cors: (optional)
        :param bool debug: (optional) Enable debug to debug the CA.
        :param float crlsizelimit: (optional) Max size of an acceptable CRL in
               bytes.
        :param ConfigCATls tls: (optional)
        :param ConfigCACa ca: (optional)
        :param ConfigCACrl crl: (optional)
        :param ConfigCARegistry registry: (optional)
        :param ConfigCADb db: (optional)
        :param ConfigCAAffiliations affiliations: (optional) Set the keys to the
               desired affiliation parent names. The keys 'org1' and 'org2' are examples.
        :param ConfigCACsr csr: (optional)
        :param ConfigCAIdemix idemix: (optional)
        :param Bccsp bccsp: (optional) Configures the Blockchain Crypto Service
               Providers (bccsp).
        :param ConfigCAIntermediate intermediate: (optional)
        :param ConfigCACfg cfg: (optional)
        :param Metrics metrics: (optional)
        """
        self.cors = cors
        self.debug = debug
        self.crlsizelimit = crlsizelimit
        self.tls = tls
        self.ca = ca
        self.crl = crl
        self.registry = registry
        self.db = db
        self.affiliations = affiliations
        self.csr = csr
        self.idemix = idemix
        self.bccsp = bccsp
        self.intermediate = intermediate
        self.cfg = cfg
        self.metrics = metrics

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCAUpdate':
        """Initialize a ConfigCAUpdate object from a json dictionary."""
        args = {}
        if 'cors' in _dict:
            args['cors'] = ConfigCACors.from_dict(_dict.get('cors'))
        if 'debug' in _dict:
            args['debug'] = _dict.get('debug')
        if 'crlsizelimit' in _dict:
            args['crlsizelimit'] = _dict.get('crlsizelimit')
        if 'tls' in _dict:
            args['tls'] = ConfigCATls.from_dict(_dict.get('tls'))
        if 'ca' in _dict:
            args['ca'] = ConfigCACa.from_dict(_dict.get('ca'))
        if 'crl' in _dict:
            args['crl'] = ConfigCACrl.from_dict(_dict.get('crl'))
        if 'registry' in _dict:
            args['registry'] = ConfigCARegistry.from_dict(_dict.get('registry'))
        if 'db' in _dict:
            args['db'] = ConfigCADb.from_dict(_dict.get('db'))
        if 'affiliations' in _dict:
            args['affiliations'] = ConfigCAAffiliations.from_dict(_dict.get('affiliations'))
        if 'csr' in _dict:
            args['csr'] = ConfigCACsr.from_dict(_dict.get('csr'))
        if 'idemix' in _dict:
            args['idemix'] = ConfigCAIdemix.from_dict(_dict.get('idemix'))
        if 'BCCSP' in _dict:
            args['bccsp'] = Bccsp.from_dict(_dict.get('BCCSP'))
        if 'intermediate' in _dict:
            args['intermediate'] = ConfigCAIntermediate.from_dict(_dict.get('intermediate'))
        if 'cfg' in _dict:
            args['cfg'] = ConfigCACfg.from_dict(_dict.get('cfg'))
        if 'metrics' in _dict:
            args['metrics'] = Metrics.from_dict(_dict.get('metrics'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCAUpdate object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'cors') and self.cors is not None:
            _dict['cors'] = self.cors.to_dict()
        if hasattr(self, 'debug') and self.debug is not None:
            _dict['debug'] = self.debug
        if hasattr(self, 'crlsizelimit') and self.crlsizelimit is not None:
            _dict['crlsizelimit'] = self.crlsizelimit
        if hasattr(self, 'tls') and self.tls is not None:
            _dict['tls'] = self.tls.to_dict()
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        if hasattr(self, 'crl') and self.crl is not None:
            _dict['crl'] = self.crl.to_dict()
        if hasattr(self, 'registry') and self.registry is not None:
            _dict['registry'] = self.registry.to_dict()
        if hasattr(self, 'db') and self.db is not None:
            _dict['db'] = self.db.to_dict()
        if hasattr(self, 'affiliations') and self.affiliations is not None:
            _dict['affiliations'] = self.affiliations.to_dict()
        if hasattr(self, 'csr') and self.csr is not None:
            _dict['csr'] = self.csr.to_dict()
        if hasattr(self, 'idemix') and self.idemix is not None:
            _dict['idemix'] = self.idemix.to_dict()
        if hasattr(self, 'bccsp') and self.bccsp is not None:
            _dict['BCCSP'] = self.bccsp.to_dict()
        if hasattr(self, 'intermediate') and self.intermediate is not None:
            _dict['intermediate'] = self.intermediate.to_dict()
        if hasattr(self, 'cfg') and self.cfg is not None:
            _dict['cfg'] = self.cfg.to_dict()
        if hasattr(self, 'metrics') and self.metrics is not None:
            _dict['metrics'] = self.metrics.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCAUpdate object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCAUpdate') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCAUpdate') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCAAffiliations():
    """
    Set the keys to the desired affiliation parent names. The keys 'org1' and 'org2' are
    examples.

    :attr List[str] org1: (optional)
    :attr List[str] org2: (optional)
    """

    # The set of defined properties for the class
    _properties = frozenset(['org1', 'org2'])

    def __init__(self,
                 *,
                 org1: List[str] = None,
                 org2: List[str] = None,
                 **kwargs) -> None:
        """
        Initialize a ConfigCAAffiliations object.

        :param List[str] org1: (optional)
        :param List[str] org2: (optional)
        :param **kwargs: (optional) Any additional properties.
        """
        self.org1 = org1
        self.org2 = org2
        for _key, _value in kwargs.items():
            setattr(self, _key, _value)

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCAAffiliations':
        """Initialize a ConfigCAAffiliations object from a json dictionary."""
        args = {}
        if 'org1' in _dict:
            args['org1'] = _dict.get('org1')
        if 'org2' in _dict:
            args['org2'] = _dict.get('org2')
        args.update({k:v for (k, v) in _dict.items() if k not in cls._properties})
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCAAffiliations object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'org1') and self.org1 is not None:
            _dict['org1'] = self.org1
        if hasattr(self, 'org2') and self.org2 is not None:
            _dict['org2'] = self.org2
        for _key in [k for k in vars(self).keys() if k not in ConfigCAAffiliations._properties]:
            if getattr(self, _key, None) is not None:
                _dict[_key] = getattr(self, _key)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCAAffiliations object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCAAffiliations') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCAAffiliations') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCACa():
    """
    ConfigCACa.

    :attr str keyfile: (optional) The CA's private key as base 64 encoded PEM.
    :attr str certfile: (optional) The CA's certificate as base 64 encoded PEM.
    :attr str chainfile: (optional) The CA's certificate chain as base 64 encoded
          PEM.
    """

    def __init__(self,
                 *,
                 keyfile: str = None,
                 certfile: str = None,
                 chainfile: str = None) -> None:
        """
        Initialize a ConfigCACa object.

        :param str keyfile: (optional) The CA's private key as base 64 encoded PEM.
        :param str certfile: (optional) The CA's certificate as base 64 encoded
               PEM.
        :param str chainfile: (optional) The CA's certificate chain as base 64
               encoded PEM.
        """
        self.keyfile = keyfile
        self.certfile = certfile
        self.chainfile = chainfile

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCACa':
        """Initialize a ConfigCACa object from a json dictionary."""
        args = {}
        if 'keyfile' in _dict:
            args['keyfile'] = _dict.get('keyfile')
        if 'certfile' in _dict:
            args['certfile'] = _dict.get('certfile')
        if 'chainfile' in _dict:
            args['chainfile'] = _dict.get('chainfile')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCACa object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'keyfile') and self.keyfile is not None:
            _dict['keyfile'] = self.keyfile
        if hasattr(self, 'certfile') and self.certfile is not None:
            _dict['certfile'] = self.certfile
        if hasattr(self, 'chainfile') and self.chainfile is not None:
            _dict['chainfile'] = self.chainfile
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCACa object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCACa') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCACa') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCACfg():
    """
    ConfigCACfg.

    :attr ConfigCACfgIdentities identities:
    """

    def __init__(self,
                 identities: 'ConfigCACfgIdentities') -> None:
        """
        Initialize a ConfigCACfg object.

        :param ConfigCACfgIdentities identities:
        """
        self.identities = identities

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCACfg':
        """Initialize a ConfigCACfg object from a json dictionary."""
        args = {}
        if 'identities' in _dict:
            args['identities'] = ConfigCACfgIdentities.from_dict(_dict.get('identities'))
        else:
            raise ValueError('Required property \'identities\' not present in ConfigCACfg JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCACfg object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'identities') and self.identities is not None:
            _dict['identities'] = self.identities.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCACfg object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCACfg') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCACfg') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCACors():
    """
    ConfigCACors.

    :attr bool enabled:
    :attr List[str] origins:
    """

    def __init__(self,
                 enabled: bool,
                 origins: List[str]) -> None:
        """
        Initialize a ConfigCACors object.

        :param bool enabled:
        :param List[str] origins:
        """
        self.enabled = enabled
        self.origins = origins

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCACors':
        """Initialize a ConfigCACors object from a json dictionary."""
        args = {}
        if 'enabled' in _dict:
            args['enabled'] = _dict.get('enabled')
        else:
            raise ValueError('Required property \'enabled\' not present in ConfigCACors JSON')
        if 'origins' in _dict:
            args['origins'] = _dict.get('origins')
        else:
            raise ValueError('Required property \'origins\' not present in ConfigCACors JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCACors object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'enabled') and self.enabled is not None:
            _dict['enabled'] = self.enabled
        if hasattr(self, 'origins') and self.origins is not None:
            _dict['origins'] = self.origins
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCACors object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCACors') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCACors') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCACrl():
    """
    ConfigCACrl.

    :attr str expiry: Expiration of the CRL (Certificate Revocation List) generated
          by the 'gencrl' requests.
    """

    def __init__(self,
                 expiry: str) -> None:
        """
        Initialize a ConfigCACrl object.

        :param str expiry: Expiration of the CRL (Certificate Revocation List)
               generated by the 'gencrl' requests.
        """
        self.expiry = expiry

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCACrl':
        """Initialize a ConfigCACrl object from a json dictionary."""
        args = {}
        if 'expiry' in _dict:
            args['expiry'] = _dict.get('expiry')
        else:
            raise ValueError('Required property \'expiry\' not present in ConfigCACrl JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCACrl object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'expiry') and self.expiry is not None:
            _dict['expiry'] = self.expiry
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCACrl object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCACrl') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCACrl') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCACsr():
    """
    ConfigCACsr.

    :attr str cn: The Common Name for the CSRs.
    :attr ConfigCACsrKeyrequest keyrequest: (optional)
    :attr List[ConfigCACsrNamesItem] names:
    :attr List[str] hosts: (optional)
    :attr ConfigCACsrCa ca:
    """

    def __init__(self,
                 cn: str,
                 names: List['ConfigCACsrNamesItem'],
                 ca: 'ConfigCACsrCa',
                 *,
                 keyrequest: 'ConfigCACsrKeyrequest' = None,
                 hosts: List[str] = None) -> None:
        """
        Initialize a ConfigCACsr object.

        :param str cn: The Common Name for the CSRs.
        :param List[ConfigCACsrNamesItem] names:
        :param ConfigCACsrCa ca:
        :param ConfigCACsrKeyrequest keyrequest: (optional)
        :param List[str] hosts: (optional)
        """
        self.cn = cn
        self.keyrequest = keyrequest
        self.names = names
        self.hosts = hosts
        self.ca = ca

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCACsr':
        """Initialize a ConfigCACsr object from a json dictionary."""
        args = {}
        if 'cn' in _dict:
            args['cn'] = _dict.get('cn')
        else:
            raise ValueError('Required property \'cn\' not present in ConfigCACsr JSON')
        if 'keyrequest' in _dict:
            args['keyrequest'] = ConfigCACsrKeyrequest.from_dict(_dict.get('keyrequest'))
        if 'names' in _dict:
            args['names'] = [ConfigCACsrNamesItem.from_dict(x) for x in _dict.get('names')]
        else:
            raise ValueError('Required property \'names\' not present in ConfigCACsr JSON')
        if 'hosts' in _dict:
            args['hosts'] = _dict.get('hosts')
        if 'ca' in _dict:
            args['ca'] = ConfigCACsrCa.from_dict(_dict.get('ca'))
        else:
            raise ValueError('Required property \'ca\' not present in ConfigCACsr JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCACsr object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'cn') and self.cn is not None:
            _dict['cn'] = self.cn
        if hasattr(self, 'keyrequest') and self.keyrequest is not None:
            _dict['keyrequest'] = self.keyrequest.to_dict()
        if hasattr(self, 'names') and self.names is not None:
            _dict['names'] = [x.to_dict() for x in self.names]
        if hasattr(self, 'hosts') and self.hosts is not None:
            _dict['hosts'] = self.hosts
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCACsr object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCACsr') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCACsr') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCADb():
    """
    ConfigCADb.

    :attr str type: The type of database. Either 'sqlite3', 'postgres', 'mysql'.
          Defaults 'sqlite3'.
    :attr str datasource: Build this string - "host=\<hostname> port=\<port>
          user=\<username> password=\<password> dbname=ibmclouddb sslmode=verify-full".
    :attr ConfigCADbTls tls: (optional)
    """

    def __init__(self,
                 type: str,
                 datasource: str,
                 *,
                 tls: 'ConfigCADbTls' = None) -> None:
        """
        Initialize a ConfigCADb object.

        :param str type: The type of database. Either 'sqlite3', 'postgres',
               'mysql'. Defaults 'sqlite3'.
        :param str datasource: Build this string - "host=\<hostname> port=\<port>
               user=\<username> password=\<password> dbname=ibmclouddb
               sslmode=verify-full".
        :param ConfigCADbTls tls: (optional)
        """
        self.type = type
        self.datasource = datasource
        self.tls = tls

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCADb':
        """Initialize a ConfigCADb object from a json dictionary."""
        args = {}
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        else:
            raise ValueError('Required property \'type\' not present in ConfigCADb JSON')
        if 'datasource' in _dict:
            args['datasource'] = _dict.get('datasource')
        else:
            raise ValueError('Required property \'datasource\' not present in ConfigCADb JSON')
        if 'tls' in _dict:
            args['tls'] = ConfigCADbTls.from_dict(_dict.get('tls'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCADb object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'datasource') and self.datasource is not None:
            _dict['datasource'] = self.datasource
        if hasattr(self, 'tls') and self.tls is not None:
            _dict['tls'] = self.tls.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCADb object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCADb') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCADb') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class TypeEnum(str, Enum):
        """
        The type of database. Either 'sqlite3', 'postgres', 'mysql'. Defaults 'sqlite3'.
        """
        SQLITE3 = 'sqlite3'
        POSTGRES = 'postgres'
        MYSQL = 'mysql'


class ConfigCAIdemix():
    """
    ConfigCAIdemix.

    :attr float rhpoolsize: Specifies the revocation pool size.
    :attr str nonceexpiration: Specifies the expiration for the nonces.
    :attr str noncesweepinterval: Specifies frequency at which expired nonces are
          removed from data store.
    """

    def __init__(self,
                 rhpoolsize: float,
                 nonceexpiration: str,
                 noncesweepinterval: str) -> None:
        """
        Initialize a ConfigCAIdemix object.

        :param float rhpoolsize: Specifies the revocation pool size.
        :param str nonceexpiration: Specifies the expiration for the nonces.
        :param str noncesweepinterval: Specifies frequency at which expired nonces
               are removed from data store.
        """
        self.rhpoolsize = rhpoolsize
        self.nonceexpiration = nonceexpiration
        self.noncesweepinterval = noncesweepinterval

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCAIdemix':
        """Initialize a ConfigCAIdemix object from a json dictionary."""
        args = {}
        if 'rhpoolsize' in _dict:
            args['rhpoolsize'] = _dict.get('rhpoolsize')
        else:
            raise ValueError('Required property \'rhpoolsize\' not present in ConfigCAIdemix JSON')
        if 'nonceexpiration' in _dict:
            args['nonceexpiration'] = _dict.get('nonceexpiration')
        else:
            raise ValueError('Required property \'nonceexpiration\' not present in ConfigCAIdemix JSON')
        if 'noncesweepinterval' in _dict:
            args['noncesweepinterval'] = _dict.get('noncesweepinterval')
        else:
            raise ValueError('Required property \'noncesweepinterval\' not present in ConfigCAIdemix JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCAIdemix object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'rhpoolsize') and self.rhpoolsize is not None:
            _dict['rhpoolsize'] = self.rhpoolsize
        if hasattr(self, 'nonceexpiration') and self.nonceexpiration is not None:
            _dict['nonceexpiration'] = self.nonceexpiration
        if hasattr(self, 'noncesweepinterval') and self.noncesweepinterval is not None:
            _dict['noncesweepinterval'] = self.noncesweepinterval
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCAIdemix object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCAIdemix') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCAIdemix') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCAIntermediate():
    """
    ConfigCAIntermediate.

    :attr ConfigCAIntermediateParentserver parentserver:
    :attr ConfigCAIntermediateEnrollment enrollment: (optional)
    :attr ConfigCAIntermediateTls tls: (optional)
    """

    def __init__(self,
                 parentserver: 'ConfigCAIntermediateParentserver',
                 *,
                 enrollment: 'ConfigCAIntermediateEnrollment' = None,
                 tls: 'ConfigCAIntermediateTls' = None) -> None:
        """
        Initialize a ConfigCAIntermediate object.

        :param ConfigCAIntermediateParentserver parentserver:
        :param ConfigCAIntermediateEnrollment enrollment: (optional)
        :param ConfigCAIntermediateTls tls: (optional)
        """
        self.parentserver = parentserver
        self.enrollment = enrollment
        self.tls = tls

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCAIntermediate':
        """Initialize a ConfigCAIntermediate object from a json dictionary."""
        args = {}
        if 'parentserver' in _dict:
            args['parentserver'] = ConfigCAIntermediateParentserver.from_dict(_dict.get('parentserver'))
        else:
            raise ValueError('Required property \'parentserver\' not present in ConfigCAIntermediate JSON')
        if 'enrollment' in _dict:
            args['enrollment'] = ConfigCAIntermediateEnrollment.from_dict(_dict.get('enrollment'))
        if 'tls' in _dict:
            args['tls'] = ConfigCAIntermediateTls.from_dict(_dict.get('tls'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCAIntermediate object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'parentserver') and self.parentserver is not None:
            _dict['parentserver'] = self.parentserver.to_dict()
        if hasattr(self, 'enrollment') and self.enrollment is not None:
            _dict['enrollment'] = self.enrollment.to_dict()
        if hasattr(self, 'tls') and self.tls is not None:
            _dict['tls'] = self.tls.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCAIntermediate object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCAIntermediate') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCAIntermediate') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCARegistry():
    """
    ConfigCARegistry.

    :attr float maxenrollments: Default maximum number of enrollments per id. Set -1
          for infinite.
    :attr List[ConfigCARegistryIdentitiesItem] identities:
    """

    def __init__(self,
                 maxenrollments: float,
                 identities: List['ConfigCARegistryIdentitiesItem']) -> None:
        """
        Initialize a ConfigCARegistry object.

        :param float maxenrollments: Default maximum number of enrollments per id.
               Set -1 for infinite.
        :param List[ConfigCARegistryIdentitiesItem] identities:
        """
        self.maxenrollments = maxenrollments
        self.identities = identities

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCARegistry':
        """Initialize a ConfigCARegistry object from a json dictionary."""
        args = {}
        if 'maxenrollments' in _dict:
            args['maxenrollments'] = _dict.get('maxenrollments')
        else:
            raise ValueError('Required property \'maxenrollments\' not present in ConfigCARegistry JSON')
        if 'identities' in _dict:
            args['identities'] = [ConfigCARegistryIdentitiesItem.from_dict(x) for x in _dict.get('identities')]
        else:
            raise ValueError('Required property \'identities\' not present in ConfigCARegistry JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCARegistry object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'maxenrollments') and self.maxenrollments is not None:
            _dict['maxenrollments'] = self.maxenrollments
        if hasattr(self, 'identities') and self.identities is not None:
            _dict['identities'] = [x.to_dict() for x in self.identities]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCARegistry object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCARegistry') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCARegistry') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCASigning():
    """
    ConfigCASigning.

    :attr ConfigCASigningDefault default: (optional)
    :attr ConfigCASigningProfiles profiles: (optional)
    """

    def __init__(self,
                 *,
                 default: 'ConfigCASigningDefault' = None,
                 profiles: 'ConfigCASigningProfiles' = None) -> None:
        """
        Initialize a ConfigCASigning object.

        :param ConfigCASigningDefault default: (optional)
        :param ConfigCASigningProfiles profiles: (optional)
        """
        self.default = default
        self.profiles = profiles

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCASigning':
        """Initialize a ConfigCASigning object from a json dictionary."""
        args = {}
        if 'default' in _dict:
            args['default'] = ConfigCASigningDefault.from_dict(_dict.get('default'))
        if 'profiles' in _dict:
            args['profiles'] = ConfigCASigningProfiles.from_dict(_dict.get('profiles'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCASigning object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'default') and self.default is not None:
            _dict['default'] = self.default.to_dict()
        if hasattr(self, 'profiles') and self.profiles is not None:
            _dict['profiles'] = self.profiles.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCASigning object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCASigning') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCASigning') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigCATls():
    """
    ConfigCATls.

    :attr str keyfile: The CA's private key as base 64 encoded PEM.
    :attr str certfile: The CA's certificate as base 64 encoded PEM.
    :attr ConfigCATlsClientauth clientauth: (optional)
    """

    def __init__(self,
                 keyfile: str,
                 certfile: str,
                 *,
                 clientauth: 'ConfigCATlsClientauth' = None) -> None:
        """
        Initialize a ConfigCATls object.

        :param str keyfile: The CA's private key as base 64 encoded PEM.
        :param str certfile: The CA's certificate as base 64 encoded PEM.
        :param ConfigCATlsClientauth clientauth: (optional)
        """
        self.keyfile = keyfile
        self.certfile = certfile
        self.clientauth = clientauth

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigCATls':
        """Initialize a ConfigCATls object from a json dictionary."""
        args = {}
        if 'keyfile' in _dict:
            args['keyfile'] = _dict.get('keyfile')
        else:
            raise ValueError('Required property \'keyfile\' not present in ConfigCATls JSON')
        if 'certfile' in _dict:
            args['certfile'] = _dict.get('certfile')
        else:
            raise ValueError('Required property \'certfile\' not present in ConfigCATls JSON')
        if 'clientauth' in _dict:
            args['clientauth'] = ConfigCATlsClientauth.from_dict(_dict.get('clientauth'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigCATls object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'keyfile') and self.keyfile is not None:
            _dict['keyfile'] = self.keyfile
        if hasattr(self, 'certfile') and self.certfile is not None:
            _dict['certfile'] = self.certfile
        if hasattr(self, 'clientauth') and self.clientauth is not None:
            _dict['clientauth'] = self.clientauth.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigCATls object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigCATls') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigCATls') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigOrdererCreate():
    """
    Override the [Fabric Orderer configuration
    file](https://github.com/hyperledger/fabric/blob/release-1.4/sampleconfig/orderer.yaml)
    if you want use custom attributes to configure the Orderer. Omit if not.
    *The nested field **names** below are not case-sensitive.*.

    :attr ConfigOrdererGeneral general: (optional)
    :attr ConfigOrdererDebug debug: (optional) Controls the debugging options for
          the orderer.
    :attr ConfigOrdererMetrics metrics: (optional)
    """

    def __init__(self,
                 *,
                 general: 'ConfigOrdererGeneral' = None,
                 debug: 'ConfigOrdererDebug' = None,
                 metrics: 'ConfigOrdererMetrics' = None) -> None:
        """
        Initialize a ConfigOrdererCreate object.

        :param ConfigOrdererGeneral general: (optional)
        :param ConfigOrdererDebug debug: (optional) Controls the debugging options
               for the orderer.
        :param ConfigOrdererMetrics metrics: (optional)
        """
        self.general = general
        self.debug = debug
        self.metrics = metrics

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigOrdererCreate':
        """Initialize a ConfigOrdererCreate object from a json dictionary."""
        args = {}
        if 'General' in _dict:
            args['general'] = ConfigOrdererGeneral.from_dict(_dict.get('General'))
        if 'Debug' in _dict:
            args['debug'] = ConfigOrdererDebug.from_dict(_dict.get('Debug'))
        if 'Metrics' in _dict:
            args['metrics'] = ConfigOrdererMetrics.from_dict(_dict.get('Metrics'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigOrdererCreate object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'general') and self.general is not None:
            _dict['General'] = self.general.to_dict()
        if hasattr(self, 'debug') and self.debug is not None:
            _dict['Debug'] = self.debug.to_dict()
        if hasattr(self, 'metrics') and self.metrics is not None:
            _dict['Metrics'] = self.metrics.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigOrdererCreate object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigOrdererCreate') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigOrdererCreate') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigOrdererMetricsStatsd():
    """
    The statsd configuration.

    :attr str network: (optional) Network protocol to use.
    :attr str address: (optional) The address of the statsd server. Include
          hostname/ip and port.
    :attr str write_interval: (optional) The frequency at which locally cached
          counters and gauges are pushed to statsd.
    :attr str prefix: (optional) The string that is prepended to all emitted statsd
          metrics.
    """

    def __init__(self,
                 *,
                 network: str = None,
                 address: str = None,
                 write_interval: str = None,
                 prefix: str = None) -> None:
        """
        Initialize a ConfigOrdererMetricsStatsd object.

        :param str network: (optional) Network protocol to use.
        :param str address: (optional) The address of the statsd server. Include
               hostname/ip and port.
        :param str write_interval: (optional) The frequency at which locally cached
               counters and gauges are pushed to statsd.
        :param str prefix: (optional) The string that is prepended to all emitted
               statsd metrics.
        """
        self.network = network
        self.address = address
        self.write_interval = write_interval
        self.prefix = prefix

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigOrdererMetricsStatsd':
        """Initialize a ConfigOrdererMetricsStatsd object from a json dictionary."""
        args = {}
        if 'Network' in _dict:
            args['network'] = _dict.get('Network')
        if 'Address' in _dict:
            args['address'] = _dict.get('Address')
        if 'WriteInterval' in _dict:
            args['write_interval'] = _dict.get('WriteInterval')
        if 'Prefix' in _dict:
            args['prefix'] = _dict.get('Prefix')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigOrdererMetricsStatsd object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'network') and self.network is not None:
            _dict['Network'] = self.network
        if hasattr(self, 'address') and self.address is not None:
            _dict['Address'] = self.address
        if hasattr(self, 'write_interval') and self.write_interval is not None:
            _dict['WriteInterval'] = self.write_interval
        if hasattr(self, 'prefix') and self.prefix is not None:
            _dict['Prefix'] = self.prefix
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigOrdererMetricsStatsd object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigOrdererMetricsStatsd') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigOrdererMetricsStatsd') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class NetworkEnum(str, Enum):
        """
        Network protocol to use.
        """
        UDP = 'udp'
        TCP = 'tcp'


class ConfigOrdererUpdate():
    """
    Update the [Fabric Orderer configuration
    file](https://github.com/hyperledger/fabric/blob/release-1.4/sampleconfig/orderer.yaml)
    if you want use custom attributes to configure the Orderer. Omit if not.
    *The nested field **names** below are not case-sensitive.*
    *The nested fields sent will be merged with the existing settings.*.

    :attr ConfigOrdererGeneralUpdate general: (optional)
    :attr ConfigOrdererDebug debug: (optional) Controls the debugging options for
          the orderer.
    :attr ConfigOrdererMetrics metrics: (optional)
    """

    def __init__(self,
                 *,
                 general: 'ConfigOrdererGeneralUpdate' = None,
                 debug: 'ConfigOrdererDebug' = None,
                 metrics: 'ConfigOrdererMetrics' = None) -> None:
        """
        Initialize a ConfigOrdererUpdate object.

        :param ConfigOrdererGeneralUpdate general: (optional)
        :param ConfigOrdererDebug debug: (optional) Controls the debugging options
               for the orderer.
        :param ConfigOrdererMetrics metrics: (optional)
        """
        self.general = general
        self.debug = debug
        self.metrics = metrics

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigOrdererUpdate':
        """Initialize a ConfigOrdererUpdate object from a json dictionary."""
        args = {}
        if 'General' in _dict:
            args['general'] = ConfigOrdererGeneralUpdate.from_dict(_dict.get('General'))
        if 'Debug' in _dict:
            args['debug'] = ConfigOrdererDebug.from_dict(_dict.get('Debug'))
        if 'Metrics' in _dict:
            args['metrics'] = ConfigOrdererMetrics.from_dict(_dict.get('Metrics'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigOrdererUpdate object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'general') and self.general is not None:
            _dict['General'] = self.general.to_dict()
        if hasattr(self, 'debug') and self.debug is not None:
            _dict['Debug'] = self.debug.to_dict()
        if hasattr(self, 'metrics') and self.metrics is not None:
            _dict['Metrics'] = self.metrics.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigOrdererUpdate object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigOrdererUpdate') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigOrdererUpdate') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigOrdererAuthentication():
    """
    Contains configuration parameters that are related to authenticating client messages.

    :attr str time_window: (optional) The maximum acceptable difference between the
          current server time and the client's time.
    :attr bool no_expiration_checks: (optional) Indicates if the orderer should
          ignore expired identities. Should only be used temporarily to recover from an
          extreme event such as the expiration of administrators. Defaults `false`.
    """

    def __init__(self,
                 *,
                 time_window: str = None,
                 no_expiration_checks: bool = None) -> None:
        """
        Initialize a ConfigOrdererAuthentication object.

        :param str time_window: (optional) The maximum acceptable difference
               between the current server time and the client's time.
        :param bool no_expiration_checks: (optional) Indicates if the orderer
               should ignore expired identities. Should only be used temporarily to
               recover from an extreme event such as the expiration of administrators.
               Defaults `false`.
        """
        self.time_window = time_window
        self.no_expiration_checks = no_expiration_checks

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigOrdererAuthentication':
        """Initialize a ConfigOrdererAuthentication object from a json dictionary."""
        args = {}
        if 'TimeWindow' in _dict:
            args['time_window'] = _dict.get('TimeWindow')
        if 'NoExpirationChecks' in _dict:
            args['no_expiration_checks'] = _dict.get('NoExpirationChecks')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigOrdererAuthentication object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'time_window') and self.time_window is not None:
            _dict['TimeWindow'] = self.time_window
        if hasattr(self, 'no_expiration_checks') and self.no_expiration_checks is not None:
            _dict['NoExpirationChecks'] = self.no_expiration_checks
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigOrdererAuthentication object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigOrdererAuthentication') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigOrdererAuthentication') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigOrdererDebug():
    """
    Controls the debugging options for the orderer.

    :attr str broadcast_trace_dir: (optional) Path to directory. If set will cause
          each request to the Broadcast service to be written to a file in this directory.
    :attr str deliver_trace_dir: (optional) Path to directory. If set will cause
          each request to the Deliver service to be written to a file in this directory.
    """

    def __init__(self,
                 *,
                 broadcast_trace_dir: str = None,
                 deliver_trace_dir: str = None) -> None:
        """
        Initialize a ConfigOrdererDebug object.

        :param str broadcast_trace_dir: (optional) Path to directory. If set will
               cause each request to the Broadcast service to be written to a file in this
               directory.
        :param str deliver_trace_dir: (optional) Path to directory. If set will
               cause each request to the Deliver service to be written to a file in this
               directory.
        """
        self.broadcast_trace_dir = broadcast_trace_dir
        self.deliver_trace_dir = deliver_trace_dir

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigOrdererDebug':
        """Initialize a ConfigOrdererDebug object from a json dictionary."""
        args = {}
        if 'BroadcastTraceDir' in _dict:
            args['broadcast_trace_dir'] = _dict.get('BroadcastTraceDir')
        if 'DeliverTraceDir' in _dict:
            args['deliver_trace_dir'] = _dict.get('DeliverTraceDir')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigOrdererDebug object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'broadcast_trace_dir') and self.broadcast_trace_dir is not None:
            _dict['BroadcastTraceDir'] = self.broadcast_trace_dir
        if hasattr(self, 'deliver_trace_dir') and self.deliver_trace_dir is not None:
            _dict['DeliverTraceDir'] = self.deliver_trace_dir
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigOrdererDebug object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigOrdererDebug') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigOrdererDebug') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigOrdererGeneral():
    """
    ConfigOrdererGeneral.

    :attr ConfigOrdererKeepalive keepalive: (optional) Keep alive settings for the
          GRPC server.
    :attr Bccsp bccsp: (optional) Configures the Blockchain Crypto Service Providers
          (bccsp).
    :attr ConfigOrdererAuthentication authentication: (optional) Contains
          configuration parameters that are related to authenticating client messages.
    """

    def __init__(self,
                 *,
                 keepalive: 'ConfigOrdererKeepalive' = None,
                 bccsp: 'Bccsp' = None,
                 authentication: 'ConfigOrdererAuthentication' = None) -> None:
        """
        Initialize a ConfigOrdererGeneral object.

        :param ConfigOrdererKeepalive keepalive: (optional) Keep alive settings for
               the GRPC server.
        :param Bccsp bccsp: (optional) Configures the Blockchain Crypto Service
               Providers (bccsp).
        :param ConfigOrdererAuthentication authentication: (optional) Contains
               configuration parameters that are related to authenticating client
               messages.
        """
        self.keepalive = keepalive
        self.bccsp = bccsp
        self.authentication = authentication

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigOrdererGeneral':
        """Initialize a ConfigOrdererGeneral object from a json dictionary."""
        args = {}
        if 'Keepalive' in _dict:
            args['keepalive'] = ConfigOrdererKeepalive.from_dict(_dict.get('Keepalive'))
        if 'BCCSP' in _dict:
            args['bccsp'] = Bccsp.from_dict(_dict.get('BCCSP'))
        if 'Authentication' in _dict:
            args['authentication'] = ConfigOrdererAuthentication.from_dict(_dict.get('Authentication'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigOrdererGeneral object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'keepalive') and self.keepalive is not None:
            _dict['Keepalive'] = self.keepalive.to_dict()
        if hasattr(self, 'bccsp') and self.bccsp is not None:
            _dict['BCCSP'] = self.bccsp.to_dict()
        if hasattr(self, 'authentication') and self.authentication is not None:
            _dict['Authentication'] = self.authentication.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigOrdererGeneral object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigOrdererGeneral') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigOrdererGeneral') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigOrdererGeneralUpdate():
    """
    ConfigOrdererGeneralUpdate.

    :attr ConfigOrdererKeepalive keepalive: (optional) Keep alive settings for the
          GRPC server.
    :attr ConfigOrdererAuthentication authentication: (optional) Contains
          configuration parameters that are related to authenticating client messages.
    """

    def __init__(self,
                 *,
                 keepalive: 'ConfigOrdererKeepalive' = None,
                 authentication: 'ConfigOrdererAuthentication' = None) -> None:
        """
        Initialize a ConfigOrdererGeneralUpdate object.

        :param ConfigOrdererKeepalive keepalive: (optional) Keep alive settings for
               the GRPC server.
        :param ConfigOrdererAuthentication authentication: (optional) Contains
               configuration parameters that are related to authenticating client
               messages.
        """
        self.keepalive = keepalive
        self.authentication = authentication

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigOrdererGeneralUpdate':
        """Initialize a ConfigOrdererGeneralUpdate object from a json dictionary."""
        args = {}
        if 'Keepalive' in _dict:
            args['keepalive'] = ConfigOrdererKeepalive.from_dict(_dict.get('Keepalive'))
        if 'Authentication' in _dict:
            args['authentication'] = ConfigOrdererAuthentication.from_dict(_dict.get('Authentication'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigOrdererGeneralUpdate object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'keepalive') and self.keepalive is not None:
            _dict['Keepalive'] = self.keepalive.to_dict()
        if hasattr(self, 'authentication') and self.authentication is not None:
            _dict['Authentication'] = self.authentication.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigOrdererGeneralUpdate object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigOrdererGeneralUpdate') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigOrdererGeneralUpdate') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigOrdererKeepalive():
    """
    Keep alive settings for the GRPC server.

    :attr str server_min_interval: (optional) The minimum time between client pings.
          If a client sends pings more frequently the server will disconnect from the
          client.
    :attr str server_interval: (optional) The time between pings to clients.
    :attr str server_timeout: (optional) The duration the server will wait for a
          response from a client before closing the connection.
    """

    def __init__(self,
                 *,
                 server_min_interval: str = None,
                 server_interval: str = None,
                 server_timeout: str = None) -> None:
        """
        Initialize a ConfigOrdererKeepalive object.

        :param str server_min_interval: (optional) The minimum time between client
               pings. If a client sends pings more frequently the server will disconnect
               from the client.
        :param str server_interval: (optional) The time between pings to clients.
        :param str server_timeout: (optional) The duration the server will wait for
               a response from a client before closing the connection.
        """
        self.server_min_interval = server_min_interval
        self.server_interval = server_interval
        self.server_timeout = server_timeout

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigOrdererKeepalive':
        """Initialize a ConfigOrdererKeepalive object from a json dictionary."""
        args = {}
        if 'ServerMinInterval' in _dict:
            args['server_min_interval'] = _dict.get('ServerMinInterval')
        if 'ServerInterval' in _dict:
            args['server_interval'] = _dict.get('ServerInterval')
        if 'ServerTimeout' in _dict:
            args['server_timeout'] = _dict.get('ServerTimeout')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigOrdererKeepalive object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'server_min_interval') and self.server_min_interval is not None:
            _dict['ServerMinInterval'] = self.server_min_interval
        if hasattr(self, 'server_interval') and self.server_interval is not None:
            _dict['ServerInterval'] = self.server_interval
        if hasattr(self, 'server_timeout') and self.server_timeout is not None:
            _dict['ServerTimeout'] = self.server_timeout
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigOrdererKeepalive object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigOrdererKeepalive') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigOrdererKeepalive') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigOrdererMetrics():
    """
    ConfigOrdererMetrics.

    :attr str provider: (optional) The metrics provider to use.
    :attr ConfigOrdererMetricsStatsd statsd: (optional) The statsd configuration.
    """

    def __init__(self,
                 *,
                 provider: str = None,
                 statsd: 'ConfigOrdererMetricsStatsd' = None) -> None:
        """
        Initialize a ConfigOrdererMetrics object.

        :param str provider: (optional) The metrics provider to use.
        :param ConfigOrdererMetricsStatsd statsd: (optional) The statsd
               configuration.
        """
        self.provider = provider
        self.statsd = statsd

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigOrdererMetrics':
        """Initialize a ConfigOrdererMetrics object from a json dictionary."""
        args = {}
        if 'Provider' in _dict:
            args['provider'] = _dict.get('Provider')
        if 'Statsd' in _dict:
            args['statsd'] = ConfigOrdererMetricsStatsd.from_dict(_dict.get('Statsd'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigOrdererMetrics object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'provider') and self.provider is not None:
            _dict['Provider'] = self.provider
        if hasattr(self, 'statsd') and self.statsd is not None:
            _dict['Statsd'] = self.statsd.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigOrdererMetrics object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigOrdererMetrics') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigOrdererMetrics') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class ProviderEnum(str, Enum):
        """
        The metrics provider to use.
        """
        DISABLED = 'disabled'
        STATSD = 'statsd'
        PROMETHEUS = 'prometheus'


class ConfigPeerChaincodeExternalBuildersItem():
    """
    ConfigPeerChaincodeExternalBuildersItem.

    :attr str path: (optional) The path to a build directory.
    :attr str name: (optional) The name of this builder.
    :attr List[str] environment_whitelist: (optional)
    """

    def __init__(self,
                 *,
                 path: str = None,
                 name: str = None,
                 environment_whitelist: List[str] = None) -> None:
        """
        Initialize a ConfigPeerChaincodeExternalBuildersItem object.

        :param str path: (optional) The path to a build directory.
        :param str name: (optional) The name of this builder.
        :param List[str] environment_whitelist: (optional)
        """
        self.path = path
        self.name = name
        self.environment_whitelist = environment_whitelist

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerChaincodeExternalBuildersItem':
        """Initialize a ConfigPeerChaincodeExternalBuildersItem object from a json dictionary."""
        args = {}
        if 'path' in _dict:
            args['path'] = _dict.get('path')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'environmentWhitelist' in _dict:
            args['environment_whitelist'] = _dict.get('environmentWhitelist')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerChaincodeExternalBuildersItem object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'path') and self.path is not None:
            _dict['path'] = self.path
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'environment_whitelist') and self.environment_whitelist is not None:
            _dict['environmentWhitelist'] = self.environment_whitelist
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerChaincodeExternalBuildersItem object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerChaincodeExternalBuildersItem') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerChaincodeExternalBuildersItem') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerChaincodeGolang():
    """
    ConfigPeerChaincodeGolang.

    :attr bool dynamic_link: (optional) Controls if golang chaincode should be built
          with dynamic linking or static linking. Defaults `false` (static).
    """

    def __init__(self,
                 *,
                 dynamic_link: bool = None) -> None:
        """
        Initialize a ConfigPeerChaincodeGolang object.

        :param bool dynamic_link: (optional) Controls if golang chaincode should be
               built with dynamic linking or static linking. Defaults `false` (static).
        """
        self.dynamic_link = dynamic_link

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerChaincodeGolang':
        """Initialize a ConfigPeerChaincodeGolang object from a json dictionary."""
        args = {}
        if 'dynamicLink' in _dict:
            args['dynamic_link'] = _dict.get('dynamicLink')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerChaincodeGolang object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'dynamic_link') and self.dynamic_link is not None:
            _dict['dynamicLink'] = self.dynamic_link
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerChaincodeGolang object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerChaincodeGolang') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerChaincodeGolang') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerChaincodeLogging():
    """
    ConfigPeerChaincodeLogging.

    :attr str level: (optional) Default logging level for loggers within chaincode
          containers.
    :attr str shim: (optional) Override default level for the 'shim' logger.
    :attr str format: (optional) Override the default log format for chaincode
          container logs.
    """

    def __init__(self,
                 *,
                 level: str = None,
                 shim: str = None,
                 format: str = None) -> None:
        """
        Initialize a ConfigPeerChaincodeLogging object.

        :param str level: (optional) Default logging level for loggers within
               chaincode containers.
        :param str shim: (optional) Override default level for the 'shim' logger.
        :param str format: (optional) Override the default log format for chaincode
               container logs.
        """
        self.level = level
        self.shim = shim
        self.format = format

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerChaincodeLogging':
        """Initialize a ConfigPeerChaincodeLogging object from a json dictionary."""
        args = {}
        if 'level' in _dict:
            args['level'] = _dict.get('level')
        if 'shim' in _dict:
            args['shim'] = _dict.get('shim')
        if 'format' in _dict:
            args['format'] = _dict.get('format')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerChaincodeLogging object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'level') and self.level is not None:
            _dict['level'] = self.level
        if hasattr(self, 'shim') and self.shim is not None:
            _dict['shim'] = self.shim
        if hasattr(self, 'format') and self.format is not None:
            _dict['format'] = self.format
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerChaincodeLogging object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerChaincodeLogging') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerChaincodeLogging') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class LevelEnum(str, Enum):
        """
        Default logging level for loggers within chaincode containers.
        """
        FATAL = 'fatal'
        PANIC = 'panic'
        ERROR = 'error'
        WARNING = 'warning'
        INFO = 'info'
        DEBUG = 'debug'


    class ShimEnum(str, Enum):
        """
        Override default level for the 'shim' logger.
        """
        FATAL = 'fatal'
        PANIC = 'panic'
        ERROR = 'error'
        WARNING = 'warning'
        INFO = 'info'
        DEBUG = 'debug'


class ConfigPeerChaincodeSystem():
    """
    The complete whitelist for system chaincodes. To append a new chaincode add the new id
    to the default list.

    :attr bool cscc: (optional) Adds the system chaincode `cscc` to the whitelist.
    :attr bool lscc: (optional) Adds the system chaincode `lscc` to the whitelist.
    :attr bool escc: (optional) Adds the system chaincode `escc` to the whitelist.
    :attr bool vscc: (optional) Adds the system chaincode `vscc` to the whitelist.
    :attr bool qscc: (optional) Adds the system chaincode `qscc` to the whitelist.
    """

    def __init__(self,
                 *,
                 cscc: bool = None,
                 lscc: bool = None,
                 escc: bool = None,
                 vscc: bool = None,
                 qscc: bool = None) -> None:
        """
        Initialize a ConfigPeerChaincodeSystem object.

        :param bool cscc: (optional) Adds the system chaincode `cscc` to the
               whitelist.
        :param bool lscc: (optional) Adds the system chaincode `lscc` to the
               whitelist.
        :param bool escc: (optional) Adds the system chaincode `escc` to the
               whitelist.
        :param bool vscc: (optional) Adds the system chaincode `vscc` to the
               whitelist.
        :param bool qscc: (optional) Adds the system chaincode `qscc` to the
               whitelist.
        """
        self.cscc = cscc
        self.lscc = lscc
        self.escc = escc
        self.vscc = vscc
        self.qscc = qscc

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerChaincodeSystem':
        """Initialize a ConfigPeerChaincodeSystem object from a json dictionary."""
        args = {}
        if 'cscc' in _dict:
            args['cscc'] = _dict.get('cscc')
        if 'lscc' in _dict:
            args['lscc'] = _dict.get('lscc')
        if 'escc' in _dict:
            args['escc'] = _dict.get('escc')
        if 'vscc' in _dict:
            args['vscc'] = _dict.get('vscc')
        if 'qscc' in _dict:
            args['qscc'] = _dict.get('qscc')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerChaincodeSystem object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'cscc') and self.cscc is not None:
            _dict['cscc'] = self.cscc
        if hasattr(self, 'lscc') and self.lscc is not None:
            _dict['lscc'] = self.lscc
        if hasattr(self, 'escc') and self.escc is not None:
            _dict['escc'] = self.escc
        if hasattr(self, 'vscc') and self.vscc is not None:
            _dict['vscc'] = self.vscc
        if hasattr(self, 'qscc') and self.qscc is not None:
            _dict['qscc'] = self.qscc
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerChaincodeSystem object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerChaincodeSystem') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerChaincodeSystem') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerCreate():
    """
    Override the [Fabric Peer configuration
    file](https://github.com/hyperledger/fabric/blob/release-1.4/sampleconfig/core.yaml)
    if you want use custom attributes to configure the Peer. Omit if not.
    *The nested field **names** below are not case-sensitive.*.

    :attr ConfigPeerCreatePeer peer: (optional)
    :attr ConfigPeerChaincode chaincode: (optional)
    :attr Metrics metrics: (optional)
    """

    def __init__(self,
                 *,
                 peer: 'ConfigPeerCreatePeer' = None,
                 chaincode: 'ConfigPeerChaincode' = None,
                 metrics: 'Metrics' = None) -> None:
        """
        Initialize a ConfigPeerCreate object.

        :param ConfigPeerCreatePeer peer: (optional)
        :param ConfigPeerChaincode chaincode: (optional)
        :param Metrics metrics: (optional)
        """
        self.peer = peer
        self.chaincode = chaincode
        self.metrics = metrics

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerCreate':
        """Initialize a ConfigPeerCreate object from a json dictionary."""
        args = {}
        if 'peer' in _dict:
            args['peer'] = ConfigPeerCreatePeer.from_dict(_dict.get('peer'))
        if 'chaincode' in _dict:
            args['chaincode'] = ConfigPeerChaincode.from_dict(_dict.get('chaincode'))
        if 'metrics' in _dict:
            args['metrics'] = Metrics.from_dict(_dict.get('metrics'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerCreate object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'peer') and self.peer is not None:
            _dict['peer'] = self.peer.to_dict()
        if hasattr(self, 'chaincode') and self.chaincode is not None:
            _dict['chaincode'] = self.chaincode.to_dict()
        if hasattr(self, 'metrics') and self.metrics is not None:
            _dict['metrics'] = self.metrics.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerCreate object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerCreate') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerCreate') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerCreatePeer():
    """
    ConfigPeerCreatePeer.

    :attr str id: (optional) A unique id used to identify this instance.
    :attr str network_id: (optional) The ID to logically separate one network from
          another.
    :attr ConfigPeerKeepalive keepalive: (optional) Keep alive settings between the
          peer server and clients.
    :attr ConfigPeerGossip gossip: (optional)
    :attr ConfigPeerAuthentication authentication: (optional)
    :attr Bccsp bccsp: (optional) Configures the Blockchain Crypto Service Providers
          (bccsp).
    :attr ConfigPeerClient client: (optional)
    :attr ConfigPeerDeliveryclient deliveryclient: (optional)
    :attr ConfigPeerAdminService admin_service: (optional) Used for administrative
          operations such as control over logger levels. Only peer administrators can use
          the service.
    :attr float validator_pool_size: (optional) Number of go-routines that will
          execute transaction validation in parallel. By default, the peer chooses the
          number of CPUs on the machine. It is recommended to use the default values and
          not set this field.
    :attr ConfigPeerDiscovery discovery: (optional) The discovery service is used by
          clients to query information about peers. Such as - which peers have joined a
          channel, what is the latest channel config, and what possible sets of peers
          satisfy the endorsement policy (given a smart contract and a channel).
    :attr ConfigPeerLimits limits: (optional)
    """

    def __init__(self,
                 *,
                 id: str = None,
                 network_id: str = None,
                 keepalive: 'ConfigPeerKeepalive' = None,
                 gossip: 'ConfigPeerGossip' = None,
                 authentication: 'ConfigPeerAuthentication' = None,
                 bccsp: 'Bccsp' = None,
                 client: 'ConfigPeerClient' = None,
                 deliveryclient: 'ConfigPeerDeliveryclient' = None,
                 admin_service: 'ConfigPeerAdminService' = None,
                 validator_pool_size: float = None,
                 discovery: 'ConfigPeerDiscovery' = None,
                 limits: 'ConfigPeerLimits' = None) -> None:
        """
        Initialize a ConfigPeerCreatePeer object.

        :param str id: (optional) A unique id used to identify this instance.
        :param str network_id: (optional) The ID to logically separate one network
               from another.
        :param ConfigPeerKeepalive keepalive: (optional) Keep alive settings
               between the peer server and clients.
        :param ConfigPeerGossip gossip: (optional)
        :param ConfigPeerAuthentication authentication: (optional)
        :param Bccsp bccsp: (optional) Configures the Blockchain Crypto Service
               Providers (bccsp).
        :param ConfigPeerClient client: (optional)
        :param ConfigPeerDeliveryclient deliveryclient: (optional)
        :param ConfigPeerAdminService admin_service: (optional) Used for
               administrative operations such as control over logger levels. Only peer
               administrators can use the service.
        :param float validator_pool_size: (optional) Number of go-routines that
               will execute transaction validation in parallel. By default, the peer
               chooses the number of CPUs on the machine. It is recommended to use the
               default values and not set this field.
        :param ConfigPeerDiscovery discovery: (optional) The discovery service is
               used by clients to query information about peers. Such as - which peers
               have joined a channel, what is the latest channel config, and what possible
               sets of peers satisfy the endorsement policy (given a smart contract and a
               channel).
        :param ConfigPeerLimits limits: (optional)
        """
        self.id = id
        self.network_id = network_id
        self.keepalive = keepalive
        self.gossip = gossip
        self.authentication = authentication
        self.bccsp = bccsp
        self.client = client
        self.deliveryclient = deliveryclient
        self.admin_service = admin_service
        self.validator_pool_size = validator_pool_size
        self.discovery = discovery
        self.limits = limits

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerCreatePeer':
        """Initialize a ConfigPeerCreatePeer object from a json dictionary."""
        args = {}
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'networkId' in _dict:
            args['network_id'] = _dict.get('networkId')
        if 'keepalive' in _dict:
            args['keepalive'] = ConfigPeerKeepalive.from_dict(_dict.get('keepalive'))
        if 'gossip' in _dict:
            args['gossip'] = ConfigPeerGossip.from_dict(_dict.get('gossip'))
        if 'authentication' in _dict:
            args['authentication'] = ConfigPeerAuthentication.from_dict(_dict.get('authentication'))
        if 'BCCSP' in _dict:
            args['bccsp'] = Bccsp.from_dict(_dict.get('BCCSP'))
        if 'client' in _dict:
            args['client'] = ConfigPeerClient.from_dict(_dict.get('client'))
        if 'deliveryclient' in _dict:
            args['deliveryclient'] = ConfigPeerDeliveryclient.from_dict(_dict.get('deliveryclient'))
        if 'adminService' in _dict:
            args['admin_service'] = ConfigPeerAdminService.from_dict(_dict.get('adminService'))
        if 'validatorPoolSize' in _dict:
            args['validator_pool_size'] = _dict.get('validatorPoolSize')
        if 'discovery' in _dict:
            args['discovery'] = ConfigPeerDiscovery.from_dict(_dict.get('discovery'))
        if 'limits' in _dict:
            args['limits'] = ConfigPeerLimits.from_dict(_dict.get('limits'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerCreatePeer object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'network_id') and self.network_id is not None:
            _dict['networkId'] = self.network_id
        if hasattr(self, 'keepalive') and self.keepalive is not None:
            _dict['keepalive'] = self.keepalive.to_dict()
        if hasattr(self, 'gossip') and self.gossip is not None:
            _dict['gossip'] = self.gossip.to_dict()
        if hasattr(self, 'authentication') and self.authentication is not None:
            _dict['authentication'] = self.authentication.to_dict()
        if hasattr(self, 'bccsp') and self.bccsp is not None:
            _dict['BCCSP'] = self.bccsp.to_dict()
        if hasattr(self, 'client') and self.client is not None:
            _dict['client'] = self.client.to_dict()
        if hasattr(self, 'deliveryclient') and self.deliveryclient is not None:
            _dict['deliveryclient'] = self.deliveryclient.to_dict()
        if hasattr(self, 'admin_service') and self.admin_service is not None:
            _dict['adminService'] = self.admin_service.to_dict()
        if hasattr(self, 'validator_pool_size') and self.validator_pool_size is not None:
            _dict['validatorPoolSize'] = self.validator_pool_size
        if hasattr(self, 'discovery') and self.discovery is not None:
            _dict['discovery'] = self.discovery.to_dict()
        if hasattr(self, 'limits') and self.limits is not None:
            _dict['limits'] = self.limits.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerCreatePeer object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerCreatePeer') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerCreatePeer') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerDeliveryclientAddressOverridesItem():
    """
    ConfigPeerDeliveryclientAddressOverridesItem.

    :attr str from_: (optional) The address in the channel configuration that will
          be overridden.
    :attr str to: (optional) The address to use.
    :attr str ca_certs_file: (optional) The path to the CA's cert file.
    """

    def __init__(self,
                 *,
                 from_: str = None,
                 to: str = None,
                 ca_certs_file: str = None) -> None:
        """
        Initialize a ConfigPeerDeliveryclientAddressOverridesItem object.

        :param str from_: (optional) The address in the channel configuration that
               will be overridden.
        :param str to: (optional) The address to use.
        :param str ca_certs_file: (optional) The path to the CA's cert file.
        """
        self.from_ = from_
        self.to = to
        self.ca_certs_file = ca_certs_file

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerDeliveryclientAddressOverridesItem':
        """Initialize a ConfigPeerDeliveryclientAddressOverridesItem object from a json dictionary."""
        args = {}
        if 'from' in _dict:
            args['from_'] = _dict.get('from')
        if 'to' in _dict:
            args['to'] = _dict.get('to')
        if 'caCertsFile' in _dict:
            args['ca_certs_file'] = _dict.get('caCertsFile')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerDeliveryclientAddressOverridesItem object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'from_') and self.from_ is not None:
            _dict['from'] = self.from_
        if hasattr(self, 'to') and self.to is not None:
            _dict['to'] = self.to
        if hasattr(self, 'ca_certs_file') and self.ca_certs_file is not None:
            _dict['caCertsFile'] = self.ca_certs_file
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerDeliveryclientAddressOverridesItem object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerDeliveryclientAddressOverridesItem') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerDeliveryclientAddressOverridesItem') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerGossipElection():
    """
    Leader election service configuration.

    :attr str startup_grace_period: (optional) Longest time the peer will wait for
          stable membership during leader election startup.
    :attr str membership_sample_interval: (optional) Frequency that gossip
          membership samples to check its stability.
    :attr str leader_alive_threshold: (optional) Amount of time after the last
          declaration message for the peer to perform another leader election.
    :attr str leader_election_duration: (optional) Amount of time between the peer
          sending a propose message and it declaring itself as a leader.
    """

    def __init__(self,
                 *,
                 startup_grace_period: str = None,
                 membership_sample_interval: str = None,
                 leader_alive_threshold: str = None,
                 leader_election_duration: str = None) -> None:
        """
        Initialize a ConfigPeerGossipElection object.

        :param str startup_grace_period: (optional) Longest time the peer will wait
               for stable membership during leader election startup.
        :param str membership_sample_interval: (optional) Frequency that gossip
               membership samples to check its stability.
        :param str leader_alive_threshold: (optional) Amount of time after the last
               declaration message for the peer to perform another leader election.
        :param str leader_election_duration: (optional) Amount of time between the
               peer sending a propose message and it declaring itself as a leader.
        """
        self.startup_grace_period = startup_grace_period
        self.membership_sample_interval = membership_sample_interval
        self.leader_alive_threshold = leader_alive_threshold
        self.leader_election_duration = leader_election_duration

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerGossipElection':
        """Initialize a ConfigPeerGossipElection object from a json dictionary."""
        args = {}
        if 'startupGracePeriod' in _dict:
            args['startup_grace_period'] = _dict.get('startupGracePeriod')
        if 'membershipSampleInterval' in _dict:
            args['membership_sample_interval'] = _dict.get('membershipSampleInterval')
        if 'leaderAliveThreshold' in _dict:
            args['leader_alive_threshold'] = _dict.get('leaderAliveThreshold')
        if 'leaderElectionDuration' in _dict:
            args['leader_election_duration'] = _dict.get('leaderElectionDuration')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerGossipElection object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'startup_grace_period') and self.startup_grace_period is not None:
            _dict['startupGracePeriod'] = self.startup_grace_period
        if hasattr(self, 'membership_sample_interval') and self.membership_sample_interval is not None:
            _dict['membershipSampleInterval'] = self.membership_sample_interval
        if hasattr(self, 'leader_alive_threshold') and self.leader_alive_threshold is not None:
            _dict['leaderAliveThreshold'] = self.leader_alive_threshold
        if hasattr(self, 'leader_election_duration') and self.leader_election_duration is not None:
            _dict['leaderElectionDuration'] = self.leader_election_duration
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerGossipElection object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerGossipElection') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerGossipElection') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerGossipPvtData():
    """
    ConfigPeerGossipPvtData.

    :attr str pull_retry_threshold: (optional) Determines the maximum time to
          attempt to pull private data for a block before that block is committed without
          the private data.
    :attr float transientstore_max_block_retention: (optional) As private data
          enters the transient store, it is associated with the peer's current ledger's
          height. This field defines the maximum difference between the current ledger's
          height on commit, and the private data residing inside the transient store.
          Private data outside this range is not guaranteed to exist and will be purged
          periodically.
    :attr str push_ack_timeout: (optional) Maximum time to wait for an
          acknowledgment from each peer's private data push.
    :attr float btl_pull_margin: (optional) Block to live pulling margin. Used as a
          buffer to prevent peers from trying to pull private data from others peers that
          are soon to be purged. "Soon" defined as blocks that will be purged in the next
          N blocks. This helps a newly joined peer catch up quicker.
    :attr float reconcile_batch_size: (optional) Determines the maximum batch size
          of missing private data that will be reconciled in a single iteration. The
          process of reconciliation is done in an endless loop. The "reconciler" in each
          iteration tries to pull from the other peers with the most recent missing blocks
          and this maximum batch size limitation.
    :attr str reconcile_sleep_interval: (optional) Determines the time "reconciler"
          sleeps from the end of an iteration until the beginning of the next iteration.
    :attr bool reconciliation_enabled: (optional) Determines whether private data
          reconciliation is enabled or not.
    :attr bool skip_pulling_invalid_transactions_during_commit: (optional) Controls
          whether pulling invalid transaction's private data from other peers need to be
          skipped during the commit time. If `true` it will be pulled through
          "reconciler".
    :attr ConfigPeerGossipPvtDataImplicitCollectionDisseminationPolicy
          implicit_collection_dissemination_policy: (optional)
    """

    def __init__(self,
                 *,
                 pull_retry_threshold: str = None,
                 transientstore_max_block_retention: float = None,
                 push_ack_timeout: str = None,
                 btl_pull_margin: float = None,
                 reconcile_batch_size: float = None,
                 reconcile_sleep_interval: str = None,
                 reconciliation_enabled: bool = None,
                 skip_pulling_invalid_transactions_during_commit: bool = None,
                 implicit_collection_dissemination_policy: 'ConfigPeerGossipPvtDataImplicitCollectionDisseminationPolicy' = None) -> None:
        """
        Initialize a ConfigPeerGossipPvtData object.

        :param str pull_retry_threshold: (optional) Determines the maximum time to
               attempt to pull private data for a block before that block is committed
               without the private data.
        :param float transientstore_max_block_retention: (optional) As private data
               enters the transient store, it is associated with the peer's current
               ledger's height. This field defines the maximum difference between the
               current ledger's height on commit, and the private data residing inside the
               transient store. Private data outside this range is not guaranteed to exist
               and will be purged periodically.
        :param str push_ack_timeout: (optional) Maximum time to wait for an
               acknowledgment from each peer's private data push.
        :param float btl_pull_margin: (optional) Block to live pulling margin. Used
               as a buffer to prevent peers from trying to pull private data from others
               peers that are soon to be purged. "Soon" defined as blocks that will be
               purged in the next N blocks. This helps a newly joined peer catch up
               quicker.
        :param float reconcile_batch_size: (optional) Determines the maximum batch
               size of missing private data that will be reconciled in a single iteration.
               The process of reconciliation is done in an endless loop. The "reconciler"
               in each iteration tries to pull from the other peers with the most recent
               missing blocks and this maximum batch size limitation.
        :param str reconcile_sleep_interval: (optional) Determines the time
               "reconciler" sleeps from the end of an iteration until the beginning of the
               next iteration.
        :param bool reconciliation_enabled: (optional) Determines whether private
               data reconciliation is enabled or not.
        :param bool skip_pulling_invalid_transactions_during_commit: (optional)
               Controls whether pulling invalid transaction's private data from other
               peers need to be skipped during the commit time. If `true` it will be
               pulled through "reconciler".
        :param ConfigPeerGossipPvtDataImplicitCollectionDisseminationPolicy
               implicit_collection_dissemination_policy: (optional)
        """
        self.pull_retry_threshold = pull_retry_threshold
        self.transientstore_max_block_retention = transientstore_max_block_retention
        self.push_ack_timeout = push_ack_timeout
        self.btl_pull_margin = btl_pull_margin
        self.reconcile_batch_size = reconcile_batch_size
        self.reconcile_sleep_interval = reconcile_sleep_interval
        self.reconciliation_enabled = reconciliation_enabled
        self.skip_pulling_invalid_transactions_during_commit = skip_pulling_invalid_transactions_during_commit
        self.implicit_collection_dissemination_policy = implicit_collection_dissemination_policy

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerGossipPvtData':
        """Initialize a ConfigPeerGossipPvtData object from a json dictionary."""
        args = {}
        if 'pullRetryThreshold' in _dict:
            args['pull_retry_threshold'] = _dict.get('pullRetryThreshold')
        if 'transientstoreMaxBlockRetention' in _dict:
            args['transientstore_max_block_retention'] = _dict.get('transientstoreMaxBlockRetention')
        if 'pushAckTimeout' in _dict:
            args['push_ack_timeout'] = _dict.get('pushAckTimeout')
        if 'btlPullMargin' in _dict:
            args['btl_pull_margin'] = _dict.get('btlPullMargin')
        if 'reconcileBatchSize' in _dict:
            args['reconcile_batch_size'] = _dict.get('reconcileBatchSize')
        if 'reconcileSleepInterval' in _dict:
            args['reconcile_sleep_interval'] = _dict.get('reconcileSleepInterval')
        if 'reconciliationEnabled' in _dict:
            args['reconciliation_enabled'] = _dict.get('reconciliationEnabled')
        if 'skipPullingInvalidTransactionsDuringCommit' in _dict:
            args['skip_pulling_invalid_transactions_during_commit'] = _dict.get('skipPullingInvalidTransactionsDuringCommit')
        if 'implicitCollectionDisseminationPolicy' in _dict:
            args['implicit_collection_dissemination_policy'] = ConfigPeerGossipPvtDataImplicitCollectionDisseminationPolicy.from_dict(_dict.get('implicitCollectionDisseminationPolicy'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerGossipPvtData object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'pull_retry_threshold') and self.pull_retry_threshold is not None:
            _dict['pullRetryThreshold'] = self.pull_retry_threshold
        if hasattr(self, 'transientstore_max_block_retention') and self.transientstore_max_block_retention is not None:
            _dict['transientstoreMaxBlockRetention'] = self.transientstore_max_block_retention
        if hasattr(self, 'push_ack_timeout') and self.push_ack_timeout is not None:
            _dict['pushAckTimeout'] = self.push_ack_timeout
        if hasattr(self, 'btl_pull_margin') and self.btl_pull_margin is not None:
            _dict['btlPullMargin'] = self.btl_pull_margin
        if hasattr(self, 'reconcile_batch_size') and self.reconcile_batch_size is not None:
            _dict['reconcileBatchSize'] = self.reconcile_batch_size
        if hasattr(self, 'reconcile_sleep_interval') and self.reconcile_sleep_interval is not None:
            _dict['reconcileSleepInterval'] = self.reconcile_sleep_interval
        if hasattr(self, 'reconciliation_enabled') and self.reconciliation_enabled is not None:
            _dict['reconciliationEnabled'] = self.reconciliation_enabled
        if hasattr(self, 'skip_pulling_invalid_transactions_during_commit') and self.skip_pulling_invalid_transactions_during_commit is not None:
            _dict['skipPullingInvalidTransactionsDuringCommit'] = self.skip_pulling_invalid_transactions_during_commit
        if hasattr(self, 'implicit_collection_dissemination_policy') and self.implicit_collection_dissemination_policy is not None:
            _dict['implicitCollectionDisseminationPolicy'] = self.implicit_collection_dissemination_policy.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerGossipPvtData object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerGossipPvtData') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerGossipPvtData') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerGossipPvtDataImplicitCollectionDisseminationPolicy():
    """
    ConfigPeerGossipPvtDataImplicitCollectionDisseminationPolicy.

    :attr float required_peer_count: (optional) Defines the minimum number of peers
          to successfully disseminate private data during endorsement.
    :attr float max_peer_count: (optional) Defines the maximum number of peers to
          attempt to disseminate private data during endorsement.
    """

    def __init__(self,
                 *,
                 required_peer_count: float = None,
                 max_peer_count: float = None) -> None:
        """
        Initialize a ConfigPeerGossipPvtDataImplicitCollectionDisseminationPolicy object.

        :param float required_peer_count: (optional) Defines the minimum number of
               peers to successfully disseminate private data during endorsement.
        :param float max_peer_count: (optional) Defines the maximum number of peers
               to attempt to disseminate private data during endorsement.
        """
        self.required_peer_count = required_peer_count
        self.max_peer_count = max_peer_count

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerGossipPvtDataImplicitCollectionDisseminationPolicy':
        """Initialize a ConfigPeerGossipPvtDataImplicitCollectionDisseminationPolicy object from a json dictionary."""
        args = {}
        if 'requiredPeerCount' in _dict:
            args['required_peer_count'] = _dict.get('requiredPeerCount')
        if 'maxPeerCount' in _dict:
            args['max_peer_count'] = _dict.get('maxPeerCount')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerGossipPvtDataImplicitCollectionDisseminationPolicy object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'required_peer_count') and self.required_peer_count is not None:
            _dict['requiredPeerCount'] = self.required_peer_count
        if hasattr(self, 'max_peer_count') and self.max_peer_count is not None:
            _dict['maxPeerCount'] = self.max_peer_count
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerGossipPvtDataImplicitCollectionDisseminationPolicy object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerGossipPvtDataImplicitCollectionDisseminationPolicy') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerGossipPvtDataImplicitCollectionDisseminationPolicy') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerGossipState():
    """
    Gossip state transfer related configuration.

    :attr bool enabled: (optional) Controls if the state transfer is enabled or not.
          If state transfer is active, it syncs up missing blocks and allows lagging peers
          to catch up with the rest of the network.
    :attr str check_interval: (optional) The frequency to check whether a peer is
          lagging behind enough to request blocks by using state transfer from another
          peer.
    :attr str response_timeout: (optional) Amount of time to wait for state transfer
          responses from other peers.
    :attr float batch_size: (optional) Number of blocks to request by using state
          transfer from another peer.
    :attr float block_buffer_size: (optional) Maximum difference between the lowest
          and highest block sequence number. In order to ensure that there are no holes
          the actual buffer size is twice this distance.
    :attr float max_retries: (optional) Maximum number of retries of a single state
          transfer request.
    """

    def __init__(self,
                 *,
                 enabled: bool = None,
                 check_interval: str = None,
                 response_timeout: str = None,
                 batch_size: float = None,
                 block_buffer_size: float = None,
                 max_retries: float = None) -> None:
        """
        Initialize a ConfigPeerGossipState object.

        :param bool enabled: (optional) Controls if the state transfer is enabled
               or not. If state transfer is active, it syncs up missing blocks and allows
               lagging peers to catch up with the rest of the network.
        :param str check_interval: (optional) The frequency to check whether a peer
               is lagging behind enough to request blocks by using state transfer from
               another peer.
        :param str response_timeout: (optional) Amount of time to wait for state
               transfer responses from other peers.
        :param float batch_size: (optional) Number of blocks to request by using
               state transfer from another peer.
        :param float block_buffer_size: (optional) Maximum difference between the
               lowest and highest block sequence number. In order to ensure that there are
               no holes the actual buffer size is twice this distance.
        :param float max_retries: (optional) Maximum number of retries of a single
               state transfer request.
        """
        self.enabled = enabled
        self.check_interval = check_interval
        self.response_timeout = response_timeout
        self.batch_size = batch_size
        self.block_buffer_size = block_buffer_size
        self.max_retries = max_retries

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerGossipState':
        """Initialize a ConfigPeerGossipState object from a json dictionary."""
        args = {}
        if 'enabled' in _dict:
            args['enabled'] = _dict.get('enabled')
        if 'checkInterval' in _dict:
            args['check_interval'] = _dict.get('checkInterval')
        if 'responseTimeout' in _dict:
            args['response_timeout'] = _dict.get('responseTimeout')
        if 'batchSize' in _dict:
            args['batch_size'] = _dict.get('batchSize')
        if 'blockBufferSize' in _dict:
            args['block_buffer_size'] = _dict.get('blockBufferSize')
        if 'maxRetries' in _dict:
            args['max_retries'] = _dict.get('maxRetries')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerGossipState object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'enabled') and self.enabled is not None:
            _dict['enabled'] = self.enabled
        if hasattr(self, 'check_interval') and self.check_interval is not None:
            _dict['checkInterval'] = self.check_interval
        if hasattr(self, 'response_timeout') and self.response_timeout is not None:
            _dict['responseTimeout'] = self.response_timeout
        if hasattr(self, 'batch_size') and self.batch_size is not None:
            _dict['batchSize'] = self.batch_size
        if hasattr(self, 'block_buffer_size') and self.block_buffer_size is not None:
            _dict['blockBufferSize'] = self.block_buffer_size
        if hasattr(self, 'max_retries') and self.max_retries is not None:
            _dict['maxRetries'] = self.max_retries
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerGossipState object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerGossipState') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerGossipState') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerKeepaliveClient():
    """
    ConfigPeerKeepaliveClient.

    :attr str interval: (optional) The time between pings to other peer nodes. Must
          greater than or equal to the minInterval.
    :attr str timeout: (optional) The duration a client waits for a peer's response
          before it closes the connection.
    """

    def __init__(self,
                 *,
                 interval: str = None,
                 timeout: str = None) -> None:
        """
        Initialize a ConfigPeerKeepaliveClient object.

        :param str interval: (optional) The time between pings to other peer nodes.
               Must greater than or equal to the minInterval.
        :param str timeout: (optional) The duration a client waits for a peer's
               response before it closes the connection.
        """
        self.interval = interval
        self.timeout = timeout

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerKeepaliveClient':
        """Initialize a ConfigPeerKeepaliveClient object from a json dictionary."""
        args = {}
        if 'interval' in _dict:
            args['interval'] = _dict.get('interval')
        if 'timeout' in _dict:
            args['timeout'] = _dict.get('timeout')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerKeepaliveClient object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'interval') and self.interval is not None:
            _dict['interval'] = self.interval
        if hasattr(self, 'timeout') and self.timeout is not None:
            _dict['timeout'] = self.timeout
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerKeepaliveClient object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerKeepaliveClient') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerKeepaliveClient') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerKeepaliveDeliveryClient():
    """
    ConfigPeerKeepaliveDeliveryClient.

    :attr str interval: (optional) The time between pings to ordering nodes. Must
          greater than or equal to the minInterval.
    :attr str timeout: (optional) The duration a client waits for an orderer's
          response before it closes the connection.
    """

    def __init__(self,
                 *,
                 interval: str = None,
                 timeout: str = None) -> None:
        """
        Initialize a ConfigPeerKeepaliveDeliveryClient object.

        :param str interval: (optional) The time between pings to ordering nodes.
               Must greater than or equal to the minInterval.
        :param str timeout: (optional) The duration a client waits for an orderer's
               response before it closes the connection.
        """
        self.interval = interval
        self.timeout = timeout

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerKeepaliveDeliveryClient':
        """Initialize a ConfigPeerKeepaliveDeliveryClient object from a json dictionary."""
        args = {}
        if 'interval' in _dict:
            args['interval'] = _dict.get('interval')
        if 'timeout' in _dict:
            args['timeout'] = _dict.get('timeout')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerKeepaliveDeliveryClient object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'interval') and self.interval is not None:
            _dict['interval'] = self.interval
        if hasattr(self, 'timeout') and self.timeout is not None:
            _dict['timeout'] = self.timeout
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerKeepaliveDeliveryClient object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerKeepaliveDeliveryClient') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerKeepaliveDeliveryClient') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerLimitsConcurrency():
    """
    ConfigPeerLimitsConcurrency.

    :attr float endorser_service: (optional) Limits the number of concurrent
          requests to the endorser service. The endorser service handles application and
          system chaincode deployment and invocations (including queries).
    :attr float deliver_service: (optional) Limits the number of concurrent requests
          to the deliver service. The deliver service handles block and transaction
          events.
    """

    def __init__(self,
                 *,
                 endorser_service: float = None,
                 deliver_service: float = None) -> None:
        """
        Initialize a ConfigPeerLimitsConcurrency object.

        :param float endorser_service: (optional) Limits the number of concurrent
               requests to the endorser service. The endorser service handles application
               and system chaincode deployment and invocations (including queries).
        :param float deliver_service: (optional) Limits the number of concurrent
               requests to the deliver service. The deliver service handles block and
               transaction events.
        """
        self.endorser_service = endorser_service
        self.deliver_service = deliver_service

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerLimitsConcurrency':
        """Initialize a ConfigPeerLimitsConcurrency object from a json dictionary."""
        args = {}
        if 'endorserService' in _dict:
            args['endorser_service'] = _dict.get('endorserService')
        if 'deliverService' in _dict:
            args['deliver_service'] = _dict.get('deliverService')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerLimitsConcurrency object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'endorser_service') and self.endorser_service is not None:
            _dict['endorserService'] = self.endorser_service
        if hasattr(self, 'deliver_service') and self.deliver_service is not None:
            _dict['deliverService'] = self.deliver_service
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerLimitsConcurrency object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerLimitsConcurrency') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerLimitsConcurrency') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerUpdate():
    """
    Update the [Fabric Peer configuration
    file](https://github.com/hyperledger/fabric/blob/release-1.4/sampleconfig/core.yaml)
    if you want use custom attributes to configure the Peer. Omit if not.
    *The nested field **names** below are not case-sensitive.*
    *The nested fields sent will be merged with the existing settings.*.

    :attr ConfigPeerUpdatePeer peer: (optional)
    :attr ConfigPeerChaincode chaincode: (optional)
    :attr Metrics metrics: (optional)
    """

    def __init__(self,
                 *,
                 peer: 'ConfigPeerUpdatePeer' = None,
                 chaincode: 'ConfigPeerChaincode' = None,
                 metrics: 'Metrics' = None) -> None:
        """
        Initialize a ConfigPeerUpdate object.

        :param ConfigPeerUpdatePeer peer: (optional)
        :param ConfigPeerChaincode chaincode: (optional)
        :param Metrics metrics: (optional)
        """
        self.peer = peer
        self.chaincode = chaincode
        self.metrics = metrics

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerUpdate':
        """Initialize a ConfigPeerUpdate object from a json dictionary."""
        args = {}
        if 'peer' in _dict:
            args['peer'] = ConfigPeerUpdatePeer.from_dict(_dict.get('peer'))
        if 'chaincode' in _dict:
            args['chaincode'] = ConfigPeerChaincode.from_dict(_dict.get('chaincode'))
        if 'metrics' in _dict:
            args['metrics'] = Metrics.from_dict(_dict.get('metrics'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerUpdate object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'peer') and self.peer is not None:
            _dict['peer'] = self.peer.to_dict()
        if hasattr(self, 'chaincode') and self.chaincode is not None:
            _dict['chaincode'] = self.chaincode.to_dict()
        if hasattr(self, 'metrics') and self.metrics is not None:
            _dict['metrics'] = self.metrics.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerUpdate object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerUpdate') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerUpdate') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerUpdatePeer():
    """
    ConfigPeerUpdatePeer.

    :attr str id: (optional) A unique id used to identify this instance.
    :attr str network_id: (optional) The ID to logically separate one network from
          another.
    :attr ConfigPeerKeepalive keepalive: (optional) Keep alive settings between the
          peer server and clients.
    :attr ConfigPeerGossip gossip: (optional)
    :attr ConfigPeerAuthentication authentication: (optional)
    :attr ConfigPeerClient client: (optional)
    :attr ConfigPeerDeliveryclient deliveryclient: (optional)
    :attr ConfigPeerAdminService admin_service: (optional) Used for administrative
          operations such as control over logger levels. Only peer administrators can use
          the service.
    :attr float validator_pool_size: (optional) Number of go-routines that will
          execute transaction validation in parallel. By default, the peer chooses the
          number of CPUs on the machine. It is recommended to use the default values and
          not set this field.
    :attr ConfigPeerDiscovery discovery: (optional) The discovery service is used by
          clients to query information about peers. Such as - which peers have joined a
          channel, what is the latest channel config, and what possible sets of peers
          satisfy the endorsement policy (given a smart contract and a channel).
    :attr ConfigPeerLimits limits: (optional)
    """

    def __init__(self,
                 *,
                 id: str = None,
                 network_id: str = None,
                 keepalive: 'ConfigPeerKeepalive' = None,
                 gossip: 'ConfigPeerGossip' = None,
                 authentication: 'ConfigPeerAuthentication' = None,
                 client: 'ConfigPeerClient' = None,
                 deliveryclient: 'ConfigPeerDeliveryclient' = None,
                 admin_service: 'ConfigPeerAdminService' = None,
                 validator_pool_size: float = None,
                 discovery: 'ConfigPeerDiscovery' = None,
                 limits: 'ConfigPeerLimits' = None) -> None:
        """
        Initialize a ConfigPeerUpdatePeer object.

        :param str id: (optional) A unique id used to identify this instance.
        :param str network_id: (optional) The ID to logically separate one network
               from another.
        :param ConfigPeerKeepalive keepalive: (optional) Keep alive settings
               between the peer server and clients.
        :param ConfigPeerGossip gossip: (optional)
        :param ConfigPeerAuthentication authentication: (optional)
        :param ConfigPeerClient client: (optional)
        :param ConfigPeerDeliveryclient deliveryclient: (optional)
        :param ConfigPeerAdminService admin_service: (optional) Used for
               administrative operations such as control over logger levels. Only peer
               administrators can use the service.
        :param float validator_pool_size: (optional) Number of go-routines that
               will execute transaction validation in parallel. By default, the peer
               chooses the number of CPUs on the machine. It is recommended to use the
               default values and not set this field.
        :param ConfigPeerDiscovery discovery: (optional) The discovery service is
               used by clients to query information about peers. Such as - which peers
               have joined a channel, what is the latest channel config, and what possible
               sets of peers satisfy the endorsement policy (given a smart contract and a
               channel).
        :param ConfigPeerLimits limits: (optional)
        """
        self.id = id
        self.network_id = network_id
        self.keepalive = keepalive
        self.gossip = gossip
        self.authentication = authentication
        self.client = client
        self.deliveryclient = deliveryclient
        self.admin_service = admin_service
        self.validator_pool_size = validator_pool_size
        self.discovery = discovery
        self.limits = limits

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerUpdatePeer':
        """Initialize a ConfigPeerUpdatePeer object from a json dictionary."""
        args = {}
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'networkId' in _dict:
            args['network_id'] = _dict.get('networkId')
        if 'keepalive' in _dict:
            args['keepalive'] = ConfigPeerKeepalive.from_dict(_dict.get('keepalive'))
        if 'gossip' in _dict:
            args['gossip'] = ConfigPeerGossip.from_dict(_dict.get('gossip'))
        if 'authentication' in _dict:
            args['authentication'] = ConfigPeerAuthentication.from_dict(_dict.get('authentication'))
        if 'client' in _dict:
            args['client'] = ConfigPeerClient.from_dict(_dict.get('client'))
        if 'deliveryclient' in _dict:
            args['deliveryclient'] = ConfigPeerDeliveryclient.from_dict(_dict.get('deliveryclient'))
        if 'adminService' in _dict:
            args['admin_service'] = ConfigPeerAdminService.from_dict(_dict.get('adminService'))
        if 'validatorPoolSize' in _dict:
            args['validator_pool_size'] = _dict.get('validatorPoolSize')
        if 'discovery' in _dict:
            args['discovery'] = ConfigPeerDiscovery.from_dict(_dict.get('discovery'))
        if 'limits' in _dict:
            args['limits'] = ConfigPeerLimits.from_dict(_dict.get('limits'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerUpdatePeer object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'network_id') and self.network_id is not None:
            _dict['networkId'] = self.network_id
        if hasattr(self, 'keepalive') and self.keepalive is not None:
            _dict['keepalive'] = self.keepalive.to_dict()
        if hasattr(self, 'gossip') and self.gossip is not None:
            _dict['gossip'] = self.gossip.to_dict()
        if hasattr(self, 'authentication') and self.authentication is not None:
            _dict['authentication'] = self.authentication.to_dict()
        if hasattr(self, 'client') and self.client is not None:
            _dict['client'] = self.client.to_dict()
        if hasattr(self, 'deliveryclient') and self.deliveryclient is not None:
            _dict['deliveryclient'] = self.deliveryclient.to_dict()
        if hasattr(self, 'admin_service') and self.admin_service is not None:
            _dict['adminService'] = self.admin_service.to_dict()
        if hasattr(self, 'validator_pool_size') and self.validator_pool_size is not None:
            _dict['validatorPoolSize'] = self.validator_pool_size
        if hasattr(self, 'discovery') and self.discovery is not None:
            _dict['discovery'] = self.discovery.to_dict()
        if hasattr(self, 'limits') and self.limits is not None:
            _dict['limits'] = self.limits.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerUpdatePeer object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerUpdatePeer') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerUpdatePeer') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerAdminService():
    """
    Used for administrative operations such as control over logger levels. Only peer
    administrators can use the service.

    :attr str listen_address: The interface and port on which the admin server will
          listen on. Defaults to the same address as the peer's listen address and port
          7051.
    """

    def __init__(self,
                 listen_address: str) -> None:
        """
        Initialize a ConfigPeerAdminService object.

        :param str listen_address: The interface and port on which the admin server
               will listen on. Defaults to the same address as the peer's listen address
               and port 7051.
        """
        self.listen_address = listen_address

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerAdminService':
        """Initialize a ConfigPeerAdminService object from a json dictionary."""
        args = {}
        if 'listenAddress' in _dict:
            args['listen_address'] = _dict.get('listenAddress')
        else:
            raise ValueError('Required property \'listenAddress\' not present in ConfigPeerAdminService JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerAdminService object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'listen_address') and self.listen_address is not None:
            _dict['listenAddress'] = self.listen_address
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerAdminService object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerAdminService') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerAdminService') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerAuthentication():
    """
    ConfigPeerAuthentication.

    :attr str timewindow: The maximum acceptable difference between the current
          server time and the client's time.
    """

    def __init__(self,
                 timewindow: str) -> None:
        """
        Initialize a ConfigPeerAuthentication object.

        :param str timewindow: The maximum acceptable difference between the
               current server time and the client's time.
        """
        self.timewindow = timewindow

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerAuthentication':
        """Initialize a ConfigPeerAuthentication object from a json dictionary."""
        args = {}
        if 'timewindow' in _dict:
            args['timewindow'] = _dict.get('timewindow')
        else:
            raise ValueError('Required property \'timewindow\' not present in ConfigPeerAuthentication JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerAuthentication object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'timewindow') and self.timewindow is not None:
            _dict['timewindow'] = self.timewindow
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerAuthentication object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerAuthentication') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerAuthentication') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerChaincode():
    """
    ConfigPeerChaincode.

    :attr ConfigPeerChaincodeGolang golang: (optional)
    :attr List[ConfigPeerChaincodeExternalBuildersItem] external_builders:
          (optional) List of directories to treat as external builders/launches of
          chaincode.
    :attr str install_timeout: (optional) Maximum duration to wait for the chaincode
          build and install process to complete.
    :attr str startuptimeout: (optional) Time for starting up a container and
          waiting for Register to come through.
    :attr str executetimeout: (optional) Time for Invoke and Init calls to return.
          This timeout is used by all chaincodes in all the channels, including system
          chaincodes. Note that if the image is not available the peer needs to build the
          image, which will take additional time.
    :attr ConfigPeerChaincodeSystem system: (optional) The complete whitelist for
          system chaincodes. To append a new chaincode add the new id to the default list.
    :attr ConfigPeerChaincodeLogging logging: (optional)
    """

    def __init__(self,
                 *,
                 golang: 'ConfigPeerChaincodeGolang' = None,
                 external_builders: List['ConfigPeerChaincodeExternalBuildersItem'] = None,
                 install_timeout: str = None,
                 startuptimeout: str = None,
                 executetimeout: str = None,
                 system: 'ConfigPeerChaincodeSystem' = None,
                 logging: 'ConfigPeerChaincodeLogging' = None) -> None:
        """
        Initialize a ConfigPeerChaincode object.

        :param ConfigPeerChaincodeGolang golang: (optional)
        :param List[ConfigPeerChaincodeExternalBuildersItem] external_builders:
               (optional) List of directories to treat as external builders/launches of
               chaincode.
        :param str install_timeout: (optional) Maximum duration to wait for the
               chaincode build and install process to complete.
        :param str startuptimeout: (optional) Time for starting up a container and
               waiting for Register to come through.
        :param str executetimeout: (optional) Time for Invoke and Init calls to
               return. This timeout is used by all chaincodes in all the channels,
               including system chaincodes. Note that if the image is not available the
               peer needs to build the image, which will take additional time.
        :param ConfigPeerChaincodeSystem system: (optional) The complete whitelist
               for system chaincodes. To append a new chaincode add the new id to the
               default list.
        :param ConfigPeerChaincodeLogging logging: (optional)
        """
        self.golang = golang
        self.external_builders = external_builders
        self.install_timeout = install_timeout
        self.startuptimeout = startuptimeout
        self.executetimeout = executetimeout
        self.system = system
        self.logging = logging

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerChaincode':
        """Initialize a ConfigPeerChaincode object from a json dictionary."""
        args = {}
        if 'golang' in _dict:
            args['golang'] = ConfigPeerChaincodeGolang.from_dict(_dict.get('golang'))
        if 'externalBuilders' in _dict:
            args['external_builders'] = [ConfigPeerChaincodeExternalBuildersItem.from_dict(x) for x in _dict.get('externalBuilders')]
        if 'installTimeout' in _dict:
            args['install_timeout'] = _dict.get('installTimeout')
        if 'startuptimeout' in _dict:
            args['startuptimeout'] = _dict.get('startuptimeout')
        if 'executetimeout' in _dict:
            args['executetimeout'] = _dict.get('executetimeout')
        if 'system' in _dict:
            args['system'] = ConfigPeerChaincodeSystem.from_dict(_dict.get('system'))
        if 'logging' in _dict:
            args['logging'] = ConfigPeerChaincodeLogging.from_dict(_dict.get('logging'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerChaincode object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'golang') and self.golang is not None:
            _dict['golang'] = self.golang.to_dict()
        if hasattr(self, 'external_builders') and self.external_builders is not None:
            _dict['externalBuilders'] = [x.to_dict() for x in self.external_builders]
        if hasattr(self, 'install_timeout') and self.install_timeout is not None:
            _dict['installTimeout'] = self.install_timeout
        if hasattr(self, 'startuptimeout') and self.startuptimeout is not None:
            _dict['startuptimeout'] = self.startuptimeout
        if hasattr(self, 'executetimeout') and self.executetimeout is not None:
            _dict['executetimeout'] = self.executetimeout
        if hasattr(self, 'system') and self.system is not None:
            _dict['system'] = self.system.to_dict()
        if hasattr(self, 'logging') and self.logging is not None:
            _dict['logging'] = self.logging.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerChaincode object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerChaincode') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerChaincode') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerClient():
    """
    ConfigPeerClient.

    :attr str conn_timeout: The timeout for a network connection.
    """

    def __init__(self,
                 conn_timeout: str) -> None:
        """
        Initialize a ConfigPeerClient object.

        :param str conn_timeout: The timeout for a network connection.
        """
        self.conn_timeout = conn_timeout

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerClient':
        """Initialize a ConfigPeerClient object from a json dictionary."""
        args = {}
        if 'connTimeout' in _dict:
            args['conn_timeout'] = _dict.get('connTimeout')
        else:
            raise ValueError('Required property \'connTimeout\' not present in ConfigPeerClient JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerClient object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'conn_timeout') and self.conn_timeout is not None:
            _dict['connTimeout'] = self.conn_timeout
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerClient object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerClient') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerClient') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerDeliveryclient():
    """
    ConfigPeerDeliveryclient.

    :attr str reconnect_total_time_threshold: (optional) Total time to spend
          retrying connections to ordering nodes before giving up and returning an error.
    :attr str conn_timeout: (optional) The timeout for a network connection.
    :attr str re_connect_backoff_threshold: (optional) Maximum delay between
          consecutive connection retry attempts to ordering nodes.
    :attr List[ConfigPeerDeliveryclientAddressOverridesItem] address_overrides:
          (optional) A list of orderer endpoint addresses in channel configurations that
          should be overridden. Typically used when the original orderer addresses no
          longer exist.
    """

    def __init__(self,
                 *,
                 reconnect_total_time_threshold: str = None,
                 conn_timeout: str = None,
                 re_connect_backoff_threshold: str = None,
                 address_overrides: List['ConfigPeerDeliveryclientAddressOverridesItem'] = None) -> None:
        """
        Initialize a ConfigPeerDeliveryclient object.

        :param str reconnect_total_time_threshold: (optional) Total time to spend
               retrying connections to ordering nodes before giving up and returning an
               error.
        :param str conn_timeout: (optional) The timeout for a network connection.
        :param str re_connect_backoff_threshold: (optional) Maximum delay between
               consecutive connection retry attempts to ordering nodes.
        :param List[ConfigPeerDeliveryclientAddressOverridesItem]
               address_overrides: (optional) A list of orderer endpoint addresses in
               channel configurations that should be overridden. Typically used when the
               original orderer addresses no longer exist.
        """
        self.reconnect_total_time_threshold = reconnect_total_time_threshold
        self.conn_timeout = conn_timeout
        self.re_connect_backoff_threshold = re_connect_backoff_threshold
        self.address_overrides = address_overrides

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerDeliveryclient':
        """Initialize a ConfigPeerDeliveryclient object from a json dictionary."""
        args = {}
        if 'reconnectTotalTimeThreshold' in _dict:
            args['reconnect_total_time_threshold'] = _dict.get('reconnectTotalTimeThreshold')
        if 'connTimeout' in _dict:
            args['conn_timeout'] = _dict.get('connTimeout')
        if 'reConnectBackoffThreshold' in _dict:
            args['re_connect_backoff_threshold'] = _dict.get('reConnectBackoffThreshold')
        if 'addressOverrides' in _dict:
            args['address_overrides'] = [ConfigPeerDeliveryclientAddressOverridesItem.from_dict(x) for x in _dict.get('addressOverrides')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerDeliveryclient object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'reconnect_total_time_threshold') and self.reconnect_total_time_threshold is not None:
            _dict['reconnectTotalTimeThreshold'] = self.reconnect_total_time_threshold
        if hasattr(self, 'conn_timeout') and self.conn_timeout is not None:
            _dict['connTimeout'] = self.conn_timeout
        if hasattr(self, 're_connect_backoff_threshold') and self.re_connect_backoff_threshold is not None:
            _dict['reConnectBackoffThreshold'] = self.re_connect_backoff_threshold
        if hasattr(self, 'address_overrides') and self.address_overrides is not None:
            _dict['addressOverrides'] = [x.to_dict() for x in self.address_overrides]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerDeliveryclient object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerDeliveryclient') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerDeliveryclient') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerDiscovery():
    """
    The discovery service is used by clients to query information about peers. Such as -
    which peers have joined a channel, what is the latest channel config, and what
    possible sets of peers satisfy the endorsement policy (given a smart contract and a
    channel).

    :attr bool enabled: (optional) Determines whether the discover service is
          available or not.
    :attr bool auth_cache_enabled: (optional) Determines whether the authentication
          cache is enabled or not.
    :attr float auth_cache_max_size: (optional) Maximum size of the cache. If
          exceeded a purge takes place.
    :attr float auth_cache_purge_retention_ratio: (optional) The proportion (0 - 1)
          of entries that remain in the cache after the cache is purged due to
          overpopulation.
    :attr bool org_members_allowed_access: (optional) Whether to allow non-admins to
          perform non-channel scoped queries. When `false`, it means that only peer admins
          can perform non-channel scoped queries.
    """

    def __init__(self,
                 *,
                 enabled: bool = None,
                 auth_cache_enabled: bool = None,
                 auth_cache_max_size: float = None,
                 auth_cache_purge_retention_ratio: float = None,
                 org_members_allowed_access: bool = None) -> None:
        """
        Initialize a ConfigPeerDiscovery object.

        :param bool enabled: (optional) Determines whether the discover service is
               available or not.
        :param bool auth_cache_enabled: (optional) Determines whether the
               authentication cache is enabled or not.
        :param float auth_cache_max_size: (optional) Maximum size of the cache. If
               exceeded a purge takes place.
        :param float auth_cache_purge_retention_ratio: (optional) The proportion (0
               - 1) of entries that remain in the cache after the cache is purged due to
               overpopulation.
        :param bool org_members_allowed_access: (optional) Whether to allow
               non-admins to perform non-channel scoped queries. When `false`, it means
               that only peer admins can perform non-channel scoped queries.
        """
        self.enabled = enabled
        self.auth_cache_enabled = auth_cache_enabled
        self.auth_cache_max_size = auth_cache_max_size
        self.auth_cache_purge_retention_ratio = auth_cache_purge_retention_ratio
        self.org_members_allowed_access = org_members_allowed_access

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerDiscovery':
        """Initialize a ConfigPeerDiscovery object from a json dictionary."""
        args = {}
        if 'enabled' in _dict:
            args['enabled'] = _dict.get('enabled')
        if 'authCacheEnabled' in _dict:
            args['auth_cache_enabled'] = _dict.get('authCacheEnabled')
        if 'authCacheMaxSize' in _dict:
            args['auth_cache_max_size'] = _dict.get('authCacheMaxSize')
        if 'authCachePurgeRetentionRatio' in _dict:
            args['auth_cache_purge_retention_ratio'] = _dict.get('authCachePurgeRetentionRatio')
        if 'orgMembersAllowedAccess' in _dict:
            args['org_members_allowed_access'] = _dict.get('orgMembersAllowedAccess')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerDiscovery object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'enabled') and self.enabled is not None:
            _dict['enabled'] = self.enabled
        if hasattr(self, 'auth_cache_enabled') and self.auth_cache_enabled is not None:
            _dict['authCacheEnabled'] = self.auth_cache_enabled
        if hasattr(self, 'auth_cache_max_size') and self.auth_cache_max_size is not None:
            _dict['authCacheMaxSize'] = self.auth_cache_max_size
        if hasattr(self, 'auth_cache_purge_retention_ratio') and self.auth_cache_purge_retention_ratio is not None:
            _dict['authCachePurgeRetentionRatio'] = self.auth_cache_purge_retention_ratio
        if hasattr(self, 'org_members_allowed_access') and self.org_members_allowed_access is not None:
            _dict['orgMembersAllowedAccess'] = self.org_members_allowed_access
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerDiscovery object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerDiscovery') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerDiscovery') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerGossip():
    """
    ConfigPeerGossip.

    :attr bool use_leader_election: (optional) Decides whether a peer will use a
          dynamic algorithm for "leader" selection (instead of a static leader). The
          leader is the peer that establishes a connection with the ordering service (OS).
          The leader pulls ledger blocks from the OS. It is recommended to use leader
          election for large networks of peers.
    :attr bool org_leader: (optional) Decides whether this peer should be an
          organization "leader". It maintains a connection with the ordering service and
          disseminate blocks to peers in its own organization.
    :attr str membership_tracker_interval: (optional) The frequency to poll on
          membershipTracker.
    :attr float max_block_count_to_store: (optional) Maximum number of blocks that
          can be stored in memory.
    :attr str max_propagation_burst_latency: (optional) Maximum time between
          consecutive message pushes.
    :attr float max_propagation_burst_size: (optional) Maximum number of messages
          that are stored until a push to remote peers is triggered.
    :attr float propagate_iterations: (optional) Number of times a message is pushed
          to remote peers.
    :attr str pull_interval: (optional) Determines the frequency of pull phases.
    :attr float pull_peer_num: (optional) Number of peers to pull from.
    :attr str request_state_info_interval: (optional) Determines the frequency of
          pulling stateInfo messages from peers.
    :attr str publish_state_info_interval: (optional) Determines the frequency of
          pushing stateInfo messages to peers.
    :attr str state_info_retention_interval: (optional) Maximum time a stateInfo
          message is kept.
    :attr str publish_cert_period: (optional) Time after startup to start including
          certificates in Alive messages.
    :attr bool skip_block_verification: (optional) Decides whether the peer should
          skip the verification of block messages.
    :attr str dial_timeout: (optional) The timeout for dialing a network request.
    :attr str conn_timeout: (optional) The timeout for a network connection.
    :attr float recv_buff_size: (optional) Number of received messages to hold in
          buffer.
    :attr float send_buff_size: (optional) Number of sent messages to hold in
          buffer.
    :attr str digest_wait_time: (optional) Time to wait before the pull-engine
          processes incoming digests. Should be slightly smaller than requestWaitTime.
    :attr str request_wait_time: (optional) Time to wait before pull-engine removes
          the incoming nonce. Should be slightly bigger than digestWaitTime.
    :attr str response_wait_time: (optional) Time to wait before the pull-engine
          ends.
    :attr str alive_time_interval: (optional) Alive check frequency.
    :attr str alive_expiration_timeout: (optional) Alive expiration timeout.
    :attr str reconnect_interval: (optional) Reconnect frequency.
    :attr ConfigPeerGossipElection election: (optional) Leader election service
          configuration.
    :attr ConfigPeerGossipPvtData pvt_data: (optional)
    :attr ConfigPeerGossipState state: (optional) Gossip state transfer related
          configuration.
    """

    def __init__(self,
                 *,
                 use_leader_election: bool = None,
                 org_leader: bool = None,
                 membership_tracker_interval: str = None,
                 max_block_count_to_store: float = None,
                 max_propagation_burst_latency: str = None,
                 max_propagation_burst_size: float = None,
                 propagate_iterations: float = None,
                 pull_interval: str = None,
                 pull_peer_num: float = None,
                 request_state_info_interval: str = None,
                 publish_state_info_interval: str = None,
                 state_info_retention_interval: str = None,
                 publish_cert_period: str = None,
                 skip_block_verification: bool = None,
                 dial_timeout: str = None,
                 conn_timeout: str = None,
                 recv_buff_size: float = None,
                 send_buff_size: float = None,
                 digest_wait_time: str = None,
                 request_wait_time: str = None,
                 response_wait_time: str = None,
                 alive_time_interval: str = None,
                 alive_expiration_timeout: str = None,
                 reconnect_interval: str = None,
                 election: 'ConfigPeerGossipElection' = None,
                 pvt_data: 'ConfigPeerGossipPvtData' = None,
                 state: 'ConfigPeerGossipState' = None) -> None:
        """
        Initialize a ConfigPeerGossip object.

        :param bool use_leader_election: (optional) Decides whether a peer will use
               a dynamic algorithm for "leader" selection (instead of a static leader).
               The leader is the peer that establishes a connection with the ordering
               service (OS). The leader pulls ledger blocks from the OS. It is recommended
               to use leader election for large networks of peers.
        :param bool org_leader: (optional) Decides whether this peer should be an
               organization "leader". It maintains a connection with the ordering service
               and disseminate blocks to peers in its own organization.
        :param str membership_tracker_interval: (optional) The frequency to poll on
               membershipTracker.
        :param float max_block_count_to_store: (optional) Maximum number of blocks
               that can be stored in memory.
        :param str max_propagation_burst_latency: (optional) Maximum time between
               consecutive message pushes.
        :param float max_propagation_burst_size: (optional) Maximum number of
               messages that are stored until a push to remote peers is triggered.
        :param float propagate_iterations: (optional) Number of times a message is
               pushed to remote peers.
        :param str pull_interval: (optional) Determines the frequency of pull
               phases.
        :param float pull_peer_num: (optional) Number of peers to pull from.
        :param str request_state_info_interval: (optional) Determines the frequency
               of pulling stateInfo messages from peers.
        :param str publish_state_info_interval: (optional) Determines the frequency
               of pushing stateInfo messages to peers.
        :param str state_info_retention_interval: (optional) Maximum time a
               stateInfo message is kept.
        :param str publish_cert_period: (optional) Time after startup to start
               including certificates in Alive messages.
        :param bool skip_block_verification: (optional) Decides whether the peer
               should skip the verification of block messages.
        :param str dial_timeout: (optional) The timeout for dialing a network
               request.
        :param str conn_timeout: (optional) The timeout for a network connection.
        :param float recv_buff_size: (optional) Number of received messages to hold
               in buffer.
        :param float send_buff_size: (optional) Number of sent messages to hold in
               buffer.
        :param str digest_wait_time: (optional) Time to wait before the pull-engine
               processes incoming digests. Should be slightly smaller than
               requestWaitTime.
        :param str request_wait_time: (optional) Time to wait before pull-engine
               removes the incoming nonce. Should be slightly bigger than digestWaitTime.
        :param str response_wait_time: (optional) Time to wait before the
               pull-engine ends.
        :param str alive_time_interval: (optional) Alive check frequency.
        :param str alive_expiration_timeout: (optional) Alive expiration timeout.
        :param str reconnect_interval: (optional) Reconnect frequency.
        :param ConfigPeerGossipElection election: (optional) Leader election
               service configuration.
        :param ConfigPeerGossipPvtData pvt_data: (optional)
        :param ConfigPeerGossipState state: (optional) Gossip state transfer
               related configuration.
        """
        self.use_leader_election = use_leader_election
        self.org_leader = org_leader
        self.membership_tracker_interval = membership_tracker_interval
        self.max_block_count_to_store = max_block_count_to_store
        self.max_propagation_burst_latency = max_propagation_burst_latency
        self.max_propagation_burst_size = max_propagation_burst_size
        self.propagate_iterations = propagate_iterations
        self.pull_interval = pull_interval
        self.pull_peer_num = pull_peer_num
        self.request_state_info_interval = request_state_info_interval
        self.publish_state_info_interval = publish_state_info_interval
        self.state_info_retention_interval = state_info_retention_interval
        self.publish_cert_period = publish_cert_period
        self.skip_block_verification = skip_block_verification
        self.dial_timeout = dial_timeout
        self.conn_timeout = conn_timeout
        self.recv_buff_size = recv_buff_size
        self.send_buff_size = send_buff_size
        self.digest_wait_time = digest_wait_time
        self.request_wait_time = request_wait_time
        self.response_wait_time = response_wait_time
        self.alive_time_interval = alive_time_interval
        self.alive_expiration_timeout = alive_expiration_timeout
        self.reconnect_interval = reconnect_interval
        self.election = election
        self.pvt_data = pvt_data
        self.state = state

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerGossip':
        """Initialize a ConfigPeerGossip object from a json dictionary."""
        args = {}
        if 'useLeaderElection' in _dict:
            args['use_leader_election'] = _dict.get('useLeaderElection')
        if 'orgLeader' in _dict:
            args['org_leader'] = _dict.get('orgLeader')
        if 'membershipTrackerInterval' in _dict:
            args['membership_tracker_interval'] = _dict.get('membershipTrackerInterval')
        if 'maxBlockCountToStore' in _dict:
            args['max_block_count_to_store'] = _dict.get('maxBlockCountToStore')
        if 'maxPropagationBurstLatency' in _dict:
            args['max_propagation_burst_latency'] = _dict.get('maxPropagationBurstLatency')
        if 'maxPropagationBurstSize' in _dict:
            args['max_propagation_burst_size'] = _dict.get('maxPropagationBurstSize')
        if 'propagateIterations' in _dict:
            args['propagate_iterations'] = _dict.get('propagateIterations')
        if 'pullInterval' in _dict:
            args['pull_interval'] = _dict.get('pullInterval')
        if 'pullPeerNum' in _dict:
            args['pull_peer_num'] = _dict.get('pullPeerNum')
        if 'requestStateInfoInterval' in _dict:
            args['request_state_info_interval'] = _dict.get('requestStateInfoInterval')
        if 'publishStateInfoInterval' in _dict:
            args['publish_state_info_interval'] = _dict.get('publishStateInfoInterval')
        if 'stateInfoRetentionInterval' in _dict:
            args['state_info_retention_interval'] = _dict.get('stateInfoRetentionInterval')
        if 'publishCertPeriod' in _dict:
            args['publish_cert_period'] = _dict.get('publishCertPeriod')
        if 'skipBlockVerification' in _dict:
            args['skip_block_verification'] = _dict.get('skipBlockVerification')
        if 'dialTimeout' in _dict:
            args['dial_timeout'] = _dict.get('dialTimeout')
        if 'connTimeout' in _dict:
            args['conn_timeout'] = _dict.get('connTimeout')
        if 'recvBuffSize' in _dict:
            args['recv_buff_size'] = _dict.get('recvBuffSize')
        if 'sendBuffSize' in _dict:
            args['send_buff_size'] = _dict.get('sendBuffSize')
        if 'digestWaitTime' in _dict:
            args['digest_wait_time'] = _dict.get('digestWaitTime')
        if 'requestWaitTime' in _dict:
            args['request_wait_time'] = _dict.get('requestWaitTime')
        if 'responseWaitTime' in _dict:
            args['response_wait_time'] = _dict.get('responseWaitTime')
        if 'aliveTimeInterval' in _dict:
            args['alive_time_interval'] = _dict.get('aliveTimeInterval')
        if 'aliveExpirationTimeout' in _dict:
            args['alive_expiration_timeout'] = _dict.get('aliveExpirationTimeout')
        if 'reconnectInterval' in _dict:
            args['reconnect_interval'] = _dict.get('reconnectInterval')
        if 'election' in _dict:
            args['election'] = ConfigPeerGossipElection.from_dict(_dict.get('election'))
        if 'pvtData' in _dict:
            args['pvt_data'] = ConfigPeerGossipPvtData.from_dict(_dict.get('pvtData'))
        if 'state' in _dict:
            args['state'] = ConfigPeerGossipState.from_dict(_dict.get('state'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerGossip object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'use_leader_election') and self.use_leader_election is not None:
            _dict['useLeaderElection'] = self.use_leader_election
        if hasattr(self, 'org_leader') and self.org_leader is not None:
            _dict['orgLeader'] = self.org_leader
        if hasattr(self, 'membership_tracker_interval') and self.membership_tracker_interval is not None:
            _dict['membershipTrackerInterval'] = self.membership_tracker_interval
        if hasattr(self, 'max_block_count_to_store') and self.max_block_count_to_store is not None:
            _dict['maxBlockCountToStore'] = self.max_block_count_to_store
        if hasattr(self, 'max_propagation_burst_latency') and self.max_propagation_burst_latency is not None:
            _dict['maxPropagationBurstLatency'] = self.max_propagation_burst_latency
        if hasattr(self, 'max_propagation_burst_size') and self.max_propagation_burst_size is not None:
            _dict['maxPropagationBurstSize'] = self.max_propagation_burst_size
        if hasattr(self, 'propagate_iterations') and self.propagate_iterations is not None:
            _dict['propagateIterations'] = self.propagate_iterations
        if hasattr(self, 'pull_interval') and self.pull_interval is not None:
            _dict['pullInterval'] = self.pull_interval
        if hasattr(self, 'pull_peer_num') and self.pull_peer_num is not None:
            _dict['pullPeerNum'] = self.pull_peer_num
        if hasattr(self, 'request_state_info_interval') and self.request_state_info_interval is not None:
            _dict['requestStateInfoInterval'] = self.request_state_info_interval
        if hasattr(self, 'publish_state_info_interval') and self.publish_state_info_interval is not None:
            _dict['publishStateInfoInterval'] = self.publish_state_info_interval
        if hasattr(self, 'state_info_retention_interval') and self.state_info_retention_interval is not None:
            _dict['stateInfoRetentionInterval'] = self.state_info_retention_interval
        if hasattr(self, 'publish_cert_period') and self.publish_cert_period is not None:
            _dict['publishCertPeriod'] = self.publish_cert_period
        if hasattr(self, 'skip_block_verification') and self.skip_block_verification is not None:
            _dict['skipBlockVerification'] = self.skip_block_verification
        if hasattr(self, 'dial_timeout') and self.dial_timeout is not None:
            _dict['dialTimeout'] = self.dial_timeout
        if hasattr(self, 'conn_timeout') and self.conn_timeout is not None:
            _dict['connTimeout'] = self.conn_timeout
        if hasattr(self, 'recv_buff_size') and self.recv_buff_size is not None:
            _dict['recvBuffSize'] = self.recv_buff_size
        if hasattr(self, 'send_buff_size') and self.send_buff_size is not None:
            _dict['sendBuffSize'] = self.send_buff_size
        if hasattr(self, 'digest_wait_time') and self.digest_wait_time is not None:
            _dict['digestWaitTime'] = self.digest_wait_time
        if hasattr(self, 'request_wait_time') and self.request_wait_time is not None:
            _dict['requestWaitTime'] = self.request_wait_time
        if hasattr(self, 'response_wait_time') and self.response_wait_time is not None:
            _dict['responseWaitTime'] = self.response_wait_time
        if hasattr(self, 'alive_time_interval') and self.alive_time_interval is not None:
            _dict['aliveTimeInterval'] = self.alive_time_interval
        if hasattr(self, 'alive_expiration_timeout') and self.alive_expiration_timeout is not None:
            _dict['aliveExpirationTimeout'] = self.alive_expiration_timeout
        if hasattr(self, 'reconnect_interval') and self.reconnect_interval is not None:
            _dict['reconnectInterval'] = self.reconnect_interval
        if hasattr(self, 'election') and self.election is not None:
            _dict['election'] = self.election.to_dict()
        if hasattr(self, 'pvt_data') and self.pvt_data is not None:
            _dict['pvtData'] = self.pvt_data.to_dict()
        if hasattr(self, 'state') and self.state is not None:
            _dict['state'] = self.state.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerGossip object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerGossip') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerGossip') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerKeepalive():
    """
    Keep alive settings between the peer server and clients.

    :attr str min_interval: (optional) The minimum time between client pings. If a
          client sends pings more frequently the server disconnects from the client.
    :attr ConfigPeerKeepaliveClient client: (optional)
    :attr ConfigPeerKeepaliveDeliveryClient delivery_client: (optional)
    """

    def __init__(self,
                 *,
                 min_interval: str = None,
                 client: 'ConfigPeerKeepaliveClient' = None,
                 delivery_client: 'ConfigPeerKeepaliveDeliveryClient' = None) -> None:
        """
        Initialize a ConfigPeerKeepalive object.

        :param str min_interval: (optional) The minimum time between client pings.
               If a client sends pings more frequently the server disconnects from the
               client.
        :param ConfigPeerKeepaliveClient client: (optional)
        :param ConfigPeerKeepaliveDeliveryClient delivery_client: (optional)
        """
        self.min_interval = min_interval
        self.client = client
        self.delivery_client = delivery_client

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerKeepalive':
        """Initialize a ConfigPeerKeepalive object from a json dictionary."""
        args = {}
        if 'minInterval' in _dict:
            args['min_interval'] = _dict.get('minInterval')
        if 'client' in _dict:
            args['client'] = ConfigPeerKeepaliveClient.from_dict(_dict.get('client'))
        if 'deliveryClient' in _dict:
            args['delivery_client'] = ConfigPeerKeepaliveDeliveryClient.from_dict(_dict.get('deliveryClient'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerKeepalive object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'min_interval') and self.min_interval is not None:
            _dict['minInterval'] = self.min_interval
        if hasattr(self, 'client') and self.client is not None:
            _dict['client'] = self.client.to_dict()
        if hasattr(self, 'delivery_client') and self.delivery_client is not None:
            _dict['deliveryClient'] = self.delivery_client.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerKeepalive object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerKeepalive') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerKeepalive') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ConfigPeerLimits():
    """
    ConfigPeerLimits.

    :attr ConfigPeerLimitsConcurrency concurrency: (optional)
    """

    def __init__(self,
                 *,
                 concurrency: 'ConfigPeerLimitsConcurrency' = None) -> None:
        """
        Initialize a ConfigPeerLimits object.

        :param ConfigPeerLimitsConcurrency concurrency: (optional)
        """
        self.concurrency = concurrency

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ConfigPeerLimits':
        """Initialize a ConfigPeerLimits object from a json dictionary."""
        args = {}
        if 'concurrency' in _dict:
            args['concurrency'] = ConfigPeerLimitsConcurrency.from_dict(_dict.get('concurrency'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ConfigPeerLimits object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'concurrency') and self.concurrency is not None:
            _dict['concurrency'] = self.concurrency.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ConfigPeerLimits object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ConfigPeerLimits') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ConfigPeerLimits') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CpuHealthStats():
    """
    CpuHealthStats.

    :attr str model: (optional) Model of CPU core.
    :attr float speed: (optional) Speed of core in MHz.
    :attr CpuHealthStatsTimes times: (optional)
    """

    def __init__(self,
                 *,
                 model: str = None,
                 speed: float = None,
                 times: 'CpuHealthStatsTimes' = None) -> None:
        """
        Initialize a CpuHealthStats object.

        :param str model: (optional) Model of CPU core.
        :param float speed: (optional) Speed of core in MHz.
        :param CpuHealthStatsTimes times: (optional)
        """
        self.model = model
        self.speed = speed
        self.times = times

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CpuHealthStats':
        """Initialize a CpuHealthStats object from a json dictionary."""
        args = {}
        if 'model' in _dict:
            args['model'] = _dict.get('model')
        if 'speed' in _dict:
            args['speed'] = _dict.get('speed')
        if 'times' in _dict:
            args['times'] = CpuHealthStatsTimes.from_dict(_dict.get('times'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CpuHealthStats object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'model') and self.model is not None:
            _dict['model'] = self.model
        if hasattr(self, 'speed') and self.speed is not None:
            _dict['speed'] = self.speed
        if hasattr(self, 'times') and self.times is not None:
            _dict['times'] = self.times.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CpuHealthStats object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CpuHealthStats') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CpuHealthStats') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CpuHealthStatsTimes():
    """
    CpuHealthStatsTimes.

    :attr float idle: (optional) ms CPU is in idle.
    :attr float irq: (optional) ms CPU is in irq.
    :attr float nice: (optional) ms CPU is in nice.
    :attr float sys: (optional) ms CPU is in sys.
    :attr float user: (optional) ms CPU is in user.
    """

    def __init__(self,
                 *,
                 idle: float = None,
                 irq: float = None,
                 nice: float = None,
                 sys: float = None,
                 user: float = None) -> None:
        """
        Initialize a CpuHealthStatsTimes object.

        :param float idle: (optional) ms CPU is in idle.
        :param float irq: (optional) ms CPU is in irq.
        :param float nice: (optional) ms CPU is in nice.
        :param float sys: (optional) ms CPU is in sys.
        :param float user: (optional) ms CPU is in user.
        """
        self.idle = idle
        self.irq = irq
        self.nice = nice
        self.sys = sys
        self.user = user

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CpuHealthStatsTimes':
        """Initialize a CpuHealthStatsTimes object from a json dictionary."""
        args = {}
        if 'idle' in _dict:
            args['idle'] = _dict.get('idle')
        if 'irq' in _dict:
            args['irq'] = _dict.get('irq')
        if 'nice' in _dict:
            args['nice'] = _dict.get('nice')
        if 'sys' in _dict:
            args['sys'] = _dict.get('sys')
        if 'user' in _dict:
            args['user'] = _dict.get('user')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CpuHealthStatsTimes object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'idle') and self.idle is not None:
            _dict['idle'] = self.idle
        if hasattr(self, 'irq') and self.irq is not None:
            _dict['irq'] = self.irq
        if hasattr(self, 'nice') and self.nice is not None:
            _dict['nice'] = self.nice
        if hasattr(self, 'sys') and self.sys is not None:
            _dict['sys'] = self.sys
        if hasattr(self, 'user') and self.user is not None:
            _dict['user'] = self.user
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CpuHealthStatsTimes object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CpuHealthStatsTimes') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CpuHealthStatsTimes') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CreateCaBodyConfigOverride():
    """
    Set `config_override` to create the root/initial enroll id and enroll secret as well
    as enabling custom CA configurations (such as using postgres). See the [Fabric CA
    configuration
    file](https://hyperledger-fabric-ca.readthedocs.io/en/release-1.4/serverconfig.html)
    for more information about each parameter.
    The field `tlsca` is optional. The IBP console will copy the value of
    `config_override.ca` into `config_override.tlsca` if `config_override.tlsca` is
    omitted (which is recommended).
    *The nested field **names** below are not case-sensitive.*.

    :attr ConfigCACreate ca:
    :attr ConfigCACreate tlsca: (optional)
    """

    def __init__(self,
                 ca: 'ConfigCACreate',
                 *,
                 tlsca: 'ConfigCACreate' = None) -> None:
        """
        Initialize a CreateCaBodyConfigOverride object.

        :param ConfigCACreate ca:
        :param ConfigCACreate tlsca: (optional)
        """
        self.ca = ca
        self.tlsca = tlsca

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CreateCaBodyConfigOverride':
        """Initialize a CreateCaBodyConfigOverride object from a json dictionary."""
        args = {}
        if 'ca' in _dict:
            args['ca'] = ConfigCACreate.from_dict(_dict.get('ca'))
        else:
            raise ValueError('Required property \'ca\' not present in CreateCaBodyConfigOverride JSON')
        if 'tlsca' in _dict:
            args['tlsca'] = ConfigCACreate.from_dict(_dict.get('tlsca'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CreateCaBodyConfigOverride object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        if hasattr(self, 'tlsca') and self.tlsca is not None:
            _dict['tlsca'] = self.tlsca.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CreateCaBodyConfigOverride object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CreateCaBodyConfigOverride') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CreateCaBodyConfigOverride') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CreateCaBodyResources():
    """
    CPU and memory properties. This feature is not available if using a free Kubernetes
    cluster.

    :attr ResourceObject ca: This field requires the use of Fabric v1.4.* and
          higher.
    """

    def __init__(self,
                 ca: 'ResourceObject') -> None:
        """
        Initialize a CreateCaBodyResources object.

        :param ResourceObject ca: This field requires the use of Fabric v1.4.* and
               higher.
        """
        self.ca = ca

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CreateCaBodyResources':
        """Initialize a CreateCaBodyResources object from a json dictionary."""
        args = {}
        if 'ca' in _dict:
            args['ca'] = ResourceObject.from_dict(_dict.get('ca'))
        else:
            raise ValueError('Required property \'ca\' not present in CreateCaBodyResources JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CreateCaBodyResources object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CreateCaBodyResources object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CreateCaBodyResources') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CreateCaBodyResources') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CreateCaBodyStorage():
    """
    Disk space properties. This feature is not available if using a free Kubernetes
    cluster.

    :attr StorageObject ca:
    """

    def __init__(self,
                 ca: 'StorageObject') -> None:
        """
        Initialize a CreateCaBodyStorage object.

        :param StorageObject ca:
        """
        self.ca = ca

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CreateCaBodyStorage':
        """Initialize a CreateCaBodyStorage object from a json dictionary."""
        args = {}
        if 'ca' in _dict:
            args['ca'] = StorageObject.from_dict(_dict.get('ca'))
        else:
            raise ValueError('Required property \'ca\' not present in CreateCaBodyStorage JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CreateCaBodyStorage object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CreateCaBodyStorage object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CreateCaBodyStorage') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CreateCaBodyStorage') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CreateOrdererRaftBodyResources():
    """
    CPU and memory properties. This feature is not available if using a free Kubernetes
    cluster.

    :attr ResourceObject orderer: This field requires the use of Fabric v1.4.* and
          higher.
    :attr ResourceObject proxy: (optional) This field requires the use of Fabric
          v1.4.* and higher.
    """

    def __init__(self,
                 orderer: 'ResourceObject',
                 *,
                 proxy: 'ResourceObject' = None) -> None:
        """
        Initialize a CreateOrdererRaftBodyResources object.

        :param ResourceObject orderer: This field requires the use of Fabric v1.4.*
               and higher.
        :param ResourceObject proxy: (optional) This field requires the use of
               Fabric v1.4.* and higher.
        """
        self.orderer = orderer
        self.proxy = proxy

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CreateOrdererRaftBodyResources':
        """Initialize a CreateOrdererRaftBodyResources object from a json dictionary."""
        args = {}
        if 'orderer' in _dict:
            args['orderer'] = ResourceObject.from_dict(_dict.get('orderer'))
        else:
            raise ValueError('Required property \'orderer\' not present in CreateOrdererRaftBodyResources JSON')
        if 'proxy' in _dict:
            args['proxy'] = ResourceObject.from_dict(_dict.get('proxy'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CreateOrdererRaftBodyResources object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'orderer') and self.orderer is not None:
            _dict['orderer'] = self.orderer.to_dict()
        if hasattr(self, 'proxy') and self.proxy is not None:
            _dict['proxy'] = self.proxy.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CreateOrdererRaftBodyResources object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CreateOrdererRaftBodyResources') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CreateOrdererRaftBodyResources') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CreateOrdererRaftBodyStorage():
    """
    Disk space properties. This feature is not available if using a free Kubernetes
    cluster.

    :attr StorageObject orderer:
    """

    def __init__(self,
                 orderer: 'StorageObject') -> None:
        """
        Initialize a CreateOrdererRaftBodyStorage object.

        :param StorageObject orderer:
        """
        self.orderer = orderer

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CreateOrdererRaftBodyStorage':
        """Initialize a CreateOrdererRaftBodyStorage object from a json dictionary."""
        args = {}
        if 'orderer' in _dict:
            args['orderer'] = StorageObject.from_dict(_dict.get('orderer'))
        else:
            raise ValueError('Required property \'orderer\' not present in CreateOrdererRaftBodyStorage JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CreateOrdererRaftBodyStorage object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'orderer') and self.orderer is not None:
            _dict['orderer'] = self.orderer.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CreateOrdererRaftBodyStorage object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CreateOrdererRaftBodyStorage') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CreateOrdererRaftBodyStorage') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CreatePeerBodyStorage():
    """
    Disk space properties. This feature is not available if using a free Kubernetes
    cluster.

    :attr StorageObject peer:
    :attr StorageObject statedb: (optional)
    """

    def __init__(self,
                 peer: 'StorageObject',
                 *,
                 statedb: 'StorageObject' = None) -> None:
        """
        Initialize a CreatePeerBodyStorage object.

        :param StorageObject peer:
        :param StorageObject statedb: (optional)
        """
        self.peer = peer
        self.statedb = statedb

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CreatePeerBodyStorage':
        """Initialize a CreatePeerBodyStorage object from a json dictionary."""
        args = {}
        if 'peer' in _dict:
            args['peer'] = StorageObject.from_dict(_dict.get('peer'))
        else:
            raise ValueError('Required property \'peer\' not present in CreatePeerBodyStorage JSON')
        if 'statedb' in _dict:
            args['statedb'] = StorageObject.from_dict(_dict.get('statedb'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CreatePeerBodyStorage object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'peer') and self.peer is not None:
            _dict['peer'] = self.peer.to_dict()
        if hasattr(self, 'statedb') and self.statedb is not None:
            _dict['statedb'] = self.statedb.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CreatePeerBodyStorage object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CreatePeerBodyStorage') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CreatePeerBodyStorage') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CryptoEnrollmentComponent():
    """
    CryptoEnrollmentComponent.

    :attr List[str] admincerts: (optional) An array that contains base 64 encoded
          PEM identity certificates for administrators. Also known as signing certificates
          of an organization administrator.
    """

    def __init__(self,
                 *,
                 admincerts: List[str] = None) -> None:
        """
        Initialize a CryptoEnrollmentComponent object.

        :param List[str] admincerts: (optional) An array that contains base 64
               encoded PEM identity certificates for administrators. Also known as signing
               certificates of an organization administrator.
        """
        self.admincerts = admincerts

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CryptoEnrollmentComponent':
        """Initialize a CryptoEnrollmentComponent object from a json dictionary."""
        args = {}
        if 'admincerts' in _dict:
            args['admincerts'] = _dict.get('admincerts')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CryptoEnrollmentComponent object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'admincerts') and self.admincerts is not None:
            _dict['admincerts'] = self.admincerts
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CryptoEnrollmentComponent object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CryptoEnrollmentComponent') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CryptoEnrollmentComponent') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CryptoObject():
    """
    See this [topic](/docs/blockchain?topic=blockchain-ibp-v2-apis#ibp-v2-apis-config) for
    instructions on how to build a crypto object.

    :attr CryptoObjectEnrollment enrollment: (optional) This `enrollment` field
          contains data that allows a component to enroll an identity for itself. Use
          `enrollment` or `msp`, not both.
    :attr CryptoObjectMsp msp: (optional) The `msp` field contains data to allow a
          component to configure its MSP with an already enrolled identity. Use `msp` or
          `enrollment`, not both.
    """

    def __init__(self,
                 *,
                 enrollment: 'CryptoObjectEnrollment' = None,
                 msp: 'CryptoObjectMsp' = None) -> None:
        """
        Initialize a CryptoObject object.

        :param CryptoObjectEnrollment enrollment: (optional) This `enrollment`
               field contains data that allows a component to enroll an identity for
               itself. Use `enrollment` or `msp`, not both.
        :param CryptoObjectMsp msp: (optional) The `msp` field contains data to
               allow a component to configure its MSP with an already enrolled identity.
               Use `msp` or `enrollment`, not both.
        """
        self.enrollment = enrollment
        self.msp = msp

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CryptoObject':
        """Initialize a CryptoObject object from a json dictionary."""
        args = {}
        if 'enrollment' in _dict:
            args['enrollment'] = CryptoObjectEnrollment.from_dict(_dict.get('enrollment'))
        if 'msp' in _dict:
            args['msp'] = CryptoObjectMsp.from_dict(_dict.get('msp'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CryptoObject object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'enrollment') and self.enrollment is not None:
            _dict['enrollment'] = self.enrollment.to_dict()
        if hasattr(self, 'msp') and self.msp is not None:
            _dict['msp'] = self.msp.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CryptoObject object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CryptoObject') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CryptoObject') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CryptoObjectEnrollment():
    """
    This `enrollment` field contains data that allows a component to enroll an identity
    for itself. Use `enrollment` or `msp`, not both.

    :attr CryptoEnrollmentComponent component:
    :attr CryptoObjectEnrollmentCa ca:
    :attr CryptoObjectEnrollmentTlsca tlsca:
    """

    def __init__(self,
                 component: 'CryptoEnrollmentComponent',
                 ca: 'CryptoObjectEnrollmentCa',
                 tlsca: 'CryptoObjectEnrollmentTlsca') -> None:
        """
        Initialize a CryptoObjectEnrollment object.

        :param CryptoEnrollmentComponent component:
        :param CryptoObjectEnrollmentCa ca:
        :param CryptoObjectEnrollmentTlsca tlsca:
        """
        self.component = component
        self.ca = ca
        self.tlsca = tlsca

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CryptoObjectEnrollment':
        """Initialize a CryptoObjectEnrollment object from a json dictionary."""
        args = {}
        if 'component' in _dict:
            args['component'] = CryptoEnrollmentComponent.from_dict(_dict.get('component'))
        else:
            raise ValueError('Required property \'component\' not present in CryptoObjectEnrollment JSON')
        if 'ca' in _dict:
            args['ca'] = CryptoObjectEnrollmentCa.from_dict(_dict.get('ca'))
        else:
            raise ValueError('Required property \'ca\' not present in CryptoObjectEnrollment JSON')
        if 'tlsca' in _dict:
            args['tlsca'] = CryptoObjectEnrollmentTlsca.from_dict(_dict.get('tlsca'))
        else:
            raise ValueError('Required property \'tlsca\' not present in CryptoObjectEnrollment JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CryptoObjectEnrollment object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'component') and self.component is not None:
            _dict['component'] = self.component.to_dict()
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        if hasattr(self, 'tlsca') and self.tlsca is not None:
            _dict['tlsca'] = self.tlsca.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CryptoObjectEnrollment object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CryptoObjectEnrollment') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CryptoObjectEnrollment') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CryptoObjectEnrollmentCa():
    """
    CryptoObjectEnrollmentCa.

    :attr str host: The CA's hostname. Do not include protocol or port.
    :attr float port: The CA's port.
    :attr str name: The CA's "CAName" attribute. This name is used to distinguish
          this CA from the TLS CA.
    :attr str tls_cert: The TLS certificate as base 64 encoded PEM. Certificate is
          used to secure/validate a TLS connection with this component.
    :attr str enroll_id: The username of the enroll id.
    :attr str enroll_secret: The password of the enroll id.
    """

    def __init__(self,
                 host: str,
                 port: float,
                 name: str,
                 tls_cert: str,
                 enroll_id: str,
                 enroll_secret: str) -> None:
        """
        Initialize a CryptoObjectEnrollmentCa object.

        :param str host: The CA's hostname. Do not include protocol or port.
        :param float port: The CA's port.
        :param str name: The CA's "CAName" attribute. This name is used to
               distinguish this CA from the TLS CA.
        :param str tls_cert: The TLS certificate as base 64 encoded PEM.
               Certificate is used to secure/validate a TLS connection with this
               component.
        :param str enroll_id: The username of the enroll id.
        :param str enroll_secret: The password of the enroll id.
        """
        self.host = host
        self.port = port
        self.name = name
        self.tls_cert = tls_cert
        self.enroll_id = enroll_id
        self.enroll_secret = enroll_secret

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CryptoObjectEnrollmentCa':
        """Initialize a CryptoObjectEnrollmentCa object from a json dictionary."""
        args = {}
        if 'host' in _dict:
            args['host'] = _dict.get('host')
        else:
            raise ValueError('Required property \'host\' not present in CryptoObjectEnrollmentCa JSON')
        if 'port' in _dict:
            args['port'] = _dict.get('port')
        else:
            raise ValueError('Required property \'port\' not present in CryptoObjectEnrollmentCa JSON')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        else:
            raise ValueError('Required property \'name\' not present in CryptoObjectEnrollmentCa JSON')
        if 'tls_cert' in _dict:
            args['tls_cert'] = _dict.get('tls_cert')
        else:
            raise ValueError('Required property \'tls_cert\' not present in CryptoObjectEnrollmentCa JSON')
        if 'enroll_id' in _dict:
            args['enroll_id'] = _dict.get('enroll_id')
        else:
            raise ValueError('Required property \'enroll_id\' not present in CryptoObjectEnrollmentCa JSON')
        if 'enroll_secret' in _dict:
            args['enroll_secret'] = _dict.get('enroll_secret')
        else:
            raise ValueError('Required property \'enroll_secret\' not present in CryptoObjectEnrollmentCa JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CryptoObjectEnrollmentCa object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'host') and self.host is not None:
            _dict['host'] = self.host
        if hasattr(self, 'port') and self.port is not None:
            _dict['port'] = self.port
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'tls_cert') and self.tls_cert is not None:
            _dict['tls_cert'] = self.tls_cert
        if hasattr(self, 'enroll_id') and self.enroll_id is not None:
            _dict['enroll_id'] = self.enroll_id
        if hasattr(self, 'enroll_secret') and self.enroll_secret is not None:
            _dict['enroll_secret'] = self.enroll_secret
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CryptoObjectEnrollmentCa object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CryptoObjectEnrollmentCa') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CryptoObjectEnrollmentCa') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CryptoObjectEnrollmentTlsca():
    """
    CryptoObjectEnrollmentTlsca.

    :attr str host: The CA's hostname. Do not include protocol or port.
    :attr float port: The CA's port.
    :attr str name: The TLS CA's "CAName" attribute. This name is used to
          distinguish this TLS CA from the other CA.
    :attr str tls_cert: The TLS certificate as base 64 encoded PEM. Certificate is
          used to secure/validate a TLS connection with this component.
    :attr str enroll_id: The username of the enroll id.
    :attr str enroll_secret: The password of the enroll id.
    :attr List[str] csr_hosts: (optional)
    """

    def __init__(self,
                 host: str,
                 port: float,
                 name: str,
                 tls_cert: str,
                 enroll_id: str,
                 enroll_secret: str,
                 *,
                 csr_hosts: List[str] = None) -> None:
        """
        Initialize a CryptoObjectEnrollmentTlsca object.

        :param str host: The CA's hostname. Do not include protocol or port.
        :param float port: The CA's port.
        :param str name: The TLS CA's "CAName" attribute. This name is used to
               distinguish this TLS CA from the other CA.
        :param str tls_cert: The TLS certificate as base 64 encoded PEM.
               Certificate is used to secure/validate a TLS connection with this
               component.
        :param str enroll_id: The username of the enroll id.
        :param str enroll_secret: The password of the enroll id.
        :param List[str] csr_hosts: (optional)
        """
        self.host = host
        self.port = port
        self.name = name
        self.tls_cert = tls_cert
        self.enroll_id = enroll_id
        self.enroll_secret = enroll_secret
        self.csr_hosts = csr_hosts

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CryptoObjectEnrollmentTlsca':
        """Initialize a CryptoObjectEnrollmentTlsca object from a json dictionary."""
        args = {}
        if 'host' in _dict:
            args['host'] = _dict.get('host')
        else:
            raise ValueError('Required property \'host\' not present in CryptoObjectEnrollmentTlsca JSON')
        if 'port' in _dict:
            args['port'] = _dict.get('port')
        else:
            raise ValueError('Required property \'port\' not present in CryptoObjectEnrollmentTlsca JSON')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        else:
            raise ValueError('Required property \'name\' not present in CryptoObjectEnrollmentTlsca JSON')
        if 'tls_cert' in _dict:
            args['tls_cert'] = _dict.get('tls_cert')
        else:
            raise ValueError('Required property \'tls_cert\' not present in CryptoObjectEnrollmentTlsca JSON')
        if 'enroll_id' in _dict:
            args['enroll_id'] = _dict.get('enroll_id')
        else:
            raise ValueError('Required property \'enroll_id\' not present in CryptoObjectEnrollmentTlsca JSON')
        if 'enroll_secret' in _dict:
            args['enroll_secret'] = _dict.get('enroll_secret')
        else:
            raise ValueError('Required property \'enroll_secret\' not present in CryptoObjectEnrollmentTlsca JSON')
        if 'csr_hosts' in _dict:
            args['csr_hosts'] = _dict.get('csr_hosts')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CryptoObjectEnrollmentTlsca object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'host') and self.host is not None:
            _dict['host'] = self.host
        if hasattr(self, 'port') and self.port is not None:
            _dict['port'] = self.port
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'tls_cert') and self.tls_cert is not None:
            _dict['tls_cert'] = self.tls_cert
        if hasattr(self, 'enroll_id') and self.enroll_id is not None:
            _dict['enroll_id'] = self.enroll_id
        if hasattr(self, 'enroll_secret') and self.enroll_secret is not None:
            _dict['enroll_secret'] = self.enroll_secret
        if hasattr(self, 'csr_hosts') and self.csr_hosts is not None:
            _dict['csr_hosts'] = self.csr_hosts
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CryptoObjectEnrollmentTlsca object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CryptoObjectEnrollmentTlsca') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CryptoObjectEnrollmentTlsca') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class CryptoObjectMsp():
    """
    The `msp` field contains data to allow a component to configure its MSP with an
    already enrolled identity. Use `msp` or `enrollment`, not both.

    :attr MspCryptoComp component:
    :attr MspCryptoCa ca:
    :attr MspCryptoCa tlsca:
    """

    def __init__(self,
                 component: 'MspCryptoComp',
                 ca: 'MspCryptoCa',
                 tlsca: 'MspCryptoCa') -> None:
        """
        Initialize a CryptoObjectMsp object.

        :param MspCryptoComp component:
        :param MspCryptoCa ca:
        :param MspCryptoCa tlsca:
        """
        self.component = component
        self.ca = ca
        self.tlsca = tlsca

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CryptoObjectMsp':
        """Initialize a CryptoObjectMsp object from a json dictionary."""
        args = {}
        if 'component' in _dict:
            args['component'] = MspCryptoComp.from_dict(_dict.get('component'))
        else:
            raise ValueError('Required property \'component\' not present in CryptoObjectMsp JSON')
        if 'ca' in _dict:
            args['ca'] = MspCryptoCa.from_dict(_dict.get('ca'))
        else:
            raise ValueError('Required property \'ca\' not present in CryptoObjectMsp JSON')
        if 'tlsca' in _dict:
            args['tlsca'] = MspCryptoCa.from_dict(_dict.get('tlsca'))
        else:
            raise ValueError('Required property \'tlsca\' not present in CryptoObjectMsp JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CryptoObjectMsp object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'component') and self.component is not None:
            _dict['component'] = self.component.to_dict()
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        if hasattr(self, 'tlsca') and self.tlsca is not None:
            _dict['tlsca'] = self.tlsca.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CryptoObjectMsp object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'CryptoObjectMsp') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CryptoObjectMsp') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class DeleteAllNotificationsResponse():
    """
    DeleteAllNotificationsResponse.

    :attr str message: (optional) Response message. "ok" indicates the api completed
          successfully.
    :attr str details: (optional) Text showing what was deleted.
    """

    def __init__(self,
                 *,
                 message: str = None,
                 details: str = None) -> None:
        """
        Initialize a DeleteAllNotificationsResponse object.

        :param str message: (optional) Response message. "ok" indicates the api
               completed successfully.
        :param str details: (optional) Text showing what was deleted.
        """
        self.message = message
        self.details = details

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'DeleteAllNotificationsResponse':
        """Initialize a DeleteAllNotificationsResponse object from a json dictionary."""
        args = {}
        if 'message' in _dict:
            args['message'] = _dict.get('message')
        if 'details' in _dict:
            args['details'] = _dict.get('details')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a DeleteAllNotificationsResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'message') and self.message is not None:
            _dict['message'] = self.message
        if hasattr(self, 'details') and self.details is not None:
            _dict['details'] = self.details
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this DeleteAllNotificationsResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'DeleteAllNotificationsResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'DeleteAllNotificationsResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class DeleteAllSessionsResponse():
    """
    DeleteAllSessionsResponse.

    :attr str message: (optional) Response message. Indicates the api completed
          successfully.
    """

    def __init__(self,
                 *,
                 message: str = None) -> None:
        """
        Initialize a DeleteAllSessionsResponse object.

        :param str message: (optional) Response message. Indicates the api
               completed successfully.
        """
        self.message = message

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'DeleteAllSessionsResponse':
        """Initialize a DeleteAllSessionsResponse object from a json dictionary."""
        args = {}
        if 'message' in _dict:
            args['message'] = _dict.get('message')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a DeleteAllSessionsResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'message') and self.message is not None:
            _dict['message'] = self.message
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this DeleteAllSessionsResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'DeleteAllSessionsResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'DeleteAllSessionsResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class DeleteComponentResponse():
    """
    DeleteComponentResponse.

    :attr str message: (optional)
    :attr str type: (optional) The type of this component. Such as: "fabric-peer",
          "fabric-ca", "fabric-orderer", etc.
    :attr str id: (optional) The unique identifier of this component.
    :attr str display_name: (optional) A descriptive name for this peer. The IBP
          console tile displays this name.
    """

    def __init__(self,
                 *,
                 message: str = None,
                 type: str = None,
                 id: str = None,
                 display_name: str = None) -> None:
        """
        Initialize a DeleteComponentResponse object.

        :param str message: (optional)
        :param str type: (optional) The type of this component. Such as:
               "fabric-peer", "fabric-ca", "fabric-orderer", etc.
        :param str id: (optional) The unique identifier of this component.
        :param str display_name: (optional) A descriptive name for this peer. The
               IBP console tile displays this name.
        """
        self.message = message
        self.type = type
        self.id = id
        self.display_name = display_name

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'DeleteComponentResponse':
        """Initialize a DeleteComponentResponse object from a json dictionary."""
        args = {}
        if 'message' in _dict:
            args['message'] = _dict.get('message')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'display_name' in _dict:
            args['display_name'] = _dict.get('display_name')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a DeleteComponentResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'message') and self.message is not None:
            _dict['message'] = self.message
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'display_name') and self.display_name is not None:
            _dict['display_name'] = self.display_name
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this DeleteComponentResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'DeleteComponentResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'DeleteComponentResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class DeleteMultiComponentsResponse():
    """
    DeleteMultiComponentsResponse.

    :attr List[DeleteComponentResponse] deleted: (optional)
    """

    def __init__(self,
                 *,
                 deleted: List['DeleteComponentResponse'] = None) -> None:
        """
        Initialize a DeleteMultiComponentsResponse object.

        :param List[DeleteComponentResponse] deleted: (optional)
        """
        self.deleted = deleted

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'DeleteMultiComponentsResponse':
        """Initialize a DeleteMultiComponentsResponse object from a json dictionary."""
        args = {}
        if 'deleted' in _dict:
            args['deleted'] = [DeleteComponentResponse.from_dict(x) for x in _dict.get('deleted')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a DeleteMultiComponentsResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'deleted') and self.deleted is not None:
            _dict['deleted'] = [x.to_dict() for x in self.deleted]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this DeleteMultiComponentsResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'DeleteMultiComponentsResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'DeleteMultiComponentsResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class DeleteSignatureCollectionResponse():
    """
    DeleteSignatureCollectionResponse.

    :attr str message: (optional) Response message. "ok" indicates the api completed
          successfully.
    :attr str tx_id: (optional) The unique transaction ID of this signature
          collection. Must start with a letter.
    """

    def __init__(self,
                 *,
                 message: str = None,
                 tx_id: str = None) -> None:
        """
        Initialize a DeleteSignatureCollectionResponse object.

        :param str message: (optional) Response message. "ok" indicates the api
               completed successfully.
        :param str tx_id: (optional) The unique transaction ID of this signature
               collection. Must start with a letter.
        """
        self.message = message
        self.tx_id = tx_id

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'DeleteSignatureCollectionResponse':
        """Initialize a DeleteSignatureCollectionResponse object from a json dictionary."""
        args = {}
        if 'message' in _dict:
            args['message'] = _dict.get('message')
        if 'tx_id' in _dict:
            args['tx_id'] = _dict.get('tx_id')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a DeleteSignatureCollectionResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'message') and self.message is not None:
            _dict['message'] = self.message
        if hasattr(self, 'tx_id') and self.tx_id is not None:
            _dict['tx_id'] = self.tx_id
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this DeleteSignatureCollectionResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'DeleteSignatureCollectionResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'DeleteSignatureCollectionResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class EditAdminCertsResponse():
    """
    EditAdminCertsResponse.

    :attr float changes_made: (optional) The total number of admin certificate
          additions and deletions.
    :attr List[EditAdminCertsResponseSetAdminCertsItem] set_admin_certs: (optional)
          Array of certs there were set.
    """

    def __init__(self,
                 *,
                 changes_made: float = None,
                 set_admin_certs: List['EditAdminCertsResponseSetAdminCertsItem'] = None) -> None:
        """
        Initialize a EditAdminCertsResponse object.

        :param float changes_made: (optional) The total number of admin certificate
               additions and deletions.
        :param List[EditAdminCertsResponseSetAdminCertsItem] set_admin_certs:
               (optional) Array of certs there were set.
        """
        self.changes_made = changes_made
        self.set_admin_certs = set_admin_certs

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'EditAdminCertsResponse':
        """Initialize a EditAdminCertsResponse object from a json dictionary."""
        args = {}
        if 'changes_made' in _dict:
            args['changes_made'] = _dict.get('changes_made')
        if 'set_admin_certs' in _dict:
            args['set_admin_certs'] = [EditAdminCertsResponseSetAdminCertsItem.from_dict(x) for x in _dict.get('set_admin_certs')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a EditAdminCertsResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'changes_made') and self.changes_made is not None:
            _dict['changes_made'] = self.changes_made
        if hasattr(self, 'set_admin_certs') and self.set_admin_certs is not None:
            _dict['set_admin_certs'] = [x.to_dict() for x in self.set_admin_certs]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this EditAdminCertsResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'EditAdminCertsResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'EditAdminCertsResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class EditAdminCertsResponseSetAdminCertsItem():
    """
    EditAdminCertsResponseSetAdminCertsItem.

    :attr str base_64_pem: (optional) A certificate as base 64 encoded PEM. Also
          known as the signing certificate of an organization admin.
    :attr str issuer: (optional) The issuer string in the certificate.
    :attr float not_after_ts: (optional) UTC timestamp of the last ms the
          certificate is valid.
    :attr float not_before_ts: (optional) UTC timestamp of the earliest ms the
          certificate is valid.
    :attr str serial_number_hex: (optional) The "unique" id of the certificates.
    :attr str signature_algorithm: (optional) The crypto algorithm that signed the
          public key in the certificate.
    :attr str subject: (optional) The subject string in the certificate.
    :attr float x509_version: (optional) The X.509 version/format.
    :attr str time_left: (optional) A friendly (human readable) duration until
          certificate expiration.
    """

    def __init__(self,
                 *,
                 base_64_pem: str = None,
                 issuer: str = None,
                 not_after_ts: float = None,
                 not_before_ts: float = None,
                 serial_number_hex: str = None,
                 signature_algorithm: str = None,
                 subject: str = None,
                 x509_version: float = None,
                 time_left: str = None) -> None:
        """
        Initialize a EditAdminCertsResponseSetAdminCertsItem object.

        :param str base_64_pem: (optional) A certificate as base 64 encoded PEM.
               Also known as the signing certificate of an organization admin.
        :param str issuer: (optional) The issuer string in the certificate.
        :param float not_after_ts: (optional) UTC timestamp of the last ms the
               certificate is valid.
        :param float not_before_ts: (optional) UTC timestamp of the earliest ms the
               certificate is valid.
        :param str serial_number_hex: (optional) The "unique" id of the
               certificates.
        :param str signature_algorithm: (optional) The crypto algorithm that signed
               the public key in the certificate.
        :param str subject: (optional) The subject string in the certificate.
        :param float x509_version: (optional) The X.509 version/format.
        :param str time_left: (optional) A friendly (human readable) duration until
               certificate expiration.
        """
        self.base_64_pem = base_64_pem
        self.issuer = issuer
        self.not_after_ts = not_after_ts
        self.not_before_ts = not_before_ts
        self.serial_number_hex = serial_number_hex
        self.signature_algorithm = signature_algorithm
        self.subject = subject
        self.x509_version = x509_version
        self.time_left = time_left

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'EditAdminCertsResponseSetAdminCertsItem':
        """Initialize a EditAdminCertsResponseSetAdminCertsItem object from a json dictionary."""
        args = {}
        if 'base_64_pem' in _dict:
            args['base_64_pem'] = _dict.get('base_64_pem')
        if 'issuer' in _dict:
            args['issuer'] = _dict.get('issuer')
        if 'not_after_ts' in _dict:
            args['not_after_ts'] = _dict.get('not_after_ts')
        if 'not_before_ts' in _dict:
            args['not_before_ts'] = _dict.get('not_before_ts')
        if 'serial_number_hex' in _dict:
            args['serial_number_hex'] = _dict.get('serial_number_hex')
        if 'signature_algorithm' in _dict:
            args['signature_algorithm'] = _dict.get('signature_algorithm')
        if 'subject' in _dict:
            args['subject'] = _dict.get('subject')
        if 'X509_version' in _dict:
            args['x509_version'] = _dict.get('X509_version')
        if 'time_left' in _dict:
            args['time_left'] = _dict.get('time_left')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a EditAdminCertsResponseSetAdminCertsItem object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'base_64_pem') and self.base_64_pem is not None:
            _dict['base_64_pem'] = self.base_64_pem
        if hasattr(self, 'issuer') and self.issuer is not None:
            _dict['issuer'] = self.issuer
        if hasattr(self, 'not_after_ts') and self.not_after_ts is not None:
            _dict['not_after_ts'] = self.not_after_ts
        if hasattr(self, 'not_before_ts') and self.not_before_ts is not None:
            _dict['not_before_ts'] = self.not_before_ts
        if hasattr(self, 'serial_number_hex') and self.serial_number_hex is not None:
            _dict['serial_number_hex'] = self.serial_number_hex
        if hasattr(self, 'signature_algorithm') and self.signature_algorithm is not None:
            _dict['signature_algorithm'] = self.signature_algorithm
        if hasattr(self, 'subject') and self.subject is not None:
            _dict['subject'] = self.subject
        if hasattr(self, 'x509_version') and self.x509_version is not None:
            _dict['X509_version'] = self.x509_version
        if hasattr(self, 'time_left') and self.time_left is not None:
            _dict['time_left'] = self.time_left
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this EditAdminCertsResponseSetAdminCertsItem object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'EditAdminCertsResponseSetAdminCertsItem') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'EditAdminCertsResponseSetAdminCertsItem') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class EditLogSettingsBody():
    """
    File system logging settings. All body fields are optional (only send the fields that
    you want to change). _Changes to this field will restart the IBP console server(s)_.

    :attr LoggingSettingsClient client: (optional) The client side (browser) logging
          settings. _Changes to this field will restart the IBP console server(s)_.
    :attr LoggingSettingsServer server: (optional) The server side logging settings.
          _Changes to this field will restart the IBP console server(s)_.
    """

    def __init__(self,
                 *,
                 client: 'LoggingSettingsClient' = None,
                 server: 'LoggingSettingsServer' = None) -> None:
        """
        Initialize a EditLogSettingsBody object.

        :param LoggingSettingsClient client: (optional) The client side (browser)
               logging settings. _Changes to this field will restart the IBP console
               server(s)_.
        :param LoggingSettingsServer server: (optional) The server side logging
               settings. _Changes to this field will restart the IBP console server(s)_.
        """
        self.client = client
        self.server = server

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'EditLogSettingsBody':
        """Initialize a EditLogSettingsBody object from a json dictionary."""
        args = {}
        if 'client' in _dict:
            args['client'] = LoggingSettingsClient.from_dict(_dict.get('client'))
        if 'server' in _dict:
            args['server'] = LoggingSettingsServer.from_dict(_dict.get('server'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a EditLogSettingsBody object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'client') and self.client is not None:
            _dict['client'] = self.client.to_dict()
        if hasattr(self, 'server') and self.server is not None:
            _dict['server'] = self.server.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this EditLogSettingsBody object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'EditLogSettingsBody') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'EditLogSettingsBody') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class EditSettingsBodyInactivityTimeouts():
    """
    EditSettingsBodyInactivityTimeouts.

    :attr bool enabled: (optional) Indicates if the auto log out logic is enabled or
          disabled. Defaults `false`. _Refresh browser after changes_.
    :attr float max_idle_time: (optional) Maximum time in milliseconds for a browser
          client to be idle. Once exceeded the user is logged out. Defaults to `90000` ms
          (1.5 minutes). _Refresh browser after changes_.
    """

    def __init__(self,
                 *,
                 enabled: bool = None,
                 max_idle_time: float = None) -> None:
        """
        Initialize a EditSettingsBodyInactivityTimeouts object.

        :param bool enabled: (optional) Indicates if the auto log out logic is
               enabled or disabled. Defaults `false`. _Refresh browser after changes_.
        :param float max_idle_time: (optional) Maximum time in milliseconds for a
               browser client to be idle. Once exceeded the user is logged out. Defaults
               to `90000` ms (1.5 minutes). _Refresh browser after changes_.
        """
        self.enabled = enabled
        self.max_idle_time = max_idle_time

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'EditSettingsBodyInactivityTimeouts':
        """Initialize a EditSettingsBodyInactivityTimeouts object from a json dictionary."""
        args = {}
        if 'enabled' in _dict:
            args['enabled'] = _dict.get('enabled')
        if 'max_idle_time' in _dict:
            args['max_idle_time'] = _dict.get('max_idle_time')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a EditSettingsBodyInactivityTimeouts object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'enabled') and self.enabled is not None:
            _dict['enabled'] = self.enabled
        if hasattr(self, 'max_idle_time') and self.max_idle_time is not None:
            _dict['max_idle_time'] = self.max_idle_time
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this EditSettingsBodyInactivityTimeouts object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'EditSettingsBodyInactivityTimeouts') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'EditSettingsBodyInactivityTimeouts') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class FabVersionObject():
    """
    FabVersionObject.

    :attr bool default: (optional) Indicates if this is the Fabric version that will
          be used if none is selected.
    :attr str version: (optional) The Fabric version.
    :attr object image: (optional) Detailed image information for this Fabric
          release.
    """

    def __init__(self,
                 *,
                 default: bool = None,
                 version: str = None,
                 image: object = None) -> None:
        """
        Initialize a FabVersionObject object.

        :param bool default: (optional) Indicates if this is the Fabric version
               that will be used if none is selected.
        :param str version: (optional) The Fabric version.
        :param object image: (optional) Detailed image information for this Fabric
               release.
        """
        self.default = default
        self.version = version
        self.image = image

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'FabVersionObject':
        """Initialize a FabVersionObject object from a json dictionary."""
        args = {}
        if 'default' in _dict:
            args['default'] = _dict.get('default')
        if 'version' in _dict:
            args['version'] = _dict.get('version')
        if 'image' in _dict:
            args['image'] = _dict.get('image')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a FabVersionObject object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'default') and self.default is not None:
            _dict['default'] = self.default
        if hasattr(self, 'version') and self.version is not None:
            _dict['version'] = self.version
        if hasattr(self, 'image') and self.image is not None:
            _dict['image'] = self.image
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this FabVersionObject object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'FabVersionObject') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'FabVersionObject') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class FabricVersionDictionary():
    """
    A supported release of Fabric for this component type.

    :attr FabVersionObject _1_4_6_2: (optional)
    :attr FabVersionObject _2_1_0_0: (optional)
    """

    # The set of defined properties for the class
    _properties = frozenset(['_1_4_6_2', '1.4.6-2', '_2_1_0_0', '2.1.0-0'])

    def __init__(self,
                 *,
                 _1_4_6_2: 'FabVersionObject' = None,
                 _2_1_0_0: 'FabVersionObject' = None,
                 **kwargs) -> None:
        """
        Initialize a FabricVersionDictionary object.

        :param FabVersionObject _1_4_6_2: (optional)
        :param FabVersionObject _2_1_0_0: (optional)
        :param **kwargs: (optional) Any additional properties.
        """
        self._1_4_6_2 = _1_4_6_2
        self._2_1_0_0 = _2_1_0_0
        for _key, _value in kwargs.items():
            setattr(self, _key, _value)

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'FabricVersionDictionary':
        """Initialize a FabricVersionDictionary object from a json dictionary."""
        args = {}
        if '1.4.6-2' in _dict:
            args['_1_4_6_2'] = FabVersionObject.from_dict(_dict.get('1.4.6-2'))
        if '2.1.0-0' in _dict:
            args['_2_1_0_0'] = FabVersionObject.from_dict(_dict.get('2.1.0-0'))
        args.update({k:v for (k, v) in _dict.items() if k not in cls._properties})
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a FabricVersionDictionary object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, '_1_4_6_2') and self._1_4_6_2 is not None:
            _dict['1.4.6-2'] = self._1_4_6_2.to_dict()
        if hasattr(self, '_2_1_0_0') and self._2_1_0_0 is not None:
            _dict['2.1.0-0'] = self._2_1_0_0.to_dict()
        for _key in [k for k in vars(self).keys() if k not in FabricVersionDictionary._properties]:
            if getattr(self, _key, None) is not None:
                _dict[_key] = getattr(self, _key)
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this FabricVersionDictionary object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'FabricVersionDictionary') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'FabricVersionDictionary') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GenericComponentResponse():
    """
    Contains the details of a component. Not all components have the same fields, see
    description of each field for details.

    :attr str id: (optional) The unique identifier of this component. [Available on
          all component types].
    :attr str type: (optional) The type of this component [Available on all
          component types].
    :attr str display_name: (optional) The displayed name of this component.
          [Available on all component types].
    :attr str grpcwp_url: (optional) The URL for the grpc web proxy for this
          component. [Available on peer/orderer components].
    :attr str api_url: (optional) The gRPC URL for the component. Typically, client
          applications would send requests to this URL. [Available on ca/peer/orderer
          components].
    :attr str operations_url: (optional) Used by Fabric health checker to monitor
          health status of the node. For more information, see [Fabric
          documentation](https://hyperledger-fabric.readthedocs.io/en/release-1.4/operations_service.html).
          [Available on ca/peer/orderer components].
    :attr GenericComponentResponseMsp msp: (optional)
    :attr str msp_id: (optional) The MSP id that is related to this component.
          [Available on all components].
    :attr str location: (optional) Indicates where the component is running.
    :attr NodeOuGeneral node_ou: (optional)
    :attr GenericComponentResponseResources resources: (optional) The **cached**
          Kubernetes resource attributes for this component. [Available on ca/peer/orderer
          components w/query parameter 'deployment_attrs'].
    :attr str scheme_version: (optional) The versioning of the IBP console format of
          this JSON.
    :attr str state_db: (optional) The type of ledger database for a peer.
          [Available on peer components w/query parameter 'deployment_attrs'].
    :attr GenericComponentResponseStorage storage: (optional) The **cached**
          Kubernetes storage attributes for this component. [Available on ca/peer/orderer
          components w/query parameter 'deployment_attrs'].
    :attr float timestamp: (optional) UNIX timestamp of component creation, UTC, ms.
          [Available on all components].
    :attr List[str] tags: (optional)
    :attr str version: (optional) The cached Hyperledger Fabric version for this
          component. [Available on ca/peer/orderer components w/query parameter
          'deployment_attrs'].
    :attr str zone: (optional) The Kubernetes zone of this component's deployment.
          [Available on ca/peer/orderer components w/query parameter 'deployment_attrs'].
    """

    def __init__(self,
                 *,
                 id: str = None,
                 type: str = None,
                 display_name: str = None,
                 grpcwp_url: str = None,
                 api_url: str = None,
                 operations_url: str = None,
                 msp: 'GenericComponentResponseMsp' = None,
                 msp_id: str = None,
                 location: str = None,
                 node_ou: 'NodeOuGeneral' = None,
                 resources: 'GenericComponentResponseResources' = None,
                 scheme_version: str = None,
                 state_db: str = None,
                 storage: 'GenericComponentResponseStorage' = None,
                 timestamp: float = None,
                 tags: List[str] = None,
                 version: str = None,
                 zone: str = None) -> None:
        """
        Initialize a GenericComponentResponse object.

        :param str id: (optional) The unique identifier of this component.
               [Available on all component types].
        :param str type: (optional) The type of this component [Available on all
               component types].
        :param str display_name: (optional) The displayed name of this component.
               [Available on all component types].
        :param str grpcwp_url: (optional) The URL for the grpc web proxy for this
               component. [Available on peer/orderer components].
        :param str api_url: (optional) The gRPC URL for the component. Typically,
               client applications would send requests to this URL. [Available on
               ca/peer/orderer components].
        :param str operations_url: (optional) Used by Fabric health checker to
               monitor health status of the node. For more information, see [Fabric
               documentation](https://hyperledger-fabric.readthedocs.io/en/release-1.4/operations_service.html).
               [Available on ca/peer/orderer components].
        :param GenericComponentResponseMsp msp: (optional)
        :param str msp_id: (optional) The MSP id that is related to this component.
               [Available on all components].
        :param str location: (optional) Indicates where the component is running.
        :param NodeOuGeneral node_ou: (optional)
        :param GenericComponentResponseResources resources: (optional) The
               **cached** Kubernetes resource attributes for this component. [Available on
               ca/peer/orderer components w/query parameter 'deployment_attrs'].
        :param str scheme_version: (optional) The versioning of the IBP console
               format of this JSON.
        :param str state_db: (optional) The type of ledger database for a peer.
               [Available on peer components w/query parameter 'deployment_attrs'].
        :param GenericComponentResponseStorage storage: (optional) The **cached**
               Kubernetes storage attributes for this component. [Available on
               ca/peer/orderer components w/query parameter 'deployment_attrs'].
        :param float timestamp: (optional) UNIX timestamp of component creation,
               UTC, ms. [Available on all components].
        :param List[str] tags: (optional)
        :param str version: (optional) The cached Hyperledger Fabric version for
               this component. [Available on ca/peer/orderer components w/query parameter
               'deployment_attrs'].
        :param str zone: (optional) The Kubernetes zone of this component's
               deployment. [Available on ca/peer/orderer components w/query parameter
               'deployment_attrs'].
        """
        self.id = id
        self.type = type
        self.display_name = display_name
        self.grpcwp_url = grpcwp_url
        self.api_url = api_url
        self.operations_url = operations_url
        self.msp = msp
        self.msp_id = msp_id
        self.location = location
        self.node_ou = node_ou
        self.resources = resources
        self.scheme_version = scheme_version
        self.state_db = state_db
        self.storage = storage
        self.timestamp = timestamp
        self.tags = tags
        self.version = version
        self.zone = zone

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GenericComponentResponse':
        """Initialize a GenericComponentResponse object from a json dictionary."""
        args = {}
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'display_name' in _dict:
            args['display_name'] = _dict.get('display_name')
        if 'grpcwp_url' in _dict:
            args['grpcwp_url'] = _dict.get('grpcwp_url')
        if 'api_url' in _dict:
            args['api_url'] = _dict.get('api_url')
        if 'operations_url' in _dict:
            args['operations_url'] = _dict.get('operations_url')
        if 'msp' in _dict:
            args['msp'] = GenericComponentResponseMsp.from_dict(_dict.get('msp'))
        if 'msp_id' in _dict:
            args['msp_id'] = _dict.get('msp_id')
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'node_ou' in _dict:
            args['node_ou'] = NodeOuGeneral.from_dict(_dict.get('node_ou'))
        if 'resources' in _dict:
            args['resources'] = GenericComponentResponseResources.from_dict(_dict.get('resources'))
        if 'scheme_version' in _dict:
            args['scheme_version'] = _dict.get('scheme_version')
        if 'state_db' in _dict:
            args['state_db'] = _dict.get('state_db')
        if 'storage' in _dict:
            args['storage'] = GenericComponentResponseStorage.from_dict(_dict.get('storage'))
        if 'timestamp' in _dict:
            args['timestamp'] = _dict.get('timestamp')
        if 'tags' in _dict:
            args['tags'] = _dict.get('tags')
        if 'version' in _dict:
            args['version'] = _dict.get('version')
        if 'zone' in _dict:
            args['zone'] = _dict.get('zone')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GenericComponentResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'display_name') and self.display_name is not None:
            _dict['display_name'] = self.display_name
        if hasattr(self, 'grpcwp_url') and self.grpcwp_url is not None:
            _dict['grpcwp_url'] = self.grpcwp_url
        if hasattr(self, 'api_url') and self.api_url is not None:
            _dict['api_url'] = self.api_url
        if hasattr(self, 'operations_url') and self.operations_url is not None:
            _dict['operations_url'] = self.operations_url
        if hasattr(self, 'msp') and self.msp is not None:
            _dict['msp'] = self.msp.to_dict()
        if hasattr(self, 'msp_id') and self.msp_id is not None:
            _dict['msp_id'] = self.msp_id
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'node_ou') and self.node_ou is not None:
            _dict['node_ou'] = self.node_ou.to_dict()
        if hasattr(self, 'resources') and self.resources is not None:
            _dict['resources'] = self.resources.to_dict()
        if hasattr(self, 'scheme_version') and self.scheme_version is not None:
            _dict['scheme_version'] = self.scheme_version
        if hasattr(self, 'state_db') and self.state_db is not None:
            _dict['state_db'] = self.state_db
        if hasattr(self, 'storage') and self.storage is not None:
            _dict['storage'] = self.storage.to_dict()
        if hasattr(self, 'timestamp') and self.timestamp is not None:
            _dict['timestamp'] = self.timestamp
        if hasattr(self, 'tags') and self.tags is not None:
            _dict['tags'] = self.tags
        if hasattr(self, 'version') and self.version is not None:
            _dict['version'] = self.version
        if hasattr(self, 'zone') and self.zone is not None:
            _dict['zone'] = self.zone
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GenericComponentResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GenericComponentResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GenericComponentResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class TypeEnum(str, Enum):
        """
        The type of this component [Available on all component types].
        """
        FABRIC_PEER = 'fabric-peer'
        FABRIC_CA = 'fabric-ca'
        FABRIC_ORDERER = 'fabric-orderer'


class GenericComponentResponseMsp():
    """
    GenericComponentResponseMsp.

    :attr GenericComponentResponseMspCa ca: (optional)
    :attr GenericComponentResponseMspTlsca tlsca: (optional)
    :attr GenericComponentResponseMspComponent component: (optional)
    """

    def __init__(self,
                 *,
                 ca: 'GenericComponentResponseMspCa' = None,
                 tlsca: 'GenericComponentResponseMspTlsca' = None,
                 component: 'GenericComponentResponseMspComponent' = None) -> None:
        """
        Initialize a GenericComponentResponseMsp object.

        :param GenericComponentResponseMspCa ca: (optional)
        :param GenericComponentResponseMspTlsca tlsca: (optional)
        :param GenericComponentResponseMspComponent component: (optional)
        """
        self.ca = ca
        self.tlsca = tlsca
        self.component = component

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GenericComponentResponseMsp':
        """Initialize a GenericComponentResponseMsp object from a json dictionary."""
        args = {}
        if 'ca' in _dict:
            args['ca'] = GenericComponentResponseMspCa.from_dict(_dict.get('ca'))
        if 'tlsca' in _dict:
            args['tlsca'] = GenericComponentResponseMspTlsca.from_dict(_dict.get('tlsca'))
        if 'component' in _dict:
            args['component'] = GenericComponentResponseMspComponent.from_dict(_dict.get('component'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GenericComponentResponseMsp object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        if hasattr(self, 'tlsca') and self.tlsca is not None:
            _dict['tlsca'] = self.tlsca.to_dict()
        if hasattr(self, 'component') and self.component is not None:
            _dict['component'] = self.component.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GenericComponentResponseMsp object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GenericComponentResponseMsp') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GenericComponentResponseMsp') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GenericComponentResponseMspCa():
    """
    GenericComponentResponseMspCa.

    :attr str name: (optional) The "name" to distinguish this CA from the TLS CA.
          [Available on ca components].
    :attr List[str] root_certs: (optional) An array that contains one or more base
          64 encoded PEM root certificates for the CA. [Available on ca/peer/orderer
          components].
    """

    def __init__(self,
                 *,
                 name: str = None,
                 root_certs: List[str] = None) -> None:
        """
        Initialize a GenericComponentResponseMspCa object.

        :param str name: (optional) The "name" to distinguish this CA from the TLS
               CA. [Available on ca components].
        :param List[str] root_certs: (optional) An array that contains one or more
               base 64 encoded PEM root certificates for the CA. [Available on
               ca/peer/orderer components].
        """
        self.name = name
        self.root_certs = root_certs

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GenericComponentResponseMspCa':
        """Initialize a GenericComponentResponseMspCa object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'root_certs' in _dict:
            args['root_certs'] = _dict.get('root_certs')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GenericComponentResponseMspCa object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'root_certs') and self.root_certs is not None:
            _dict['root_certs'] = self.root_certs
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GenericComponentResponseMspCa object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GenericComponentResponseMspCa') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GenericComponentResponseMspCa') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GenericComponentResponseMspComponent():
    """
    GenericComponentResponseMspComponent.

    :attr str tls_cert: (optional) The TLS certificate as base 64 encoded PEM.
          Certificate is used to secure/validate a TLS connection with this component.
    :attr str ecert: (optional) An identity certificate (base 64 encoded PEM) for
          this component that was signed by the CA (aka enrollment certificate).
          [Available on peer/orderer components w/query parameter 'deployment_attrs'].
    :attr List[str] admin_certs: (optional) An array that contains base 64 encoded
          PEM identity certificates for administrators. Also known as signing certificates
          of an organization administrator. [Available on peer/orderer components w/query
          parameter 'deployment_attrs'].
    """

    def __init__(self,
                 *,
                 tls_cert: str = None,
                 ecert: str = None,
                 admin_certs: List[str] = None) -> None:
        """
        Initialize a GenericComponentResponseMspComponent object.

        :param str tls_cert: (optional) The TLS certificate as base 64 encoded PEM.
               Certificate is used to secure/validate a TLS connection with this
               component.
        :param str ecert: (optional) An identity certificate (base 64 encoded PEM)
               for this component that was signed by the CA (aka enrollment certificate).
               [Available on peer/orderer components w/query parameter
               'deployment_attrs'].
        :param List[str] admin_certs: (optional) An array that contains base 64
               encoded PEM identity certificates for administrators. Also known as signing
               certificates of an organization administrator. [Available on peer/orderer
               components w/query parameter 'deployment_attrs'].
        """
        self.tls_cert = tls_cert
        self.ecert = ecert
        self.admin_certs = admin_certs

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GenericComponentResponseMspComponent':
        """Initialize a GenericComponentResponseMspComponent object from a json dictionary."""
        args = {}
        if 'tls_cert' in _dict:
            args['tls_cert'] = _dict.get('tls_cert')
        if 'ecert' in _dict:
            args['ecert'] = _dict.get('ecert')
        if 'admin_certs' in _dict:
            args['admin_certs'] = _dict.get('admin_certs')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GenericComponentResponseMspComponent object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'tls_cert') and self.tls_cert is not None:
            _dict['tls_cert'] = self.tls_cert
        if hasattr(self, 'ecert') and self.ecert is not None:
            _dict['ecert'] = self.ecert
        if hasattr(self, 'admin_certs') and self.admin_certs is not None:
            _dict['admin_certs'] = self.admin_certs
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GenericComponentResponseMspComponent object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GenericComponentResponseMspComponent') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GenericComponentResponseMspComponent') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GenericComponentResponseMspTlsca():
    """
    GenericComponentResponseMspTlsca.

    :attr str name: (optional) The "name" to distinguish this CA from the other CA.
          [Available on ca components].
    :attr List[str] root_certs: (optional) An array that contains one or more base
          64 encoded PEM root certificates for the TLS CA. [Available on ca/peer/orderer
          components].
    """

    def __init__(self,
                 *,
                 name: str = None,
                 root_certs: List[str] = None) -> None:
        """
        Initialize a GenericComponentResponseMspTlsca object.

        :param str name: (optional) The "name" to distinguish this CA from the
               other CA. [Available on ca components].
        :param List[str] root_certs: (optional) An array that contains one or more
               base 64 encoded PEM root certificates for the TLS CA. [Available on
               ca/peer/orderer components].
        """
        self.name = name
        self.root_certs = root_certs

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GenericComponentResponseMspTlsca':
        """Initialize a GenericComponentResponseMspTlsca object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'root_certs' in _dict:
            args['root_certs'] = _dict.get('root_certs')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GenericComponentResponseMspTlsca object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'root_certs') and self.root_certs is not None:
            _dict['root_certs'] = self.root_certs
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GenericComponentResponseMspTlsca object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GenericComponentResponseMspTlsca') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GenericComponentResponseMspTlsca') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GenericComponentResponseResources():
    """
    The **cached** Kubernetes resource attributes for this component. [Available on
    ca/peer/orderer components w/query parameter 'deployment_attrs'].

    :attr GenericResources ca: (optional)
    :attr GenericResources peer: (optional)
    :attr GenericResources orderer: (optional)
    :attr GenericResources proxy: (optional)
    :attr GenericResources statedb: (optional)
    """

    def __init__(self,
                 *,
                 ca: 'GenericResources' = None,
                 peer: 'GenericResources' = None,
                 orderer: 'GenericResources' = None,
                 proxy: 'GenericResources' = None,
                 statedb: 'GenericResources' = None) -> None:
        """
        Initialize a GenericComponentResponseResources object.

        :param GenericResources ca: (optional)
        :param GenericResources peer: (optional)
        :param GenericResources orderer: (optional)
        :param GenericResources proxy: (optional)
        :param GenericResources statedb: (optional)
        """
        self.ca = ca
        self.peer = peer
        self.orderer = orderer
        self.proxy = proxy
        self.statedb = statedb

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GenericComponentResponseResources':
        """Initialize a GenericComponentResponseResources object from a json dictionary."""
        args = {}
        if 'ca' in _dict:
            args['ca'] = GenericResources.from_dict(_dict.get('ca'))
        if 'peer' in _dict:
            args['peer'] = GenericResources.from_dict(_dict.get('peer'))
        if 'orderer' in _dict:
            args['orderer'] = GenericResources.from_dict(_dict.get('orderer'))
        if 'proxy' in _dict:
            args['proxy'] = GenericResources.from_dict(_dict.get('proxy'))
        if 'statedb' in _dict:
            args['statedb'] = GenericResources.from_dict(_dict.get('statedb'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GenericComponentResponseResources object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        if hasattr(self, 'peer') and self.peer is not None:
            _dict['peer'] = self.peer.to_dict()
        if hasattr(self, 'orderer') and self.orderer is not None:
            _dict['orderer'] = self.orderer.to_dict()
        if hasattr(self, 'proxy') and self.proxy is not None:
            _dict['proxy'] = self.proxy.to_dict()
        if hasattr(self, 'statedb') and self.statedb is not None:
            _dict['statedb'] = self.statedb.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GenericComponentResponseResources object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GenericComponentResponseResources') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GenericComponentResponseResources') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GenericComponentResponseStorage():
    """
    The **cached** Kubernetes storage attributes for this component. [Available on
    ca/peer/orderer components w/query parameter 'deployment_attrs'].

    :attr StorageObject ca: (optional)
    :attr StorageObject peer: (optional)
    :attr StorageObject orderer: (optional)
    :attr StorageObject statedb: (optional)
    """

    def __init__(self,
                 *,
                 ca: 'StorageObject' = None,
                 peer: 'StorageObject' = None,
                 orderer: 'StorageObject' = None,
                 statedb: 'StorageObject' = None) -> None:
        """
        Initialize a GenericComponentResponseStorage object.

        :param StorageObject ca: (optional)
        :param StorageObject peer: (optional)
        :param StorageObject orderer: (optional)
        :param StorageObject statedb: (optional)
        """
        self.ca = ca
        self.peer = peer
        self.orderer = orderer
        self.statedb = statedb

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GenericComponentResponseStorage':
        """Initialize a GenericComponentResponseStorage object from a json dictionary."""
        args = {}
        if 'ca' in _dict:
            args['ca'] = StorageObject.from_dict(_dict.get('ca'))
        if 'peer' in _dict:
            args['peer'] = StorageObject.from_dict(_dict.get('peer'))
        if 'orderer' in _dict:
            args['orderer'] = StorageObject.from_dict(_dict.get('orderer'))
        if 'statedb' in _dict:
            args['statedb'] = StorageObject.from_dict(_dict.get('statedb'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GenericComponentResponseStorage object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        if hasattr(self, 'peer') and self.peer is not None:
            _dict['peer'] = self.peer.to_dict()
        if hasattr(self, 'orderer') and self.orderer is not None:
            _dict['orderer'] = self.orderer.to_dict()
        if hasattr(self, 'statedb') and self.statedb is not None:
            _dict['statedb'] = self.statedb.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GenericComponentResponseStorage object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GenericComponentResponseStorage') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GenericComponentResponseStorage') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GenericResourceLimits():
    """
    GenericResourceLimits.

    :attr str cpu: (optional)
    :attr str memory: (optional)
    """

    def __init__(self,
                 *,
                 cpu: str = None,
                 memory: str = None) -> None:
        """
        Initialize a GenericResourceLimits object.

        :param str cpu: (optional)
        :param str memory: (optional)
        """
        self.cpu = cpu
        self.memory = memory

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GenericResourceLimits':
        """Initialize a GenericResourceLimits object from a json dictionary."""
        args = {}
        if 'cpu' in _dict:
            args['cpu'] = _dict.get('cpu')
        if 'memory' in _dict:
            args['memory'] = _dict.get('memory')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GenericResourceLimits object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'cpu') and self.cpu is not None:
            _dict['cpu'] = self.cpu
        if hasattr(self, 'memory') and self.memory is not None:
            _dict['memory'] = self.memory
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GenericResourceLimits object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GenericResourceLimits') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GenericResourceLimits') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GenericResources():
    """
    GenericResources.

    :attr GenericResourcesRequests requests: (optional)
    :attr GenericResourceLimits limits: (optional)
    """

    def __init__(self,
                 *,
                 requests: 'GenericResourcesRequests' = None,
                 limits: 'GenericResourceLimits' = None) -> None:
        """
        Initialize a GenericResources object.

        :param GenericResourcesRequests requests: (optional)
        :param GenericResourceLimits limits: (optional)
        """
        self.requests = requests
        self.limits = limits

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GenericResources':
        """Initialize a GenericResources object from a json dictionary."""
        args = {}
        if 'requests' in _dict:
            args['requests'] = GenericResourcesRequests.from_dict(_dict.get('requests'))
        if 'limits' in _dict:
            args['limits'] = GenericResourceLimits.from_dict(_dict.get('limits'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GenericResources object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'requests') and self.requests is not None:
            _dict['requests'] = self.requests.to_dict()
        if hasattr(self, 'limits') and self.limits is not None:
            _dict['limits'] = self.limits.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GenericResources object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GenericResources') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GenericResources') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GenericResourcesRequests():
    """
    GenericResourcesRequests.

    :attr str cpu: (optional)
    :attr str memory: (optional)
    """

    def __init__(self,
                 *,
                 cpu: str = None,
                 memory: str = None) -> None:
        """
        Initialize a GenericResourcesRequests object.

        :param str cpu: (optional)
        :param str memory: (optional)
        """
        self.cpu = cpu
        self.memory = memory

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GenericResourcesRequests':
        """Initialize a GenericResourcesRequests object from a json dictionary."""
        args = {}
        if 'cpu' in _dict:
            args['cpu'] = _dict.get('cpu')
        if 'memory' in _dict:
            args['memory'] = _dict.get('memory')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GenericResourcesRequests object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'cpu') and self.cpu is not None:
            _dict['cpu'] = self.cpu
        if hasattr(self, 'memory') and self.memory is not None:
            _dict['memory'] = self.memory
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GenericResourcesRequests object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GenericResourcesRequests') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GenericResourcesRequests') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GetAthenaHealthStatsResponse():
    """
    Contains various health statistics like up time and cache sizes.

    :attr GetAthenaHealthStatsResponseOPTOOLS optools: (optional)
    :attr GetAthenaHealthStatsResponseOS os: (optional)
    """

    def __init__(self,
                 *,
                 optools: 'GetAthenaHealthStatsResponseOPTOOLS' = None,
                 os: 'GetAthenaHealthStatsResponseOS' = None) -> None:
        """
        Initialize a GetAthenaHealthStatsResponse object.

        :param GetAthenaHealthStatsResponseOPTOOLS optools: (optional)
        :param GetAthenaHealthStatsResponseOS os: (optional)
        """
        self.optools = optools
        self.os = os

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GetAthenaHealthStatsResponse':
        """Initialize a GetAthenaHealthStatsResponse object from a json dictionary."""
        args = {}
        if 'OPTOOLS' in _dict:
            args['optools'] = GetAthenaHealthStatsResponseOPTOOLS.from_dict(_dict.get('OPTOOLS'))
        if 'OS' in _dict:
            args['os'] = GetAthenaHealthStatsResponseOS.from_dict(_dict.get('OS'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GetAthenaHealthStatsResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'optools') and self.optools is not None:
            _dict['OPTOOLS'] = self.optools.to_dict()
        if hasattr(self, 'os') and self.os is not None:
            _dict['OS'] = self.os.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GetAthenaHealthStatsResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GetAthenaHealthStatsResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GetAthenaHealthStatsResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GetAthenaHealthStatsResponseOPTOOLS():
    """
    GetAthenaHealthStatsResponseOPTOOLS.

    :attr str instance_id: (optional) Random/unique id for a process running IBP
          console.
    :attr float now: (optional) UTC UNIX timestamp of the current time according to
          the server. In milliseconds.
    :attr float born: (optional) UTC UNIX timestamp of when the server started. In
          milliseconds.
    :attr str up_time: (optional) Total time the IBP console server has been
          running.
    :attr GetAthenaHealthStatsResponseOPTOOLSMemoryUsage memory_usage: (optional)
    :attr CacheData session_cache_stats: (optional)
    :attr CacheData couch_cache_stats: (optional)
    :attr CacheData iam_cache_stats: (optional)
    :attr CacheData proxy_cache: (optional)
    """

    def __init__(self,
                 *,
                 instance_id: str = None,
                 now: float = None,
                 born: float = None,
                 up_time: str = None,
                 memory_usage: 'GetAthenaHealthStatsResponseOPTOOLSMemoryUsage' = None,
                 session_cache_stats: 'CacheData' = None,
                 couch_cache_stats: 'CacheData' = None,
                 iam_cache_stats: 'CacheData' = None,
                 proxy_cache: 'CacheData' = None) -> None:
        """
        Initialize a GetAthenaHealthStatsResponseOPTOOLS object.

        :param str instance_id: (optional) Random/unique id for a process running
               IBP console.
        :param float now: (optional) UTC UNIX timestamp of the current time
               according to the server. In milliseconds.
        :param float born: (optional) UTC UNIX timestamp of when the server
               started. In milliseconds.
        :param str up_time: (optional) Total time the IBP console server has been
               running.
        :param GetAthenaHealthStatsResponseOPTOOLSMemoryUsage memory_usage:
               (optional)
        :param CacheData session_cache_stats: (optional)
        :param CacheData couch_cache_stats: (optional)
        :param CacheData iam_cache_stats: (optional)
        :param CacheData proxy_cache: (optional)
        """
        self.instance_id = instance_id
        self.now = now
        self.born = born
        self.up_time = up_time
        self.memory_usage = memory_usage
        self.session_cache_stats = session_cache_stats
        self.couch_cache_stats = couch_cache_stats
        self.iam_cache_stats = iam_cache_stats
        self.proxy_cache = proxy_cache

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GetAthenaHealthStatsResponseOPTOOLS':
        """Initialize a GetAthenaHealthStatsResponseOPTOOLS object from a json dictionary."""
        args = {}
        if 'instance_id' in _dict:
            args['instance_id'] = _dict.get('instance_id')
        if 'now' in _dict:
            args['now'] = _dict.get('now')
        if 'born' in _dict:
            args['born'] = _dict.get('born')
        if 'up_time' in _dict:
            args['up_time'] = _dict.get('up_time')
        if 'memory_usage' in _dict:
            args['memory_usage'] = GetAthenaHealthStatsResponseOPTOOLSMemoryUsage.from_dict(_dict.get('memory_usage'))
        if 'session_cache_stats' in _dict:
            args['session_cache_stats'] = CacheData.from_dict(_dict.get('session_cache_stats'))
        if 'couch_cache_stats' in _dict:
            args['couch_cache_stats'] = CacheData.from_dict(_dict.get('couch_cache_stats'))
        if 'iam_cache_stats' in _dict:
            args['iam_cache_stats'] = CacheData.from_dict(_dict.get('iam_cache_stats'))
        if 'proxy_cache' in _dict:
            args['proxy_cache'] = CacheData.from_dict(_dict.get('proxy_cache'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GetAthenaHealthStatsResponseOPTOOLS object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'instance_id') and self.instance_id is not None:
            _dict['instance_id'] = self.instance_id
        if hasattr(self, 'now') and self.now is not None:
            _dict['now'] = self.now
        if hasattr(self, 'born') and self.born is not None:
            _dict['born'] = self.born
        if hasattr(self, 'up_time') and self.up_time is not None:
            _dict['up_time'] = self.up_time
        if hasattr(self, 'memory_usage') and self.memory_usage is not None:
            _dict['memory_usage'] = self.memory_usage.to_dict()
        if hasattr(self, 'session_cache_stats') and self.session_cache_stats is not None:
            _dict['session_cache_stats'] = self.session_cache_stats.to_dict()
        if hasattr(self, 'couch_cache_stats') and self.couch_cache_stats is not None:
            _dict['couch_cache_stats'] = self.couch_cache_stats.to_dict()
        if hasattr(self, 'iam_cache_stats') and self.iam_cache_stats is not None:
            _dict['iam_cache_stats'] = self.iam_cache_stats.to_dict()
        if hasattr(self, 'proxy_cache') and self.proxy_cache is not None:
            _dict['proxy_cache'] = self.proxy_cache.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GetAthenaHealthStatsResponseOPTOOLS object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GetAthenaHealthStatsResponseOPTOOLS') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GetAthenaHealthStatsResponseOPTOOLS') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GetAthenaHealthStatsResponseOPTOOLSMemoryUsage():
    """
    GetAthenaHealthStatsResponseOPTOOLSMemoryUsage.

    :attr str rss: (optional) Resident set size - total memory allocated for the
          process.
    :attr str heap_total: (optional) Memory allocated for the heap of V8.
    :attr str heap_used: (optional) Current heap used by V8.
    :attr str external: (optional) Memory used by bound C++ objects.
    """

    def __init__(self,
                 *,
                 rss: str = None,
                 heap_total: str = None,
                 heap_used: str = None,
                 external: str = None) -> None:
        """
        Initialize a GetAthenaHealthStatsResponseOPTOOLSMemoryUsage object.

        :param str rss: (optional) Resident set size - total memory allocated for
               the process.
        :param str heap_total: (optional) Memory allocated for the heap of V8.
        :param str heap_used: (optional) Current heap used by V8.
        :param str external: (optional) Memory used by bound C++ objects.
        """
        self.rss = rss
        self.heap_total = heap_total
        self.heap_used = heap_used
        self.external = external

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GetAthenaHealthStatsResponseOPTOOLSMemoryUsage':
        """Initialize a GetAthenaHealthStatsResponseOPTOOLSMemoryUsage object from a json dictionary."""
        args = {}
        if 'rss' in _dict:
            args['rss'] = _dict.get('rss')
        if 'heapTotal' in _dict:
            args['heap_total'] = _dict.get('heapTotal')
        if 'heapUsed' in _dict:
            args['heap_used'] = _dict.get('heapUsed')
        if 'external' in _dict:
            args['external'] = _dict.get('external')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GetAthenaHealthStatsResponseOPTOOLSMemoryUsage object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'rss') and self.rss is not None:
            _dict['rss'] = self.rss
        if hasattr(self, 'heap_total') and self.heap_total is not None:
            _dict['heapTotal'] = self.heap_total
        if hasattr(self, 'heap_used') and self.heap_used is not None:
            _dict['heapUsed'] = self.heap_used
        if hasattr(self, 'external') and self.external is not None:
            _dict['external'] = self.external
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GetAthenaHealthStatsResponseOPTOOLSMemoryUsage object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GetAthenaHealthStatsResponseOPTOOLSMemoryUsage') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GetAthenaHealthStatsResponseOPTOOLSMemoryUsage') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GetAthenaHealthStatsResponseOS():
    """
    GetAthenaHealthStatsResponseOS.

    :attr str arch: (optional) CPU architecture.
    :attr str type: (optional) Operating system name.
    :attr str endian: (optional) Endianness of the CPU. LE = Little Endian, BE = Big
          Endian.
    :attr List[float] loadavg: (optional) CPU load in 1, 5, & 15 minute averages.
          n/a on windows.
    :attr List[CpuHealthStats] cpus: (optional)
    :attr str total_memory: (optional) Total memory known to the operating system.
    :attr str free_memory: (optional) Free memory on the operating system.
    :attr str up_time: (optional) Time operating system has been running.
    """

    def __init__(self,
                 *,
                 arch: str = None,
                 type: str = None,
                 endian: str = None,
                 loadavg: List[float] = None,
                 cpus: List['CpuHealthStats'] = None,
                 total_memory: str = None,
                 free_memory: str = None,
                 up_time: str = None) -> None:
        """
        Initialize a GetAthenaHealthStatsResponseOS object.

        :param str arch: (optional) CPU architecture.
        :param str type: (optional) Operating system name.
        :param str endian: (optional) Endianness of the CPU. LE = Little Endian, BE
               = Big Endian.
        :param List[float] loadavg: (optional) CPU load in 1, 5, & 15 minute
               averages. n/a on windows.
        :param List[CpuHealthStats] cpus: (optional)
        :param str total_memory: (optional) Total memory known to the operating
               system.
        :param str free_memory: (optional) Free memory on the operating system.
        :param str up_time: (optional) Time operating system has been running.
        """
        self.arch = arch
        self.type = type
        self.endian = endian
        self.loadavg = loadavg
        self.cpus = cpus
        self.total_memory = total_memory
        self.free_memory = free_memory
        self.up_time = up_time

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GetAthenaHealthStatsResponseOS':
        """Initialize a GetAthenaHealthStatsResponseOS object from a json dictionary."""
        args = {}
        if 'arch' in _dict:
            args['arch'] = _dict.get('arch')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'endian' in _dict:
            args['endian'] = _dict.get('endian')
        if 'loadavg' in _dict:
            args['loadavg'] = _dict.get('loadavg')
        if 'cpus' in _dict:
            args['cpus'] = [CpuHealthStats.from_dict(x) for x in _dict.get('cpus')]
        if 'total_memory' in _dict:
            args['total_memory'] = _dict.get('total_memory')
        if 'free_memory' in _dict:
            args['free_memory'] = _dict.get('free_memory')
        if 'up_time' in _dict:
            args['up_time'] = _dict.get('up_time')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GetAthenaHealthStatsResponseOS object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'arch') and self.arch is not None:
            _dict['arch'] = self.arch
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'endian') and self.endian is not None:
            _dict['endian'] = self.endian
        if hasattr(self, 'loadavg') and self.loadavg is not None:
            _dict['loadavg'] = self.loadavg
        if hasattr(self, 'cpus') and self.cpus is not None:
            _dict['cpus'] = [x.to_dict() for x in self.cpus]
        if hasattr(self, 'total_memory') and self.total_memory is not None:
            _dict['total_memory'] = self.total_memory
        if hasattr(self, 'free_memory') and self.free_memory is not None:
            _dict['free_memory'] = self.free_memory
        if hasattr(self, 'up_time') and self.up_time is not None:
            _dict['up_time'] = self.up_time
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GetAthenaHealthStatsResponseOS object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GetAthenaHealthStatsResponseOS') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GetAthenaHealthStatsResponseOS') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GetFabricVersionsResponse():
    """
    GetFabricVersionsResponse.

    :attr GetFabricVersionsResponseVersions versions: (optional)
    """

    def __init__(self,
                 *,
                 versions: 'GetFabricVersionsResponseVersions' = None) -> None:
        """
        Initialize a GetFabricVersionsResponse object.

        :param GetFabricVersionsResponseVersions versions: (optional)
        """
        self.versions = versions

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GetFabricVersionsResponse':
        """Initialize a GetFabricVersionsResponse object from a json dictionary."""
        args = {}
        if 'versions' in _dict:
            args['versions'] = GetFabricVersionsResponseVersions.from_dict(_dict.get('versions'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GetFabricVersionsResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'versions') and self.versions is not None:
            _dict['versions'] = self.versions.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GetFabricVersionsResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GetFabricVersionsResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GetFabricVersionsResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GetFabricVersionsResponseVersions():
    """
    GetFabricVersionsResponseVersions.

    :attr FabricVersionDictionary ca: (optional) A supported release of Fabric for
          this component type.
    :attr FabricVersionDictionary peer: (optional) A supported release of Fabric for
          this component type.
    :attr FabricVersionDictionary orderer: (optional) A supported release of Fabric
          for this component type.
    """

    def __init__(self,
                 *,
                 ca: 'FabricVersionDictionary' = None,
                 peer: 'FabricVersionDictionary' = None,
                 orderer: 'FabricVersionDictionary' = None) -> None:
        """
        Initialize a GetFabricVersionsResponseVersions object.

        :param FabricVersionDictionary ca: (optional) A supported release of Fabric
               for this component type.
        :param FabricVersionDictionary peer: (optional) A supported release of
               Fabric for this component type.
        :param FabricVersionDictionary orderer: (optional) A supported release of
               Fabric for this component type.
        """
        self.ca = ca
        self.peer = peer
        self.orderer = orderer

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GetFabricVersionsResponseVersions':
        """Initialize a GetFabricVersionsResponseVersions object from a json dictionary."""
        args = {}
        if 'ca' in _dict:
            args['ca'] = FabricVersionDictionary.from_dict(_dict.get('ca'))
        if 'peer' in _dict:
            args['peer'] = FabricVersionDictionary.from_dict(_dict.get('peer'))
        if 'orderer' in _dict:
            args['orderer'] = FabricVersionDictionary.from_dict(_dict.get('orderer'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GetFabricVersionsResponseVersions object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        if hasattr(self, 'peer') and self.peer is not None:
            _dict['peer'] = self.peer.to_dict()
        if hasattr(self, 'orderer') and self.orderer is not None:
            _dict['orderer'] = self.orderer.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GetFabricVersionsResponseVersions object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GetFabricVersionsResponseVersions') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GetFabricVersionsResponseVersions') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GetMSPCertificateResponse():
    """
    GetMSPCertificateResponse.

    :attr List[MspPublicData] msps: (optional)
    """

    def __init__(self,
                 *,
                 msps: List['MspPublicData'] = None) -> None:
        """
        Initialize a GetMSPCertificateResponse object.

        :param List[MspPublicData] msps: (optional)
        """
        self.msps = msps

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GetMSPCertificateResponse':
        """Initialize a GetMSPCertificateResponse object from a json dictionary."""
        args = {}
        if 'msps' in _dict:
            args['msps'] = [MspPublicData.from_dict(x) for x in _dict.get('msps')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GetMSPCertificateResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'msps') and self.msps is not None:
            _dict['msps'] = [x.to_dict() for x in self.msps]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GetMSPCertificateResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GetMSPCertificateResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GetMSPCertificateResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GetMultiComponentsResponse():
    """
    Contains the details of multiple components the UI has onboarded.

    :attr List[GenericComponentResponse] components: (optional) Array of components
          the UI has onboarded.
    """

    def __init__(self,
                 *,
                 components: List['GenericComponentResponse'] = None) -> None:
        """
        Initialize a GetMultiComponentsResponse object.

        :param List[GenericComponentResponse] components: (optional) Array of
               components the UI has onboarded.
        """
        self.components = components

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GetMultiComponentsResponse':
        """Initialize a GetMultiComponentsResponse object from a json dictionary."""
        args = {}
        if 'components' in _dict:
            args['components'] = [GenericComponentResponse.from_dict(x) for x in _dict.get('components')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GetMultiComponentsResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'components') and self.components is not None:
            _dict['components'] = [x.to_dict() for x in self.components]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GetMultiComponentsResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GetMultiComponentsResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GetMultiComponentsResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GetNotificationsResponse():
    """
    GetNotificationsResponse.

    :attr float total: (optional) Number of notifications in database.
    :attr float returning: (optional) Number of notifications returned.
    :attr List[NotificationData] notifications: (optional) This array is ordered by
          creation date.
    """

    def __init__(self,
                 *,
                 total: float = None,
                 returning: float = None,
                 notifications: List['NotificationData'] = None) -> None:
        """
        Initialize a GetNotificationsResponse object.

        :param float total: (optional) Number of notifications in database.
        :param float returning: (optional) Number of notifications returned.
        :param List[NotificationData] notifications: (optional) This array is
               ordered by creation date.
        """
        self.total = total
        self.returning = returning
        self.notifications = notifications

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GetNotificationsResponse':
        """Initialize a GetNotificationsResponse object from a json dictionary."""
        args = {}
        if 'total' in _dict:
            args['total'] = _dict.get('total')
        if 'returning' in _dict:
            args['returning'] = _dict.get('returning')
        if 'notifications' in _dict:
            args['notifications'] = [NotificationData.from_dict(x) for x in _dict.get('notifications')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GetNotificationsResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'total') and self.total is not None:
            _dict['total'] = self.total
        if hasattr(self, 'returning') and self.returning is not None:
            _dict['returning'] = self.returning
        if hasattr(self, 'notifications') and self.notifications is not None:
            _dict['notifications'] = [x.to_dict() for x in self.notifications]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GetNotificationsResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GetNotificationsResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GetNotificationsResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GetPublicSettingsResponse():
    """
    Contains the details of all public settings for the UI.

    :attr str activity_tracker_path: (optional) The path to the activity tracker
          file. This file holds details of all activity. Defaults to '?' (disabled).
    :attr str athena_id: (optional) Random/unique id for the process running the IBP
          console server.
    :attr str auth_scheme: (optional) The type of auth protecting the UI.
    :attr str callback_uri: (optional) Route used for an SSO callback uri. Only used
          if AUTH_SCHEME is "iam".
    :attr GetPublicSettingsResponseCLUSTERDATA cluster_data: (optional)
    :attr str configtxlator_url: (optional) URL used for a configtxlator rest
          server.
    :attr GetPublicSettingsResponseCRN crn: (optional) metadata about the IBM Cloud
          service instance. [Only populated if using IBM Cloud].
    :attr str crn_string: (optional)
    :attr List[str] csp_header_values: (optional) array of strings that define the
          Content Security Policy headers for the IBP console.
    :attr str db_system: (optional) The id of the database for internal documents.
    :attr str deployer_url: (optional) URL of the companion application for the IBP
          console.
    :attr str domain: (optional) Browser cookies will use this value for their
          domain property. Thus it should match the URL's domain in the browser. `null` is
          valid if serving over http.
    :attr str environment: (optional) Either "dev" "staging" or "prod". Controls
          different security settings and minor things such as the amount of time to cache
          content.
    :attr GetPublicSettingsResponseFABRICCAPABILITIES fabric_capabilities:
          (optional) Contains the Hyperledger Fabric capabilities flags that should be
          used.
    :attr object feature_flags: (optional) Configures th IBP console to
          enable/disable features.
    :attr GetPublicSettingsResponseFILELOGGING file_logging: (optional) File logging
          settings.
    :attr str host_url: (optional) The external URL to reach the IBP console.
    :attr bool iam_cache_enabled: (optional) If true an in memory cache will be used
          to interface with the IBM IAM (an authorization) service. [Only applies if IBP
          is running in IBM Cloud].
    :attr str iam_url: (optional) The URL to reach the IBM IAM service. [Only
          applies if IBP is running in IBM Cloud].
    :attr str ibm_id_callback_url: (optional) The URL to use during SSO login with
          the IBM IAM service. [Only applies if IBP is running in IBM Cloud].
    :attr bool ignore_config_file: (optional) If true the config file will not be
          loaded during startup. Thus settings in the config file will not take effect.
    :attr GetPublicSettingsResponseINACTIVITYTIMEOUTS inactivity_timeouts:
          (optional)
    :attr str infrastructure: (optional) What type of infrastructure is being used
          to run the IBP console. "ibmcloud", "azure", "other".
    :attr str landing_url: (optional)
    :attr str login_uri: (optional) path for user login.
    :attr str logout_uri: (optional) path for user logout.
    :attr float max_req_per_min: (optional) The number of `/api/*` requests per
          minute to allow. Exceeding this limit results in 429 error responses.
    :attr float max_req_per_min_ak: (optional) The number of `/ak/api/*` requests
          per minute to allow. Exceeding this limit results in 429 error responses.
    :attr bool memory_cache_enabled: (optional) If true an in memory cache will be
          used against couchdb requests.
    :attr str port: (optional) Internal port that IBP console is running on.
    :attr bool proxy_cache_enabled: (optional) If true an in memory cache will be
          used for internal proxy requests.
    :attr str proxy_tls_fabric_reqs: (optional) If `"always"` requests to Fabric
          components will go through the IBP console server. If `true` requests to Fabric
          components with IP based URLs will go through the IBP console server, while
          Fabric components with hostname based URLs will go directly from the browser to
          the component. If `false` all requests to Fabric components will go directly
          from the browser to the component.
    :attr str proxy_tls_http_url: (optional) The URL to use to proxy an http request
          to a Fabric component.
    :attr object proxy_tls_ws_url: (optional) The URL to use to proxy WebSocket
          request to a Fabric component.
    :attr str region: (optional) If it's "local", things like https are disabled.
    :attr bool session_cache_enabled: (optional) If true an in memory cache will be
          used for browser session data.
    :attr object timeouts: (optional) Various timeouts for different Fabric
          operations.
    :attr SettingsTimestampData timestamps: (optional)
    :attr object transaction_visibility: (optional) Controls if Fabric transaction
          details are visible on the UI.
    :attr str trust_proxy: (optional) Controls if proxy headers such as
          `X-Forwarded-*` should be parsed to gather data such as the client's IP.
    :attr bool trust_unknown_certs: (optional) Controls if signatures in a signature
          collection APIs should skip verification or not.
    :attr GetPublicSettingsResponseVERSIONS versions: (optional) The various commit
          hashes of components powering this IBP console.
    """

    def __init__(self,
                 *,
                 activity_tracker_path: str = None,
                 athena_id: str = None,
                 auth_scheme: str = None,
                 callback_uri: str = None,
                 cluster_data: 'GetPublicSettingsResponseCLUSTERDATA' = None,
                 configtxlator_url: str = None,
                 crn: 'GetPublicSettingsResponseCRN' = None,
                 crn_string: str = None,
                 csp_header_values: List[str] = None,
                 db_system: str = None,
                 deployer_url: str = None,
                 domain: str = None,
                 environment: str = None,
                 fabric_capabilities: 'GetPublicSettingsResponseFABRICCAPABILITIES' = None,
                 feature_flags: object = None,
                 file_logging: 'GetPublicSettingsResponseFILELOGGING' = None,
                 host_url: str = None,
                 iam_cache_enabled: bool = None,
                 iam_url: str = None,
                 ibm_id_callback_url: str = None,
                 ignore_config_file: bool = None,
                 inactivity_timeouts: 'GetPublicSettingsResponseINACTIVITYTIMEOUTS' = None,
                 infrastructure: str = None,
                 landing_url: str = None,
                 login_uri: str = None,
                 logout_uri: str = None,
                 max_req_per_min: float = None,
                 max_req_per_min_ak: float = None,
                 memory_cache_enabled: bool = None,
                 port: str = None,
                 proxy_cache_enabled: bool = None,
                 proxy_tls_fabric_reqs: str = None,
                 proxy_tls_http_url: str = None,
                 proxy_tls_ws_url: object = None,
                 region: str = None,
                 session_cache_enabled: bool = None,
                 timeouts: object = None,
                 timestamps: 'SettingsTimestampData' = None,
                 transaction_visibility: object = None,
                 trust_proxy: str = None,
                 trust_unknown_certs: bool = None,
                 versions: 'GetPublicSettingsResponseVERSIONS' = None) -> None:
        """
        Initialize a GetPublicSettingsResponse object.

        :param str activity_tracker_path: (optional) The path to the activity
               tracker file. This file holds details of all activity. Defaults to '?'
               (disabled).
        :param str athena_id: (optional) Random/unique id for the process running
               the IBP console server.
        :param str auth_scheme: (optional) The type of auth protecting the UI.
        :param str callback_uri: (optional) Route used for an SSO callback uri.
               Only used if AUTH_SCHEME is "iam".
        :param GetPublicSettingsResponseCLUSTERDATA cluster_data: (optional)
        :param str configtxlator_url: (optional) URL used for a configtxlator rest
               server.
        :param GetPublicSettingsResponseCRN crn: (optional) metadata about the IBM
               Cloud service instance. [Only populated if using IBM Cloud].
        :param str crn_string: (optional)
        :param List[str] csp_header_values: (optional) array of strings that define
               the Content Security Policy headers for the IBP console.
        :param str db_system: (optional) The id of the database for internal
               documents.
        :param str deployer_url: (optional) URL of the companion application for
               the IBP console.
        :param str domain: (optional) Browser cookies will use this value for their
               domain property. Thus it should match the URL's domain in the browser.
               `null` is valid if serving over http.
        :param str environment: (optional) Either "dev" "staging" or "prod".
               Controls different security settings and minor things such as the amount of
               time to cache content.
        :param GetPublicSettingsResponseFABRICCAPABILITIES fabric_capabilities:
               (optional) Contains the Hyperledger Fabric capabilities flags that should
               be used.
        :param object feature_flags: (optional) Configures th IBP console to
               enable/disable features.
        :param GetPublicSettingsResponseFILELOGGING file_logging: (optional) File
               logging settings.
        :param str host_url: (optional) The external URL to reach the IBP console.
        :param bool iam_cache_enabled: (optional) If true an in memory cache will
               be used to interface with the IBM IAM (an authorization) service. [Only
               applies if IBP is running in IBM Cloud].
        :param str iam_url: (optional) The URL to reach the IBM IAM service. [Only
               applies if IBP is running in IBM Cloud].
        :param str ibm_id_callback_url: (optional) The URL to use during SSO login
               with the IBM IAM service. [Only applies if IBP is running in IBM Cloud].
        :param bool ignore_config_file: (optional) If true the config file will not
               be loaded during startup. Thus settings in the config file will not take
               effect.
        :param GetPublicSettingsResponseINACTIVITYTIMEOUTS inactivity_timeouts:
               (optional)
        :param str infrastructure: (optional) What type of infrastructure is being
               used to run the IBP console. "ibmcloud", "azure", "other".
        :param str landing_url: (optional)
        :param str login_uri: (optional) path for user login.
        :param str logout_uri: (optional) path for user logout.
        :param float max_req_per_min: (optional) The number of `/api/*` requests
               per minute to allow. Exceeding this limit results in 429 error responses.
        :param float max_req_per_min_ak: (optional) The number of `/ak/api/*`
               requests per minute to allow. Exceeding this limit results in 429 error
               responses.
        :param bool memory_cache_enabled: (optional) If true an in memory cache
               will be used against couchdb requests.
        :param str port: (optional) Internal port that IBP console is running on.
        :param bool proxy_cache_enabled: (optional) If true an in memory cache will
               be used for internal proxy requests.
        :param str proxy_tls_fabric_reqs: (optional) If `"always"` requests to
               Fabric components will go through the IBP console server. If `true`
               requests to Fabric components with IP based URLs will go through the IBP
               console server, while Fabric components with hostname based URLs will go
               directly from the browser to the component. If `false` all requests to
               Fabric components will go directly from the browser to the component.
        :param str proxy_tls_http_url: (optional) The URL to use to proxy an http
               request to a Fabric component.
        :param object proxy_tls_ws_url: (optional) The URL to use to proxy
               WebSocket request to a Fabric component.
        :param str region: (optional) If it's "local", things like https are
               disabled.
        :param bool session_cache_enabled: (optional) If true an in memory cache
               will be used for browser session data.
        :param object timeouts: (optional) Various timeouts for different Fabric
               operations.
        :param SettingsTimestampData timestamps: (optional)
        :param object transaction_visibility: (optional) Controls if Fabric
               transaction details are visible on the UI.
        :param str trust_proxy: (optional) Controls if proxy headers such as
               `X-Forwarded-*` should be parsed to gather data such as the client's IP.
        :param bool trust_unknown_certs: (optional) Controls if signatures in a
               signature collection APIs should skip verification or not.
        :param GetPublicSettingsResponseVERSIONS versions: (optional) The various
               commit hashes of components powering this IBP console.
        """
        self.activity_tracker_path = activity_tracker_path
        self.athena_id = athena_id
        self.auth_scheme = auth_scheme
        self.callback_uri = callback_uri
        self.cluster_data = cluster_data
        self.configtxlator_url = configtxlator_url
        self.crn = crn
        self.crn_string = crn_string
        self.csp_header_values = csp_header_values
        self.db_system = db_system
        self.deployer_url = deployer_url
        self.domain = domain
        self.environment = environment
        self.fabric_capabilities = fabric_capabilities
        self.feature_flags = feature_flags
        self.file_logging = file_logging
        self.host_url = host_url
        self.iam_cache_enabled = iam_cache_enabled
        self.iam_url = iam_url
        self.ibm_id_callback_url = ibm_id_callback_url
        self.ignore_config_file = ignore_config_file
        self.inactivity_timeouts = inactivity_timeouts
        self.infrastructure = infrastructure
        self.landing_url = landing_url
        self.login_uri = login_uri
        self.logout_uri = logout_uri
        self.max_req_per_min = max_req_per_min
        self.max_req_per_min_ak = max_req_per_min_ak
        self.memory_cache_enabled = memory_cache_enabled
        self.port = port
        self.proxy_cache_enabled = proxy_cache_enabled
        self.proxy_tls_fabric_reqs = proxy_tls_fabric_reqs
        self.proxy_tls_http_url = proxy_tls_http_url
        self.proxy_tls_ws_url = proxy_tls_ws_url
        self.region = region
        self.session_cache_enabled = session_cache_enabled
        self.timeouts = timeouts
        self.timestamps = timestamps
        self.transaction_visibility = transaction_visibility
        self.trust_proxy = trust_proxy
        self.trust_unknown_certs = trust_unknown_certs
        self.versions = versions

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GetPublicSettingsResponse':
        """Initialize a GetPublicSettingsResponse object from a json dictionary."""
        args = {}
        if 'ACTIVITY_TRACKER_PATH' in _dict:
            args['activity_tracker_path'] = _dict.get('ACTIVITY_TRACKER_PATH')
        if 'ATHENA_ID' in _dict:
            args['athena_id'] = _dict.get('ATHENA_ID')
        if 'AUTH_SCHEME' in _dict:
            args['auth_scheme'] = _dict.get('AUTH_SCHEME')
        if 'CALLBACK_URI' in _dict:
            args['callback_uri'] = _dict.get('CALLBACK_URI')
        if 'CLUSTER_DATA' in _dict:
            args['cluster_data'] = GetPublicSettingsResponseCLUSTERDATA.from_dict(_dict.get('CLUSTER_DATA'))
        if 'CONFIGTXLATOR_URL' in _dict:
            args['configtxlator_url'] = _dict.get('CONFIGTXLATOR_URL')
        if 'CRN' in _dict:
            args['crn'] = GetPublicSettingsResponseCRN.from_dict(_dict.get('CRN'))
        if 'CRN_STRING' in _dict:
            args['crn_string'] = _dict.get('CRN_STRING')
        if 'CSP_HEADER_VALUES' in _dict:
            args['csp_header_values'] = _dict.get('CSP_HEADER_VALUES')
        if 'DB_SYSTEM' in _dict:
            args['db_system'] = _dict.get('DB_SYSTEM')
        if 'DEPLOYER_URL' in _dict:
            args['deployer_url'] = _dict.get('DEPLOYER_URL')
        if 'DOMAIN' in _dict:
            args['domain'] = _dict.get('DOMAIN')
        if 'ENVIRONMENT' in _dict:
            args['environment'] = _dict.get('ENVIRONMENT')
        if 'FABRIC_CAPABILITIES' in _dict:
            args['fabric_capabilities'] = GetPublicSettingsResponseFABRICCAPABILITIES.from_dict(_dict.get('FABRIC_CAPABILITIES'))
        if 'FEATURE_FLAGS' in _dict:
            args['feature_flags'] = _dict.get('FEATURE_FLAGS')
        if 'FILE_LOGGING' in _dict:
            args['file_logging'] = GetPublicSettingsResponseFILELOGGING.from_dict(_dict.get('FILE_LOGGING'))
        if 'HOST_URL' in _dict:
            args['host_url'] = _dict.get('HOST_URL')
        if 'IAM_CACHE_ENABLED' in _dict:
            args['iam_cache_enabled'] = _dict.get('IAM_CACHE_ENABLED')
        if 'IAM_URL' in _dict:
            args['iam_url'] = _dict.get('IAM_URL')
        if 'IBM_ID_CALLBACK_URL' in _dict:
            args['ibm_id_callback_url'] = _dict.get('IBM_ID_CALLBACK_URL')
        if 'IGNORE_CONFIG_FILE' in _dict:
            args['ignore_config_file'] = _dict.get('IGNORE_CONFIG_FILE')
        if 'INACTIVITY_TIMEOUTS' in _dict:
            args['inactivity_timeouts'] = GetPublicSettingsResponseINACTIVITYTIMEOUTS.from_dict(_dict.get('INACTIVITY_TIMEOUTS'))
        if 'INFRASTRUCTURE' in _dict:
            args['infrastructure'] = _dict.get('INFRASTRUCTURE')
        if 'LANDING_URL' in _dict:
            args['landing_url'] = _dict.get('LANDING_URL')
        if 'LOGIN_URI' in _dict:
            args['login_uri'] = _dict.get('LOGIN_URI')
        if 'LOGOUT_URI' in _dict:
            args['logout_uri'] = _dict.get('LOGOUT_URI')
        if 'MAX_REQ_PER_MIN' in _dict:
            args['max_req_per_min'] = _dict.get('MAX_REQ_PER_MIN')
        if 'MAX_REQ_PER_MIN_AK' in _dict:
            args['max_req_per_min_ak'] = _dict.get('MAX_REQ_PER_MIN_AK')
        if 'MEMORY_CACHE_ENABLED' in _dict:
            args['memory_cache_enabled'] = _dict.get('MEMORY_CACHE_ENABLED')
        if 'PORT' in _dict:
            args['port'] = _dict.get('PORT')
        if 'PROXY_CACHE_ENABLED' in _dict:
            args['proxy_cache_enabled'] = _dict.get('PROXY_CACHE_ENABLED')
        if 'PROXY_TLS_FABRIC_REQS' in _dict:
            args['proxy_tls_fabric_reqs'] = _dict.get('PROXY_TLS_FABRIC_REQS')
        if 'PROXY_TLS_HTTP_URL' in _dict:
            args['proxy_tls_http_url'] = _dict.get('PROXY_TLS_HTTP_URL')
        if 'PROXY_TLS_WS_URL' in _dict:
            args['proxy_tls_ws_url'] = _dict.get('PROXY_TLS_WS_URL')
        if 'REGION' in _dict:
            args['region'] = _dict.get('REGION')
        if 'SESSION_CACHE_ENABLED' in _dict:
            args['session_cache_enabled'] = _dict.get('SESSION_CACHE_ENABLED')
        if 'TIMEOUTS' in _dict:
            args['timeouts'] = _dict.get('TIMEOUTS')
        if 'TIMESTAMPS' in _dict:
            args['timestamps'] = SettingsTimestampData.from_dict(_dict.get('TIMESTAMPS'))
        if 'TRANSACTION_VISIBILITY' in _dict:
            args['transaction_visibility'] = _dict.get('TRANSACTION_VISIBILITY')
        if 'TRUST_PROXY' in _dict:
            args['trust_proxy'] = _dict.get('TRUST_PROXY')
        if 'TRUST_UNKNOWN_CERTS' in _dict:
            args['trust_unknown_certs'] = _dict.get('TRUST_UNKNOWN_CERTS')
        if 'VERSIONS' in _dict:
            args['versions'] = GetPublicSettingsResponseVERSIONS.from_dict(_dict.get('VERSIONS'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GetPublicSettingsResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'activity_tracker_path') and self.activity_tracker_path is not None:
            _dict['ACTIVITY_TRACKER_PATH'] = self.activity_tracker_path
        if hasattr(self, 'athena_id') and self.athena_id is not None:
            _dict['ATHENA_ID'] = self.athena_id
        if hasattr(self, 'auth_scheme') and self.auth_scheme is not None:
            _dict['AUTH_SCHEME'] = self.auth_scheme
        if hasattr(self, 'callback_uri') and self.callback_uri is not None:
            _dict['CALLBACK_URI'] = self.callback_uri
        if hasattr(self, 'cluster_data') and self.cluster_data is not None:
            _dict['CLUSTER_DATA'] = self.cluster_data.to_dict()
        if hasattr(self, 'configtxlator_url') and self.configtxlator_url is not None:
            _dict['CONFIGTXLATOR_URL'] = self.configtxlator_url
        if hasattr(self, 'crn') and self.crn is not None:
            _dict['CRN'] = self.crn.to_dict()
        if hasattr(self, 'crn_string') and self.crn_string is not None:
            _dict['CRN_STRING'] = self.crn_string
        if hasattr(self, 'csp_header_values') and self.csp_header_values is not None:
            _dict['CSP_HEADER_VALUES'] = self.csp_header_values
        if hasattr(self, 'db_system') and self.db_system is not None:
            _dict['DB_SYSTEM'] = self.db_system
        if hasattr(self, 'deployer_url') and self.deployer_url is not None:
            _dict['DEPLOYER_URL'] = self.deployer_url
        if hasattr(self, 'domain') and self.domain is not None:
            _dict['DOMAIN'] = self.domain
        if hasattr(self, 'environment') and self.environment is not None:
            _dict['ENVIRONMENT'] = self.environment
        if hasattr(self, 'fabric_capabilities') and self.fabric_capabilities is not None:
            _dict['FABRIC_CAPABILITIES'] = self.fabric_capabilities.to_dict()
        if hasattr(self, 'feature_flags') and self.feature_flags is not None:
            _dict['FEATURE_FLAGS'] = self.feature_flags
        if hasattr(self, 'file_logging') and self.file_logging is not None:
            _dict['FILE_LOGGING'] = self.file_logging.to_dict()
        if hasattr(self, 'host_url') and self.host_url is not None:
            _dict['HOST_URL'] = self.host_url
        if hasattr(self, 'iam_cache_enabled') and self.iam_cache_enabled is not None:
            _dict['IAM_CACHE_ENABLED'] = self.iam_cache_enabled
        if hasattr(self, 'iam_url') and self.iam_url is not None:
            _dict['IAM_URL'] = self.iam_url
        if hasattr(self, 'ibm_id_callback_url') and self.ibm_id_callback_url is not None:
            _dict['IBM_ID_CALLBACK_URL'] = self.ibm_id_callback_url
        if hasattr(self, 'ignore_config_file') and self.ignore_config_file is not None:
            _dict['IGNORE_CONFIG_FILE'] = self.ignore_config_file
        if hasattr(self, 'inactivity_timeouts') and self.inactivity_timeouts is not None:
            _dict['INACTIVITY_TIMEOUTS'] = self.inactivity_timeouts.to_dict()
        if hasattr(self, 'infrastructure') and self.infrastructure is not None:
            _dict['INFRASTRUCTURE'] = self.infrastructure
        if hasattr(self, 'landing_url') and self.landing_url is not None:
            _dict['LANDING_URL'] = self.landing_url
        if hasattr(self, 'login_uri') and self.login_uri is not None:
            _dict['LOGIN_URI'] = self.login_uri
        if hasattr(self, 'logout_uri') and self.logout_uri is not None:
            _dict['LOGOUT_URI'] = self.logout_uri
        if hasattr(self, 'max_req_per_min') and self.max_req_per_min is not None:
            _dict['MAX_REQ_PER_MIN'] = self.max_req_per_min
        if hasattr(self, 'max_req_per_min_ak') and self.max_req_per_min_ak is not None:
            _dict['MAX_REQ_PER_MIN_AK'] = self.max_req_per_min_ak
        if hasattr(self, 'memory_cache_enabled') and self.memory_cache_enabled is not None:
            _dict['MEMORY_CACHE_ENABLED'] = self.memory_cache_enabled
        if hasattr(self, 'port') and self.port is not None:
            _dict['PORT'] = self.port
        if hasattr(self, 'proxy_cache_enabled') and self.proxy_cache_enabled is not None:
            _dict['PROXY_CACHE_ENABLED'] = self.proxy_cache_enabled
        if hasattr(self, 'proxy_tls_fabric_reqs') and self.proxy_tls_fabric_reqs is not None:
            _dict['PROXY_TLS_FABRIC_REQS'] = self.proxy_tls_fabric_reqs
        if hasattr(self, 'proxy_tls_http_url') and self.proxy_tls_http_url is not None:
            _dict['PROXY_TLS_HTTP_URL'] = self.proxy_tls_http_url
        if hasattr(self, 'proxy_tls_ws_url') and self.proxy_tls_ws_url is not None:
            _dict['PROXY_TLS_WS_URL'] = self.proxy_tls_ws_url
        if hasattr(self, 'region') and self.region is not None:
            _dict['REGION'] = self.region
        if hasattr(self, 'session_cache_enabled') and self.session_cache_enabled is not None:
            _dict['SESSION_CACHE_ENABLED'] = self.session_cache_enabled
        if hasattr(self, 'timeouts') and self.timeouts is not None:
            _dict['TIMEOUTS'] = self.timeouts
        if hasattr(self, 'timestamps') and self.timestamps is not None:
            _dict['TIMESTAMPS'] = self.timestamps.to_dict()
        if hasattr(self, 'transaction_visibility') and self.transaction_visibility is not None:
            _dict['TRANSACTION_VISIBILITY'] = self.transaction_visibility
        if hasattr(self, 'trust_proxy') and self.trust_proxy is not None:
            _dict['TRUST_PROXY'] = self.trust_proxy
        if hasattr(self, 'trust_unknown_certs') and self.trust_unknown_certs is not None:
            _dict['TRUST_UNKNOWN_CERTS'] = self.trust_unknown_certs
        if hasattr(self, 'versions') and self.versions is not None:
            _dict['VERSIONS'] = self.versions.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GetPublicSettingsResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GetPublicSettingsResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GetPublicSettingsResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GetPublicSettingsResponseCLUSTERDATA():
    """
    GetPublicSettingsResponseCLUSTERDATA.

    :attr str type: (optional) Indicates whether this is a paid or free IBP console.
    """

    def __init__(self,
                 *,
                 type: str = None) -> None:
        """
        Initialize a GetPublicSettingsResponseCLUSTERDATA object.

        :param str type: (optional) Indicates whether this is a paid or free IBP
               console.
        """
        self.type = type

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GetPublicSettingsResponseCLUSTERDATA':
        """Initialize a GetPublicSettingsResponseCLUSTERDATA object from a json dictionary."""
        args = {}
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GetPublicSettingsResponseCLUSTERDATA object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GetPublicSettingsResponseCLUSTERDATA object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GetPublicSettingsResponseCLUSTERDATA') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GetPublicSettingsResponseCLUSTERDATA') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GetPublicSettingsResponseCRN():
    """
    metadata about the IBM Cloud service instance. [Only populated if using IBM Cloud].

    :attr str account_id: (optional)
    :attr str c_name: (optional)
    :attr str c_type: (optional)
    :attr str instance_id: (optional)
    :attr str location: (optional)
    :attr str resource_id: (optional)
    :attr str resource_type: (optional)
    :attr str service_name: (optional)
    :attr str version: (optional)
    """

    def __init__(self,
                 *,
                 account_id: str = None,
                 c_name: str = None,
                 c_type: str = None,
                 instance_id: str = None,
                 location: str = None,
                 resource_id: str = None,
                 resource_type: str = None,
                 service_name: str = None,
                 version: str = None) -> None:
        """
        Initialize a GetPublicSettingsResponseCRN object.

        :param str account_id: (optional)
        :param str c_name: (optional)
        :param str c_type: (optional)
        :param str instance_id: (optional)
        :param str location: (optional)
        :param str resource_id: (optional)
        :param str resource_type: (optional)
        :param str service_name: (optional)
        :param str version: (optional)
        """
        self.account_id = account_id
        self.c_name = c_name
        self.c_type = c_type
        self.instance_id = instance_id
        self.location = location
        self.resource_id = resource_id
        self.resource_type = resource_type
        self.service_name = service_name
        self.version = version

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GetPublicSettingsResponseCRN':
        """Initialize a GetPublicSettingsResponseCRN object from a json dictionary."""
        args = {}
        if 'account_id' in _dict:
            args['account_id'] = _dict.get('account_id')
        if 'c_name' in _dict:
            args['c_name'] = _dict.get('c_name')
        if 'c_type' in _dict:
            args['c_type'] = _dict.get('c_type')
        if 'instance_id' in _dict:
            args['instance_id'] = _dict.get('instance_id')
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'resource_id' in _dict:
            args['resource_id'] = _dict.get('resource_id')
        if 'resource_type' in _dict:
            args['resource_type'] = _dict.get('resource_type')
        if 'service_name' in _dict:
            args['service_name'] = _dict.get('service_name')
        if 'version' in _dict:
            args['version'] = _dict.get('version')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GetPublicSettingsResponseCRN object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'account_id') and self.account_id is not None:
            _dict['account_id'] = self.account_id
        if hasattr(self, 'c_name') and self.c_name is not None:
            _dict['c_name'] = self.c_name
        if hasattr(self, 'c_type') and self.c_type is not None:
            _dict['c_type'] = self.c_type
        if hasattr(self, 'instance_id') and self.instance_id is not None:
            _dict['instance_id'] = self.instance_id
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'resource_id') and self.resource_id is not None:
            _dict['resource_id'] = self.resource_id
        if hasattr(self, 'resource_type') and self.resource_type is not None:
            _dict['resource_type'] = self.resource_type
        if hasattr(self, 'service_name') and self.service_name is not None:
            _dict['service_name'] = self.service_name
        if hasattr(self, 'version') and self.version is not None:
            _dict['version'] = self.version
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GetPublicSettingsResponseCRN object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GetPublicSettingsResponseCRN') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GetPublicSettingsResponseCRN') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GetPublicSettingsResponseFABRICCAPABILITIES():
    """
    Contains the Hyperledger Fabric capabilities flags that should be used.

    :attr List[str] application: (optional)
    :attr List[str] channel: (optional)
    :attr List[str] orderer: (optional)
    """

    def __init__(self,
                 *,
                 application: List[str] = None,
                 channel: List[str] = None,
                 orderer: List[str] = None) -> None:
        """
        Initialize a GetPublicSettingsResponseFABRICCAPABILITIES object.

        :param List[str] application: (optional)
        :param List[str] channel: (optional)
        :param List[str] orderer: (optional)
        """
        self.application = application
        self.channel = channel
        self.orderer = orderer

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GetPublicSettingsResponseFABRICCAPABILITIES':
        """Initialize a GetPublicSettingsResponseFABRICCAPABILITIES object from a json dictionary."""
        args = {}
        if 'application' in _dict:
            args['application'] = _dict.get('application')
        if 'channel' in _dict:
            args['channel'] = _dict.get('channel')
        if 'orderer' in _dict:
            args['orderer'] = _dict.get('orderer')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GetPublicSettingsResponseFABRICCAPABILITIES object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'application') and self.application is not None:
            _dict['application'] = self.application
        if hasattr(self, 'channel') and self.channel is not None:
            _dict['channel'] = self.channel
        if hasattr(self, 'orderer') and self.orderer is not None:
            _dict['orderer'] = self.orderer
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GetPublicSettingsResponseFABRICCAPABILITIES object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GetPublicSettingsResponseFABRICCAPABILITIES') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GetPublicSettingsResponseFABRICCAPABILITIES') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GetPublicSettingsResponseFILELOGGING():
    """
    File logging settings.

    :attr LogSettingsResponse server: (optional) The logging settings for the client
          and server.
    :attr LogSettingsResponse client: (optional) The logging settings for the client
          and server.
    """

    def __init__(self,
                 *,
                 server: 'LogSettingsResponse' = None,
                 client: 'LogSettingsResponse' = None) -> None:
        """
        Initialize a GetPublicSettingsResponseFILELOGGING object.

        :param LogSettingsResponse server: (optional) The logging settings for the
               client and server.
        :param LogSettingsResponse client: (optional) The logging settings for the
               client and server.
        """
        self.server = server
        self.client = client

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GetPublicSettingsResponseFILELOGGING':
        """Initialize a GetPublicSettingsResponseFILELOGGING object from a json dictionary."""
        args = {}
        if 'server' in _dict:
            args['server'] = LogSettingsResponse.from_dict(_dict.get('server'))
        if 'client' in _dict:
            args['client'] = LogSettingsResponse.from_dict(_dict.get('client'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GetPublicSettingsResponseFILELOGGING object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'server') and self.server is not None:
            _dict['server'] = self.server.to_dict()
        if hasattr(self, 'client') and self.client is not None:
            _dict['client'] = self.client.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GetPublicSettingsResponseFILELOGGING object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GetPublicSettingsResponseFILELOGGING') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GetPublicSettingsResponseFILELOGGING') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GetPublicSettingsResponseINACTIVITYTIMEOUTS():
    """
    GetPublicSettingsResponseINACTIVITYTIMEOUTS.

    :attr bool enabled: (optional)
    :attr float max_idle_time: (optional) How long to wait before auto-logging out a
          user. In milliseconds.
    """

    def __init__(self,
                 *,
                 enabled: bool = None,
                 max_idle_time: float = None) -> None:
        """
        Initialize a GetPublicSettingsResponseINACTIVITYTIMEOUTS object.

        :param bool enabled: (optional)
        :param float max_idle_time: (optional) How long to wait before auto-logging
               out a user. In milliseconds.
        """
        self.enabled = enabled
        self.max_idle_time = max_idle_time

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GetPublicSettingsResponseINACTIVITYTIMEOUTS':
        """Initialize a GetPublicSettingsResponseINACTIVITYTIMEOUTS object from a json dictionary."""
        args = {}
        if 'enabled' in _dict:
            args['enabled'] = _dict.get('enabled')
        if 'max_idle_time' in _dict:
            args['max_idle_time'] = _dict.get('max_idle_time')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GetPublicSettingsResponseINACTIVITYTIMEOUTS object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'enabled') and self.enabled is not None:
            _dict['enabled'] = self.enabled
        if hasattr(self, 'max_idle_time') and self.max_idle_time is not None:
            _dict['max_idle_time'] = self.max_idle_time
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GetPublicSettingsResponseINACTIVITYTIMEOUTS object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GetPublicSettingsResponseINACTIVITYTIMEOUTS') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GetPublicSettingsResponseINACTIVITYTIMEOUTS') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class GetPublicSettingsResponseVERSIONS():
    """
    The various commit hashes of components powering this IBP console.

    :attr str apollo: (optional) The commit hash of Apollo code (front-end).
    :attr str athena: (optional) The commit hash of Athena code (back-end).
    :attr str stitch: (optional) The commit hash of Stitch code (fabric-sdk).
    :attr str tag: (optional) The tag of the build powering this IBP console.
    """

    def __init__(self,
                 *,
                 apollo: str = None,
                 athena: str = None,
                 stitch: str = None,
                 tag: str = None) -> None:
        """
        Initialize a GetPublicSettingsResponseVERSIONS object.

        :param str apollo: (optional) The commit hash of Apollo code (front-end).
        :param str athena: (optional) The commit hash of Athena code (back-end).
        :param str stitch: (optional) The commit hash of Stitch code (fabric-sdk).
        :param str tag: (optional) The tag of the build powering this IBP console.
        """
        self.apollo = apollo
        self.athena = athena
        self.stitch = stitch
        self.tag = tag

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'GetPublicSettingsResponseVERSIONS':
        """Initialize a GetPublicSettingsResponseVERSIONS object from a json dictionary."""
        args = {}
        if 'apollo' in _dict:
            args['apollo'] = _dict.get('apollo')
        if 'athena' in _dict:
            args['athena'] = _dict.get('athena')
        if 'stitch' in _dict:
            args['stitch'] = _dict.get('stitch')
        if 'tag' in _dict:
            args['tag'] = _dict.get('tag')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a GetPublicSettingsResponseVERSIONS object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'apollo') and self.apollo is not None:
            _dict['apollo'] = self.apollo
        if hasattr(self, 'athena') and self.athena is not None:
            _dict['athena'] = self.athena
        if hasattr(self, 'stitch') and self.stitch is not None:
            _dict['stitch'] = self.stitch
        if hasattr(self, 'tag') and self.tag is not None:
            _dict['tag'] = self.tag
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this GetPublicSettingsResponseVERSIONS object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'GetPublicSettingsResponseVERSIONS') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'GetPublicSettingsResponseVERSIONS') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ImportCaBodyMsp():
    """
    ImportCaBodyMsp.

    :attr ImportCaBodyMspCa ca:
    :attr ImportCaBodyMspTlsca tlsca:
    :attr ImportCaBodyMspComponent component:
    """

    def __init__(self,
                 ca: 'ImportCaBodyMspCa',
                 tlsca: 'ImportCaBodyMspTlsca',
                 component: 'ImportCaBodyMspComponent') -> None:
        """
        Initialize a ImportCaBodyMsp object.

        :param ImportCaBodyMspCa ca:
        :param ImportCaBodyMspTlsca tlsca:
        :param ImportCaBodyMspComponent component:
        """
        self.ca = ca
        self.tlsca = tlsca
        self.component = component

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ImportCaBodyMsp':
        """Initialize a ImportCaBodyMsp object from a json dictionary."""
        args = {}
        if 'ca' in _dict:
            args['ca'] = ImportCaBodyMspCa.from_dict(_dict.get('ca'))
        else:
            raise ValueError('Required property \'ca\' not present in ImportCaBodyMsp JSON')
        if 'tlsca' in _dict:
            args['tlsca'] = ImportCaBodyMspTlsca.from_dict(_dict.get('tlsca'))
        else:
            raise ValueError('Required property \'tlsca\' not present in ImportCaBodyMsp JSON')
        if 'component' in _dict:
            args['component'] = ImportCaBodyMspComponent.from_dict(_dict.get('component'))
        else:
            raise ValueError('Required property \'component\' not present in ImportCaBodyMsp JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ImportCaBodyMsp object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        if hasattr(self, 'tlsca') and self.tlsca is not None:
            _dict['tlsca'] = self.tlsca.to_dict()
        if hasattr(self, 'component') and self.component is not None:
            _dict['component'] = self.component.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ImportCaBodyMsp object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ImportCaBodyMsp') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ImportCaBodyMsp') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ImportCaBodyMspCa():
    """
    ImportCaBodyMspCa.

    :attr str name: The "name" to distinguish this CA from the TLS CA.
    :attr List[str] root_certs: (optional) An array that contains one or more base
          64 encoded PEM root certificates for the CA.
    """

    def __init__(self,
                 name: str,
                 *,
                 root_certs: List[str] = None) -> None:
        """
        Initialize a ImportCaBodyMspCa object.

        :param str name: The "name" to distinguish this CA from the TLS CA.
        :param List[str] root_certs: (optional) An array that contains one or more
               base 64 encoded PEM root certificates for the CA.
        """
        self.name = name
        self.root_certs = root_certs

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ImportCaBodyMspCa':
        """Initialize a ImportCaBodyMspCa object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        else:
            raise ValueError('Required property \'name\' not present in ImportCaBodyMspCa JSON')
        if 'root_certs' in _dict:
            args['root_certs'] = _dict.get('root_certs')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ImportCaBodyMspCa object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'root_certs') and self.root_certs is not None:
            _dict['root_certs'] = self.root_certs
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ImportCaBodyMspCa object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ImportCaBodyMspCa') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ImportCaBodyMspCa') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ImportCaBodyMspComponent():
    """
    ImportCaBodyMspComponent.

    :attr str tls_cert: The TLS certificate as base 64 encoded PEM. Certificate is
          used to secure/validate a TLS connection with this component.
    """

    def __init__(self,
                 tls_cert: str) -> None:
        """
        Initialize a ImportCaBodyMspComponent object.

        :param str tls_cert: The TLS certificate as base 64 encoded PEM.
               Certificate is used to secure/validate a TLS connection with this
               component.
        """
        self.tls_cert = tls_cert

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ImportCaBodyMspComponent':
        """Initialize a ImportCaBodyMspComponent object from a json dictionary."""
        args = {}
        if 'tls_cert' in _dict:
            args['tls_cert'] = _dict.get('tls_cert')
        else:
            raise ValueError('Required property \'tls_cert\' not present in ImportCaBodyMspComponent JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ImportCaBodyMspComponent object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'tls_cert') and self.tls_cert is not None:
            _dict['tls_cert'] = self.tls_cert
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ImportCaBodyMspComponent object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ImportCaBodyMspComponent') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ImportCaBodyMspComponent') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ImportCaBodyMspTlsca():
    """
    ImportCaBodyMspTlsca.

    :attr str name: The "name" to distinguish this CA from the other CA.
    :attr List[str] root_certs: (optional) An array that contains one or more base
          64 encoded PEM root certificates for the TLS CA.
    """

    def __init__(self,
                 name: str,
                 *,
                 root_certs: List[str] = None) -> None:
        """
        Initialize a ImportCaBodyMspTlsca object.

        :param str name: The "name" to distinguish this CA from the other CA.
        :param List[str] root_certs: (optional) An array that contains one or more
               base 64 encoded PEM root certificates for the TLS CA.
        """
        self.name = name
        self.root_certs = root_certs

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ImportCaBodyMspTlsca':
        """Initialize a ImportCaBodyMspTlsca object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        else:
            raise ValueError('Required property \'name\' not present in ImportCaBodyMspTlsca JSON')
        if 'root_certs' in _dict:
            args['root_certs'] = _dict.get('root_certs')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ImportCaBodyMspTlsca object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'root_certs') and self.root_certs is not None:
            _dict['root_certs'] = self.root_certs
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ImportCaBodyMspTlsca object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ImportCaBodyMspTlsca') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ImportCaBodyMspTlsca') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class LogSettingsResponse():
    """
    The logging settings for the client and server.

    :attr LoggingSettingsClient client: (optional) The client side (browser) logging
          settings. _Changes to this field will restart the IBP console server(s)_.
    :attr LoggingSettingsServer server: (optional) The server side logging settings.
          _Changes to this field will restart the IBP console server(s)_.
    """

    def __init__(self,
                 *,
                 client: 'LoggingSettingsClient' = None,
                 server: 'LoggingSettingsServer' = None) -> None:
        """
        Initialize a LogSettingsResponse object.

        :param LoggingSettingsClient client: (optional) The client side (browser)
               logging settings. _Changes to this field will restart the IBP console
               server(s)_.
        :param LoggingSettingsServer server: (optional) The server side logging
               settings. _Changes to this field will restart the IBP console server(s)_.
        """
        self.client = client
        self.server = server

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'LogSettingsResponse':
        """Initialize a LogSettingsResponse object from a json dictionary."""
        args = {}
        if 'client' in _dict:
            args['client'] = LoggingSettingsClient.from_dict(_dict.get('client'))
        if 'server' in _dict:
            args['server'] = LoggingSettingsServer.from_dict(_dict.get('server'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a LogSettingsResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'client') and self.client is not None:
            _dict['client'] = self.client.to_dict()
        if hasattr(self, 'server') and self.server is not None:
            _dict['server'] = self.server.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this LogSettingsResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'LogSettingsResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'LogSettingsResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class LoggingSettingsClient():
    """
    The client side (browser) logging settings. _Changes to this field will restart the
    IBP console server(s)_.

    :attr bool enabled: (optional) If `true` logging will be stored to a file on the
          file system.
    :attr str level: (optional) Valid log levels: "error", "warn", "info",
          "verbose", "debug", or "silly".
    :attr bool unique_name: (optional) If `true` log file names will have a random
          suffix.
    """

    def __init__(self,
                 *,
                 enabled: bool = None,
                 level: str = None,
                 unique_name: bool = None) -> None:
        """
        Initialize a LoggingSettingsClient object.

        :param bool enabled: (optional) If `true` logging will be stored to a file
               on the file system.
        :param str level: (optional) Valid log levels: "error", "warn", "info",
               "verbose", "debug", or "silly".
        :param bool unique_name: (optional) If `true` log file names will have a
               random suffix.
        """
        self.enabled = enabled
        self.level = level
        self.unique_name = unique_name

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'LoggingSettingsClient':
        """Initialize a LoggingSettingsClient object from a json dictionary."""
        args = {}
        if 'enabled' in _dict:
            args['enabled'] = _dict.get('enabled')
        if 'level' in _dict:
            args['level'] = _dict.get('level')
        if 'unique_name' in _dict:
            args['unique_name'] = _dict.get('unique_name')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a LoggingSettingsClient object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'enabled') and self.enabled is not None:
            _dict['enabled'] = self.enabled
        if hasattr(self, 'level') and self.level is not None:
            _dict['level'] = self.level
        if hasattr(self, 'unique_name') and self.unique_name is not None:
            _dict['unique_name'] = self.unique_name
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this LoggingSettingsClient object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'LoggingSettingsClient') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'LoggingSettingsClient') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class LevelEnum(str, Enum):
        """
        Valid log levels: "error", "warn", "info", "verbose", "debug", or "silly".
        """
        ERROR = 'error'
        WARN = 'warn'
        INFO = 'info'
        VERBOSE = 'verbose'
        DEBUG = 'debug'
        SILLY = 'silly'


class LoggingSettingsServer():
    """
    The server side logging settings. _Changes to this field will restart the IBP console
    server(s)_.

    :attr bool enabled: (optional) If `true` logging will be stored to a file on the
          file system.
    :attr str level: (optional) Valid log levels: "error", "warn", "info",
          "verbose", "debug", or "silly".
    :attr bool unique_name: (optional) If `true` log file names will have a random
          suffix.
    """

    def __init__(self,
                 *,
                 enabled: bool = None,
                 level: str = None,
                 unique_name: bool = None) -> None:
        """
        Initialize a LoggingSettingsServer object.

        :param bool enabled: (optional) If `true` logging will be stored to a file
               on the file system.
        :param str level: (optional) Valid log levels: "error", "warn", "info",
               "verbose", "debug", or "silly".
        :param bool unique_name: (optional) If `true` log file names will have a
               random suffix.
        """
        self.enabled = enabled
        self.level = level
        self.unique_name = unique_name

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'LoggingSettingsServer':
        """Initialize a LoggingSettingsServer object from a json dictionary."""
        args = {}
        if 'enabled' in _dict:
            args['enabled'] = _dict.get('enabled')
        if 'level' in _dict:
            args['level'] = _dict.get('level')
        if 'unique_name' in _dict:
            args['unique_name'] = _dict.get('unique_name')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a LoggingSettingsServer object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'enabled') and self.enabled is not None:
            _dict['enabled'] = self.enabled
        if hasattr(self, 'level') and self.level is not None:
            _dict['level'] = self.level
        if hasattr(self, 'unique_name') and self.unique_name is not None:
            _dict['unique_name'] = self.unique_name
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this LoggingSettingsServer object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'LoggingSettingsServer') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'LoggingSettingsServer') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class LevelEnum(str, Enum):
        """
        Valid log levels: "error", "warn", "info", "verbose", "debug", or "silly".
        """
        ERROR = 'error'
        WARN = 'warn'
        INFO = 'info'
        VERBOSE = 'verbose'
        DEBUG = 'debug'
        SILLY = 'silly'


class Metrics():
    """
    Metrics.

    :attr str provider: Metrics provider to use. Can be either 'statsd',
          'prometheus', or 'disabled'.
    :attr MetricsStatsd statsd: (optional)
    """

    def __init__(self,
                 provider: str,
                 *,
                 statsd: 'MetricsStatsd' = None) -> None:
        """
        Initialize a Metrics object.

        :param str provider: Metrics provider to use. Can be either 'statsd',
               'prometheus', or 'disabled'.
        :param MetricsStatsd statsd: (optional)
        """
        self.provider = provider
        self.statsd = statsd

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Metrics':
        """Initialize a Metrics object from a json dictionary."""
        args = {}
        if 'provider' in _dict:
            args['provider'] = _dict.get('provider')
        else:
            raise ValueError('Required property \'provider\' not present in Metrics JSON')
        if 'statsd' in _dict:
            args['statsd'] = MetricsStatsd.from_dict(_dict.get('statsd'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Metrics object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'provider') and self.provider is not None:
            _dict['provider'] = self.provider
        if hasattr(self, 'statsd') and self.statsd is not None:
            _dict['statsd'] = self.statsd.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Metrics object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Metrics') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Metrics') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class ProviderEnum(str, Enum):
        """
        Metrics provider to use. Can be either 'statsd', 'prometheus', or 'disabled'.
        """
        STATSD = 'statsd'
        PROMETHEUS = 'prometheus'
        DISABLED = 'disabled'


class MetricsStatsd():
    """
    MetricsStatsd.

    :attr str network: Either UDP or TCP.
    :attr str address: The address of the statsd server. Include hostname/ip and
          port.
    :attr str write_interval: The frequency at which locally cached counters and
          gauges are pushed to statsd.
    :attr str prefix: The string that is prepended to all emitted statsd metrics.
    """

    def __init__(self,
                 network: str,
                 address: str,
                 write_interval: str,
                 prefix: str) -> None:
        """
        Initialize a MetricsStatsd object.

        :param str network: Either UDP or TCP.
        :param str address: The address of the statsd server. Include hostname/ip
               and port.
        :param str write_interval: The frequency at which locally cached counters
               and gauges are pushed to statsd.
        :param str prefix: The string that is prepended to all emitted statsd
               metrics.
        """
        self.network = network
        self.address = address
        self.write_interval = write_interval
        self.prefix = prefix

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MetricsStatsd':
        """Initialize a MetricsStatsd object from a json dictionary."""
        args = {}
        if 'network' in _dict:
            args['network'] = _dict.get('network')
        else:
            raise ValueError('Required property \'network\' not present in MetricsStatsd JSON')
        if 'address' in _dict:
            args['address'] = _dict.get('address')
        else:
            raise ValueError('Required property \'address\' not present in MetricsStatsd JSON')
        if 'writeInterval' in _dict:
            args['write_interval'] = _dict.get('writeInterval')
        else:
            raise ValueError('Required property \'writeInterval\' not present in MetricsStatsd JSON')
        if 'prefix' in _dict:
            args['prefix'] = _dict.get('prefix')
        else:
            raise ValueError('Required property \'prefix\' not present in MetricsStatsd JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MetricsStatsd object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'network') and self.network is not None:
            _dict['network'] = self.network
        if hasattr(self, 'address') and self.address is not None:
            _dict['address'] = self.address
        if hasattr(self, 'write_interval') and self.write_interval is not None:
            _dict['writeInterval'] = self.write_interval
        if hasattr(self, 'prefix') and self.prefix is not None:
            _dict['prefix'] = self.prefix
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this MetricsStatsd object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'MetricsStatsd') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MetricsStatsd') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class NetworkEnum(str, Enum):
        """
        Either UDP or TCP.
        """
        UDP = 'udp'
        TCP = 'tcp'


class MspCryptoCa():
    """
    MspCryptoCa.

    :attr List[str] root_certs: An array that contains one or more base 64 encoded
          PEM CA root certificates.
    :attr List[str] ca_intermediate_certs: (optional) An array that contains base 64
          encoded PEM intermediate CA certificates.
    """

    def __init__(self,
                 root_certs: List[str],
                 *,
                 ca_intermediate_certs: List[str] = None) -> None:
        """
        Initialize a MspCryptoCa object.

        :param List[str] root_certs: An array that contains one or more base 64
               encoded PEM CA root certificates.
        :param List[str] ca_intermediate_certs: (optional) An array that contains
               base 64 encoded PEM intermediate CA certificates.
        """
        self.root_certs = root_certs
        self.ca_intermediate_certs = ca_intermediate_certs

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MspCryptoCa':
        """Initialize a MspCryptoCa object from a json dictionary."""
        args = {}
        if 'root_certs' in _dict:
            args['root_certs'] = _dict.get('root_certs')
        else:
            raise ValueError('Required property \'root_certs\' not present in MspCryptoCa JSON')
        if 'ca_intermediate_certs' in _dict:
            args['ca_intermediate_certs'] = _dict.get('ca_intermediate_certs')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MspCryptoCa object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'root_certs') and self.root_certs is not None:
            _dict['root_certs'] = self.root_certs
        if hasattr(self, 'ca_intermediate_certs') and self.ca_intermediate_certs is not None:
            _dict['ca_intermediate_certs'] = self.ca_intermediate_certs
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this MspCryptoCa object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'MspCryptoCa') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MspCryptoCa') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class MspCryptoComp():
    """
    MspCryptoComp.

    :attr str ekey: An identity private key (base 64 encoded PEM) for this component
          (aka enrollment private key).
    :attr str ecert: An identity certificate (base 64 encoded PEM) for this
          component that was signed by the CA (aka enrollment certificate).
    :attr List[str] admin_certs: (optional) An array that contains base 64 encoded
          PEM identity certificates for administrators. Also known as signing certificates
          of an organization administrator.
    :attr str tls_key: A private key (base 64 encoded PEM) for this component's TLS.
    :attr str tls_cert: The TLS certificate as base 64 encoded PEM. Certificate is
          used to secure/validate a TLS connection with this component.
    :attr ClientAuth client_auth: (optional)
    """

    def __init__(self,
                 ekey: str,
                 ecert: str,
                 tls_key: str,
                 tls_cert: str,
                 *,
                 admin_certs: List[str] = None,
                 client_auth: 'ClientAuth' = None) -> None:
        """
        Initialize a MspCryptoComp object.

        :param str ekey: An identity private key (base 64 encoded PEM) for this
               component (aka enrollment private key).
        :param str ecert: An identity certificate (base 64 encoded PEM) for this
               component that was signed by the CA (aka enrollment certificate).
        :param str tls_key: A private key (base 64 encoded PEM) for this
               component's TLS.
        :param str tls_cert: The TLS certificate as base 64 encoded PEM.
               Certificate is used to secure/validate a TLS connection with this
               component.
        :param List[str] admin_certs: (optional) An array that contains base 64
               encoded PEM identity certificates for administrators. Also known as signing
               certificates of an organization administrator.
        :param ClientAuth client_auth: (optional)
        """
        self.ekey = ekey
        self.ecert = ecert
        self.admin_certs = admin_certs
        self.tls_key = tls_key
        self.tls_cert = tls_cert
        self.client_auth = client_auth

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MspCryptoComp':
        """Initialize a MspCryptoComp object from a json dictionary."""
        args = {}
        if 'ekey' in _dict:
            args['ekey'] = _dict.get('ekey')
        else:
            raise ValueError('Required property \'ekey\' not present in MspCryptoComp JSON')
        if 'ecert' in _dict:
            args['ecert'] = _dict.get('ecert')
        else:
            raise ValueError('Required property \'ecert\' not present in MspCryptoComp JSON')
        if 'admin_certs' in _dict:
            args['admin_certs'] = _dict.get('admin_certs')
        if 'tls_key' in _dict:
            args['tls_key'] = _dict.get('tls_key')
        else:
            raise ValueError('Required property \'tls_key\' not present in MspCryptoComp JSON')
        if 'tls_cert' in _dict:
            args['tls_cert'] = _dict.get('tls_cert')
        else:
            raise ValueError('Required property \'tls_cert\' not present in MspCryptoComp JSON')
        if 'client_auth' in _dict:
            args['client_auth'] = ClientAuth.from_dict(_dict.get('client_auth'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MspCryptoComp object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'ekey') and self.ekey is not None:
            _dict['ekey'] = self.ekey
        if hasattr(self, 'ecert') and self.ecert is not None:
            _dict['ecert'] = self.ecert
        if hasattr(self, 'admin_certs') and self.admin_certs is not None:
            _dict['admin_certs'] = self.admin_certs
        if hasattr(self, 'tls_key') and self.tls_key is not None:
            _dict['tls_key'] = self.tls_key
        if hasattr(self, 'tls_cert') and self.tls_cert is not None:
            _dict['tls_cert'] = self.tls_cert
        if hasattr(self, 'client_auth') and self.client_auth is not None:
            _dict['client_auth'] = self.client_auth.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this MspCryptoComp object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'MspCryptoComp') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MspCryptoComp') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class MspCryptoFieldCa():
    """
    MspCryptoFieldCa.

    :attr str name: (optional) The CA's "CAName" attribute. This name is used to
          distinguish this CA from the TLS CA.
    :attr List[str] root_certs: (optional) An array that contains one or more base
          64 encoded PEM CA root certificates.
    """

    def __init__(self,
                 *,
                 name: str = None,
                 root_certs: List[str] = None) -> None:
        """
        Initialize a MspCryptoFieldCa object.

        :param str name: (optional) The CA's "CAName" attribute. This name is used
               to distinguish this CA from the TLS CA.
        :param List[str] root_certs: (optional) An array that contains one or more
               base 64 encoded PEM CA root certificates.
        """
        self.name = name
        self.root_certs = root_certs

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MspCryptoFieldCa':
        """Initialize a MspCryptoFieldCa object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'root_certs' in _dict:
            args['root_certs'] = _dict.get('root_certs')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MspCryptoFieldCa object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'root_certs') and self.root_certs is not None:
            _dict['root_certs'] = self.root_certs
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this MspCryptoFieldCa object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'MspCryptoFieldCa') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MspCryptoFieldCa') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class MspCryptoFieldComponent():
    """
    MspCryptoFieldComponent.

    :attr str tls_cert: The TLS certificate as base 64 encoded PEM. Certificate is
          used to secure/validate a TLS connection with this component.
    :attr str ecert: (optional) An identity certificate (base 64 encoded PEM) for
          this component that was signed by the CA (aka enrollment certificate).
    :attr List[str] admin_certs: (optional) An array that contains base 64 encoded
          PEM identity certificates for administrators. Also known as signing certificates
          of an organization administrator.
    """

    def __init__(self,
                 tls_cert: str,
                 *,
                 ecert: str = None,
                 admin_certs: List[str] = None) -> None:
        """
        Initialize a MspCryptoFieldComponent object.

        :param str tls_cert: The TLS certificate as base 64 encoded PEM.
               Certificate is used to secure/validate a TLS connection with this
               component.
        :param str ecert: (optional) An identity certificate (base 64 encoded PEM)
               for this component that was signed by the CA (aka enrollment certificate).
        :param List[str] admin_certs: (optional) An array that contains base 64
               encoded PEM identity certificates for administrators. Also known as signing
               certificates of an organization administrator.
        """
        self.tls_cert = tls_cert
        self.ecert = ecert
        self.admin_certs = admin_certs

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MspCryptoFieldComponent':
        """Initialize a MspCryptoFieldComponent object from a json dictionary."""
        args = {}
        if 'tls_cert' in _dict:
            args['tls_cert'] = _dict.get('tls_cert')
        else:
            raise ValueError('Required property \'tls_cert\' not present in MspCryptoFieldComponent JSON')
        if 'ecert' in _dict:
            args['ecert'] = _dict.get('ecert')
        if 'admin_certs' in _dict:
            args['admin_certs'] = _dict.get('admin_certs')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MspCryptoFieldComponent object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'tls_cert') and self.tls_cert is not None:
            _dict['tls_cert'] = self.tls_cert
        if hasattr(self, 'ecert') and self.ecert is not None:
            _dict['ecert'] = self.ecert
        if hasattr(self, 'admin_certs') and self.admin_certs is not None:
            _dict['admin_certs'] = self.admin_certs
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this MspCryptoFieldComponent object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'MspCryptoFieldComponent') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MspCryptoFieldComponent') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class MspCryptoFieldTlsca():
    """
    MspCryptoFieldTlsca.

    :attr str name: (optional) The TLS CA's "CAName" attribute. This name is used to
          distinguish this TLS CA from the other CA.
    :attr List[str] root_certs: An array that contains one or more base 64 encoded
          PEM root certificates for the TLS CA.
    """

    def __init__(self,
                 root_certs: List[str],
                 *,
                 name: str = None) -> None:
        """
        Initialize a MspCryptoFieldTlsca object.

        :param List[str] root_certs: An array that contains one or more base 64
               encoded PEM root certificates for the TLS CA.
        :param str name: (optional) The TLS CA's "CAName" attribute. This name is
               used to distinguish this TLS CA from the other CA.
        """
        self.name = name
        self.root_certs = root_certs

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MspCryptoFieldTlsca':
        """Initialize a MspCryptoFieldTlsca object from a json dictionary."""
        args = {}
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'root_certs' in _dict:
            args['root_certs'] = _dict.get('root_certs')
        else:
            raise ValueError('Required property \'root_certs\' not present in MspCryptoFieldTlsca JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MspCryptoFieldTlsca object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'root_certs') and self.root_certs is not None:
            _dict['root_certs'] = self.root_certs
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this MspCryptoFieldTlsca object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'MspCryptoFieldTlsca') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MspCryptoFieldTlsca') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class MspPublicData():
    """
    MspPublicData.

    :attr str msp_id: (optional) The MSP id that is related to this component.
    :attr List[str] root_certs: (optional) An array that contains one or more base
          64 encoded PEM root certificates for the MSP.
    :attr List[str] admins: (optional) An array that contains base 64 encoded PEM
          identity certificates for administrators. Also known as signing certificates of
          an organization administrator.
    :attr List[str] tls_root_certs: (optional) An array that contains one or more
          base 64 encoded PEM TLS root certificates.
    """

    def __init__(self,
                 *,
                 msp_id: str = None,
                 root_certs: List[str] = None,
                 admins: List[str] = None,
                 tls_root_certs: List[str] = None) -> None:
        """
        Initialize a MspPublicData object.

        :param str msp_id: (optional) The MSP id that is related to this component.
        :param List[str] root_certs: (optional) An array that contains one or more
               base 64 encoded PEM root certificates for the MSP.
        :param List[str] admins: (optional) An array that contains base 64 encoded
               PEM identity certificates for administrators. Also known as signing
               certificates of an organization administrator.
        :param List[str] tls_root_certs: (optional) An array that contains one or
               more base 64 encoded PEM TLS root certificates.
        """
        self.msp_id = msp_id
        self.root_certs = root_certs
        self.admins = admins
        self.tls_root_certs = tls_root_certs

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MspPublicData':
        """Initialize a MspPublicData object from a json dictionary."""
        args = {}
        if 'msp_id' in _dict:
            args['msp_id'] = _dict.get('msp_id')
        if 'root_certs' in _dict:
            args['root_certs'] = _dict.get('root_certs')
        if 'admins' in _dict:
            args['admins'] = _dict.get('admins')
        if 'tls_root_certs' in _dict:
            args['tls_root_certs'] = _dict.get('tls_root_certs')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MspPublicData object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'msp_id') and self.msp_id is not None:
            _dict['msp_id'] = self.msp_id
        if hasattr(self, 'root_certs') and self.root_certs is not None:
            _dict['root_certs'] = self.root_certs
        if hasattr(self, 'admins') and self.admins is not None:
            _dict['admins'] = self.admins
        if hasattr(self, 'tls_root_certs') and self.tls_root_certs is not None:
            _dict['tls_root_certs'] = self.tls_root_certs
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this MspPublicData object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'MspPublicData') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MspPublicData') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class MspResponse():
    """
    Contains the details of an MSP (Membership Service Provider).

    :attr str id: (optional) The unique identifier of this component.
    :attr str type: (optional) The type of this component. Such as: "fabric-peer",
          "fabric-ca", "fabric-orderer", etc.
    :attr str display_name: (optional) A descriptive name for this MSP. The IBP
          console tile displays this name.
    :attr str msp_id: (optional) The MSP id that is related to this component.
    :attr float timestamp: (optional) UTC UNIX timestamp of component onboarding to
          the UI. In milliseconds.
    :attr List[str] tags: (optional)
    :attr List[str] root_certs: (optional) An array that contains one or more base
          64 encoded PEM root certificates for the MSP.
    :attr List[str] intermediate_certs: (optional) An array that contains base 64
          encoded PEM intermediate certificates.
    :attr List[str] admins: (optional) An array that contains base 64 encoded PEM
          identity certificates for administrators. Also known as signing certificates of
          an organization administrator.
    :attr str scheme_version: (optional) The versioning of the IBP console format of
          this JSON.
    :attr List[str] tls_root_certs: (optional) An array that contains one or more
          base 64 encoded PEM TLS root certificates.
    """

    def __init__(self,
                 *,
                 id: str = None,
                 type: str = None,
                 display_name: str = None,
                 msp_id: str = None,
                 timestamp: float = None,
                 tags: List[str] = None,
                 root_certs: List[str] = None,
                 intermediate_certs: List[str] = None,
                 admins: List[str] = None,
                 scheme_version: str = None,
                 tls_root_certs: List[str] = None) -> None:
        """
        Initialize a MspResponse object.

        :param str id: (optional) The unique identifier of this component.
        :param str type: (optional) The type of this component. Such as:
               "fabric-peer", "fabric-ca", "fabric-orderer", etc.
        :param str display_name: (optional) A descriptive name for this MSP. The
               IBP console tile displays this name.
        :param str msp_id: (optional) The MSP id that is related to this component.
        :param float timestamp: (optional) UTC UNIX timestamp of component
               onboarding to the UI. In milliseconds.
        :param List[str] tags: (optional)
        :param List[str] root_certs: (optional) An array that contains one or more
               base 64 encoded PEM root certificates for the MSP.
        :param List[str] intermediate_certs: (optional) An array that contains base
               64 encoded PEM intermediate certificates.
        :param List[str] admins: (optional) An array that contains base 64 encoded
               PEM identity certificates for administrators. Also known as signing
               certificates of an organization administrator.
        :param str scheme_version: (optional) The versioning of the IBP console
               format of this JSON.
        :param List[str] tls_root_certs: (optional) An array that contains one or
               more base 64 encoded PEM TLS root certificates.
        """
        self.id = id
        self.type = type
        self.display_name = display_name
        self.msp_id = msp_id
        self.timestamp = timestamp
        self.tags = tags
        self.root_certs = root_certs
        self.intermediate_certs = intermediate_certs
        self.admins = admins
        self.scheme_version = scheme_version
        self.tls_root_certs = tls_root_certs

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MspResponse':
        """Initialize a MspResponse object from a json dictionary."""
        args = {}
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'display_name' in _dict:
            args['display_name'] = _dict.get('display_name')
        if 'msp_id' in _dict:
            args['msp_id'] = _dict.get('msp_id')
        if 'timestamp' in _dict:
            args['timestamp'] = _dict.get('timestamp')
        if 'tags' in _dict:
            args['tags'] = _dict.get('tags')
        if 'root_certs' in _dict:
            args['root_certs'] = _dict.get('root_certs')
        if 'intermediate_certs' in _dict:
            args['intermediate_certs'] = _dict.get('intermediate_certs')
        if 'admins' in _dict:
            args['admins'] = _dict.get('admins')
        if 'scheme_version' in _dict:
            args['scheme_version'] = _dict.get('scheme_version')
        if 'tls_root_certs' in _dict:
            args['tls_root_certs'] = _dict.get('tls_root_certs')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MspResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'display_name') and self.display_name is not None:
            _dict['display_name'] = self.display_name
        if hasattr(self, 'msp_id') and self.msp_id is not None:
            _dict['msp_id'] = self.msp_id
        if hasattr(self, 'timestamp') and self.timestamp is not None:
            _dict['timestamp'] = self.timestamp
        if hasattr(self, 'tags') and self.tags is not None:
            _dict['tags'] = self.tags
        if hasattr(self, 'root_certs') and self.root_certs is not None:
            _dict['root_certs'] = self.root_certs
        if hasattr(self, 'intermediate_certs') and self.intermediate_certs is not None:
            _dict['intermediate_certs'] = self.intermediate_certs
        if hasattr(self, 'admins') and self.admins is not None:
            _dict['admins'] = self.admins
        if hasattr(self, 'scheme_version') and self.scheme_version is not None:
            _dict['scheme_version'] = self.scheme_version
        if hasattr(self, 'tls_root_certs') and self.tls_root_certs is not None:
            _dict['tls_root_certs'] = self.tls_root_certs
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this MspResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'MspResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MspResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class NotificationData():
    """
    NotificationData.

    :attr str id: (optional) Unique id for the notification.
    :attr str type: (optional) Values can be "notification", "webhook_tx" or
          "other".
    :attr str status: (optional) Values can be "pending", "error", or "success".
    :attr str by: (optional) The end user who initiated the action for the
          notification.
    :attr str message: (optional) Text describing the outcome of the transaction.
    :attr float ts_display: (optional) UTC UNIX timestamp of the notification's
          creation. In milliseconds.
    """

    def __init__(self,
                 *,
                 id: str = None,
                 type: str = None,
                 status: str = None,
                 by: str = None,
                 message: str = None,
                 ts_display: float = None) -> None:
        """
        Initialize a NotificationData object.

        :param str id: (optional) Unique id for the notification.
        :param str type: (optional) Values can be "notification", "webhook_tx" or
               "other".
        :param str status: (optional) Values can be "pending", "error", or
               "success".
        :param str by: (optional) The end user who initiated the action for the
               notification.
        :param str message: (optional) Text describing the outcome of the
               transaction.
        :param float ts_display: (optional) UTC UNIX timestamp of the
               notification's creation. In milliseconds.
        """
        self.id = id
        self.type = type
        self.status = status
        self.by = by
        self.message = message
        self.ts_display = ts_display

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'NotificationData':
        """Initialize a NotificationData object from a json dictionary."""
        args = {}
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'status' in _dict:
            args['status'] = _dict.get('status')
        if 'by' in _dict:
            args['by'] = _dict.get('by')
        if 'message' in _dict:
            args['message'] = _dict.get('message')
        if 'ts_display' in _dict:
            args['ts_display'] = _dict.get('ts_display')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a NotificationData object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'status') and self.status is not None:
            _dict['status'] = self.status
        if hasattr(self, 'by') and self.by is not None:
            _dict['by'] = self.by
        if hasattr(self, 'message') and self.message is not None:
            _dict['message'] = self.message
        if hasattr(self, 'ts_display') and self.ts_display is not None:
            _dict['ts_display'] = self.ts_display
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this NotificationData object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'NotificationData') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'NotificationData') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class OrdererResponse():
    """
    Contains the details of an ordering node.

    :attr str id: (optional) The unique identifier of this component.
    :attr str dep_component_id: (optional) The unique id for the component in
          Kubernetes. Not available if component was imported.
    :attr str api_url: (optional) The gRPC URL for the orderer. Typically, client
          applications would send requests to this URL. Include the protocol, hostname/ip
          and port.
    :attr str display_name: (optional) A descriptive base name for each ordering
          node. One or more child IBP console tiles display this name.
    :attr str grpcwp_url: (optional) The gRPC web proxy URL in front of the orderer.
          Include the protocol, hostname/ip and port.
    :attr str location: (optional) Indicates where the component is running.
    :attr str operations_url: (optional) Used by Fabric health checker to monitor
          the health status of this orderer node. For more information, see [Fabric
          documentation](https://hyperledger-fabric.readthedocs.io/en/release-1.4/operations_service.html).
          Include the protocol, hostname/ip and port.
    :attr str orderer_type: (optional) The type of Fabric orderer. Currently, only
          the type `"raft"` is supported.
          [etcd/raft](/docs/blockchain?topic=blockchain-ibp-console-build-network#ibp-console-build-network-ordering-console).
    :attr object config_override: (optional) The **cached** configuration override
          that was set for the Kubernetes deployment. Field does not exist if an override
          was not set of if the component was imported.
    :attr bool consenter_proposal_fin: (optional) The state of a pre-created orderer
          node. A value of `true` means that the orderer node was added as a system
          channel consenter. This is a manual field. Set it yourself after finishing the
          raft append flow to indicate that this node is ready for use. See the [Submit
          config block to orderer](#submit-block) API description for more details about
          appending raft nodes.
    :attr NodeOu node_ou: (optional)
    :attr MspCryptoField msp: (optional) The msp crypto data.
    :attr str msp_id: (optional) The MSP id that is related to this component.
    :attr OrdererResponseResources resources: (optional) The **cached** Kubernetes
          resource attributes for this component. Not available if orderer was imported.
    :attr str scheme_version: (optional) The versioning of the IBP console format of
          this JSON.
    :attr OrdererResponseStorage storage: (optional) The **cached** Kubernetes
          storage attributes for this component. Not available if orderer was imported.
    :attr str system_channel_id: (optional) The name of the system channel. Defaults
          to `testchainid`.
    :attr List[str] tags: (optional)
    :attr float timestamp: (optional) UTC UNIX timestamp of component onboarding to
          the UI. In milliseconds.
    :attr str type: (optional) The type of this component. Such as: "fabric-peer",
          "fabric-ca", "fabric-orderer", etc.
    :attr str version: (optional) The cached Hyperledger Fabric release version.
    :attr str zone: (optional) Specify the Kubernetes zone for the deployment. The
          deployment will use a k8s node in this zone. Find the list of possible zones by
          retrieving your Kubernetes node labels: `kubectl get nodes --show-labels`. [More
          information](https://kubernetes.io/docs/setup/best-practices/multiple-zones).
    """

    def __init__(self,
                 *,
                 id: str = None,
                 dep_component_id: str = None,
                 api_url: str = None,
                 display_name: str = None,
                 grpcwp_url: str = None,
                 location: str = None,
                 operations_url: str = None,
                 orderer_type: str = None,
                 config_override: object = None,
                 consenter_proposal_fin: bool = None,
                 node_ou: 'NodeOu' = None,
                 msp: 'MspCryptoField' = None,
                 msp_id: str = None,
                 resources: 'OrdererResponseResources' = None,
                 scheme_version: str = None,
                 storage: 'OrdererResponseStorage' = None,
                 system_channel_id: str = None,
                 tags: List[str] = None,
                 timestamp: float = None,
                 type: str = None,
                 version: str = None,
                 zone: str = None) -> None:
        """
        Initialize a OrdererResponse object.

        :param str id: (optional) The unique identifier of this component.
        :param str dep_component_id: (optional) The unique id for the component in
               Kubernetes. Not available if component was imported.
        :param str api_url: (optional) The gRPC URL for the orderer. Typically,
               client applications would send requests to this URL. Include the protocol,
               hostname/ip and port.
        :param str display_name: (optional) A descriptive base name for each
               ordering node. One or more child IBP console tiles display this name.
        :param str grpcwp_url: (optional) The gRPC web proxy URL in front of the
               orderer. Include the protocol, hostname/ip and port.
        :param str location: (optional) Indicates where the component is running.
        :param str operations_url: (optional) Used by Fabric health checker to
               monitor the health status of this orderer node. For more information, see
               [Fabric
               documentation](https://hyperledger-fabric.readthedocs.io/en/release-1.4/operations_service.html).
               Include the protocol, hostname/ip and port.
        :param str orderer_type: (optional) The type of Fabric orderer. Currently,
               only the type `"raft"` is supported.
               [etcd/raft](/docs/blockchain?topic=blockchain-ibp-console-build-network#ibp-console-build-network-ordering-console).
        :param object config_override: (optional) The **cached** configuration
               override that was set for the Kubernetes deployment. Field does not exist
               if an override was not set of if the component was imported.
        :param bool consenter_proposal_fin: (optional) The state of a pre-created
               orderer node. A value of `true` means that the orderer node was added as a
               system channel consenter. This is a manual field. Set it yourself after
               finishing the raft append flow to indicate that this node is ready for use.
               See the [Submit config block to orderer](#submit-block) API description for
               more details about appending raft nodes.
        :param NodeOu node_ou: (optional)
        :param MspCryptoField msp: (optional) The msp crypto data.
        :param str msp_id: (optional) The MSP id that is related to this component.
        :param OrdererResponseResources resources: (optional) The **cached**
               Kubernetes resource attributes for this component. Not available if orderer
               was imported.
        :param str scheme_version: (optional) The versioning of the IBP console
               format of this JSON.
        :param OrdererResponseStorage storage: (optional) The **cached** Kubernetes
               storage attributes for this component. Not available if orderer was
               imported.
        :param str system_channel_id: (optional) The name of the system channel.
               Defaults to `testchainid`.
        :param List[str] tags: (optional)
        :param float timestamp: (optional) UTC UNIX timestamp of component
               onboarding to the UI. In milliseconds.
        :param str type: (optional) The type of this component. Such as:
               "fabric-peer", "fabric-ca", "fabric-orderer", etc.
        :param str version: (optional) The cached Hyperledger Fabric release
               version.
        :param str zone: (optional) Specify the Kubernetes zone for the deployment.
               The deployment will use a k8s node in this zone. Find the list of possible
               zones by retrieving your Kubernetes node labels: `kubectl get nodes
               --show-labels`. [More
               information](https://kubernetes.io/docs/setup/best-practices/multiple-zones).
        """
        self.id = id
        self.dep_component_id = dep_component_id
        self.api_url = api_url
        self.display_name = display_name
        self.grpcwp_url = grpcwp_url
        self.location = location
        self.operations_url = operations_url
        self.orderer_type = orderer_type
        self.config_override = config_override
        self.consenter_proposal_fin = consenter_proposal_fin
        self.node_ou = node_ou
        self.msp = msp
        self.msp_id = msp_id
        self.resources = resources
        self.scheme_version = scheme_version
        self.storage = storage
        self.system_channel_id = system_channel_id
        self.tags = tags
        self.timestamp = timestamp
        self.type = type
        self.version = version
        self.zone = zone

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'OrdererResponse':
        """Initialize a OrdererResponse object from a json dictionary."""
        args = {}
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'dep_component_id' in _dict:
            args['dep_component_id'] = _dict.get('dep_component_id')
        if 'api_url' in _dict:
            args['api_url'] = _dict.get('api_url')
        if 'display_name' in _dict:
            args['display_name'] = _dict.get('display_name')
        if 'grpcwp_url' in _dict:
            args['grpcwp_url'] = _dict.get('grpcwp_url')
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'operations_url' in _dict:
            args['operations_url'] = _dict.get('operations_url')
        if 'orderer_type' in _dict:
            args['orderer_type'] = _dict.get('orderer_type')
        if 'config_override' in _dict:
            args['config_override'] = _dict.get('config_override')
        if 'consenter_proposal_fin' in _dict:
            args['consenter_proposal_fin'] = _dict.get('consenter_proposal_fin')
        if 'node_ou' in _dict:
            args['node_ou'] = NodeOu.from_dict(_dict.get('node_ou'))
        if 'msp' in _dict:
            args['msp'] = MspCryptoField.from_dict(_dict.get('msp'))
        if 'msp_id' in _dict:
            args['msp_id'] = _dict.get('msp_id')
        if 'resources' in _dict:
            args['resources'] = OrdererResponseResources.from_dict(_dict.get('resources'))
        if 'scheme_version' in _dict:
            args['scheme_version'] = _dict.get('scheme_version')
        if 'storage' in _dict:
            args['storage'] = OrdererResponseStorage.from_dict(_dict.get('storage'))
        if 'system_channel_id' in _dict:
            args['system_channel_id'] = _dict.get('system_channel_id')
        if 'tags' in _dict:
            args['tags'] = _dict.get('tags')
        if 'timestamp' in _dict:
            args['timestamp'] = _dict.get('timestamp')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'version' in _dict:
            args['version'] = _dict.get('version')
        if 'zone' in _dict:
            args['zone'] = _dict.get('zone')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a OrdererResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'dep_component_id') and self.dep_component_id is not None:
            _dict['dep_component_id'] = self.dep_component_id
        if hasattr(self, 'api_url') and self.api_url is not None:
            _dict['api_url'] = self.api_url
        if hasattr(self, 'display_name') and self.display_name is not None:
            _dict['display_name'] = self.display_name
        if hasattr(self, 'grpcwp_url') and self.grpcwp_url is not None:
            _dict['grpcwp_url'] = self.grpcwp_url
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'operations_url') and self.operations_url is not None:
            _dict['operations_url'] = self.operations_url
        if hasattr(self, 'orderer_type') and self.orderer_type is not None:
            _dict['orderer_type'] = self.orderer_type
        if hasattr(self, 'config_override') and self.config_override is not None:
            _dict['config_override'] = self.config_override
        if hasattr(self, 'consenter_proposal_fin') and self.consenter_proposal_fin is not None:
            _dict['consenter_proposal_fin'] = self.consenter_proposal_fin
        if hasattr(self, 'node_ou') and self.node_ou is not None:
            _dict['node_ou'] = self.node_ou.to_dict()
        if hasattr(self, 'msp') and self.msp is not None:
            _dict['msp'] = self.msp.to_dict()
        if hasattr(self, 'msp_id') and self.msp_id is not None:
            _dict['msp_id'] = self.msp_id
        if hasattr(self, 'resources') and self.resources is not None:
            _dict['resources'] = self.resources.to_dict()
        if hasattr(self, 'scheme_version') and self.scheme_version is not None:
            _dict['scheme_version'] = self.scheme_version
        if hasattr(self, 'storage') and self.storage is not None:
            _dict['storage'] = self.storage.to_dict()
        if hasattr(self, 'system_channel_id') and self.system_channel_id is not None:
            _dict['system_channel_id'] = self.system_channel_id
        if hasattr(self, 'tags') and self.tags is not None:
            _dict['tags'] = self.tags
        if hasattr(self, 'timestamp') and self.timestamp is not None:
            _dict['timestamp'] = self.timestamp
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'version') and self.version is not None:
            _dict['version'] = self.version
        if hasattr(self, 'zone') and self.zone is not None:
            _dict['zone'] = self.zone
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this OrdererResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'OrdererResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'OrdererResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class OrdererTypeEnum(str, Enum):
        """
        The type of Fabric orderer. Currently, only the type `"raft"` is supported.
        [etcd/raft](/docs/blockchain?topic=blockchain-ibp-console-build-network#ibp-console-build-network-ordering-console).
        """
        RAFT = 'raft'


class OrdererResponseResources():
    """
    The **cached** Kubernetes resource attributes for this component. Not available if
    orderer was imported.

    :attr GenericResources orderer: (optional)
    :attr GenericResources proxy: (optional)
    """

    def __init__(self,
                 *,
                 orderer: 'GenericResources' = None,
                 proxy: 'GenericResources' = None) -> None:
        """
        Initialize a OrdererResponseResources object.

        :param GenericResources orderer: (optional)
        :param GenericResources proxy: (optional)
        """
        self.orderer = orderer
        self.proxy = proxy

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'OrdererResponseResources':
        """Initialize a OrdererResponseResources object from a json dictionary."""
        args = {}
        if 'orderer' in _dict:
            args['orderer'] = GenericResources.from_dict(_dict.get('orderer'))
        if 'proxy' in _dict:
            args['proxy'] = GenericResources.from_dict(_dict.get('proxy'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a OrdererResponseResources object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'orderer') and self.orderer is not None:
            _dict['orderer'] = self.orderer.to_dict()
        if hasattr(self, 'proxy') and self.proxy is not None:
            _dict['proxy'] = self.proxy.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this OrdererResponseResources object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'OrdererResponseResources') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'OrdererResponseResources') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class OrdererResponseStorage():
    """
    The **cached** Kubernetes storage attributes for this component. Not available if
    orderer was imported.

    :attr StorageObject orderer: (optional)
    """

    def __init__(self,
                 *,
                 orderer: 'StorageObject' = None) -> None:
        """
        Initialize a OrdererResponseStorage object.

        :param StorageObject orderer: (optional)
        """
        self.orderer = orderer

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'OrdererResponseStorage':
        """Initialize a OrdererResponseStorage object from a json dictionary."""
        args = {}
        if 'orderer' in _dict:
            args['orderer'] = StorageObject.from_dict(_dict.get('orderer'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a OrdererResponseStorage object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'orderer') and self.orderer is not None:
            _dict['orderer'] = self.orderer.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this OrdererResponseStorage object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'OrdererResponseStorage') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'OrdererResponseStorage') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class PeerResources():
    """
    CPU and memory properties. This feature is not available if using a free Kubernetes
    cluster.

    :attr ResourceObjectFabV2 chaincodelauncher: (optional) This field requires the
          use of Fabric v2.1.* and higher.
    :attr ResourceObjectCouchDb couchdb: (optional) *Legacy field name* Use the
          field `statedb` instead. This field requires the use of Fabric v1.4.* and
          higher.
    :attr ResourceObject statedb: (optional) This field requires the use of Fabric
          v1.4.* and higher.
    :attr ResourceObjectFabV1 dind: (optional) This field requires the use of Fabric
          v1.4.* and **lower**.
    :attr ResourceObjectFabV1 fluentd: (optional) This field requires the use of
          Fabric v1.4.* and **lower**.
    :attr ResourceObject peer: (optional) This field requires the use of Fabric
          v1.4.* and higher.
    :attr ResourceObject proxy: (optional) This field requires the use of Fabric
          v1.4.* and higher.
    """

    def __init__(self,
                 *,
                 chaincodelauncher: 'ResourceObjectFabV2' = None,
                 couchdb: 'ResourceObjectCouchDb' = None,
                 statedb: 'ResourceObject' = None,
                 dind: 'ResourceObjectFabV1' = None,
                 fluentd: 'ResourceObjectFabV1' = None,
                 peer: 'ResourceObject' = None,
                 proxy: 'ResourceObject' = None) -> None:
        """
        Initialize a PeerResources object.

        :param ResourceObjectFabV2 chaincodelauncher: (optional) This field
               requires the use of Fabric v2.1.* and higher.
        :param ResourceObjectCouchDb couchdb: (optional) *Legacy field name* Use
               the field `statedb` instead. This field requires the use of Fabric v1.4.*
               and higher.
        :param ResourceObject statedb: (optional) This field requires the use of
               Fabric v1.4.* and higher.
        :param ResourceObjectFabV1 dind: (optional) This field requires the use of
               Fabric v1.4.* and **lower**.
        :param ResourceObjectFabV1 fluentd: (optional) This field requires the use
               of Fabric v1.4.* and **lower**.
        :param ResourceObject peer: (optional) This field requires the use of
               Fabric v1.4.* and higher.
        :param ResourceObject proxy: (optional) This field requires the use of
               Fabric v1.4.* and higher.
        """
        self.chaincodelauncher = chaincodelauncher
        self.couchdb = couchdb
        self.statedb = statedb
        self.dind = dind
        self.fluentd = fluentd
        self.peer = peer
        self.proxy = proxy

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'PeerResources':
        """Initialize a PeerResources object from a json dictionary."""
        args = {}
        if 'chaincodelauncher' in _dict:
            args['chaincodelauncher'] = ResourceObjectFabV2.from_dict(_dict.get('chaincodelauncher'))
        if 'couchdb' in _dict:
            args['couchdb'] = ResourceObjectCouchDb.from_dict(_dict.get('couchdb'))
        if 'statedb' in _dict:
            args['statedb'] = ResourceObject.from_dict(_dict.get('statedb'))
        if 'dind' in _dict:
            args['dind'] = ResourceObjectFabV1.from_dict(_dict.get('dind'))
        if 'fluentd' in _dict:
            args['fluentd'] = ResourceObjectFabV1.from_dict(_dict.get('fluentd'))
        if 'peer' in _dict:
            args['peer'] = ResourceObject.from_dict(_dict.get('peer'))
        if 'proxy' in _dict:
            args['proxy'] = ResourceObject.from_dict(_dict.get('proxy'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a PeerResources object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'chaincodelauncher') and self.chaincodelauncher is not None:
            _dict['chaincodelauncher'] = self.chaincodelauncher.to_dict()
        if hasattr(self, 'couchdb') and self.couchdb is not None:
            _dict['couchdb'] = self.couchdb.to_dict()
        if hasattr(self, 'statedb') and self.statedb is not None:
            _dict['statedb'] = self.statedb.to_dict()
        if hasattr(self, 'dind') and self.dind is not None:
            _dict['dind'] = self.dind.to_dict()
        if hasattr(self, 'fluentd') and self.fluentd is not None:
            _dict['fluentd'] = self.fluentd.to_dict()
        if hasattr(self, 'peer') and self.peer is not None:
            _dict['peer'] = self.peer.to_dict()
        if hasattr(self, 'proxy') and self.proxy is not None:
            _dict['proxy'] = self.proxy.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this PeerResources object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'PeerResources') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'PeerResources') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class PeerResponse():
    """
    Contains the details of a peer.

    :attr str id: (optional) The unique identifier of this component.
    :attr str dep_component_id: (optional) The unique id for the component in
          Kubernetes. Not available if component was imported.
    :attr str api_url: (optional) The gRPC URL for the peer. Typically, client
          applications would send requests to this URL. Include the protocol, hostname/ip
          and port.
    :attr str display_name: (optional) A descriptive name for this peer. The IBP
          console tile displays this name.
    :attr str grpcwp_url: (optional) The gRPC web proxy URL in front of the peer.
          Include the protocol, hostname/ip and port.
    :attr str location: (optional) Indicates where the component is running.
    :attr str operations_url: (optional) Used by Fabric health checker to monitor
          the health status of this peer. For more information, see [Fabric
          documentation](https://hyperledger-fabric.readthedocs.io/en/release-1.4/operations_service.html).
          Include the protocol, hostname/ip and port.
    :attr object config_override: (optional) The **cached** configuration override
          that was set for the Kubernetes deployment. Field does not exist if an override
          was not set of if the component was imported.
    :attr NodeOu node_ou: (optional)
    :attr MspCryptoField msp: (optional) The msp crypto data.
    :attr str msp_id: (optional) The MSP id that is related to this component.
    :attr PeerResponseResources resources: (optional) The **cached** Kubernetes
          resource attributes for this component. Not available if peer was imported.
    :attr str scheme_version: (optional) The versioning of the IBP console format of
          this JSON.
    :attr str state_db: (optional) Select the state database for the peer. Can be
          either "couchdb" or "leveldb". The default is "couchdb".
    :attr PeerResponseStorage storage: (optional) The **cached** Kubernetes storage
          attributes for this component. Not available if peer was imported.
    :attr List[str] tags: (optional)
    :attr float timestamp: (optional) UTC UNIX timestamp of component onboarding to
          the UI. In milliseconds.
    :attr str type: (optional) The type of this component. Such as: "fabric-peer",
          "fabric-ca", "fabric-orderer", etc.
    :attr str version: (optional) The cached Hyperledger Fabric release version.
    :attr str zone: (optional) Specify the Kubernetes zone for the deployment. The
          deployment will use a k8s node in this zone. Find the list of possible zones by
          retrieving your Kubernetes node labels: `kubectl get nodes --show-labels`. [More
          information](https://kubernetes.io/docs/setup/best-practices/multiple-zones).
    """

    def __init__(self,
                 *,
                 id: str = None,
                 dep_component_id: str = None,
                 api_url: str = None,
                 display_name: str = None,
                 grpcwp_url: str = None,
                 location: str = None,
                 operations_url: str = None,
                 config_override: object = None,
                 node_ou: 'NodeOu' = None,
                 msp: 'MspCryptoField' = None,
                 msp_id: str = None,
                 resources: 'PeerResponseResources' = None,
                 scheme_version: str = None,
                 state_db: str = None,
                 storage: 'PeerResponseStorage' = None,
                 tags: List[str] = None,
                 timestamp: float = None,
                 type: str = None,
                 version: str = None,
                 zone: str = None) -> None:
        """
        Initialize a PeerResponse object.

        :param str id: (optional) The unique identifier of this component.
        :param str dep_component_id: (optional) The unique id for the component in
               Kubernetes. Not available if component was imported.
        :param str api_url: (optional) The gRPC URL for the peer. Typically, client
               applications would send requests to this URL. Include the protocol,
               hostname/ip and port.
        :param str display_name: (optional) A descriptive name for this peer. The
               IBP console tile displays this name.
        :param str grpcwp_url: (optional) The gRPC web proxy URL in front of the
               peer. Include the protocol, hostname/ip and port.
        :param str location: (optional) Indicates where the component is running.
        :param str operations_url: (optional) Used by Fabric health checker to
               monitor the health status of this peer. For more information, see [Fabric
               documentation](https://hyperledger-fabric.readthedocs.io/en/release-1.4/operations_service.html).
               Include the protocol, hostname/ip and port.
        :param object config_override: (optional) The **cached** configuration
               override that was set for the Kubernetes deployment. Field does not exist
               if an override was not set of if the component was imported.
        :param NodeOu node_ou: (optional)
        :param MspCryptoField msp: (optional) The msp crypto data.
        :param str msp_id: (optional) The MSP id that is related to this component.
        :param PeerResponseResources resources: (optional) The **cached**
               Kubernetes resource attributes for this component. Not available if peer
               was imported.
        :param str scheme_version: (optional) The versioning of the IBP console
               format of this JSON.
        :param str state_db: (optional) Select the state database for the peer. Can
               be either "couchdb" or "leveldb". The default is "couchdb".
        :param PeerResponseStorage storage: (optional) The **cached** Kubernetes
               storage attributes for this component. Not available if peer was imported.
        :param List[str] tags: (optional)
        :param float timestamp: (optional) UTC UNIX timestamp of component
               onboarding to the UI. In milliseconds.
        :param str type: (optional) The type of this component. Such as:
               "fabric-peer", "fabric-ca", "fabric-orderer", etc.
        :param str version: (optional) The cached Hyperledger Fabric release
               version.
        :param str zone: (optional) Specify the Kubernetes zone for the deployment.
               The deployment will use a k8s node in this zone. Find the list of possible
               zones by retrieving your Kubernetes node labels: `kubectl get nodes
               --show-labels`. [More
               information](https://kubernetes.io/docs/setup/best-practices/multiple-zones).
        """
        self.id = id
        self.dep_component_id = dep_component_id
        self.api_url = api_url
        self.display_name = display_name
        self.grpcwp_url = grpcwp_url
        self.location = location
        self.operations_url = operations_url
        self.config_override = config_override
        self.node_ou = node_ou
        self.msp = msp
        self.msp_id = msp_id
        self.resources = resources
        self.scheme_version = scheme_version
        self.state_db = state_db
        self.storage = storage
        self.tags = tags
        self.timestamp = timestamp
        self.type = type
        self.version = version
        self.zone = zone

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'PeerResponse':
        """Initialize a PeerResponse object from a json dictionary."""
        args = {}
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        if 'dep_component_id' in _dict:
            args['dep_component_id'] = _dict.get('dep_component_id')
        if 'api_url' in _dict:
            args['api_url'] = _dict.get('api_url')
        if 'display_name' in _dict:
            args['display_name'] = _dict.get('display_name')
        if 'grpcwp_url' in _dict:
            args['grpcwp_url'] = _dict.get('grpcwp_url')
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        if 'operations_url' in _dict:
            args['operations_url'] = _dict.get('operations_url')
        if 'config_override' in _dict:
            args['config_override'] = _dict.get('config_override')
        if 'node_ou' in _dict:
            args['node_ou'] = NodeOu.from_dict(_dict.get('node_ou'))
        if 'msp' in _dict:
            args['msp'] = MspCryptoField.from_dict(_dict.get('msp'))
        if 'msp_id' in _dict:
            args['msp_id'] = _dict.get('msp_id')
        if 'resources' in _dict:
            args['resources'] = PeerResponseResources.from_dict(_dict.get('resources'))
        if 'scheme_version' in _dict:
            args['scheme_version'] = _dict.get('scheme_version')
        if 'state_db' in _dict:
            args['state_db'] = _dict.get('state_db')
        if 'storage' in _dict:
            args['storage'] = PeerResponseStorage.from_dict(_dict.get('storage'))
        if 'tags' in _dict:
            args['tags'] = _dict.get('tags')
        if 'timestamp' in _dict:
            args['timestamp'] = _dict.get('timestamp')
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'version' in _dict:
            args['version'] = _dict.get('version')
        if 'zone' in _dict:
            args['zone'] = _dict.get('zone')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a PeerResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self, 'dep_component_id') and self.dep_component_id is not None:
            _dict['dep_component_id'] = self.dep_component_id
        if hasattr(self, 'api_url') and self.api_url is not None:
            _dict['api_url'] = self.api_url
        if hasattr(self, 'display_name') and self.display_name is not None:
            _dict['display_name'] = self.display_name
        if hasattr(self, 'grpcwp_url') and self.grpcwp_url is not None:
            _dict['grpcwp_url'] = self.grpcwp_url
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'operations_url') and self.operations_url is not None:
            _dict['operations_url'] = self.operations_url
        if hasattr(self, 'config_override') and self.config_override is not None:
            _dict['config_override'] = self.config_override
        if hasattr(self, 'node_ou') and self.node_ou is not None:
            _dict['node_ou'] = self.node_ou.to_dict()
        if hasattr(self, 'msp') and self.msp is not None:
            _dict['msp'] = self.msp.to_dict()
        if hasattr(self, 'msp_id') and self.msp_id is not None:
            _dict['msp_id'] = self.msp_id
        if hasattr(self, 'resources') and self.resources is not None:
            _dict['resources'] = self.resources.to_dict()
        if hasattr(self, 'scheme_version') and self.scheme_version is not None:
            _dict['scheme_version'] = self.scheme_version
        if hasattr(self, 'state_db') and self.state_db is not None:
            _dict['state_db'] = self.state_db
        if hasattr(self, 'storage') and self.storage is not None:
            _dict['storage'] = self.storage.to_dict()
        if hasattr(self, 'tags') and self.tags is not None:
            _dict['tags'] = self.tags
        if hasattr(self, 'timestamp') and self.timestamp is not None:
            _dict['timestamp'] = self.timestamp
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'version') and self.version is not None:
            _dict['version'] = self.version
        if hasattr(self, 'zone') and self.zone is not None:
            _dict['zone'] = self.zone
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this PeerResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'PeerResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'PeerResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class StateDbEnum(str, Enum):
        """
        Select the state database for the peer. Can be either "couchdb" or "leveldb". The
        default is "couchdb".
        """
        COUCHDB = 'couchdb'
        LEVELDB = 'leveldb'


class PeerResponseResources():
    """
    The **cached** Kubernetes resource attributes for this component. Not available if
    peer was imported.

    :attr GenericResources peer: (optional)
    :attr GenericResources proxy: (optional)
    :attr GenericResources statedb: (optional)
    """

    def __init__(self,
                 *,
                 peer: 'GenericResources' = None,
                 proxy: 'GenericResources' = None,
                 statedb: 'GenericResources' = None) -> None:
        """
        Initialize a PeerResponseResources object.

        :param GenericResources peer: (optional)
        :param GenericResources proxy: (optional)
        :param GenericResources statedb: (optional)
        """
        self.peer = peer
        self.proxy = proxy
        self.statedb = statedb

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'PeerResponseResources':
        """Initialize a PeerResponseResources object from a json dictionary."""
        args = {}
        if 'peer' in _dict:
            args['peer'] = GenericResources.from_dict(_dict.get('peer'))
        if 'proxy' in _dict:
            args['proxy'] = GenericResources.from_dict(_dict.get('proxy'))
        if 'statedb' in _dict:
            args['statedb'] = GenericResources.from_dict(_dict.get('statedb'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a PeerResponseResources object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'peer') and self.peer is not None:
            _dict['peer'] = self.peer.to_dict()
        if hasattr(self, 'proxy') and self.proxy is not None:
            _dict['proxy'] = self.proxy.to_dict()
        if hasattr(self, 'statedb') and self.statedb is not None:
            _dict['statedb'] = self.statedb.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this PeerResponseResources object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'PeerResponseResources') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'PeerResponseResources') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class PeerResponseStorage():
    """
    The **cached** Kubernetes storage attributes for this component. Not available if peer
    was imported.

    :attr StorageObject peer: (optional)
    :attr StorageObject statedb: (optional)
    """

    def __init__(self,
                 *,
                 peer: 'StorageObject' = None,
                 statedb: 'StorageObject' = None) -> None:
        """
        Initialize a PeerResponseStorage object.

        :param StorageObject peer: (optional)
        :param StorageObject statedb: (optional)
        """
        self.peer = peer
        self.statedb = statedb

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'PeerResponseStorage':
        """Initialize a PeerResponseStorage object from a json dictionary."""
        args = {}
        if 'peer' in _dict:
            args['peer'] = StorageObject.from_dict(_dict.get('peer'))
        if 'statedb' in _dict:
            args['statedb'] = StorageObject.from_dict(_dict.get('statedb'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a PeerResponseStorage object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'peer') and self.peer is not None:
            _dict['peer'] = self.peer.to_dict()
        if hasattr(self, 'statedb') and self.statedb is not None:
            _dict['statedb'] = self.statedb.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this PeerResponseStorage object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'PeerResponseStorage') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'PeerResponseStorage') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class RemoveMultiComponentsResponse():
    """
    RemoveMultiComponentsResponse.

    :attr List[DeleteComponentResponse] removed: (optional)
    """

    def __init__(self,
                 *,
                 removed: List['DeleteComponentResponse'] = None) -> None:
        """
        Initialize a RemoveMultiComponentsResponse object.

        :param List[DeleteComponentResponse] removed: (optional)
        """
        self.removed = removed

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'RemoveMultiComponentsResponse':
        """Initialize a RemoveMultiComponentsResponse object from a json dictionary."""
        args = {}
        if 'removed' in _dict:
            args['removed'] = [DeleteComponentResponse.from_dict(x) for x in _dict.get('removed')]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a RemoveMultiComponentsResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'removed') and self.removed is not None:
            _dict['removed'] = [x.to_dict() for x in self.removed]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this RemoveMultiComponentsResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'RemoveMultiComponentsResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'RemoveMultiComponentsResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ResourceLimits():
    """
    ResourceLimits.

    :attr str cpu: (optional) Maximum CPU for subcomponent. Must be >=
          "requests.cpu". Defaults to the same value in "requests.cpu". [Resource
          details](/docs/blockchain?topic=blockchain-ibp-console-govern-components#ibp-console-govern-components-allocate-resources).
    :attr str memory: (optional) Maximum memory for subcomponent. Must be >=
          "requests.memory". Defaults to the same value in "requests.memory". [Resource
          details](/docs/blockchain?topic=blockchain-ibp-console-govern-components#ibp-console-govern-components-allocate-resources).
    """

    def __init__(self,
                 *,
                 cpu: str = None,
                 memory: str = None) -> None:
        """
        Initialize a ResourceLimits object.

        :param str cpu: (optional) Maximum CPU for subcomponent. Must be >=
               "requests.cpu". Defaults to the same value in "requests.cpu". [Resource
               details](/docs/blockchain?topic=blockchain-ibp-console-govern-components#ibp-console-govern-components-allocate-resources).
        :param str memory: (optional) Maximum memory for subcomponent. Must be >=
               "requests.memory". Defaults to the same value in "requests.memory".
               [Resource
               details](/docs/blockchain?topic=blockchain-ibp-console-govern-components#ibp-console-govern-components-allocate-resources).
        """
        self.cpu = cpu
        self.memory = memory

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceLimits':
        """Initialize a ResourceLimits object from a json dictionary."""
        args = {}
        if 'cpu' in _dict:
            args['cpu'] = _dict.get('cpu')
        if 'memory' in _dict:
            args['memory'] = _dict.get('memory')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceLimits object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'cpu') and self.cpu is not None:
            _dict['cpu'] = self.cpu
        if hasattr(self, 'memory') and self.memory is not None:
            _dict['memory'] = self.memory
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceLimits object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceLimits') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceLimits') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ResourceObject():
    """
    This field requires the use of Fabric v1.4.* and higher.

    :attr ResourceRequests requests:
    :attr ResourceLimits limits: (optional)
    """

    def __init__(self,
                 requests: 'ResourceRequests',
                 *,
                 limits: 'ResourceLimits' = None) -> None:
        """
        Initialize a ResourceObject object.

        :param ResourceRequests requests:
        :param ResourceLimits limits: (optional)
        """
        self.requests = requests
        self.limits = limits

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceObject':
        """Initialize a ResourceObject object from a json dictionary."""
        args = {}
        if 'requests' in _dict:
            args['requests'] = ResourceRequests.from_dict(_dict.get('requests'))
        else:
            raise ValueError('Required property \'requests\' not present in ResourceObject JSON')
        if 'limits' in _dict:
            args['limits'] = ResourceLimits.from_dict(_dict.get('limits'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceObject object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'requests') and self.requests is not None:
            _dict['requests'] = self.requests.to_dict()
        if hasattr(self, 'limits') and self.limits is not None:
            _dict['limits'] = self.limits.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceObject object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceObject') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceObject') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ResourceObjectCouchDb():
    """
    *Legacy field name* Use the field `statedb` instead. This field requires the use of
    Fabric v1.4.* and higher.

    :attr ResourceRequests requests:
    :attr ResourceLimits limits: (optional)
    """

    def __init__(self,
                 requests: 'ResourceRequests',
                 *,
                 limits: 'ResourceLimits' = None) -> None:
        """
        Initialize a ResourceObjectCouchDb object.

        :param ResourceRequests requests:
        :param ResourceLimits limits: (optional)
        """
        self.requests = requests
        self.limits = limits

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceObjectCouchDb':
        """Initialize a ResourceObjectCouchDb object from a json dictionary."""
        args = {}
        if 'requests' in _dict:
            args['requests'] = ResourceRequests.from_dict(_dict.get('requests'))
        else:
            raise ValueError('Required property \'requests\' not present in ResourceObjectCouchDb JSON')
        if 'limits' in _dict:
            args['limits'] = ResourceLimits.from_dict(_dict.get('limits'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceObjectCouchDb object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'requests') and self.requests is not None:
            _dict['requests'] = self.requests.to_dict()
        if hasattr(self, 'limits') and self.limits is not None:
            _dict['limits'] = self.limits.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceObjectCouchDb object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceObjectCouchDb') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceObjectCouchDb') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ResourceObjectFabV1():
    """
    This field requires the use of Fabric v1.4.* and **lower**.

    :attr ResourceRequests requests:
    :attr ResourceLimits limits: (optional)
    """

    def __init__(self,
                 requests: 'ResourceRequests',
                 *,
                 limits: 'ResourceLimits' = None) -> None:
        """
        Initialize a ResourceObjectFabV1 object.

        :param ResourceRequests requests:
        :param ResourceLimits limits: (optional)
        """
        self.requests = requests
        self.limits = limits

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceObjectFabV1':
        """Initialize a ResourceObjectFabV1 object from a json dictionary."""
        args = {}
        if 'requests' in _dict:
            args['requests'] = ResourceRequests.from_dict(_dict.get('requests'))
        else:
            raise ValueError('Required property \'requests\' not present in ResourceObjectFabV1 JSON')
        if 'limits' in _dict:
            args['limits'] = ResourceLimits.from_dict(_dict.get('limits'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceObjectFabV1 object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'requests') and self.requests is not None:
            _dict['requests'] = self.requests.to_dict()
        if hasattr(self, 'limits') and self.limits is not None:
            _dict['limits'] = self.limits.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceObjectFabV1 object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceObjectFabV1') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceObjectFabV1') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ResourceObjectFabV2():
    """
    This field requires the use of Fabric v2.1.* and higher.

    :attr ResourceRequests requests:
    :attr ResourceLimits limits: (optional)
    """

    def __init__(self,
                 requests: 'ResourceRequests',
                 *,
                 limits: 'ResourceLimits' = None) -> None:
        """
        Initialize a ResourceObjectFabV2 object.

        :param ResourceRequests requests:
        :param ResourceLimits limits: (optional)
        """
        self.requests = requests
        self.limits = limits

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceObjectFabV2':
        """Initialize a ResourceObjectFabV2 object from a json dictionary."""
        args = {}
        if 'requests' in _dict:
            args['requests'] = ResourceRequests.from_dict(_dict.get('requests'))
        else:
            raise ValueError('Required property \'requests\' not present in ResourceObjectFabV2 JSON')
        if 'limits' in _dict:
            args['limits'] = ResourceLimits.from_dict(_dict.get('limits'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceObjectFabV2 object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'requests') and self.requests is not None:
            _dict['requests'] = self.requests.to_dict()
        if hasattr(self, 'limits') and self.limits is not None:
            _dict['limits'] = self.limits.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceObjectFabV2 object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceObjectFabV2') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceObjectFabV2') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ResourceRequests():
    """
    ResourceRequests.

    :attr str cpu: (optional) Desired CPU for subcomponent. [Resource
          details](/docs/blockchain?topic=blockchain-ibp-console-govern-components#ibp-console-govern-components-allocate-resources).
    :attr str memory: (optional) Desired memory for subcomponent. [Resource
          details](/docs/blockchain?topic=blockchain-ibp-console-govern-components#ibp-console-govern-components-allocate-resources).
    """

    def __init__(self,
                 *,
                 cpu: str = None,
                 memory: str = None) -> None:
        """
        Initialize a ResourceRequests object.

        :param str cpu: (optional) Desired CPU for subcomponent. [Resource
               details](/docs/blockchain?topic=blockchain-ibp-console-govern-components#ibp-console-govern-components-allocate-resources).
        :param str memory: (optional) Desired memory for subcomponent. [Resource
               details](/docs/blockchain?topic=blockchain-ibp-console-govern-components#ibp-console-govern-components-allocate-resources).
        """
        self.cpu = cpu
        self.memory = memory

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ResourceRequests':
        """Initialize a ResourceRequests object from a json dictionary."""
        args = {}
        if 'cpu' in _dict:
            args['cpu'] = _dict.get('cpu')
        if 'memory' in _dict:
            args['memory'] = _dict.get('memory')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ResourceRequests object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'cpu') and self.cpu is not None:
            _dict['cpu'] = self.cpu
        if hasattr(self, 'memory') and self.memory is not None:
            _dict['memory'] = self.memory
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ResourceRequests object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ResourceRequests') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ResourceRequests') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class RestartAthenaResponse():
    """
    RestartAthenaResponse.

    :attr str message: (optional) Text describing the outcome of the api.
    """

    def __init__(self,
                 *,
                 message: str = None) -> None:
        """
        Initialize a RestartAthenaResponse object.

        :param str message: (optional) Text describing the outcome of the api.
        """
        self.message = message

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'RestartAthenaResponse':
        """Initialize a RestartAthenaResponse object from a json dictionary."""
        args = {}
        if 'message' in _dict:
            args['message'] = _dict.get('message')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a RestartAthenaResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'message') and self.message is not None:
            _dict['message'] = self.message
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this RestartAthenaResponse object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'RestartAthenaResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'RestartAthenaResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class SettingsTimestampData():
    """
    SettingsTimestampData.

    :attr float now: (optional) UTC UNIX timestamp of the current time according to
          the server. In milliseconds.
    :attr float born: (optional) UTC UNIX timestamp of when the server started. In
          milliseconds.
    :attr str next_settings_update: (optional) Time remaining until the server
          performs a hard-refresh of its settings.
    :attr str up_time: (optional) Total time the IBP console server has been
          running.
    """

    def __init__(self,
                 *,
                 now: float = None,
                 born: float = None,
                 next_settings_update: str = None,
                 up_time: str = None) -> None:
        """
        Initialize a SettingsTimestampData object.

        :param float now: (optional) UTC UNIX timestamp of the current time
               according to the server. In milliseconds.
        :param float born: (optional) UTC UNIX timestamp of when the server
               started. In milliseconds.
        :param str next_settings_update: (optional) Time remaining until the server
               performs a hard-refresh of its settings.
        :param str up_time: (optional) Total time the IBP console server has been
               running.
        """
        self.now = now
        self.born = born
        self.next_settings_update = next_settings_update
        self.up_time = up_time

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'SettingsTimestampData':
        """Initialize a SettingsTimestampData object from a json dictionary."""
        args = {}
        if 'now' in _dict:
            args['now'] = _dict.get('now')
        if 'born' in _dict:
            args['born'] = _dict.get('born')
        if 'next_settings_update' in _dict:
            args['next_settings_update'] = _dict.get('next_settings_update')
        if 'up_time' in _dict:
            args['up_time'] = _dict.get('up_time')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SettingsTimestampData object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'now') and self.now is not None:
            _dict['now'] = self.now
        if hasattr(self, 'born') and self.born is not None:
            _dict['born'] = self.born
        if hasattr(self, 'next_settings_update') and self.next_settings_update is not None:
            _dict['next_settings_update'] = self.next_settings_update
        if hasattr(self, 'up_time') and self.up_time is not None:
            _dict['up_time'] = self.up_time
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this SettingsTimestampData object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'SettingsTimestampData') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SettingsTimestampData') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class StorageObject():
    """
    StorageObject.

    :attr str size: (optional) Maximum disk space for subcomponent. [Resource
          details](/docs/blockchain?topic=blockchain-ibp-console-govern-components#ibp-console-govern-components-allocate-resources).
    :attr str class_: (optional) Kubernetes storage class for subcomponent's disk
          space.
    """

    def __init__(self,
                 *,
                 size: str = None,
                 class_: str = None) -> None:
        """
        Initialize a StorageObject object.

        :param str size: (optional) Maximum disk space for subcomponent. [Resource
               details](/docs/blockchain?topic=blockchain-ibp-console-govern-components#ibp-console-govern-components-allocate-resources).
        :param str class_: (optional) Kubernetes storage class for subcomponent's
               disk space.
        """
        self.size = size
        self.class_ = class_

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'StorageObject':
        """Initialize a StorageObject object from a json dictionary."""
        args = {}
        if 'size' in _dict:
            args['size'] = _dict.get('size')
        if 'class' in _dict:
            args['class_'] = _dict.get('class')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a StorageObject object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'size') and self.size is not None:
            _dict['size'] = self.size
        if hasattr(self, 'class_') and self.class_ is not None:
            _dict['class'] = self.class_
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this StorageObject object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'StorageObject') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'StorageObject') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class UpdateCaBodyConfigOverride():
    """
    Update the [Fabric CA configuration
    file](https://hyperledger-fabric-ca.readthedocs.io/en/release-1.4/serverconfig.html)
    if you want use custom attributes to configure advanced CA features. Omit if not.
    *The nested field **names** below are not case-sensitive.*
    *The nested fields sent will be merged with the existing settings.*.

    :attr ConfigCAUpdate ca:
    """

    def __init__(self,
                 ca: 'ConfigCAUpdate') -> None:
        """
        Initialize a UpdateCaBodyConfigOverride object.

        :param ConfigCAUpdate ca:
        """
        self.ca = ca

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'UpdateCaBodyConfigOverride':
        """Initialize a UpdateCaBodyConfigOverride object from a json dictionary."""
        args = {}
        if 'ca' in _dict:
            args['ca'] = ConfigCAUpdate.from_dict(_dict.get('ca'))
        else:
            raise ValueError('Required property \'ca\' not present in UpdateCaBodyConfigOverride JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a UpdateCaBodyConfigOverride object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this UpdateCaBodyConfigOverride object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'UpdateCaBodyConfigOverride') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'UpdateCaBodyConfigOverride') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class UpdateCaBodyResources():
    """
    CPU and memory properties. This feature is not available if using a free Kubernetes
    cluster.

    :attr ResourceObject ca: This field requires the use of Fabric v1.4.* and
          higher.
    """

    def __init__(self,
                 ca: 'ResourceObject') -> None:
        """
        Initialize a UpdateCaBodyResources object.

        :param ResourceObject ca: This field requires the use of Fabric v1.4.* and
               higher.
        """
        self.ca = ca

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'UpdateCaBodyResources':
        """Initialize a UpdateCaBodyResources object from a json dictionary."""
        args = {}
        if 'ca' in _dict:
            args['ca'] = ResourceObject.from_dict(_dict.get('ca'))
        else:
            raise ValueError('Required property \'ca\' not present in UpdateCaBodyResources JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a UpdateCaBodyResources object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this UpdateCaBodyResources object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'UpdateCaBodyResources') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'UpdateCaBodyResources') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class UpdateEnrollmentCryptoField():
    """
    Edit the `enrollment` crypto data of this component. Editing the `enrollment` field is
    only possible if this component was created using the `crypto.enrollment` field, else
    see the `crypto.msp` field.

    :attr CryptoEnrollmentComponent component: (optional)
    :attr UpdateEnrollmentCryptoFieldCa ca: (optional)
    :attr UpdateEnrollmentCryptoFieldTlsca tlsca: (optional)
    """

    def __init__(self,
                 *,
                 component: 'CryptoEnrollmentComponent' = None,
                 ca: 'UpdateEnrollmentCryptoFieldCa' = None,
                 tlsca: 'UpdateEnrollmentCryptoFieldTlsca' = None) -> None:
        """
        Initialize a UpdateEnrollmentCryptoField object.

        :param CryptoEnrollmentComponent component: (optional)
        :param UpdateEnrollmentCryptoFieldCa ca: (optional)
        :param UpdateEnrollmentCryptoFieldTlsca tlsca: (optional)
        """
        self.component = component
        self.ca = ca
        self.tlsca = tlsca

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'UpdateEnrollmentCryptoField':
        """Initialize a UpdateEnrollmentCryptoField object from a json dictionary."""
        args = {}
        if 'component' in _dict:
            args['component'] = CryptoEnrollmentComponent.from_dict(_dict.get('component'))
        if 'ca' in _dict:
            args['ca'] = UpdateEnrollmentCryptoFieldCa.from_dict(_dict.get('ca'))
        if 'tlsca' in _dict:
            args['tlsca'] = UpdateEnrollmentCryptoFieldTlsca.from_dict(_dict.get('tlsca'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a UpdateEnrollmentCryptoField object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'component') and self.component is not None:
            _dict['component'] = self.component.to_dict()
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        if hasattr(self, 'tlsca') and self.tlsca is not None:
            _dict['tlsca'] = self.tlsca.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this UpdateEnrollmentCryptoField object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'UpdateEnrollmentCryptoField') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'UpdateEnrollmentCryptoField') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class UpdateEnrollmentCryptoFieldCa():
    """
    UpdateEnrollmentCryptoFieldCa.

    :attr str host: (optional) The CA's hostname. Do not include protocol or port.
    :attr float port: (optional) The CA's port.
    :attr str name: (optional) The CA's "CAName" attribute. This name is used to
          distinguish this CA from the TLS CA.
    :attr str tls_cert: (optional) The TLS certificate as base 64 encoded PEM.
          Certificate is used to secure/validate a TLS connection with this component.
    :attr str enroll_id: (optional) The username of the enroll id.
    :attr str enroll_secret: (optional) The password of the enroll id.
    """

    def __init__(self,
                 *,
                 host: str = None,
                 port: float = None,
                 name: str = None,
                 tls_cert: str = None,
                 enroll_id: str = None,
                 enroll_secret: str = None) -> None:
        """
        Initialize a UpdateEnrollmentCryptoFieldCa object.

        :param str host: (optional) The CA's hostname. Do not include protocol or
               port.
        :param float port: (optional) The CA's port.
        :param str name: (optional) The CA's "CAName" attribute. This name is used
               to distinguish this CA from the TLS CA.
        :param str tls_cert: (optional) The TLS certificate as base 64 encoded PEM.
               Certificate is used to secure/validate a TLS connection with this
               component.
        :param str enroll_id: (optional) The username of the enroll id.
        :param str enroll_secret: (optional) The password of the enroll id.
        """
        self.host = host
        self.port = port
        self.name = name
        self.tls_cert = tls_cert
        self.enroll_id = enroll_id
        self.enroll_secret = enroll_secret

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'UpdateEnrollmentCryptoFieldCa':
        """Initialize a UpdateEnrollmentCryptoFieldCa object from a json dictionary."""
        args = {}
        if 'host' in _dict:
            args['host'] = _dict.get('host')
        if 'port' in _dict:
            args['port'] = _dict.get('port')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'tls_cert' in _dict:
            args['tls_cert'] = _dict.get('tls_cert')
        if 'enroll_id' in _dict:
            args['enroll_id'] = _dict.get('enroll_id')
        if 'enroll_secret' in _dict:
            args['enroll_secret'] = _dict.get('enroll_secret')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a UpdateEnrollmentCryptoFieldCa object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'host') and self.host is not None:
            _dict['host'] = self.host
        if hasattr(self, 'port') and self.port is not None:
            _dict['port'] = self.port
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'tls_cert') and self.tls_cert is not None:
            _dict['tls_cert'] = self.tls_cert
        if hasattr(self, 'enroll_id') and self.enroll_id is not None:
            _dict['enroll_id'] = self.enroll_id
        if hasattr(self, 'enroll_secret') and self.enroll_secret is not None:
            _dict['enroll_secret'] = self.enroll_secret
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this UpdateEnrollmentCryptoFieldCa object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'UpdateEnrollmentCryptoFieldCa') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'UpdateEnrollmentCryptoFieldCa') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class UpdateEnrollmentCryptoFieldTlsca():
    """
    UpdateEnrollmentCryptoFieldTlsca.

    :attr str host: (optional) The CA's hostname. Do not include protocol or port.
    :attr float port: (optional) The CA's port.
    :attr str name: (optional) The TLS CA's "CAName" attribute. This name is used to
          distinguish this TLS CA from the other CA.
    :attr str tls_cert: (optional) The TLS certificate as base 64 encoded PEM.
          Certificate is used to secure/validate a TLS connection with this component.
    :attr str enroll_id: (optional) The username of the enroll id.
    :attr str enroll_secret: (optional) The password of the enroll id.
    :attr List[str] csr_hosts: (optional)
    """

    def __init__(self,
                 *,
                 host: str = None,
                 port: float = None,
                 name: str = None,
                 tls_cert: str = None,
                 enroll_id: str = None,
                 enroll_secret: str = None,
                 csr_hosts: List[str] = None) -> None:
        """
        Initialize a UpdateEnrollmentCryptoFieldTlsca object.

        :param str host: (optional) The CA's hostname. Do not include protocol or
               port.
        :param float port: (optional) The CA's port.
        :param str name: (optional) The TLS CA's "CAName" attribute. This name is
               used to distinguish this TLS CA from the other CA.
        :param str tls_cert: (optional) The TLS certificate as base 64 encoded PEM.
               Certificate is used to secure/validate a TLS connection with this
               component.
        :param str enroll_id: (optional) The username of the enroll id.
        :param str enroll_secret: (optional) The password of the enroll id.
        :param List[str] csr_hosts: (optional)
        """
        self.host = host
        self.port = port
        self.name = name
        self.tls_cert = tls_cert
        self.enroll_id = enroll_id
        self.enroll_secret = enroll_secret
        self.csr_hosts = csr_hosts

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'UpdateEnrollmentCryptoFieldTlsca':
        """Initialize a UpdateEnrollmentCryptoFieldTlsca object from a json dictionary."""
        args = {}
        if 'host' in _dict:
            args['host'] = _dict.get('host')
        if 'port' in _dict:
            args['port'] = _dict.get('port')
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        if 'tls_cert' in _dict:
            args['tls_cert'] = _dict.get('tls_cert')
        if 'enroll_id' in _dict:
            args['enroll_id'] = _dict.get('enroll_id')
        if 'enroll_secret' in _dict:
            args['enroll_secret'] = _dict.get('enroll_secret')
        if 'csr_hosts' in _dict:
            args['csr_hosts'] = _dict.get('csr_hosts')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a UpdateEnrollmentCryptoFieldTlsca object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'host') and self.host is not None:
            _dict['host'] = self.host
        if hasattr(self, 'port') and self.port is not None:
            _dict['port'] = self.port
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'tls_cert') and self.tls_cert is not None:
            _dict['tls_cert'] = self.tls_cert
        if hasattr(self, 'enroll_id') and self.enroll_id is not None:
            _dict['enroll_id'] = self.enroll_id
        if hasattr(self, 'enroll_secret') and self.enroll_secret is not None:
            _dict['enroll_secret'] = self.enroll_secret
        if hasattr(self, 'csr_hosts') and self.csr_hosts is not None:
            _dict['csr_hosts'] = self.csr_hosts
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this UpdateEnrollmentCryptoFieldTlsca object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'UpdateEnrollmentCryptoFieldTlsca') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'UpdateEnrollmentCryptoFieldTlsca') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class UpdateMspCryptoField():
    """
    Edit the `msp` crypto data of this component. Editing the `msp` field is only possible
    if this component was created using the `crypto.msp` field, else see the
    `crypto.enrollment` field.

    :attr UpdateMspCryptoFieldCa ca: (optional)
    :attr UpdateMspCryptoFieldTlsca tlsca: (optional)
    :attr UpdateMspCryptoFieldComponent component: (optional)
    """

    def __init__(self,
                 *,
                 ca: 'UpdateMspCryptoFieldCa' = None,
                 tlsca: 'UpdateMspCryptoFieldTlsca' = None,
                 component: 'UpdateMspCryptoFieldComponent' = None) -> None:
        """
        Initialize a UpdateMspCryptoField object.

        :param UpdateMspCryptoFieldCa ca: (optional)
        :param UpdateMspCryptoFieldTlsca tlsca: (optional)
        :param UpdateMspCryptoFieldComponent component: (optional)
        """
        self.ca = ca
        self.tlsca = tlsca
        self.component = component

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'UpdateMspCryptoField':
        """Initialize a UpdateMspCryptoField object from a json dictionary."""
        args = {}
        if 'ca' in _dict:
            args['ca'] = UpdateMspCryptoFieldCa.from_dict(_dict.get('ca'))
        if 'tlsca' in _dict:
            args['tlsca'] = UpdateMspCryptoFieldTlsca.from_dict(_dict.get('tlsca'))
        if 'component' in _dict:
            args['component'] = UpdateMspCryptoFieldComponent.from_dict(_dict.get('component'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a UpdateMspCryptoField object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        if hasattr(self, 'tlsca') and self.tlsca is not None:
            _dict['tlsca'] = self.tlsca.to_dict()
        if hasattr(self, 'component') and self.component is not None:
            _dict['component'] = self.component.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this UpdateMspCryptoField object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'UpdateMspCryptoField') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'UpdateMspCryptoField') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class UpdateMspCryptoFieldCa():
    """
    UpdateMspCryptoFieldCa.

    :attr List[str] root_certs: (optional) An array that contains one or more base
          64 encoded PEM CA root certificates.
    :attr List[str] ca_intermediate_certs: (optional) An array that contains base 64
          encoded PEM intermediate CA certificates.
    """

    def __init__(self,
                 *,
                 root_certs: List[str] = None,
                 ca_intermediate_certs: List[str] = None) -> None:
        """
        Initialize a UpdateMspCryptoFieldCa object.

        :param List[str] root_certs: (optional) An array that contains one or more
               base 64 encoded PEM CA root certificates.
        :param List[str] ca_intermediate_certs: (optional) An array that contains
               base 64 encoded PEM intermediate CA certificates.
        """
        self.root_certs = root_certs
        self.ca_intermediate_certs = ca_intermediate_certs

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'UpdateMspCryptoFieldCa':
        """Initialize a UpdateMspCryptoFieldCa object from a json dictionary."""
        args = {}
        if 'root_certs' in _dict:
            args['root_certs'] = _dict.get('root_certs')
        if 'ca_intermediate_certs' in _dict:
            args['ca_intermediate_certs'] = _dict.get('ca_intermediate_certs')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a UpdateMspCryptoFieldCa object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'root_certs') and self.root_certs is not None:
            _dict['root_certs'] = self.root_certs
        if hasattr(self, 'ca_intermediate_certs') and self.ca_intermediate_certs is not None:
            _dict['ca_intermediate_certs'] = self.ca_intermediate_certs
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this UpdateMspCryptoFieldCa object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'UpdateMspCryptoFieldCa') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'UpdateMspCryptoFieldCa') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class UpdateMspCryptoFieldComponent():
    """
    UpdateMspCryptoFieldComponent.

    :attr str ekey: (optional) An identity private key (base 64 encoded PEM) for
          this component (aka enrollment private key).
    :attr str ecert: (optional) An identity certificate (base 64 encoded PEM) for
          this component that was signed by the CA (aka enrollment certificate).
    :attr List[str] admin_certs: (optional) An array that contains base 64 encoded
          PEM identity certificates for administrators. Also known as signing certificates
          of an organization administrator.
    :attr str tls_key: (optional) A private key (base 64 encoded PEM) for this
          component's TLS.
    :attr str tls_cert: (optional) The TLS certificate as base 64 encoded PEM.
          Certificate is used to secure/validate a TLS connection with this component.
    :attr ClientAuth client_auth: (optional)
    """

    def __init__(self,
                 *,
                 ekey: str = None,
                 ecert: str = None,
                 admin_certs: List[str] = None,
                 tls_key: str = None,
                 tls_cert: str = None,
                 client_auth: 'ClientAuth' = None) -> None:
        """
        Initialize a UpdateMspCryptoFieldComponent object.

        :param str ekey: (optional) An identity private key (base 64 encoded PEM)
               for this component (aka enrollment private key).
        :param str ecert: (optional) An identity certificate (base 64 encoded PEM)
               for this component that was signed by the CA (aka enrollment certificate).
        :param List[str] admin_certs: (optional) An array that contains base 64
               encoded PEM identity certificates for administrators. Also known as signing
               certificates of an organization administrator.
        :param str tls_key: (optional) A private key (base 64 encoded PEM) for this
               component's TLS.
        :param str tls_cert: (optional) The TLS certificate as base 64 encoded PEM.
               Certificate is used to secure/validate a TLS connection with this
               component.
        :param ClientAuth client_auth: (optional)
        """
        self.ekey = ekey
        self.ecert = ecert
        self.admin_certs = admin_certs
        self.tls_key = tls_key
        self.tls_cert = tls_cert
        self.client_auth = client_auth

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'UpdateMspCryptoFieldComponent':
        """Initialize a UpdateMspCryptoFieldComponent object from a json dictionary."""
        args = {}
        if 'ekey' in _dict:
            args['ekey'] = _dict.get('ekey')
        if 'ecert' in _dict:
            args['ecert'] = _dict.get('ecert')
        if 'admin_certs' in _dict:
            args['admin_certs'] = _dict.get('admin_certs')
        if 'tls_key' in _dict:
            args['tls_key'] = _dict.get('tls_key')
        if 'tls_cert' in _dict:
            args['tls_cert'] = _dict.get('tls_cert')
        if 'client_auth' in _dict:
            args['client_auth'] = ClientAuth.from_dict(_dict.get('client_auth'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a UpdateMspCryptoFieldComponent object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'ekey') and self.ekey is not None:
            _dict['ekey'] = self.ekey
        if hasattr(self, 'ecert') and self.ecert is not None:
            _dict['ecert'] = self.ecert
        if hasattr(self, 'admin_certs') and self.admin_certs is not None:
            _dict['admin_certs'] = self.admin_certs
        if hasattr(self, 'tls_key') and self.tls_key is not None:
            _dict['tls_key'] = self.tls_key
        if hasattr(self, 'tls_cert') and self.tls_cert is not None:
            _dict['tls_cert'] = self.tls_cert
        if hasattr(self, 'client_auth') and self.client_auth is not None:
            _dict['client_auth'] = self.client_auth.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this UpdateMspCryptoFieldComponent object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'UpdateMspCryptoFieldComponent') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'UpdateMspCryptoFieldComponent') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class UpdateMspCryptoFieldTlsca():
    """
    UpdateMspCryptoFieldTlsca.

    :attr List[str] root_certs: (optional) An array that contains one or more base
          64 encoded PEM CA root certificates.
    :attr List[str] ca_intermediate_certs: (optional) An array that contains base 64
          encoded PEM intermediate CA certificates.
    """

    def __init__(self,
                 *,
                 root_certs: List[str] = None,
                 ca_intermediate_certs: List[str] = None) -> None:
        """
        Initialize a UpdateMspCryptoFieldTlsca object.

        :param List[str] root_certs: (optional) An array that contains one or more
               base 64 encoded PEM CA root certificates.
        :param List[str] ca_intermediate_certs: (optional) An array that contains
               base 64 encoded PEM intermediate CA certificates.
        """
        self.root_certs = root_certs
        self.ca_intermediate_certs = ca_intermediate_certs

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'UpdateMspCryptoFieldTlsca':
        """Initialize a UpdateMspCryptoFieldTlsca object from a json dictionary."""
        args = {}
        if 'root_certs' in _dict:
            args['root_certs'] = _dict.get('root_certs')
        if 'ca_intermediate_certs' in _dict:
            args['ca_intermediate_certs'] = _dict.get('ca_intermediate_certs')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a UpdateMspCryptoFieldTlsca object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'root_certs') and self.root_certs is not None:
            _dict['root_certs'] = self.root_certs
        if hasattr(self, 'ca_intermediate_certs') and self.ca_intermediate_certs is not None:
            _dict['ca_intermediate_certs'] = self.ca_intermediate_certs
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this UpdateMspCryptoFieldTlsca object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'UpdateMspCryptoFieldTlsca') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'UpdateMspCryptoFieldTlsca') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class UpdateOrdererBodyCrypto():
    """
    UpdateOrdererBodyCrypto.

    :attr UpdateEnrollmentCryptoField enrollment: (optional) Edit the `enrollment`
          crypto data of this component. Editing the `enrollment` field is only possible
          if this component was created using the `crypto.enrollment` field, else see the
          `crypto.msp` field.
    :attr UpdateMspCryptoField msp: (optional) Edit the `msp` crypto data of this
          component. Editing the `msp` field is only possible if this component was
          created using the `crypto.msp` field, else see the `crypto.enrollment` field.
    """

    def __init__(self,
                 *,
                 enrollment: 'UpdateEnrollmentCryptoField' = None,
                 msp: 'UpdateMspCryptoField' = None) -> None:
        """
        Initialize a UpdateOrdererBodyCrypto object.

        :param UpdateEnrollmentCryptoField enrollment: (optional) Edit the
               `enrollment` crypto data of this component. Editing the `enrollment` field
               is only possible if this component was created using the
               `crypto.enrollment` field, else see the `crypto.msp` field.
        :param UpdateMspCryptoField msp: (optional) Edit the `msp` crypto data of
               this component. Editing the `msp` field is only possible if this component
               was created using the `crypto.msp` field, else see the `crypto.enrollment`
               field.
        """
        self.enrollment = enrollment
        self.msp = msp

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'UpdateOrdererBodyCrypto':
        """Initialize a UpdateOrdererBodyCrypto object from a json dictionary."""
        args = {}
        if 'enrollment' in _dict:
            args['enrollment'] = UpdateEnrollmentCryptoField.from_dict(_dict.get('enrollment'))
        if 'msp' in _dict:
            args['msp'] = UpdateMspCryptoField.from_dict(_dict.get('msp'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a UpdateOrdererBodyCrypto object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'enrollment') and self.enrollment is not None:
            _dict['enrollment'] = self.enrollment.to_dict()
        if hasattr(self, 'msp') and self.msp is not None:
            _dict['msp'] = self.msp.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this UpdateOrdererBodyCrypto object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'UpdateOrdererBodyCrypto') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'UpdateOrdererBodyCrypto') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class UpdateOrdererBodyResources():
    """
    CPU and memory properties. This feature is not available if using a free Kubernetes
    cluster.

    :attr ResourceObject orderer: (optional) This field requires the use of Fabric
          v1.4.* and higher.
    :attr ResourceObject proxy: (optional) This field requires the use of Fabric
          v1.4.* and higher.
    """

    def __init__(self,
                 *,
                 orderer: 'ResourceObject' = None,
                 proxy: 'ResourceObject' = None) -> None:
        """
        Initialize a UpdateOrdererBodyResources object.

        :param ResourceObject orderer: (optional) This field requires the use of
               Fabric v1.4.* and higher.
        :param ResourceObject proxy: (optional) This field requires the use of
               Fabric v1.4.* and higher.
        """
        self.orderer = orderer
        self.proxy = proxy

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'UpdateOrdererBodyResources':
        """Initialize a UpdateOrdererBodyResources object from a json dictionary."""
        args = {}
        if 'orderer' in _dict:
            args['orderer'] = ResourceObject.from_dict(_dict.get('orderer'))
        if 'proxy' in _dict:
            args['proxy'] = ResourceObject.from_dict(_dict.get('proxy'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a UpdateOrdererBodyResources object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'orderer') and self.orderer is not None:
            _dict['orderer'] = self.orderer.to_dict()
        if hasattr(self, 'proxy') and self.proxy is not None:
            _dict['proxy'] = self.proxy.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this UpdateOrdererBodyResources object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'UpdateOrdererBodyResources') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'UpdateOrdererBodyResources') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class UpdatePeerBodyCrypto():
    """
    UpdatePeerBodyCrypto.

    :attr UpdateEnrollmentCryptoField enrollment: (optional) Edit the `enrollment`
          crypto data of this component. Editing the `enrollment` field is only possible
          if this component was created using the `crypto.enrollment` field, else see the
          `crypto.msp` field.
    :attr UpdateMspCryptoField msp: (optional) Edit the `msp` crypto data of this
          component. Editing the `msp` field is only possible if this component was
          created using the `crypto.msp` field, else see the `crypto.enrollment` field.
    """

    def __init__(self,
                 *,
                 enrollment: 'UpdateEnrollmentCryptoField' = None,
                 msp: 'UpdateMspCryptoField' = None) -> None:
        """
        Initialize a UpdatePeerBodyCrypto object.

        :param UpdateEnrollmentCryptoField enrollment: (optional) Edit the
               `enrollment` crypto data of this component. Editing the `enrollment` field
               is only possible if this component was created using the
               `crypto.enrollment` field, else see the `crypto.msp` field.
        :param UpdateMspCryptoField msp: (optional) Edit the `msp` crypto data of
               this component. Editing the `msp` field is only possible if this component
               was created using the `crypto.msp` field, else see the `crypto.enrollment`
               field.
        """
        self.enrollment = enrollment
        self.msp = msp

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'UpdatePeerBodyCrypto':
        """Initialize a UpdatePeerBodyCrypto object from a json dictionary."""
        args = {}
        if 'enrollment' in _dict:
            args['enrollment'] = UpdateEnrollmentCryptoField.from_dict(_dict.get('enrollment'))
        if 'msp' in _dict:
            args['msp'] = UpdateMspCryptoField.from_dict(_dict.get('msp'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a UpdatePeerBodyCrypto object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'enrollment') and self.enrollment is not None:
            _dict['enrollment'] = self.enrollment.to_dict()
        if hasattr(self, 'msp') and self.msp is not None:
            _dict['msp'] = self.msp.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this UpdatePeerBodyCrypto object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'UpdatePeerBodyCrypto') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'UpdatePeerBodyCrypto') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ActionEnroll():
    """
    ActionEnroll.

    :attr bool tls_cert: (optional) Set to `true` to generate a new tls cert for
          this component via enrollment.
    :attr bool ecert: (optional) Set to `true` to generate a new ecert for this
          component via enrollment.
    """

    def __init__(self,
                 *,
                 tls_cert: bool = None,
                 ecert: bool = None) -> None:
        """
        Initialize a ActionEnroll object.

        :param bool tls_cert: (optional) Set to `true` to generate a new tls cert
               for this component via enrollment.
        :param bool ecert: (optional) Set to `true` to generate a new ecert for
               this component via enrollment.
        """
        self.tls_cert = tls_cert
        self.ecert = ecert

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ActionEnroll':
        """Initialize a ActionEnroll object from a json dictionary."""
        args = {}
        if 'tls_cert' in _dict:
            args['tls_cert'] = _dict.get('tls_cert')
        if 'ecert' in _dict:
            args['ecert'] = _dict.get('ecert')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ActionEnroll object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'tls_cert') and self.tls_cert is not None:
            _dict['tls_cert'] = self.tls_cert
        if hasattr(self, 'ecert') and self.ecert is not None:
            _dict['ecert'] = self.ecert
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ActionEnroll object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ActionEnroll') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ActionEnroll') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ActionReenroll():
    """
    ActionReenroll.

    :attr bool tls_cert: (optional) Set to `true` to generate a new tls cert for
          this component via re-enrollment.
    :attr bool ecert: (optional) Set to `true` to generate a new ecert for this
          component via re-enrollment.
    """

    def __init__(self,
                 *,
                 tls_cert: bool = None,
                 ecert: bool = None) -> None:
        """
        Initialize a ActionReenroll object.

        :param bool tls_cert: (optional) Set to `true` to generate a new tls cert
               for this component via re-enrollment.
        :param bool ecert: (optional) Set to `true` to generate a new ecert for
               this component via re-enrollment.
        """
        self.tls_cert = tls_cert
        self.ecert = ecert

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ActionReenroll':
        """Initialize a ActionReenroll object from a json dictionary."""
        args = {}
        if 'tls_cert' in _dict:
            args['tls_cert'] = _dict.get('tls_cert')
        if 'ecert' in _dict:
            args['ecert'] = _dict.get('ecert')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ActionReenroll object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'tls_cert') and self.tls_cert is not None:
            _dict['tls_cert'] = self.tls_cert
        if hasattr(self, 'ecert') and self.ecert is not None:
            _dict['ecert'] = self.ecert
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ActionReenroll object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ActionReenroll') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ActionReenroll') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ActionRenew():
    """
    ActionRenew.

    :attr bool tls_cert: (optional) Set to `true` to renew the tls cert for this
          component.
    """

    def __init__(self,
                 *,
                 tls_cert: bool = None) -> None:
        """
        Initialize a ActionRenew object.

        :param bool tls_cert: (optional) Set to `true` to renew the tls cert for
               this component.
        """
        self.tls_cert = tls_cert

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ActionRenew':
        """Initialize a ActionRenew object from a json dictionary."""
        args = {}
        if 'tls_cert' in _dict:
            args['tls_cert'] = _dict.get('tls_cert')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ActionRenew object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'tls_cert') and self.tls_cert is not None:
            _dict['tls_cert'] = self.tls_cert
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ActionRenew object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ActionRenew') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ActionRenew') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class ClientAuth():
    """
    ClientAuth.

    :attr str type: (optional)
    :attr List[str] tls_certs: (optional)
    """

    def __init__(self,
                 *,
                 type: str = None,
                 tls_certs: List[str] = None) -> None:
        """
        Initialize a ClientAuth object.

        :param str type: (optional)
        :param List[str] tls_certs: (optional)
        """
        self.type = type
        self.tls_certs = tls_certs

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'ClientAuth':
        """Initialize a ClientAuth object from a json dictionary."""
        args = {}
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'tls_certs' in _dict:
            args['tls_certs'] = _dict.get('tls_certs')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a ClientAuth object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'tls_certs') and self.tls_certs is not None:
            _dict['tls_certs'] = self.tls_certs
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this ClientAuth object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'ClientAuth') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'ClientAuth') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class Hsm():
    """
    The connection details of the HSM (Hardware Security Module).

    :attr str pkcs11endpoint: The url to the HSM. Include the protocol, hostname,
          and port.
    """

    def __init__(self,
                 pkcs11endpoint: str) -> None:
        """
        Initialize a Hsm object.

        :param str pkcs11endpoint: The url to the HSM. Include the protocol,
               hostname, and port.
        """
        self.pkcs11endpoint = pkcs11endpoint

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'Hsm':
        """Initialize a Hsm object from a json dictionary."""
        args = {}
        if 'pkcs11endpoint' in _dict:
            args['pkcs11endpoint'] = _dict.get('pkcs11endpoint')
        else:
            raise ValueError('Required property \'pkcs11endpoint\' not present in Hsm JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a Hsm object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'pkcs11endpoint') and self.pkcs11endpoint is not None:
            _dict['pkcs11endpoint'] = self.pkcs11endpoint
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this Hsm object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'Hsm') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'Hsm') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class IdentityAttrs():
    """
    IdentityAttrs.

    :attr str hf_registrar_roles: (optional)
    :attr str hf_registrar_delegate_roles: (optional)
    :attr bool hf_revoker: (optional)
    :attr bool hf_intermediate_ca: (optional)
    :attr bool hf_gen_crl: (optional)
    :attr str hf_registrar_attributes: (optional)
    :attr bool hf_affiliation_mgr: (optional)
    """

    def __init__(self,
                 *,
                 hf_registrar_roles: str = None,
                 hf_registrar_delegate_roles: str = None,
                 hf_revoker: bool = None,
                 hf_intermediate_ca: bool = None,
                 hf_gen_crl: bool = None,
                 hf_registrar_attributes: str = None,
                 hf_affiliation_mgr: bool = None) -> None:
        """
        Initialize a IdentityAttrs object.

        :param str hf_registrar_roles: (optional)
        :param str hf_registrar_delegate_roles: (optional)
        :param bool hf_revoker: (optional)
        :param bool hf_intermediate_ca: (optional)
        :param bool hf_gen_crl: (optional)
        :param str hf_registrar_attributes: (optional)
        :param bool hf_affiliation_mgr: (optional)
        """
        self.hf_registrar_roles = hf_registrar_roles
        self.hf_registrar_delegate_roles = hf_registrar_delegate_roles
        self.hf_revoker = hf_revoker
        self.hf_intermediate_ca = hf_intermediate_ca
        self.hf_gen_crl = hf_gen_crl
        self.hf_registrar_attributes = hf_registrar_attributes
        self.hf_affiliation_mgr = hf_affiliation_mgr

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'IdentityAttrs':
        """Initialize a IdentityAttrs object from a json dictionary."""
        args = {}
        if 'hf.Registrar.Roles' in _dict:
            args['hf_registrar_roles'] = _dict.get('hf.Registrar.Roles')
        if 'hf.Registrar.DelegateRoles' in _dict:
            args['hf_registrar_delegate_roles'] = _dict.get('hf.Registrar.DelegateRoles')
        if 'hf.Revoker' in _dict:
            args['hf_revoker'] = _dict.get('hf.Revoker')
        if 'hf.IntermediateCA' in _dict:
            args['hf_intermediate_ca'] = _dict.get('hf.IntermediateCA')
        if 'hf.GenCRL' in _dict:
            args['hf_gen_crl'] = _dict.get('hf.GenCRL')
        if 'hf.Registrar.Attributes' in _dict:
            args['hf_registrar_attributes'] = _dict.get('hf.Registrar.Attributes')
        if 'hf.AffiliationMgr' in _dict:
            args['hf_affiliation_mgr'] = _dict.get('hf.AffiliationMgr')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a IdentityAttrs object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'hf_registrar_roles') and self.hf_registrar_roles is not None:
            _dict['hf.Registrar.Roles'] = self.hf_registrar_roles
        if hasattr(self, 'hf_registrar_delegate_roles') and self.hf_registrar_delegate_roles is not None:
            _dict['hf.Registrar.DelegateRoles'] = self.hf_registrar_delegate_roles
        if hasattr(self, 'hf_revoker') and self.hf_revoker is not None:
            _dict['hf.Revoker'] = self.hf_revoker
        if hasattr(self, 'hf_intermediate_ca') and self.hf_intermediate_ca is not None:
            _dict['hf.IntermediateCA'] = self.hf_intermediate_ca
        if hasattr(self, 'hf_gen_crl') and self.hf_gen_crl is not None:
            _dict['hf.GenCRL'] = self.hf_gen_crl
        if hasattr(self, 'hf_registrar_attributes') and self.hf_registrar_attributes is not None:
            _dict['hf.Registrar.Attributes'] = self.hf_registrar_attributes
        if hasattr(self, 'hf_affiliation_mgr') and self.hf_affiliation_mgr is not None:
            _dict['hf.AffiliationMgr'] = self.hf_affiliation_mgr
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this IdentityAttrs object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'IdentityAttrs') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'IdentityAttrs') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class MspCryptoField():
    """
    The msp crypto data.

    :attr MspCryptoFieldCa ca: (optional)
    :attr MspCryptoFieldTlsca tlsca:
    :attr MspCryptoFieldComponent component:
    """

    def __init__(self,
                 tlsca: 'MspCryptoFieldTlsca',
                 component: 'MspCryptoFieldComponent',
                 *,
                 ca: 'MspCryptoFieldCa' = None) -> None:
        """
        Initialize a MspCryptoField object.

        :param MspCryptoFieldTlsca tlsca:
        :param MspCryptoFieldComponent component:
        :param MspCryptoFieldCa ca: (optional)
        """
        self.ca = ca
        self.tlsca = tlsca
        self.component = component

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MspCryptoField':
        """Initialize a MspCryptoField object from a json dictionary."""
        args = {}
        if 'ca' in _dict:
            args['ca'] = MspCryptoFieldCa.from_dict(_dict.get('ca'))
        if 'tlsca' in _dict:
            args['tlsca'] = MspCryptoFieldTlsca.from_dict(_dict.get('tlsca'))
        else:
            raise ValueError('Required property \'tlsca\' not present in MspCryptoField JSON')
        if 'component' in _dict:
            args['component'] = MspCryptoFieldComponent.from_dict(_dict.get('component'))
        else:
            raise ValueError('Required property \'component\' not present in MspCryptoField JSON')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MspCryptoField object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'ca') and self.ca is not None:
            _dict['ca'] = self.ca.to_dict()
        if hasattr(self, 'tlsca') and self.tlsca is not None:
            _dict['tlsca'] = self.tlsca.to_dict()
        if hasattr(self, 'component') and self.component is not None:
            _dict['component'] = self.component.to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this MspCryptoField object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'MspCryptoField') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MspCryptoField') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class NodeOu():
    """
    NodeOu.

    :attr bool enabled: (optional) Indicates if node OUs are enabled or not.
    """

    def __init__(self,
                 *,
                 enabled: bool = None) -> None:
        """
        Initialize a NodeOu object.

        :param bool enabled: (optional) Indicates if node OUs are enabled or not.
        """
        self.enabled = enabled

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'NodeOu':
        """Initialize a NodeOu object from a json dictionary."""
        args = {}
        if 'enabled' in _dict:
            args['enabled'] = _dict.get('enabled')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a NodeOu object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'enabled') and self.enabled is not None:
            _dict['enabled'] = self.enabled
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this NodeOu object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'NodeOu') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'NodeOu') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

class NodeOuGeneral():
    """
    NodeOuGeneral.

    :attr bool enabled: (optional) Indicates if node OUs are enabled or not.
          [Available on peer/orderer components w/query parameter 'deployment_attrs'].
    """

    def __init__(self,
                 *,
                 enabled: bool = None) -> None:
        """
        Initialize a NodeOuGeneral object.

        :param bool enabled: (optional) Indicates if node OUs are enabled or not.
               [Available on peer/orderer components w/query parameter
               'deployment_attrs'].
        """
        self.enabled = enabled

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'NodeOuGeneral':
        """Initialize a NodeOuGeneral object from a json dictionary."""
        args = {}
        if 'enabled' in _dict:
            args['enabled'] = _dict.get('enabled')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a NodeOuGeneral object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'enabled') and self.enabled is not None:
            _dict['enabled'] = self.enabled
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this NodeOuGeneral object."""
        return json.dumps(self.to_dict(), indent=2)

    def __eq__(self, other: 'NodeOuGeneral') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'NodeOuGeneral') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other
