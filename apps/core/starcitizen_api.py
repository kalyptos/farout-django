"""
Star Citizen API client for fetching ship and organization data.
"""
import requests
import logging
from typing import Dict, List, Optional, Any
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class StarCitizenAPIError(Exception):
    """Exception raised for Star Citizen API errors."""
    pass


class StarCitizenAPIClient:
    """
    Client for interacting with Star Citizen API.

    API Key Format:
    The API key is included in the URL path: /{api_key}/v1/{mode}/{endpoint}
    Example: /0d32404d021613ba948ba0aeef324ef5/v1/cache/ships

    Get your API key at: https://api.starcitizen-api.com or via Discord (/api register)
    """

    BASE_URL = "https://api.starcitizen-api.com"
    CACHE_TIMEOUT = 3600  # 1 hour

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the API client."""
        self.api_key = api_key or getattr(settings, 'STARCITIZEN_API_KEY', None)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Farout-Django/1.0',
            'Accept': 'application/json'
        })

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make a request to the Star Citizen API.

        The API key is included in the URL path: /{api_key}/v1/{mode}/{endpoint}
        """
        # Build URL with API key in path
        if self.api_key:
            url = f"{self.BASE_URL}/{self.api_key}/{endpoint.lstrip('/')}"
        else:
            # Try without API key (may have rate limits)
            url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
            logger.warning("No API key configured - requests may be rate limited")

        try:
            logger.debug(f"Making request to {url} with params {params}")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Check for API error response
            if isinstance(data, dict) and not data.get('success', True):
                error_msg = data.get('message', 'Unknown API error')
                logger.error(f"API returned error: {error_msg}")
                raise StarCitizenAPIError(f"API error: {error_msg}")

            logger.debug(f"Response success: {data.get('success', 'N/A')}")
            return data
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error fetching {url}: {e}")
            raise StarCitizenAPIError(f"HTTP error: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error fetching {url}: {e}")
            raise StarCitizenAPIError(f"Request error: {e}")
        except ValueError as e:
            logger.error(f"JSON decode error for {url}: {e}")
            raise StarCitizenAPIError(f"Invalid JSON response: {e}")

    def get_ships(self) -> List[Dict[str, Any]]:
        """
        Fetch all ships from the API.

        Returns:
            List of ship dictionaries
        """
        cache_key = 'starcitizen_ships_all'
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info("Returning cached ships data")
            return cached_data

        try:
            data = self._make_request('v1/cache/ships')
            ships = data.get('data', [])
            cache.set(cache_key, ships, self.CACHE_TIMEOUT)
            logger.info(f"Fetched {len(ships)} ships from API")
            return ships
        except Exception as e:
            logger.error(f"Error fetching ships: {e}")
            raise StarCitizenAPIError(f"Failed to fetch ships: {e}")

    def get_ship(self, ship_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a specific ship by ID.

        Args:
            ship_id: Ship identifier

        Returns:
            Ship dictionary or None if not found
        """
        cache_key = f'starcitizen_ship_{ship_id}'
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info(f"Returning cached ship data for {ship_id}")
            return cached_data

        try:
            data = self._make_request(f'v1/cache/ships/{ship_id}')
            ship = data.get('data')
            if ship:
                cache.set(cache_key, ship, self.CACHE_TIMEOUT)
            return ship
        except Exception as e:
            logger.error(f"Error fetching ship {ship_id}: {e}")
            return None

    # NOTE: Manufacturers are embedded in ship data, no separate endpoint exists

    def get_organization(self, sid: str) -> Optional[Dict[str, Any]]:
        """
        Fetch organization details.

        Note: This endpoint uses 'live' mode with 'user' endpoint to fetch fresh data from RSI.

        Args:
            sid: Organization SID (e.g., 'FAROUTCORP')

        Returns:
            Organization dictionary or None if not found
        """
        cache_key = f'starcitizen_org_{sid}'
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info(f"Returning cached org data for {sid}")
            return cached_data

        try:
            # Organization data is fetched via the user endpoint in live mode
            data = self._make_request(f'v1/live/user/{sid}')
            org = data.get('data')
            if org:
                cache.set(cache_key, org, self.CACHE_TIMEOUT)
            return org
        except Exception as e:
            logger.error(f"Error fetching organization {sid}: {e}")
            return None

    def get_organization_members(self, sid: str) -> List[Dict[str, Any]]:
        """
        Fetch organization members.

        Note: This endpoint only supports 'live' mode, not 'cache' mode.
        Members are fetched directly from RSI website.

        Args:
            sid: Organization SID (e.g., 'FAROUT')

        Returns:
            List of member dictionaries
        """
        cache_key = f'starcitizen_org_members_{sid}'
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info(f"Returning cached members data for {sid}")
            return cached_data

        try:
            # Organization members only available in 'live' mode
            data = self._make_request(f'v1/live/organization_members/{sid}')
            members = data.get('data', [])
            cache.set(cache_key, members, self.CACHE_TIMEOUT)
            logger.info(f"Fetched {len(members)} members from API for {sid}")
            return members
        except Exception as e:
            logger.error(f"Error fetching members for {sid}: {e}")
            raise StarCitizenAPIError(f"Failed to fetch organization members: {e}")


# Global API client instance
api_client = StarCitizenAPIClient()
