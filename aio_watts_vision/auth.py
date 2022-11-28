from aiohttp import ClientSession, ClientResponse


class Auth:
    """Class to make authenticated requests."""

    def __init__(self, websession: ClientSession, host: str, access_token: str):
        """Initialize the auth."""
        self.websession = websession
        self.host = host
        self.access_token = access_token

    async def request(self, method: str, path: str, **kwargs) -> ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        headers["authorization"] = self.access_token

        return await self.websession.request(
            method, f"{self.host}/{path}", **kwargs, headers=headers,
        )

class Auth():
    def __init__(self, auth_callback=None, session=None,
                 client_id=None, client_secret=None,
                 access_token=None, access_token_cache_file=None):
        self._res = {}
        self.auth_callback = auth_callback
        self.pin = None
        self._access_token_cache_file = access_token_cache_file
        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = access_token

        if (access_token_cache_file is not None and
                access_token is None and
                os.path.exists(access_token_cache_file)):
            with open(access_token_cache_file, 'r') as f:
                _LOGGER.debug("Load access token from %s",
                              access_token_cache_file)
                self._res = json.load(f)
                self._callback(self._res)

        if session is not None:
            session = weakref.ref(session)

        self._session = session
        self._adapter = adapters.HTTPAdapter()

    def _cache(self):
        if self._access_token_cache_file is not None:
            with os.fdopen(os.open(self._access_token_cache_file,
                                   os.O_WRONLY | os.O_CREAT, 0o600),
                           'w') as f:
                _LOGGER.debug("Save access token to %s",
                              self._access_token_cache_file)
                json.dump(self._res, f)

    def _callback(self, res):
        if self.auth_callback is not None and isinstance(self.auth_callback,
                                                         collections.abc.Callable):
            self.auth_callback(res)

    def login(self, headers=None):
        data = {'client_id': self._client_id,
                'client_secret': self._client_secret,
                'code': self.pin,
                'grant_type': 'authorization_code'}

        post = requests.post

        if self._session:
            session = self._session()
            post = session.post

        _LOGGER.debug(">> POST %s", ACCESS_TOKEN_URL)
        response = post(ACCESS_TOKEN_URL, data=data, headers=headers)
        _LOGGER.debug("<< %s", response.status_code)
        if response.status_code != 200:
            raise AuthorizationError(response)
        self._res = response.json()

        self._cache()
        self._callback(self._res)

    @property
    def access_token(self):
        return self._res.get('access_token', self._access_token)

    def __call__(self, r):
        if self.access_token:
            r.headers['Authorization'] = 'Bearer ' + self.access_token

        return r