# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional

# Pip
from requests import get

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ----------------------------------------------------------- class: PublicIp ------------------------------------------------------------ #

class PublicIp:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def ipv4_ipify(cls) -> Optional[str]: # Reliable, but slow(from Europe)
        return cls.__get_url_text('https://api.ipify.org')

    @classmethod
    def ipv4_checkip(cls): # Fast(from Europe) and reliable
        return cls.__get_url_text('https://checkip.amazonaws.com')

    @classmethod
    def ipv4_myip(cls): # Sometimes returns None
        return cls.__get_url_text('http://myip.dnsomatic.com')

    @classmethod
    def ipv6_ident(cls):  # Fast(from Europe) and reliable
        return cls.__get_url_text('https://ident.me')

    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    @staticmethod
    def __get_url_text(url: str) -> Optional[str]:
        res = get(url)

        return res.text.strip() if res and res.text else None


# ---------------------------------------------------------------------------------------------------------------------------------------- #