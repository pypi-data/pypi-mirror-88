# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulp_deb.configuration import Configuration


class PatcheddebAptRemote(object):
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
        'name': 'str',
        'url': 'str',
        'ca_cert': 'str',
        'client_cert': 'str',
        'client_key': 'str',
        'tls_validation': 'bool',
        'proxy_url': 'str',
        'username': 'str',
        'password': 'str',
        'download_concurrency': 'int',
        'policy': 'PolicyEnum',
        'total_timeout': 'float',
        'connect_timeout': 'float',
        'sock_connect_timeout': 'float',
        'sock_read_timeout': 'float',
        'distributions': 'str',
        'components': 'str',
        'architectures': 'str',
        'sync_sources': 'bool',
        'sync_udebs': 'bool',
        'sync_installer': 'bool',
        'gpgkey': 'str',
        'ignore_missing_package_indices': 'bool'
    }

    attribute_map = {
        'name': 'name',
        'url': 'url',
        'ca_cert': 'ca_cert',
        'client_cert': 'client_cert',
        'client_key': 'client_key',
        'tls_validation': 'tls_validation',
        'proxy_url': 'proxy_url',
        'username': 'username',
        'password': 'password',
        'download_concurrency': 'download_concurrency',
        'policy': 'policy',
        'total_timeout': 'total_timeout',
        'connect_timeout': 'connect_timeout',
        'sock_connect_timeout': 'sock_connect_timeout',
        'sock_read_timeout': 'sock_read_timeout',
        'distributions': 'distributions',
        'components': 'components',
        'architectures': 'architectures',
        'sync_sources': 'sync_sources',
        'sync_udebs': 'sync_udebs',
        'sync_installer': 'sync_installer',
        'gpgkey': 'gpgkey',
        'ignore_missing_package_indices': 'ignore_missing_package_indices'
    }

    def __init__(self, name=None, url=None, ca_cert=None, client_cert=None, client_key=None, tls_validation=None, proxy_url=None, username=None, password=None, download_concurrency=None, policy=None, total_timeout=None, connect_timeout=None, sock_connect_timeout=None, sock_read_timeout=None, distributions=None, components=None, architectures=None, sync_sources=None, sync_udebs=None, sync_installer=None, gpgkey=None, ignore_missing_package_indices=None, local_vars_configuration=None):  # noqa: E501
        """PatcheddebAptRemote - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._url = None
        self._ca_cert = None
        self._client_cert = None
        self._client_key = None
        self._tls_validation = None
        self._proxy_url = None
        self._username = None
        self._password = None
        self._download_concurrency = None
        self._policy = None
        self._total_timeout = None
        self._connect_timeout = None
        self._sock_connect_timeout = None
        self._sock_read_timeout = None
        self._distributions = None
        self._components = None
        self._architectures = None
        self._sync_sources = None
        self._sync_udebs = None
        self._sync_installer = None
        self._gpgkey = None
        self._ignore_missing_package_indices = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if url is not None:
            self.url = url
        self.ca_cert = ca_cert
        self.client_cert = client_cert
        self.client_key = client_key
        if tls_validation is not None:
            self.tls_validation = tls_validation
        self.proxy_url = proxy_url
        self.username = username
        self.password = password
        if download_concurrency is not None:
            self.download_concurrency = download_concurrency
        if policy is not None:
            self.policy = policy
        self.total_timeout = total_timeout
        self.connect_timeout = connect_timeout
        self.sock_connect_timeout = sock_connect_timeout
        self.sock_read_timeout = sock_read_timeout
        if distributions is not None:
            self.distributions = distributions
        self.components = components
        self.architectures = architectures
        if sync_sources is not None:
            self.sync_sources = sync_sources
        if sync_udebs is not None:
            self.sync_udebs = sync_udebs
        if sync_installer is not None:
            self.sync_installer = sync_installer
        self.gpgkey = gpgkey
        if ignore_missing_package_indices is not None:
            self.ignore_missing_package_indices = ignore_missing_package_indices

    @property
    def name(self):
        """Gets the name of this PatcheddebAptRemote.  # noqa: E501

        A unique name for this remote.  # noqa: E501

        :return: The name of this PatcheddebAptRemote.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PatcheddebAptRemote.

        A unique name for this remote.  # noqa: E501

        :param name: The name of this PatcheddebAptRemote.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def url(self):
        """Gets the url of this PatcheddebAptRemote.  # noqa: E501

        The URL of an external content source.  # noqa: E501

        :return: The url of this PatcheddebAptRemote.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this PatcheddebAptRemote.

        The URL of an external content source.  # noqa: E501

        :param url: The url of this PatcheddebAptRemote.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def ca_cert(self):
        """Gets the ca_cert of this PatcheddebAptRemote.  # noqa: E501

        A PEM encoded CA certificate used to validate the server certificate presented by the remote server.  # noqa: E501

        :return: The ca_cert of this PatcheddebAptRemote.  # noqa: E501
        :rtype: str
        """
        return self._ca_cert

    @ca_cert.setter
    def ca_cert(self, ca_cert):
        """Sets the ca_cert of this PatcheddebAptRemote.

        A PEM encoded CA certificate used to validate the server certificate presented by the remote server.  # noqa: E501

        :param ca_cert: The ca_cert of this PatcheddebAptRemote.  # noqa: E501
        :type: str
        """

        self._ca_cert = ca_cert

    @property
    def client_cert(self):
        """Gets the client_cert of this PatcheddebAptRemote.  # noqa: E501

        A PEM encoded client certificate used for authentication.  # noqa: E501

        :return: The client_cert of this PatcheddebAptRemote.  # noqa: E501
        :rtype: str
        """
        return self._client_cert

    @client_cert.setter
    def client_cert(self, client_cert):
        """Sets the client_cert of this PatcheddebAptRemote.

        A PEM encoded client certificate used for authentication.  # noqa: E501

        :param client_cert: The client_cert of this PatcheddebAptRemote.  # noqa: E501
        :type: str
        """

        self._client_cert = client_cert

    @property
    def client_key(self):
        """Gets the client_key of this PatcheddebAptRemote.  # noqa: E501

        A PEM encoded private key used for authentication.  # noqa: E501

        :return: The client_key of this PatcheddebAptRemote.  # noqa: E501
        :rtype: str
        """
        return self._client_key

    @client_key.setter
    def client_key(self, client_key):
        """Sets the client_key of this PatcheddebAptRemote.

        A PEM encoded private key used for authentication.  # noqa: E501

        :param client_key: The client_key of this PatcheddebAptRemote.  # noqa: E501
        :type: str
        """

        self._client_key = client_key

    @property
    def tls_validation(self):
        """Gets the tls_validation of this PatcheddebAptRemote.  # noqa: E501

        If True, TLS peer validation must be performed.  # noqa: E501

        :return: The tls_validation of this PatcheddebAptRemote.  # noqa: E501
        :rtype: bool
        """
        return self._tls_validation

    @tls_validation.setter
    def tls_validation(self, tls_validation):
        """Sets the tls_validation of this PatcheddebAptRemote.

        If True, TLS peer validation must be performed.  # noqa: E501

        :param tls_validation: The tls_validation of this PatcheddebAptRemote.  # noqa: E501
        :type: bool
        """

        self._tls_validation = tls_validation

    @property
    def proxy_url(self):
        """Gets the proxy_url of this PatcheddebAptRemote.  # noqa: E501

        The proxy URL. Format: scheme://user:password@host:port  # noqa: E501

        :return: The proxy_url of this PatcheddebAptRemote.  # noqa: E501
        :rtype: str
        """
        return self._proxy_url

    @proxy_url.setter
    def proxy_url(self, proxy_url):
        """Sets the proxy_url of this PatcheddebAptRemote.

        The proxy URL. Format: scheme://user:password@host:port  # noqa: E501

        :param proxy_url: The proxy_url of this PatcheddebAptRemote.  # noqa: E501
        :type: str
        """

        self._proxy_url = proxy_url

    @property
    def username(self):
        """Gets the username of this PatcheddebAptRemote.  # noqa: E501

        The username to be used for authentication when syncing.  # noqa: E501

        :return: The username of this PatcheddebAptRemote.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this PatcheddebAptRemote.

        The username to be used for authentication when syncing.  # noqa: E501

        :param username: The username of this PatcheddebAptRemote.  # noqa: E501
        :type: str
        """

        self._username = username

    @property
    def password(self):
        """Gets the password of this PatcheddebAptRemote.  # noqa: E501

        The password to be used for authentication when syncing.  # noqa: E501

        :return: The password of this PatcheddebAptRemote.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this PatcheddebAptRemote.

        The password to be used for authentication when syncing.  # noqa: E501

        :param password: The password of this PatcheddebAptRemote.  # noqa: E501
        :type: str
        """

        self._password = password

    @property
    def download_concurrency(self):
        """Gets the download_concurrency of this PatcheddebAptRemote.  # noqa: E501

        Total number of simultaneous connections.  # noqa: E501

        :return: The download_concurrency of this PatcheddebAptRemote.  # noqa: E501
        :rtype: int
        """
        return self._download_concurrency

    @download_concurrency.setter
    def download_concurrency(self, download_concurrency):
        """Sets the download_concurrency of this PatcheddebAptRemote.

        Total number of simultaneous connections.  # noqa: E501

        :param download_concurrency: The download_concurrency of this PatcheddebAptRemote.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                download_concurrency is not None and download_concurrency < 1):  # noqa: E501
            raise ValueError("Invalid value for `download_concurrency`, must be a value greater than or equal to `1`")  # noqa: E501

        self._download_concurrency = download_concurrency

    @property
    def policy(self):
        """Gets the policy of this PatcheddebAptRemote.  # noqa: E501

        The policy to use when downloading content. The possible values include: 'immediate', 'on_demand', and 'streamed'. 'immediate' is the default.  # noqa: E501

        :return: The policy of this PatcheddebAptRemote.  # noqa: E501
        :rtype: PolicyEnum
        """
        return self._policy

    @policy.setter
    def policy(self, policy):
        """Sets the policy of this PatcheddebAptRemote.

        The policy to use when downloading content. The possible values include: 'immediate', 'on_demand', and 'streamed'. 'immediate' is the default.  # noqa: E501

        :param policy: The policy of this PatcheddebAptRemote.  # noqa: E501
        :type: PolicyEnum
        """

        self._policy = policy

    @property
    def total_timeout(self):
        """Gets the total_timeout of this PatcheddebAptRemote.  # noqa: E501

        aiohttp.ClientTimeout.total (q.v.) for download-connections.  # noqa: E501

        :return: The total_timeout of this PatcheddebAptRemote.  # noqa: E501
        :rtype: float
        """
        return self._total_timeout

    @total_timeout.setter
    def total_timeout(self, total_timeout):
        """Sets the total_timeout of this PatcheddebAptRemote.

        aiohttp.ClientTimeout.total (q.v.) for download-connections.  # noqa: E501

        :param total_timeout: The total_timeout of this PatcheddebAptRemote.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                total_timeout is not None and total_timeout < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `total_timeout`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._total_timeout = total_timeout

    @property
    def connect_timeout(self):
        """Gets the connect_timeout of this PatcheddebAptRemote.  # noqa: E501

        aiohttp.ClientTimeout.connect (q.v.) for download-connections.  # noqa: E501

        :return: The connect_timeout of this PatcheddebAptRemote.  # noqa: E501
        :rtype: float
        """
        return self._connect_timeout

    @connect_timeout.setter
    def connect_timeout(self, connect_timeout):
        """Sets the connect_timeout of this PatcheddebAptRemote.

        aiohttp.ClientTimeout.connect (q.v.) for download-connections.  # noqa: E501

        :param connect_timeout: The connect_timeout of this PatcheddebAptRemote.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                connect_timeout is not None and connect_timeout < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `connect_timeout`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._connect_timeout = connect_timeout

    @property
    def sock_connect_timeout(self):
        """Gets the sock_connect_timeout of this PatcheddebAptRemote.  # noqa: E501

        aiohttp.ClientTimeout.sock_connect (q.v.) for download-connections.  # noqa: E501

        :return: The sock_connect_timeout of this PatcheddebAptRemote.  # noqa: E501
        :rtype: float
        """
        return self._sock_connect_timeout

    @sock_connect_timeout.setter
    def sock_connect_timeout(self, sock_connect_timeout):
        """Sets the sock_connect_timeout of this PatcheddebAptRemote.

        aiohttp.ClientTimeout.sock_connect (q.v.) for download-connections.  # noqa: E501

        :param sock_connect_timeout: The sock_connect_timeout of this PatcheddebAptRemote.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                sock_connect_timeout is not None and sock_connect_timeout < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `sock_connect_timeout`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._sock_connect_timeout = sock_connect_timeout

    @property
    def sock_read_timeout(self):
        """Gets the sock_read_timeout of this PatcheddebAptRemote.  # noqa: E501

        aiohttp.ClientTimeout.sock_read (q.v.) for download-connections.  # noqa: E501

        :return: The sock_read_timeout of this PatcheddebAptRemote.  # noqa: E501
        :rtype: float
        """
        return self._sock_read_timeout

    @sock_read_timeout.setter
    def sock_read_timeout(self, sock_read_timeout):
        """Sets the sock_read_timeout of this PatcheddebAptRemote.

        aiohttp.ClientTimeout.sock_read (q.v.) for download-connections.  # noqa: E501

        :param sock_read_timeout: The sock_read_timeout of this PatcheddebAptRemote.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                sock_read_timeout is not None and sock_read_timeout < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `sock_read_timeout`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._sock_read_timeout = sock_read_timeout

    @property
    def distributions(self):
        """Gets the distributions of this PatcheddebAptRemote.  # noqa: E501

        Whitespace separated list of distributions to sync. The distribution is the path from the repository root to the \"Release\" file you want to access. This is often, but not always, equal to either the codename or the suite of the release you want to sync. If the repository you are trying to sync uses \"flat repository format\", the distribution must end with a \"/\". Based on \"/etc/apt/sources.list\" syntax.  # noqa: E501

        :return: The distributions of this PatcheddebAptRemote.  # noqa: E501
        :rtype: str
        """
        return self._distributions

    @distributions.setter
    def distributions(self, distributions):
        """Sets the distributions of this PatcheddebAptRemote.

        Whitespace separated list of distributions to sync. The distribution is the path from the repository root to the \"Release\" file you want to access. This is often, but not always, equal to either the codename or the suite of the release you want to sync. If the repository you are trying to sync uses \"flat repository format\", the distribution must end with a \"/\". Based on \"/etc/apt/sources.list\" syntax.  # noqa: E501

        :param distributions: The distributions of this PatcheddebAptRemote.  # noqa: E501
        :type: str
        """

        self._distributions = distributions

    @property
    def components(self):
        """Gets the components of this PatcheddebAptRemote.  # noqa: E501

        Whitespace separatet list of components to sync. If none are supplied, all that are available will be synchronized. Leave blank for repositores using \"flat repository format\".  # noqa: E501

        :return: The components of this PatcheddebAptRemote.  # noqa: E501
        :rtype: str
        """
        return self._components

    @components.setter
    def components(self, components):
        """Sets the components of this PatcheddebAptRemote.

        Whitespace separatet list of components to sync. If none are supplied, all that are available will be synchronized. Leave blank for repositores using \"flat repository format\".  # noqa: E501

        :param components: The components of this PatcheddebAptRemote.  # noqa: E501
        :type: str
        """

        self._components = components

    @property
    def architectures(self):
        """Gets the architectures of this PatcheddebAptRemote.  # noqa: E501

        Whitespace separated list of architectures to sync If none are supplied, all that are available will be synchronized. A list of valid architecture specification strings can be found by running \"dpkg-architecture -L\". A sync will download the intersection of the list of architectures provided via this field and those provided by the relevant \"Release\" file. Architecture=\"all\" is always synchronized and does not need to be provided here.  # noqa: E501

        :return: The architectures of this PatcheddebAptRemote.  # noqa: E501
        :rtype: str
        """
        return self._architectures

    @architectures.setter
    def architectures(self, architectures):
        """Sets the architectures of this PatcheddebAptRemote.

        Whitespace separated list of architectures to sync If none are supplied, all that are available will be synchronized. A list of valid architecture specification strings can be found by running \"dpkg-architecture -L\". A sync will download the intersection of the list of architectures provided via this field and those provided by the relevant \"Release\" file. Architecture=\"all\" is always synchronized and does not need to be provided here.  # noqa: E501

        :param architectures: The architectures of this PatcheddebAptRemote.  # noqa: E501
        :type: str
        """

        self._architectures = architectures

    @property
    def sync_sources(self):
        """Gets the sync_sources of this PatcheddebAptRemote.  # noqa: E501

        Sync source packages  # noqa: E501

        :return: The sync_sources of this PatcheddebAptRemote.  # noqa: E501
        :rtype: bool
        """
        return self._sync_sources

    @sync_sources.setter
    def sync_sources(self, sync_sources):
        """Sets the sync_sources of this PatcheddebAptRemote.

        Sync source packages  # noqa: E501

        :param sync_sources: The sync_sources of this PatcheddebAptRemote.  # noqa: E501
        :type: bool
        """

        self._sync_sources = sync_sources

    @property
    def sync_udebs(self):
        """Gets the sync_udebs of this PatcheddebAptRemote.  # noqa: E501

        Sync installer packages  # noqa: E501

        :return: The sync_udebs of this PatcheddebAptRemote.  # noqa: E501
        :rtype: bool
        """
        return self._sync_udebs

    @sync_udebs.setter
    def sync_udebs(self, sync_udebs):
        """Sets the sync_udebs of this PatcheddebAptRemote.

        Sync installer packages  # noqa: E501

        :param sync_udebs: The sync_udebs of this PatcheddebAptRemote.  # noqa: E501
        :type: bool
        """

        self._sync_udebs = sync_udebs

    @property
    def sync_installer(self):
        """Gets the sync_installer of this PatcheddebAptRemote.  # noqa: E501

        Sync installer files  # noqa: E501

        :return: The sync_installer of this PatcheddebAptRemote.  # noqa: E501
        :rtype: bool
        """
        return self._sync_installer

    @sync_installer.setter
    def sync_installer(self, sync_installer):
        """Sets the sync_installer of this PatcheddebAptRemote.

        Sync installer files  # noqa: E501

        :param sync_installer: The sync_installer of this PatcheddebAptRemote.  # noqa: E501
        :type: bool
        """

        self._sync_installer = sync_installer

    @property
    def gpgkey(self):
        """Gets the gpgkey of this PatcheddebAptRemote.  # noqa: E501

        Gpg public key to verify origin releases against  # noqa: E501

        :return: The gpgkey of this PatcheddebAptRemote.  # noqa: E501
        :rtype: str
        """
        return self._gpgkey

    @gpgkey.setter
    def gpgkey(self, gpgkey):
        """Sets the gpgkey of this PatcheddebAptRemote.

        Gpg public key to verify origin releases against  # noqa: E501

        :param gpgkey: The gpgkey of this PatcheddebAptRemote.  # noqa: E501
        :type: str
        """

        self._gpgkey = gpgkey

    @property
    def ignore_missing_package_indices(self):
        """Gets the ignore_missing_package_indices of this PatcheddebAptRemote.  # noqa: E501

        By default, upstream repositories that declare architectures and corresponding package indices in their Release files without actually publishing them, will fail to synchronize. Set this flag to True to allow the synchronization of such \"partial mirrors\" instead. Alternatively, you could make your remote filter by architectures for which the upstream repository does have indices.  # noqa: E501

        :return: The ignore_missing_package_indices of this PatcheddebAptRemote.  # noqa: E501
        :rtype: bool
        """
        return self._ignore_missing_package_indices

    @ignore_missing_package_indices.setter
    def ignore_missing_package_indices(self, ignore_missing_package_indices):
        """Sets the ignore_missing_package_indices of this PatcheddebAptRemote.

        By default, upstream repositories that declare architectures and corresponding package indices in their Release files without actually publishing them, will fail to synchronize. Set this flag to True to allow the synchronization of such \"partial mirrors\" instead. Alternatively, you could make your remote filter by architectures for which the upstream repository does have indices.  # noqa: E501

        :param ignore_missing_package_indices: The ignore_missing_package_indices of this PatcheddebAptRemote.  # noqa: E501
        :type: bool
        """

        self._ignore_missing_package_indices = ignore_missing_package_indices

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
        if not isinstance(other, PatcheddebAptRemote):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PatcheddebAptRemote):
            return True

        return self.to_dict() != other.to_dict()
