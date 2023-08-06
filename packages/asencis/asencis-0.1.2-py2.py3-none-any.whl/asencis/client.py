import sys

try:
    import requests
except ImportError:
    requests = None
else:
    try:
        # Require version 0.8.8, but don't want to depend on distutils
        version = requests.__version__
        major, minor, patch = [int(i) for i in version.split(".")]
    except Exception:
        # Probably some new-fangled version, so it should support verify
        pass
    else:
        if (major, minor, patch) < (2, 24, 0):
            sys.stderr.write(
                "Warning: the asencis library requires that your Python "
                '"requests" library be newer than version 2.24.0, but your '
                '"requests" library is version %s. asencis will fall back to '
                "an alternate HTTP library so everything should work. We "
                'recommend upgrading your "requests" library. If you have any '
                "questions, please contact support@stripe.com. (HINT: running "
                '"pip install -U requests" should upgrade your requests '
                "library to the latest version.)" % (version,)
            )
            requests = None

# from requests import Request, Session
# from requests.auth import HTTPBasicAuth
# from requests.adapters import HTTPAdapter

API_VERSION = "1"

class RequestsHTTPClient(object):
    pass

class AsencisAPIClient(RequestsHTTPClient):
    # pylint: disable=too-many-arguments, too-many-instance-attributes
    def __init__(
        self,
        domain="api.asencis.com",
        scheme="https",
        port=None,
        timeout=60,
        observer=None,
        pool_connections=10,
        pool_maxsize=10,
        **kwargs
    ):
        """
        :param secret:
            Auth token for the asencis API server.
        :param domain:
            Base URL for the asencis API server.
        :param scheme:
            ``"http"`` or ``"https"``.
        :param port:
            Port of the asencis API server.
        :param timeout:
            Read timeout in seconds.
        :param observer:
            Callback that will be passed a :any:`RequestResult` after every completed request.
        :param pool_connections:
            The number of connection pools to cache.
        :param pool_maxsize:
            The maximum number of connections to save in the pool.
        """

        self.domain = domain
        self.scheme = scheme
        self.port = (443 if scheme == "https" else 8983) if port is None else port
        self.base_url = "{}://{}/v{}".format(self.scheme, self.domain, API_VERSION)
        self.observer = observer
        self.pool_connections = pool_connections
        self.pool_maxsize = pool_maxsize

        # Optional Parameters
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.api_key = kwargs.get('api_key', None)

        # API Realm & Resources
        self.realm = kwargs.get('realm', None)
        self.resource = kwargs.get('resource', None)

        if ('session' not in kwargs):
            self.session = requests.Session()

            self.session.mount(
                'https://',
                requests.adapters.HTTPAdapter(
                    pool_connections=self.pool_connections,
                    pool_maxsize=self.pool_maxsize
                )
            )

            self.session.headers.update({
                "Accept-Encoding": "gzip",
                "Content-Type": "application/json;charset=utf-8",
                "X-asencis-Driver": "python",
                "X-asencis-API-Version": API_VERSION
            })

            self.session.timeout = timeout

        else:
            self.session = kwargs['session']

        super(AsencisAPIClient, self).__init__()

    def _perform_request(self, action, path, data, query, headers):
        """Performs an HTTP action."""
        url = self.base_url + "/" + path
        req = requests.Request(action, url, params=query, data=data, headers=headers)
        return self.session.send(self.session.prepare_request(req))

    def _perform_query(self, action, path, data, query, headers):
        return None
