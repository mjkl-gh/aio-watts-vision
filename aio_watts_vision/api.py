import asyncio
from datetime import datetime
import sys

from aiothttp import ClientSession
from aioohttp.client_exceptions import ClientResponseError

API_URL_HOSTNAME = "smarthome.wattselectronics.com"
URL_BASE = f"https://{API_URL_HOSTNAME}/"
API_URL_BASE = URL_BASE + "api/v0.1/"
URL_AUTH = URL_BASE + "auth/realms/watts/protocol/openid-connect/token"

WATTS_VISION_CLIENT_ID = "app-front"

DEFAULT_REQUEST_RETRIES = 4
DEFAULT_TIMEOUT = 10
DEFAULT_TOKEN_EXPIRATION_WINDOW = 5

class Client:
    """Interface class for the Watts Vision API"""

    username: str
    password: str
    setup: Setup | None
    devices: list[Device]
    event_listener_id: str | None
    session: ClientSession

    _refresh_token: str | None = None
    _expires_in: datetime.datetime | None = None
    _access_token: str | None = None

    def __init__(
        self,
        username: str,
        password: str,
        url: str | None = API_URL_BASE,
        token: str | None = None,
        session: ClientSession | None = None,
    ) -> None:
        """
        Constructor
        :param username: the username
        :param password: the password
        :param session: optional ClientSession
        """

        self.username = username
        self.password = password
        self._access_token = token
        self.url = url
        self.setup: Setup | None = None
        self.devices: list[Device] = []
        self.gateways: list[Gateway] = []
        self.event_listener_id: str | None = None

        self.session = session if session else ClientSession()

    async def __aenter__(self) -> Client:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close()

    async def close(self) -> None:
        await self.session.close()

    @backoff.on_exception(
        backoff.expo,
        (NotAuthenticatedException, ServerDisconnectedError),
        max_tries=2,
        on_backoff=relogin,
    )
    async def get_setup(self) -> Setup:

        return setup

    @backoff.on_exception(
        backoff.expo,
        (NotAuthenticatedException, ServerDisconnectedError),
        max_tries=2,
        on_backoff=relogin,
    )
    async def get_diagnostic_data(self) -> JSON:
        """
        Get all data about the connected user setup
            -> gateways data (serial number, activation state, ...): <gateways/gateway>
            -> setup location: <location>
            -> house places (rooms and floors): <place>
            -> setup devices: <devices>
        This data will be masked to not return any confidential or PII data.
        """
        response = await self.__get("setup")

        return obfuscate_sensitive_data(response)

    @backoff.on_exception(
        backoff.expo,
        (NotAuthenticatedException, ServerDisconnectedError),
        max_tries=2,
        on_backoff=relogin,
    )
    async def get_devices(self, refresh: bool = False) -> list[Device]:
        """
        List devices
        Per-session rate-limit : 1 calls per 1d period for this particular operation (bulk-load)
        """
        if self.devices and not refresh:
            return self.devices

        response = await self.__get("setup/devices")
        devices = [Device(**d) for d in humps.decamelize(response)]

        # Cache response
        self.devices = devices
        if self.setup:
            self.setup.devices = devices

        return devices

    @backoff.on_exception(
        backoff.expo,
        (NotAuthenticatedException, ServerDisconnectedError),
        max_tries=2,
        on_backoff=relogin,
    )
    async def get_smarthomes(self, refresh: bool = False) -> list[Smarthome]:
        """
        Get every gateways of a connected user setup
        Per-session rate-limit : 1 calls per 1d period for this particular operation (bulk-load)
        """
        if self.gateways and not refresh:
            return self.gateways

        response = await self.__get("setup/gateways")
        gateways = [Gateway(**g) for g in humps.decamelize(response)]

        # Cache response
        self.gateways = gateways
        if self.setup:
            self.setup.gateways = gateways

        return gateways

    @backoff.on_exception(
        backoff.expo,
        (NotAuthenticatedException, ServerDisconnectedError),
        max_tries=2,
        on_backoff=relogin,
    )
    async def get_execution_history(self) -> list[HistoryExecution]:
        """
        List execution history
        """
        response = await self.__get("history/executions")
        execution_history = [HistoryExecution(**h) for h in humps.decamelize(response)]

        return execution_history

    @backoff.on_exception(
        backoff.expo, NotAuthenticatedException, max_tries=2, on_backoff=relogin
    )
    async def get_device_definition(self, deviceurl: str) -> JSON | None:
        """
        Retrieve a particular setup device definition
        """
        response: dict = await self.__get(
            f"setup/devices/{urllib.parse.quote_plus(deviceurl)}"
        )

        return response.get("definition")

    @backoff.on_exception(
        backoff.expo, NotAuthenticatedException, max_tries=2, on_backoff=relogin
    )
    async def get_state(self, deviceurl: str) -> list[State]:
        """
        Retrieve states of requested device
        """
        response = await self.__get(
            f"setup/devices/{urllib.parse.quote_plus(deviceurl)}/states"
        )
        state = [State(**s) for s in humps.decamelize(response)]

        return state

    @backoff.on_exception(
        backoff.expo, NotAuthenticatedException, max_tries=2, on_backoff=relogin
    )
    async def refresh_states(self) -> None:
        """
        Ask the box to refresh all devices states for protocols supporting that operation
        """
        await self.__post("setup/devices/states/refresh")

    @backoff.on_exception(
        backoff.expo, NotAuthenticatedException, max_tries=2, on_backoff=relogin
    )
    async def get_current_execution(self, exec_id: str) -> Execution:
        """Get an action group execution currently running"""
        response = await self.__get(f"exec/current/{exec_id}")
        execution = Execution(**humps.decamelize(response))

        return execution

    @backoff.on_exception(
        backoff.expo, NotAuthenticatedException, max_tries=2, on_backoff=relogin
    )
    async def get_current_executions(self) -> list[Execution]:
        """Get all action groups executions currently running"""
        response = await self.__get("exec/current")
        executions = [Execution(**e) for e in humps.decamelize(response)]

        return executions

    @backoff.on_exception(
        backoff.expo, NotAuthenticatedException, max_tries=2, on_backoff=relogin
    )
    async def get_api_version(self) -> str:
        """Get the API version (local only)"""
        response = await self.__get("apiVersion")

        return cast(str, response["protocolVersion"])

    @backoff.on_exception(backoff.expo, TooManyExecutionsException, max_tries=10)
    @backoff.on_exception(
        backoff.expo, NotAuthenticatedException, max_tries=2, on_backoff=relogin
    )
    async def execute_command(
        self,
        device_url: str,
        command: Command | str,
        label: str | None = "python--api",
    ) -> str:
        """Send a command"""
        if isinstance(command, str):
            command = Command(command)

        response: str = await self.execute_commands(device_url, [command], label)

        return response

    @backoff.on_exception(
        backoff.expo, NotAuthenticatedException, max_tries=2, on_backoff=relogin
    )
    async def cancel_command(self, exec_id: str) -> None:
        """Cancel a running setup-level execution"""
        await self.__delete(f"/exec/current/setup/{exec_id}")

    @backoff.on_exception(
        backoff.expo, NotAuthenticatedException, max_tries=2, on_backoff=relogin
    )
    async def execute_commands(
        self,
        device_url: str,
        commands: list[Command],
        label: str | None = "python--api",
    ) -> str:
        """Send several commands in one call"""
        payload = {
            "label": label,
            "actions": [{"deviceURL": device_url, "commands": commands}],
        }
        response: dict = await self.__post("exec/apply", payload)
        return cast(str, response["execId"])

    @backoff.on_exception(
        backoff.expo,
        (NotAuthenticatedException, ServerDisconnectedError),
        max_tries=2,
        on_backoff=relogin,
    )
    async def get_scenarios(self) -> list[Scenario]:
        """List the scenarios"""
        response = await self.__get("actionGroups")
        return [Scenario(**scenario) for scenario in response]

    @backoff.on_exception(
        backoff.expo,
        (NotAuthenticatedException, ServerDisconnectedError),
        max_tries=2,
        on_backoff=relogin,
    )
    async def get_places(self) -> Place:
        """List the places"""
        response = await self.__get("setup/places")
        places = Place(**humps.decamelize(response))
        return places

    @backoff.on_exception(
        backoff.expo,
        (NotAuthenticatedException, ServerDisconnectedError),
        max_tries=2,
        on_backoff=relogin,
    )
    async def generate_local_token(self, gateway_id: str) -> str:
        """
        Generates a new token
        Access scope : Full enduser API access (enduser/*)
        """
        response = await self.__get(f"config/{gateway_id}/local/tokens/generate")

        return cast(str, response["token"])

    @backoff.on_exception(
        backoff.expo,
        (NotAuthenticatedException, ServerDisconnectedError),
        max_tries=2,
        on_backoff=relogin,
    )
    async def activate_local_token(
        self, gateway_id: str, token: str, label: str, scope: str = "devmode"
    ) -> str:
        """
        Create a token
        Access scope : Full enduser API access (enduser/*)
        """
        response = await self.__post(
            f"config/{gateway_id}/local/tokens",
            {"label": label, "token": token, "scope": scope},
        )

        return cast(str, response["requestId"])

    @backoff.on_exception(
        backoff.expo,
        (NotAuthenticatedException, ServerDisconnectedError),
        max_tries=2,
        on_backoff=relogin,
    )
    async def get_local_tokens(
        self, gateway_id: str, scope: str = "devmode"
    ) -> list[LocalToken]:
        """
        Get all gateway tokens with the given scope
        Access scope : Full enduser API access (enduser/*)
        """
        response = await self.__get(f"config/{gateway_id}/local/tokens/{scope}")
        local_tokens = [LocalToken(**lt) for lt in humps.decamelize(response)]

        return local_tokens

    @backoff.on_exception(
        backoff.expo,
        (NotAuthenticatedException, ServerDisconnectedError),
        max_tries=2,
        on_backoff=relogin,
    )
    async def delete_local_token(self, gateway_id: str, uuid: str) -> bool:
        """
        Delete a token
        Access scope : Full enduser API access (enduser/*)
        """
        await self.__delete(f"config/{gateway_id}/local/tokens/{uuid}")

        return True

    @backoff.on_exception(
        backoff.expo, NotAuthenticatedException, max_tries=2, on_backoff=relogin
    )
    async def execute_scenario(self, oid: str) -> str:
        """Execute a scenario"""
        response = await self.__post(f"exec/{oid}")
        return cast(str, response["execId"])

