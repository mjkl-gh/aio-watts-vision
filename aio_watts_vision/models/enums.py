from enum import Enum

class Mode(Enum):
    COMFORT = 0
    OFF = 1
    FROST_PROTECTION = 2
    ECO = 3
    BOOST = 4
    AUTO_CONFORT = 8
    AUTO_ECO = 11
    ON = 12
    AUTO = 13
    DISABLED = 14

class Language(Enum):
    FRANCAIS = "fr_FR"
    ENGLISH  = "en_GB"
    DEUTSCH = "de_DE"
    ITALIANO = "it_IT"
    SVENSKA = "sv_SV"
    NEDERLANDS = "nl_NL"
    ESPAÑOL = "es_ES"
    DANSk = "da_DA"
    SUOMEN_KIELI  = "fi_FI"
    NORSK = "no_NO"
    PУССКИЙ = "ru_RU"
    华人 = "zh_ZH"
