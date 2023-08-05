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

from pulpcore.client.pulp_python.configuration import Configuration


class PatchedpythonPythonRemote(object):
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
        'includes': 'object',
        'excludes': 'object',
        'prereleases': 'bool'
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
        'includes': 'includes',
        'excludes': 'excludes',
        'prereleases': 'prereleases'
    }

    def __init__(self, name=None, url=None, ca_cert=None, client_cert=None, client_key=None, tls_validation=None, proxy_url=None, username=None, password=None, download_concurrency=None, policy=None, total_timeout=None, connect_timeout=None, sock_connect_timeout=None, sock_read_timeout=None, includes=None, excludes=None, prereleases=None, local_vars_configuration=None):  # noqa: E501
        """PatchedpythonPythonRemote - a model defined in OpenAPI"""  # noqa: E501
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
        self._includes = None
        self._excludes = None
        self._prereleases = None
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
        if includes is not None:
            self.includes = includes
        if excludes is not None:
            self.excludes = excludes
        if prereleases is not None:
            self.prereleases = prereleases

    @property
    def name(self):
        """Gets the name of this PatchedpythonPythonRemote.  # noqa: E501

        A unique name for this remote.  # noqa: E501

        :return: The name of this PatchedpythonPythonRemote.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PatchedpythonPythonRemote.

        A unique name for this remote.  # noqa: E501

        :param name: The name of this PatchedpythonPythonRemote.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def url(self):
        """Gets the url of this PatchedpythonPythonRemote.  # noqa: E501

        The URL of an external content source.  # noqa: E501

        :return: The url of this PatchedpythonPythonRemote.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this PatchedpythonPythonRemote.

        The URL of an external content source.  # noqa: E501

        :param url: The url of this PatchedpythonPythonRemote.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def ca_cert(self):
        """Gets the ca_cert of this PatchedpythonPythonRemote.  # noqa: E501

        A PEM encoded CA certificate used to validate the server certificate presented by the remote server.  # noqa: E501

        :return: The ca_cert of this PatchedpythonPythonRemote.  # noqa: E501
        :rtype: str
        """
        return self._ca_cert

    @ca_cert.setter
    def ca_cert(self, ca_cert):
        """Sets the ca_cert of this PatchedpythonPythonRemote.

        A PEM encoded CA certificate used to validate the server certificate presented by the remote server.  # noqa: E501

        :param ca_cert: The ca_cert of this PatchedpythonPythonRemote.  # noqa: E501
        :type: str
        """

        self._ca_cert = ca_cert

    @property
    def client_cert(self):
        """Gets the client_cert of this PatchedpythonPythonRemote.  # noqa: E501

        A PEM encoded client certificate used for authentication.  # noqa: E501

        :return: The client_cert of this PatchedpythonPythonRemote.  # noqa: E501
        :rtype: str
        """
        return self._client_cert

    @client_cert.setter
    def client_cert(self, client_cert):
        """Sets the client_cert of this PatchedpythonPythonRemote.

        A PEM encoded client certificate used for authentication.  # noqa: E501

        :param client_cert: The client_cert of this PatchedpythonPythonRemote.  # noqa: E501
        :type: str
        """

        self._client_cert = client_cert

    @property
    def client_key(self):
        """Gets the client_key of this PatchedpythonPythonRemote.  # noqa: E501

        A PEM encoded private key used for authentication.  # noqa: E501

        :return: The client_key of this PatchedpythonPythonRemote.  # noqa: E501
        :rtype: str
        """
        return self._client_key

    @client_key.setter
    def client_key(self, client_key):
        """Sets the client_key of this PatchedpythonPythonRemote.

        A PEM encoded private key used for authentication.  # noqa: E501

        :param client_key: The client_key of this PatchedpythonPythonRemote.  # noqa: E501
        :type: str
        """

        self._client_key = client_key

    @property
    def tls_validation(self):
        """Gets the tls_validation of this PatchedpythonPythonRemote.  # noqa: E501

        If True, TLS peer validation must be performed.  # noqa: E501

        :return: The tls_validation of this PatchedpythonPythonRemote.  # noqa: E501
        :rtype: bool
        """
        return self._tls_validation

    @tls_validation.setter
    def tls_validation(self, tls_validation):
        """Sets the tls_validation of this PatchedpythonPythonRemote.

        If True, TLS peer validation must be performed.  # noqa: E501

        :param tls_validation: The tls_validation of this PatchedpythonPythonRemote.  # noqa: E501
        :type: bool
        """

        self._tls_validation = tls_validation

    @property
    def proxy_url(self):
        """Gets the proxy_url of this PatchedpythonPythonRemote.  # noqa: E501

        The proxy URL. Format: scheme://user:password@host:port  # noqa: E501

        :return: The proxy_url of this PatchedpythonPythonRemote.  # noqa: E501
        :rtype: str
        """
        return self._proxy_url

    @proxy_url.setter
    def proxy_url(self, proxy_url):
        """Sets the proxy_url of this PatchedpythonPythonRemote.

        The proxy URL. Format: scheme://user:password@host:port  # noqa: E501

        :param proxy_url: The proxy_url of this PatchedpythonPythonRemote.  # noqa: E501
        :type: str
        """

        self._proxy_url = proxy_url

    @property
    def username(self):
        """Gets the username of this PatchedpythonPythonRemote.  # noqa: E501

        The username to be used for authentication when syncing.  # noqa: E501

        :return: The username of this PatchedpythonPythonRemote.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this PatchedpythonPythonRemote.

        The username to be used for authentication when syncing.  # noqa: E501

        :param username: The username of this PatchedpythonPythonRemote.  # noqa: E501
        :type: str
        """

        self._username = username

    @property
    def password(self):
        """Gets the password of this PatchedpythonPythonRemote.  # noqa: E501

        The password to be used for authentication when syncing.  # noqa: E501

        :return: The password of this PatchedpythonPythonRemote.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this PatchedpythonPythonRemote.

        The password to be used for authentication when syncing.  # noqa: E501

        :param password: The password of this PatchedpythonPythonRemote.  # noqa: E501
        :type: str
        """

        self._password = password

    @property
    def download_concurrency(self):
        """Gets the download_concurrency of this PatchedpythonPythonRemote.  # noqa: E501

        Total number of simultaneous connections.  # noqa: E501

        :return: The download_concurrency of this PatchedpythonPythonRemote.  # noqa: E501
        :rtype: int
        """
        return self._download_concurrency

    @download_concurrency.setter
    def download_concurrency(self, download_concurrency):
        """Sets the download_concurrency of this PatchedpythonPythonRemote.

        Total number of simultaneous connections.  # noqa: E501

        :param download_concurrency: The download_concurrency of this PatchedpythonPythonRemote.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                download_concurrency is not None and download_concurrency < 1):  # noqa: E501
            raise ValueError("Invalid value for `download_concurrency`, must be a value greater than or equal to `1`")  # noqa: E501

        self._download_concurrency = download_concurrency

    @property
    def policy(self):
        """Gets the policy of this PatchedpythonPythonRemote.  # noqa: E501

        The policy to use when downloading content. The possible values include: 'immediate', 'on_demand', and 'cache_only'. 'immediate' is the default.  # noqa: E501

        :return: The policy of this PatchedpythonPythonRemote.  # noqa: E501
        :rtype: PolicyEnum
        """
        return self._policy

    @policy.setter
    def policy(self, policy):
        """Sets the policy of this PatchedpythonPythonRemote.

        The policy to use when downloading content. The possible values include: 'immediate', 'on_demand', and 'cache_only'. 'immediate' is the default.  # noqa: E501

        :param policy: The policy of this PatchedpythonPythonRemote.  # noqa: E501
        :type: PolicyEnum
        """

        self._policy = policy

    @property
    def total_timeout(self):
        """Gets the total_timeout of this PatchedpythonPythonRemote.  # noqa: E501

        aiohttp.ClientTimeout.total (q.v.) for download-connections.  # noqa: E501

        :return: The total_timeout of this PatchedpythonPythonRemote.  # noqa: E501
        :rtype: float
        """
        return self._total_timeout

    @total_timeout.setter
    def total_timeout(self, total_timeout):
        """Sets the total_timeout of this PatchedpythonPythonRemote.

        aiohttp.ClientTimeout.total (q.v.) for download-connections.  # noqa: E501

        :param total_timeout: The total_timeout of this PatchedpythonPythonRemote.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                total_timeout is not None and total_timeout < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `total_timeout`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._total_timeout = total_timeout

    @property
    def connect_timeout(self):
        """Gets the connect_timeout of this PatchedpythonPythonRemote.  # noqa: E501

        aiohttp.ClientTimeout.connect (q.v.) for download-connections.  # noqa: E501

        :return: The connect_timeout of this PatchedpythonPythonRemote.  # noqa: E501
        :rtype: float
        """
        return self._connect_timeout

    @connect_timeout.setter
    def connect_timeout(self, connect_timeout):
        """Sets the connect_timeout of this PatchedpythonPythonRemote.

        aiohttp.ClientTimeout.connect (q.v.) for download-connections.  # noqa: E501

        :param connect_timeout: The connect_timeout of this PatchedpythonPythonRemote.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                connect_timeout is not None and connect_timeout < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `connect_timeout`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._connect_timeout = connect_timeout

    @property
    def sock_connect_timeout(self):
        """Gets the sock_connect_timeout of this PatchedpythonPythonRemote.  # noqa: E501

        aiohttp.ClientTimeout.sock_connect (q.v.) for download-connections.  # noqa: E501

        :return: The sock_connect_timeout of this PatchedpythonPythonRemote.  # noqa: E501
        :rtype: float
        """
        return self._sock_connect_timeout

    @sock_connect_timeout.setter
    def sock_connect_timeout(self, sock_connect_timeout):
        """Sets the sock_connect_timeout of this PatchedpythonPythonRemote.

        aiohttp.ClientTimeout.sock_connect (q.v.) for download-connections.  # noqa: E501

        :param sock_connect_timeout: The sock_connect_timeout of this PatchedpythonPythonRemote.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                sock_connect_timeout is not None and sock_connect_timeout < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `sock_connect_timeout`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._sock_connect_timeout = sock_connect_timeout

    @property
    def sock_read_timeout(self):
        """Gets the sock_read_timeout of this PatchedpythonPythonRemote.  # noqa: E501

        aiohttp.ClientTimeout.sock_read (q.v.) for download-connections.  # noqa: E501

        :return: The sock_read_timeout of this PatchedpythonPythonRemote.  # noqa: E501
        :rtype: float
        """
        return self._sock_read_timeout

    @sock_read_timeout.setter
    def sock_read_timeout(self, sock_read_timeout):
        """Sets the sock_read_timeout of this PatchedpythonPythonRemote.

        aiohttp.ClientTimeout.sock_read (q.v.) for download-connections.  # noqa: E501

        :param sock_read_timeout: The sock_read_timeout of this PatchedpythonPythonRemote.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                sock_read_timeout is not None and sock_read_timeout < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `sock_read_timeout`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._sock_read_timeout = sock_read_timeout

    @property
    def includes(self):
        """Gets the includes of this PatchedpythonPythonRemote.  # noqa: E501

        A JSON list containing project specifiers for Python packages to include.  # noqa: E501

        :return: The includes of this PatchedpythonPythonRemote.  # noqa: E501
        :rtype: object
        """
        return self._includes

    @includes.setter
    def includes(self, includes):
        """Sets the includes of this PatchedpythonPythonRemote.

        A JSON list containing project specifiers for Python packages to include.  # noqa: E501

        :param includes: The includes of this PatchedpythonPythonRemote.  # noqa: E501
        :type: object
        """

        self._includes = includes

    @property
    def excludes(self):
        """Gets the excludes of this PatchedpythonPythonRemote.  # noqa: E501

        A JSON list containing project specifiers for Python packages to exclude.  # noqa: E501

        :return: The excludes of this PatchedpythonPythonRemote.  # noqa: E501
        :rtype: object
        """
        return self._excludes

    @excludes.setter
    def excludes(self, excludes):
        """Sets the excludes of this PatchedpythonPythonRemote.

        A JSON list containing project specifiers for Python packages to exclude.  # noqa: E501

        :param excludes: The excludes of this PatchedpythonPythonRemote.  # noqa: E501
        :type: object
        """

        self._excludes = excludes

    @property
    def prereleases(self):
        """Gets the prereleases of this PatchedpythonPythonRemote.  # noqa: E501

        Whether or not to include pre-release packages in the sync.  # noqa: E501

        :return: The prereleases of this PatchedpythonPythonRemote.  # noqa: E501
        :rtype: bool
        """
        return self._prereleases

    @prereleases.setter
    def prereleases(self, prereleases):
        """Sets the prereleases of this PatchedpythonPythonRemote.

        Whether or not to include pre-release packages in the sync.  # noqa: E501

        :param prereleases: The prereleases of this PatchedpythonPythonRemote.  # noqa: E501
        :type: bool
        """

        self._prereleases = prereleases

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
        if not isinstance(other, PatchedpythonPythonRemote):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PatchedpythonPythonRemote):
            return True

        return self.to_dict() != other.to_dict()
