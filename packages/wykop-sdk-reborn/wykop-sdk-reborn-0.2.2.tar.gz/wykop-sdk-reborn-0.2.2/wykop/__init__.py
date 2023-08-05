"""Python library for the Wykop API."""
from wykop.api.client import WykopAPI
from wykop.api.exceptions import WykopAPIError
from wykop.utils import get_version

__version__ = get_version()
