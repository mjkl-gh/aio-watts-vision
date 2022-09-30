from aiohttp import ClientSession, ClientResponseaccess_token

from .models import Token

class Auth:
    """Class to make authenticated requests."""
    username: str
    password: str
    session: ClientSession

    _refresh_token: str | None = None
    _expires_in: datetime.datetime | None = None
    access_token: str | None = None

    def __init__(self, session: ClientSession, host: str, access_token: str):
        """Initialize the auth."""
        self.session = websession
        self.host = host
        self.access_token = access_token   

    async def request(self, method: str, path: str, **kwargs) -> ClientResponse:
        """Make a request."""
        
        await self._refresh_token_if_expired()
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        return await self.session.request(
            method, f"{self.host}/{path}", **kwargs, headers=headers,
        )

    async def get(self, path: str) -> Any:
        """Make a GET request to the  API"""
        headers = {}

        await self._refresh_token_if_expired()
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        async with self.session.get(
            f"{self.server.endpoint}{path}",
            headers=headers,
        ) as response:
            await self.check_response(response)
            return await response.json()

    async def post(
        self, path: str, payload: JSON | None = None, data: JSON | None = None
    ) -> Any:
        """Make a POST request to the  API"""
        headers = {}

        if path != "login" and self.access_token:
            await self._refresh_token_if_expired()
            headers["Authorization"] = f"Bearer {self.access_token}"

        async with self.session.post(
            f"{self.server.endpoint}{path}", data=data, json=payload, headers=headers
        ) as response:
            await self.check_response(response)
            return await response.json()

    async def delete(self, path: str) -> None:
        """Make a DELETE request to the  API"""
        headers = {}

        await self._refresh_token_if_expired()

        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        async with self.session.delete(
            f"{self.server.endpoint}{path}", headers=headers
        ) as response:
            await self.check_response(response)

    @staticmethod
    async def check_response(response: ClientResponse):
        return check_response(response)

async def check_response(response: ClientResponse) -> None:
    """Check the response returned by the  API"""
    if response.status in [200, 204]:
        return

    try:
        result = await response.json(content_type=None)
    except JSONDecodeError as error:
        result = await response.text()
        if "Server is down for maintenance" in result:
            raise MaintenanceException("Server is down for maintenance") from error
        raise Exception(
            f"Unknown error while requesting {response.url}. {response.status} - {result}"
        ) from error

    if result.get("errorCode"):
        message = result.get("error")

        # {"errorCode": "AUTHENTICATION_ERROR",
        # "error": "Too many requests, try again later : login with xxx@xxx.tld"}
        if "Too many requests" in message:
            raise TooManyRequestsException(message)

        # {"errorCode": "AUTHENTICATION_ERROR", "error": "Bad credentials"}
        if message == "Bad credentials":
            raise BadCredentialsException(message)

        # {"errorCode": "RESOURCE_ACCESS_DENIED", "error": "Not authenticated"}
        if message == "Not authenticated":
            raise NotAuthenticatedException(message)

        # {"error":"Missing authorization token.","errorCode":"RESOURCE_ACCESS_DENIED"}
        if message == "Missing authorization token.":
            raise MissingAuthorizationTokenException(message)

        # {"error": "Server busy, please try again later. (Too many executions)"}
        if message == "Server busy, please try again later. (Too many executions)":
            raise TooManyExecutionsException(message)

        # {"error": "UNSUPPORTED_OPERATION", "error": "No such command : ..."}
        if "No such command" in message:
            raise InvalidCommandException(message)

        # {"errorCode": "RESOURCE_ACCESS_DENIED",  "error": "too many concurrent requests"}
        if message == "too many concurrent requests":
            raise TooManyConcurrentRequestsException(message)

        if message == "Cannot use JSESSIONID and bearer token in same request":
            raise SessionAndBearerInSameRequestException(message)

        if (
            message
            == "Too many attempts with an invalid token, temporarily banned."
        ):
            raise TooManyAttemptsBannedException(message)

        if "Invalid token : " in message:
            raise InvalidTokenException(message)

        if "Not such token with UUID: " in message:
            raise NotSuchTokenException(message)

        if "Unknown user :" in message:
            raise UnknownUserException(message)

        # {"error":"Unknown object.","errorCode":"UNSPECIFIED_ERROR"}
        if message == "Unknown object.":
            raise UnknownObjectException(message)

        # {'errorCode': 'RESOURCE_ACCESS_DENIED', 'error': 'Access denied to gateway #1234-5678-1234 for action ADD_TOKEN'}
        if "Access denied to gateway" in message:
            raise AccessDeniedToGatewayException(message)

    raise Exception(message if message else result)

async def login(username: str, password: str, url: str, session: ClientSession) -> bool:
    """
    Authenticate and create an API session allowing access to the other operations.
    """
    # Regular authentication using userId+userPassword
    payload = {"userId": username, "userPassword": password,}

    async with session.post(url, json=payload,) as response:
            await self.check_response(response)
            return Auth(session, url, response.json)
    