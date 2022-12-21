from .base import BaseAPIObject
from typing import List



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

class SmarthomeData(Smarthome):
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
    def devices(self) -> List["Device"]:
        """Return the devices of the smarthome."""
        return list(map(Device, self.attributes.get("devices", [])))


    @property
    def general_mode(self) -> bool:
        """Return the general mode of the smarthome."""
        return self.attributes.get("general_mode", None)

    
    @property
    def holiday_end(self) -> int:
        """Return the holiday_end  of the smarthome."""
        return self.attributes.get("holiday_end", None)


    @property
    def holiday_mode(self) -> str:
        """Return the holiday_mode  of the smarthome."""
        return self.attributes.get("holiday_mode", None)


    @property
    def holiday_start(self) -> bool:
        """Return the holiday_start  of the smarthome."""
        return self.attributes.get("holiday_start", None)

    
    @property
    def jet_lag(self) -> int:
        """Return the jet_lag  of the smarthome."""
        return self.attributes.get("jet_lag", None)


    @property
    def mac_address(self) -> str:
        """Return the mac_address  of the smarthome."""
        return self.attributes.get("mac_address", None)


    @property
    def modes(self) -> List["Mode"]:
        """Return the modes of the smarthome."""
        return list(map(Mode, self.attributes.get("modes", [])))


    @property
    def param_c_f(self) -> int:
        """Return the param_c_f  of the smarthome."""
        return self.attributes.get("param_c_f", None)


    @property
    def smarthome_id(self) -> str:
        """Return the id of the smarthome."""
        return self.attributes.get("id", None)


    @property
    def users(self) -> List["User"]:
        """Return the users of the smarthome."""
        return self.attributes.get("users", None)


    @property
    def zones(self) -> List["Zone"]:
        """Return the zones of the smarthome."""
        return self.attributes.get("zones", None)

class Device(BaseAPIObject):
    """Class that represents a device in the Watts Vision API"""

    @property
    def bit_override(self) ->  bool:
        """Return the bit_override of the smarthome."""
        return self.attributes.get("bit_override", None)


    @property
    def bundle_id(self) ->  int:
        """Return the bundle_id of the smarthome."""
        return self.attributes.get("bundle_id", None)


    @property
    def consigne_boost(self) ->  int:
        """Return the consigne_boost of the smarthome."""
        return self.attributes.get("consigne_boost", None)


    @property
    def consigne_confort(self) ->  int:
        """Return the consigne_confort of the smarthome."""
        return self.attributes.get("consigne_confort", None)


    @property
    def consigne_eco(self) ->  int:
        """Return the consigne_eco of the smarthome."""
        return self.attributes.get("consigne_eco", None)


    @property
    def consigne_hg(self) ->  int:
        """Return the consigne_hg of the smarthome."""
        return self.attributes.get("consigne_hg", None)


    @property
    def consigne_manuel(self) ->  int:
        """Return the consigne_manuel of the smarthome."""
        return self.attributes.get("consigne_manuel", None)


    @property
    def error_code(self) ->  int:
        """Return the error_code of the smarthome."""
        return self.attributes.get("error_code", None)


    @property
    def fan_error(self) ->  int:
        """Return the fan_error of the smarthome."""
        return self.attributes.get("fan_error", None)


    @property
    def fan_speed(self) ->  int:
        """Return the fan_speed of the smarthome."""
        return self.attributes.get("fan_speed", None)


    @property
    def gv_mode(self) ->  int:
        """Return the gv_mode of the smarthome."""
        return self.attributes.get("gv_mode", None)


    @property
    def heat_cool(self) ->  bool:
        """Return the heat_cool of the smarthome."""
        return self.attributes.get("heat_cool", None)


    @property
    def heating_up(self) ->  bool:
        """Return the heating_up of the smarthome."""
        return self.attributes.get("heating_up", None)


    @property
    def id(self) ->  str:
        """Return the id of the smarthome."""
        return self.attributes.get("id", None)


    @property
    def id_device(self) ->  str:
        """Return the id_device of the smarthome."""
        return self.attributes.get("id_device", None)


    @property
    def label_interface(self) ->  str:
        """Return the label_interface of the smarthome."""
        return self.attributes.get("label_interface", None)


    @property
    def max_set_point(self) ->  int:
        """Return the max_set_point of the smarthome."""
        return self.attributes.get("max_set_point", None)


    @property
    def min_set_point(self) ->  int:
        """Return the min_set_point of the smarthome."""
        return self.attributes.get("min_set_point", None)


    @property
    def nom_appareil(self) ->  str:
        """Return the nom_appareil of the smarthome."""
        return self.attributes.get("nom_appareil", None)


    @property
    def num_zone(self) ->  int:
        """Return the num_zone of the smarthome."""
        return self.attributes.get("num_zone", None)


    @property
    def nv_mode(self) ->  int:
        """Return the nv_mode of the smarthome."""
        return self.attributes.get("nv_mode", None)


    @property
    def on_off(self) ->  int:
        """Return the on_off of the smarthome."""
        return self.attributes.get("on_off", None)


    @property
    def programme(self) ->  List[int]:
        """Return the programme of the smarthome."""
        return list(map(int, list(self.attributes.get("programme", None))))


    @property
    def puissance_app(self) ->  int:
        """Return the puissance_app of the smarthome."""
        return self.attributes.get("puissance_app", None)


    @property
    def temperature_air(self) ->  int:
        """Return the temperature_air of the smarthome."""
        return self.attributes.get("temperature_air", None)


    @property
    def temperature_sol(self) ->  int:
        """Return the temperature_sol of the smarthome."""
        return self.attributes.get("temperature_sol", None)


    @property
    def time_boost(self) ->  int:
        """Return the time_boost of the smarthome."""
        return self.attributes.get("time_boost", None)



class Zone(BaseAPIObject):
    """Class that represents a Zone in the Watts Vision API"""
    @property
    def devices(self) ->  List["Device"]:
        """Return the devices of the smarthome."""
        return self.attributes.get("devices", None)


    @property
    def label_zone_type(self) ->  str:
        """Return the label_zone_type of the smarthome."""
        return self.attributes.get("label_zone_type", None)


    @property
    def num_zone(self) ->  int:
        """Return the num_zone of the smarthome."""
        return self.attributes.get("num_zone", None)


    @property
    def picto_zone_type(self) ->  str:
        """Return the picto_zone_type of the smarthome."""
        return self.attributes.get("picto_zone_type", None)


    @property
    def zone_img_id(self) ->  int:
        """Return the zone_img_id of the smarthome."""
        return self.attributes.get("zone_img_id", None)


    @property
    def zone_label(self) ->  str:
        """Return the zone_label of the smarthome."""
        return self.attributes.get("zone_label", None)

class Mode(BaseAPIObject):
    @property
    def bundle_id(self) ->  int:
        """Return the bundle_id of the smarthome."""
        return self.attributes.get("bundle_id", None)


    @property
    def nvgv_mode_id(self) ->  int:
        """Return the nvgv_mode_id of the smarthome."""
        return self.attributes.get("nvgv_mode_id", None)


    @property
    def smarthome_id(self) ->  str:
        """Return the smarthome_id of the smarthome."""
        return self.attributes.get("smarthome_id", None)


    @property
    def smarthome_mode_type_id(self) ->  int:
        """Return the smarthome_mode_type_id of the smarthome."""
        return self.attributes.get("smarthome_mode_type_id", None)

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
    def lang_code(self) ->  str:
        """Return the lang_code of the User."""
        return self.attributes.get("lang_code", None)

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
        return self.attributes.get("smarthomes", None)    

        