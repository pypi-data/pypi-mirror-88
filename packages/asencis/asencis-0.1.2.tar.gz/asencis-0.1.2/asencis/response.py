class RequestResult(object):
  """Stores information about a single request and response."""
  # pylint: disable=too-many-instance-attributes

    def __init__(
        self, method, path, query, request_content,
        response_raw, response_content, status_code, response_headers,
        start_time, end_time
      ):
        """
        :param method:
        HTTP VERB/METHOD
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

        self.method = method
        """"GET" or "POST"."""
        self.path = path
        """Path that was queried. Relative to client's domain."""
        self.query = query
        """URL query. ``None`` unless ``method == GET``. *Not* related to :any:`FaunaClient.query`."""
        self.request_content = request_content
        """Request data."""
        self.response_raw = response_raw
        """String value returned by the server."""
        self.response_content = response_content
        """
        Parsed value returned by the server.
        Includes "resource" wrapper dict, or may be an "errors" dict instead.
        In the case of a JSON parse error, this will be None.
        """
        self.status_code = status_code
        """HTTP status code."""
        self.response_headers = response_headers
        """A dictionary of headers with case-insensitive keys."""
        self.start_time = start_time
        """Time the request started."""
        self.end_time = end_time
        """Time the response was received."""

    @property
    def time_taken(self):
        """``end_time - start_time``"""
        return self.end_time - self.start_time
