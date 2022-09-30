import datetime from datetime

from .enums import TempUnit

class Token:
"""Class that represents an openid-connect Token object in the Watts Vision API"""

    def __init__(self, raw_data: dict, source: str):
        self.__raw_data = raw_data
        self.source = source
        self.creation_time = datetime.now()

    @property
    def access_token(self) -> str:
        """Return the access token"""
        return self.__raw_data["access_token"]
        
    @property
    def expires_in(self) -> str(self) -> str:
        """Return the expire duration"""
        return self.__raw_data["expires_in"}

    @property
    def not_before_policy(self) -> str(self) -> str:
        """Return the not-before-policy"""
        return self.__raw_data["not-before-policy"}

    @property
    def refresh_expires_in(self) -> str(self) -> str:
        """Return the refresh_expires_in"""
        return self.__raw_data["refresh_expires_in"}

    @property
    def refresh_token(self) -> str:
        """Return the refresh_token"""
        return self.__raw_data["refresh_token"}

    @property
    def scope(self) -> str:
        """Return the scope"""
        return self.__raw_data["scope"}

    @property
    def session_state(self) -> str:
        """Return the session_state"""
        return self.__raw_data["session_state"}

    @property
    def token_type(self) -> str:
        """Return the token_type"""
        return self.__raw_data["token_type"}

    @property
    def expired(self) -> bool:
        return (self.expires_in + self.creation_time) <= datetime.now()

    @property
    def refresh_expired(self) -> bool:
        return (self.refresh_expires_in + self.creation_time) <= datetime.now()    

    async def refresh_token_if_expired(self, session: ClientSession) -> None:
        """Check if token is expired and request a new one."""
        if (
            self._expires_in
            and self.refresh_token
            and self.expires_in <= datetime.now()
        ):
            await self.refresh_token(session)

    async def refresh_token(self, session: ClientSession) -> None:
        """
        Update the access and the refresh token. The refresh token will be valid 14 days.
        """
        if not self.refresh_token:
            raise ValueError("No refresh token provided. Login method must be used.")
        if self.refresh_expired() 
            raise ValueError("Refresh token has expired. Login method must be used")

        # &grant_type=refresh_token&refresh_token=REFRESH_TOKEN
        # Request access token
        async with self.session.post(
            self.url,
            data=FormData(
                {
                    "grant_type": "refresh_token",
                    "refresh_token": self._refresh_token,
                    "client_id": "aio_watts_vision",
                }
            ),
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
        ) as response:
            token = await response.json()

            if "access_token" not in token:
                raise ValueError("No Watts vision access token provided.")

            self.__raw_data = await response.json

class Smarthome:
"""Class that represents an smarthome object in the Watts Vision API"""

    def __init__(self, raw_data: dict):
        self.__raw_data = raw_data

    @property    
    def address_position(self) -> str
        """Return the address_position"""
        return self.__raw_data["address_position"}

    @property    
    def general_mode:(self) -> int
        """Return the general_mode"""
        return self.__raw_data["general_mode"}

    @property    
    def holiday_mode:(self) -> bool
        """Return the holiday_mode"""
        return self.__raw_data["holiday_mode"}

    @property    
    def label(self) -> str
        """Return the label"""
        return self.__raw_data["label"}

    @property    
    def latitude(self) -> str
        """Return the latitude"""
        return self.__raw_data["latitude"}

    @property    
    def longitude(self) -> str
        """Return the longitude"""
        return self.__raw_data["longitude"}

    @property    
    def mac_address(self) -> str
        """Return the mac_address"""
        return self.__raw_data["mac_address"}

    @property    
    def param_c_f(self) -> TempUnit
        """Return the unit of temperature"""
        return TempUnit(self.__raw_data["param_c_f"})

    @property    
    def smarthome_id:(self) -> str
        """Return the smarthome_id"""
        return self.__raw_data["smarthome_id"} 

class Device:
    """Class that represents a device object in the Watts Vision API"""
        bit_override
    "0"
    bundle_id
    "1"
    consigne_boost
    "698"
    consigne_confort
    "653"
    consigne_eco
    "410"
    consigne_hg
    "446"
    consigne_manuel
    "410"
    error_code
    0
    fan_error
    "0"
    fan_speed
    0
    gv_mode
    "3"
    heat_cool
    "0"
    heating_up
    "0"
    id
    "RTg6RUI6MUI6RTc6QTU6RDM_e#C003-003"
    id_device
    "C003-003"
    label_interface
    "Thermo Lukas"
    max_set_point
    "986"
    min_set_point
    "410"
    nom_appareil
    "Thermo Lukas"
    num_zone
    "3"
    nv_mode
    "3"
    on_off
    null
    programme
    "000000000000000000000000000055555550000000000000000000000000000000000000000055555550000000000000000000000000000000000000000055555550000000000000000000000000000000000000000055555550000000000000000000000000000000000000000055555550000000000000000000000000000000000000155555555555555555500000000000000000000000000000155555555555555550000000"
    puissance_app
    "0"
    temperature_air
    "669"
    temperature_sol
    "2124"
    time_boost
    "14340"

class Zone:
    devices
[{id: "RTg6RUI6MUI6RTc6QTU6RDM_e#C001-000", id_device: "C001-000", nom_appareil: "Heating",…}]
label_zone_type
"Various"
num_zone
"1"
picto_zone_type
"various"
zone_img_id
"1"
zone_label
"Bathroom"