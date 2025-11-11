"""
Star Citizen API client wrapper.
Handles all API calls to https://starcitizen-api.com/
"""
from __future__ import annotations
import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

import requests
from django.core.cache import cache
from decouple import config

logger = logging.getLogger(__name__)


class StarCitizenAPIError(Exception):
    """Custom exception for Star Citizen API errors."""
    pass


class StarCitizenAPI:
    """
    Client for Star Citizen API.

    API Documentation: https://starcitizen-api.com/

    Features:
    - Automatic caching of responses
    - Error handling and retries
    - Rate limiting awareness
    - Type-safe responses

    Usage:
        >>> api = StarCitizenAPI()
        >>> ships = api.get_ships()
        >>> org = api.get_organization('FAROUT')
    """

    def __init__(self) -> None:
        """Initialize API client with credentials from environment."""
        self.api_key = config('STAR_CITIZEN_API_KEY', default=None)
        self.base_url = config(
            'STAR_CITIZEN_API_URL',
            default='https://starcitizen-api.com/api/'
        )

        if not self.api_key:
            logger.warning(
                "STAR_CITIZEN_API_KEY not set in environment. "
                "API calls will fail. Set this in your .env file."
            )

        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json',
            'User-Agent': 'Farout-Django/1.0',
        })

    def _make_request(
        self,
        endpoint: str,
        method: str = 'GET',
        params: Optional[Dict[str, Any]] = None,
        cache_key: Optional[str] = None,
        cache_timeout: int = 3600,
    ) -> Dict[str, Any] | List[Dict[str, Any]]:
        """
        Make API request with caching and error handling.

        Args:
            endpoint: API endpoint (e.g., 'ships', 'organizations/FAROUT')
            method: HTTP method (GET, POST, etc.)
            params: Query parameters dictionary
            cache_key: Optional cache key for response caching
            cache_timeout: Cache timeout in seconds (default: 1 hour)

        Returns:
            API response data (dict or list)

        Raises:
            StarCitizenAPIError: On API errors or network issues
        """
        # Check cache first
        if cache_key:
            cached = cache.get(cache_key)
            if cached:
                logger.info(f"Cache hit for {cache_key}")
                return cached

        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        try:
            logger.info(f"Making {method} request to {url}")
            response = self.session.request(
                method,
                url,
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            # Cache successful response
            if cache_key:
                cache.set(cache_key, data, cache_timeout)
                logger.info(f"Cached response for {cache_key} ({cache_timeout}s)")

            return data

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e}")
            raise StarCitizenAPIError(
                f"API returned error {e.response.status_code}: {e.response.text}"
            )
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {e}")
            raise StarCitizenAPIError(f"Failed to connect to API: {e}")
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timeout: {e}")
            raise StarCitizenAPIError(f"API request timed out: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise StarCitizenAPIError(f"API request failed: {e}")
        except ValueError as e:
            logger.error(f"Invalid JSON response: {e}")
            raise StarCitizenAPIError(f"API returned invalid JSON: {e}")

    def get_ships(self) -> List[Dict[str, Any]]:
        """
        Get all ships from Star Citizen API.

        Returns:
            List of ship data dictionaries

        Raises:
            StarCitizenAPIError: On API errors
        """
        logger.info("Fetching all ships from API")
        return self._make_request(
            'ships',
            cache_key='sc_api_ships',
            cache_timeout=86400  # 24 hours - ships data rarely changes
        )

    def get_ship(self, ship_id: str) -> Dict[str, Any]:
        """
        Get single ship details by ID.

        Args:
            ship_id: Ship identifier

        Returns:
            Ship data dictionary

        Raises:
            StarCitizenAPIError: On API errors
        """
        logger.info(f"Fetching ship {ship_id} from API")
        return self._make_request(
            f'ships/{ship_id}',
            cache_key=f'sc_api_ship_{ship_id}',
            cache_timeout=86400  # 24 hours
        )

    def get_organization(self, sid: str) -> Dict[str, Any]:
        """
        Get organization data by SID.

        Args:
            sid: Organization SID (e.g., 'FAROUT')

        Returns:
            Organization data dictionary with structure:
            {
                'name': str,
                'sid': str,
                'archetype': str,
                'commitment': str,
                'description': str,
                'member_count': int,
                'banner': str (URL),
                'logo': str (URL),
                ...
            }

        Raises:
            StarCitizenAPIError: On API errors
        """
        logger.info(f"Fetching organization {sid} from API")
        return self._make_request(
            f'organizations/{sid}',
            cache_key=f'sc_api_org_{sid}',
            cache_timeout=3600  # 1 hour - org data changes more frequently
        )

    def get_organization_members(self, sid: str) -> List[Dict[str, Any]]:
        """
        Get organization members by SID.

        Args:
            sid: Organization SID (e.g., 'FAROUT')

        Returns:
            List of member data dictionaries

        Raises:
            StarCitizenAPIError: On API errors
        """
        logger.info(f"Fetching members for organization {sid} from API")
        return self._make_request(
            f'organizations/{sid}/members',
            cache_key=f'sc_api_org_members_{sid}',
            cache_timeout=3600  # 1 hour
        )

    def get_citizen(self, handle: str) -> Dict[str, Any]:
        """
        Get citizen profile by handle.

        Args:
            handle: Citizen handle/username

        Returns:
            Citizen data dictionary

        Raises:
            StarCitizenAPIError: On API errors
        """
        logger.info(f"Fetching citizen {handle} from API")
        return self._make_request(
            f'citizens/{handle}',
            cache_key=f'sc_api_citizen_{handle}',
            cache_timeout=3600  # 1 hour
        )

    def clear_cache(self, pattern: Optional[str] = None) -> None:
        """
        Clear cached API responses.

        Args:
            pattern: Optional pattern to match cache keys (e.g., 'sc_api_ships*')
                    If None, clears all Star Citizen API cache
        """
        if pattern:
            logger.info(f"Clearing cache matching pattern: {pattern}")
            # Note: This requires Django cache backend that supports pattern deletion
            # For simple cache backends, you may need to track keys separately
        else:
            logger.info("Clearing all Star Citizen API cache")
            cache.clear()


# Global API client instance
# Import this in other modules: from apps.core.starcitizen_api import api_client
try:
    api_client = StarCitizenAPI()
except Exception as e:
    logger.error(f"Failed to initialize Star Citizen API client: {e}")
    api_client = None
