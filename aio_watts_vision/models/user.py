from .base import BaseAPIObject
from .enums import Language
from typing import List

class User(BaseAPIObject):
    
    @property
    def email(self) ->  str:
        """Return the email of the User."""
        return self.attributes.get("email", None)

    @property
    def user_id(self) ->  str:
        """Return the user_id of the User."""
        return self.attributes.get("user_id", None)

    @property   
    def lang_code(self) ->  Language:
        """Return the lang_code of the User."""
        return Language(self.attributes.get("lang_code", None))

    @property   
    def cgu_id(self) ->  int:
        """Return the cgu_id of the User."""
        return self.attributes.get("cgu_id", None)\

    @property   
    def optin_stats(self) ->  bool:
        """Return the optin_stats of the User."""
        return self.attributes.get("optin_stats", None)

    @property   
    def smarthomes(self) ->  List["Smarthome"]:
        """Return the smarthomes of the User."""
        return list(Smarthome(x, self.auth) for x in self.attributes.get("smarthomes", None))

class Smarthome(BaseAPIObject):
    """Class that represents a smarthome in the Watts Vision API"""

    @property    
    def label(self) -> str:
        """Return the label of the smarthome."""
        return self.attributes.get("label", None)


    @property
    def latitude(self) -> float:
        """Return the latitude of the smarthome."""
        return self.attributes.get("latitude", None)


    @property
    def longitude(self) -> float:
        """Return the longitude of the smarthome."""
        return self.attributes.get("longitude", None)


    @property
    def address_position(self) -> str:
        """Return the address_position of the smarthome."""
        return self.attributes.get("address_position", None)

    @property
    def general_mode(self) -> bool:
        """Return the general mode of the smarthome."""
        return self.attributes.get("general_mode", None)

    @property
    def holiday_mode(self) -> str:
        """Return the holiday_mode  of the smarthome."""
        return self.attributes.get("holiday_mode", None)

    @property
    def mac_address(self) -> str:
        """Return the mac_address  of the smarthome."""
        return self.attributes.get("mac_address", None)

    @property
    def param_c_f(self) -> int:
        """Return the param_c_f  of the smarthome."""
        return self.attributes.get("param_c_f", None)


    @property
    def smarthome_id(self) -> str:
        """Return the id of the smarthome."""
        return self.attributes.get("smarthome_id", None)