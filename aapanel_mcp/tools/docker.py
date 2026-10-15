"""Docker management tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response, request_compat

# v8.0.7 v2 routes first, legacy /panel/docker/* routes as fallback
_DOCKER_ROUTES = {
    "list": ["/v2/btdocker/container/get_list", "/panel/docker/get_list"],
    "info": ["/v2/btdocker/container/get_container_info", "/panel/docker/get_container_info"],
    "start": ["/v2/btdocker/container/set_container_status", "/panel/docker/start"],
    "stop": ["/v2/btdocker/container/stop", "/panel/docker/stop"],
    "restart": ["/v2/btdocker/container/restart", "/panel/docker/restart"],
    "images": ["/v2/btdocker/image/image_list", "/panel/docker/image_list"],
    "remove_image": ["/v2/btdocker/image/remove", "/panel/docker/delete_image"],
    "networks": ["/v2/btdocker/network/get_host_network", "/panel/docker/get_host_network"],
    "volumes": ["/v2/btdocker/volume/get_volume_list", "/panel/docker/get_volume_list"],
    "logs": ["/v2/btdocker/container/get_logs", "/panel/docker/get_logs"],
}


def register_docker_tools(mcp: FastMCP) -> None:
    """Register all Docker management tools."""

    @mcp.tool()
    def docker_container_list(server: str = "") -> str:
        """List all Docker containers.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(client, _DOCKER_ROUTES["list"])
        return format_response(data)

    @mcp.tool()
    def docker_container_info(server: str = "", container_id: str = "") -> str:
        """Get detailed information about a Docker container.

        Args:
            server: Server name (optional)
            container_id: Container ID or name
        """
        client = client_manager.get_client(server or None)
        params = {"id": container_id}
        data = request_compat(client, _DOCKER_ROUTES["info"], params)
        return format_response(data)

    @mcp.tool()
    def docker_container_start(server: str = "", container_id: str = "") -> str:
        """Start a Docker container.

        Args:
            server: Server name (optional)
            container_id: Container ID or name
        """
        client = client_manager.get_client(server or None)
        params = {"id": container_id, "status": "start"}
        data = request_compat(client, _DOCKER_ROUTES["start"], params)
        return format_response(data)

    @mcp.tool()
    def docker_container_stop(server: str = "", container_id: str = "", confirmed: bool = False) -> str:
        """Stop a Docker container.

        Args:
            server: Server name (optional)
            container_id: Container ID or name
            confirmed: Must be True to confirm this destructive action
        """
        client = client_manager.get_client(server or None)
        params = {"id": container_id, "status": "stop"}
        data = request_compat(client, _DOCKER_ROUTES["stop"], params, confirmed=confirmed)
        return format_response(data)

    @mcp.tool()
    def docker_container_restart(server: str = "", container_id: str = "") -> str:
        """Restart a Docker container.

        Args:
            server: Server name (optional)
            container_id: Container ID or name
        """
        client = client_manager.get_client(server or None)
        params = {"id": container_id, "status": "restart"}
        data = request_compat(client, _DOCKER_ROUTES["restart"], params)
        return format_response(data)

    @mcp.tool()
    def docker_image_list(server: str = "") -> str:
        """List all Docker images.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(client, _DOCKER_ROUTES["images"])
        return format_response(data)

    @mcp.tool()
    def docker_image_delete(
        server: str = "",
        image_id: str = "",
        name: str = "",
        force: int = 0,
        confirmed: bool = False,
    ) -> str:
        """Delete a Docker image.

        Args:
            server: Server name (optional)
            image_id: Image ID
            name: Image tag name (optional, resolved from image list if omitted)
            force: Force delete (0 or 1)
            confirmed: Must be True to confirm this destructive action
        """
        client = client_manager.get_client(server or None)
        resolved_name = name or image_id
        if image_id and not name and confirmed:
            imgs = request_compat(client, _DOCKER_ROUTES["images"])
            image_rows = imgs.get("message", imgs) if isinstance(imgs, dict) else imgs
            if isinstance(image_rows, list):
                for img in image_rows:
                    if isinstance(img, dict) and (
                        img.get("id") == image_id or str(img.get("id", "")).endswith(image_id)
                    ):
                        resolved_name = img.get("name", resolved_name)
                        break
        params = {"id": image_id, "name": resolved_name, "force": str(force)}
        data = request_compat(client, _DOCKER_ROUTES["remove_image"], params, confirmed=confirmed)
        return format_response(data)

    @mcp.tool()
    def docker_network_list(server: str = "") -> str:
        """List all Docker networks.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(client, _DOCKER_ROUTES["networks"])
        return format_response(data)

    @mcp.tool()
    def docker_volume_list(server: str = "") -> str:
        """List all Docker volumes.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = request_compat(client, _DOCKER_ROUTES["volumes"])
        return format_response(data)

    @mcp.tool()
    def docker_get_logs(server: str = "", container_id: str = "", tail: int = 100) -> str:
        """Get Docker container logs.

        Args:
            server: Server name (optional)
            container_id: Container ID or name
            tail: Number of log lines to retrieve (default 100)
        """
        client = client_manager.get_client(server or None)
        params = {"id": container_id, "tail": tail}
        data = request_compat(client, _DOCKER_ROUTES["logs"], params)
        return format_response(data)
