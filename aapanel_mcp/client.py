"""aaPanel API client with authentication and request handling."""

import hashlib
import time
import logging
from typing import Any, Optional
from urllib.parse import urlencode

import httpx

from .config import ServerConfig
from .safety import check_request_safety

logger = logging.getLogger(__name__)


def sign_request(token: str, params: Optional[dict] = None) -> dict:
    """Generate aaPanel API request signature.

    aaPanel uses: request_token = md5(request_time + md5(token))
    """
    if params is None:
        params = {}

    request_time = int(time.time())
    token_md5 = hashlib.md5(token.encode()).hexdigest()
    request_token = hashlib.md5(f"{request_time}{token_md5}".encode()).hexdigest()

    return {
        **params,
        "request_time": request_time,
        "request_token": request_token,
    }


class aaPanelClient:
    """HTTP client for aaPanel API."""

    def __init__(self, server_config: ServerConfig):
        self.config = server_config
        self._client = httpx.Client(
            base_url=server_config.host,
            timeout=httpx.Timeout(
                connect=10.0,
                read=float(server_config.timeout),
                write=10.0,
                pool=5.0,
            ),
            verify=server_config.verify_ssl,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    def request(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        method: str = "POST",
        confirmed: bool = False,
    ) -> dict | list:
        """Send API request to aaPanel.

        Args:
            endpoint: API path (e.g. "/system?action=GetNetWork")
            params: Request parameters
            method: HTTP method (POST is default for aaPanel)
            confirmed: Must be True for destructive operations (delete, stop, uninstall, etc.)

        Returns:
            Parsed JSON response

        Raises:
            SafetyViolation: If the request is permanently blocked by safety rules
            ConfirmationRequired: If a destructive operation lacks confirmation
        """
        # Safety guard: check all requests before sending
        is_safe, message = check_request_safety(endpoint, params, confirmed)
        if not is_safe:
            if message.startswith("BLOCKED"):
                logger.warning("Safety block: %s %s", endpoint, message)
                return {"status": False, "msg": message, "blocked_by_safety": True}
            else:
                logger.info("Safety confirmation required: %s %s", endpoint, message)
                return {"status": False, "msg": message, "confirmation_required": True}

        signed_params = sign_request(self.config.token, params)

        max_retries = 2
        last_error = None

        for attempt in range(max_retries + 1):
            try:
                if method == "POST":
                    response = self._client.post(
                        endpoint,
                        data=urlencode(signed_params),
                    )
                else:
                    response = self._client.get(endpoint, params=signed_params)

                response.raise_for_status()
                data = response.json()

                if isinstance(data, dict) and data.get("status") is False:
                    msg = data.get("msg", "API request failed")
                    logger.warning("aaPanel API error on %s: %s", endpoint, msg)
                    return data

                return data

            except httpx.HTTPStatusError as e:
                # 4xx/5xx are permanent — don't retry, return immediately
                logger.warning("HTTP %d on %s: %s", e.response.status_code, endpoint, e)
                return {
                    "status": False,
                    "msg": f"HTTP {e.response.status_code}: {e}",
                    "endpoint": endpoint,
                    "error_type": "HTTPStatusError",
                }
            except httpx.ConnectError as e:
                last_error = e
                logger.warning("Connect error on %s (attempt %d/%d): %s", endpoint, attempt + 1, max_retries + 1, e)
                if attempt < max_retries:
                    time.sleep(1.0 * (attempt + 1))
            except httpx.TimeoutException as e:
                last_error = e
                logger.warning("Timeout on %s (attempt %d/%d): %s", endpoint, attempt + 1, max_retries + 1, e)
                if attempt < max_retries:
                    time.sleep(1.0 * (attempt + 1))
            except Exception as e:
                last_error = e
                logger.warning("Unexpected error on %s (attempt %d/%d): %s", endpoint, attempt + 1, max_retries + 1, e)
                if attempt < max_retries:
                    time.sleep(1.0 * (attempt + 1))

        error_msg = str(last_error) if last_error else "Unknown error"
        logger.error("All retries exhausted for %s: %s", endpoint, error_msg)
        return {
            "status": False,
            "msg": f"Request failed after {max_retries + 1} attempts: {error_msg}",
            "endpoint": endpoint,
            "error_type": type(last_error).__name__ if last_error else "Unknown",
        }

    def health_check(self) -> bool:
        """Check if the panel is reachable."""
        try:
            data = self.request("/system?action=GetNetWork")
            if isinstance(data, dict) and data.get("status") is False:
                return False
            return True
        except Exception:
            return False

    def close(self):
        """Close the HTTP client."""
        self._client.close()


class aaPanelClientManager:
    """Manages multiple aaPanel clients."""

    def __init__(self):
        self.clients: dict[str, aaPanelClient] = {}
        self.default_server: str = ""

    def init_from_config(self, config) -> None:
        """Initialize clients from MCPConfig."""
        from .config import MCPConfig

        if not isinstance(config, MCPConfig):
            raise TypeError("Expected MCPConfig instance")

        self.default_server = config.default_server
        for name, server_cfg in config.servers.items():
            self.clients[name] = aaPanelClient(server_cfg)

    def get_client(self, server: Optional[str] = None) -> aaPanelClient:
        """Get client by server name, or the default client."""
        if server is None:
            server = self.default_server
        if server not in self.clients:
            raise KeyError(
                f"Server '{server}' not found. Available: {list(self.clients.keys())}"
            )
        return self.clients[server]

    def get_server_names(self) -> list[str]:
        """Get list of configured server names."""
        return list(self.clients.keys())

    def close_all(self):
        """Close all clients."""
        for client in self.clients.values():
            client.close()
        self.clients.clear()


# Global client manager instance
client_manager = aaPanelClientManager()
