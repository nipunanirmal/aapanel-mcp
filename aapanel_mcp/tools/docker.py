"""Docker management tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response


def register_docker_tools(mcp: FastMCP) -> None:
    """Register all Docker management tools."""

    @mcp.tool()
    def docker_container_list(server: str = "") -> str:
        """List all Docker containers.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/panel/docker/get_list")
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
        data = client.request("/panel/docker/get_container_info", params)
        return format_response(data)

    @mcp.tool()
    def docker_container_start(server: str = "", container_id: str = "") -> str:
        """Start a Docker container.

        Args:
            server: Server name (optional)
            container_id: Container ID or name
        """
        client = client_manager.get_client(server or None)
        params = {"id": container_id}
        data = client.request("/panel/docker/start", params)
        return format_response(data)

    @mcp.tool()
    def docker_container_stop(server: str = "", container_id: str = "") -> str:
        """Stop a Docker container.

        Args:
            server: Server name (optional)
            container_id: Container ID or name
        """
        client = client_manager.get_client(server or None)
        params = {"id": container_id}
        data = client.request("/panel/docker/stop", params)
        return format_response(data)

    @mcp.tool()
    def docker_container_restart(server: str = "", container_id: str = "") -> str:
        """Restart a Docker container.

        Args:
            server: Server name (optional)
            container_id: Container ID or name
        """
        client = client_manager.get_client(server or None)
        params = {"id": container_id}
        data = client.request("/panel/docker/restart", params)
        return format_response(data)

    @mcp.tool()
    def docker_image_list(server: str = "") -> str:
        """List all Docker images.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/panel/docker/image_list")
        return format_response(data)

    @mcp.tool()
    def docker_image_delete(server: str = "", image_id: str = "") -> str:
        """Delete a Docker image.

        Args:
            server: Server name (optional)
            image_id: Image ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": image_id}
        data = client.request("/panel/docker/delete_image", params)
        return format_response(data)

    @mcp.tool()
    def docker_network_list(server: str = "") -> str:
        """List all Docker networks.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/panel/docker/get_host_network")
        return format_response(data)

    @mcp.tool()
    def docker_volume_list(server: str = "") -> str:
        """List all Docker volumes.

        Args:
            server: Server name (optional)
        """
        client = client_manager.get_client(server or None)
        data = client.request("/panel/docker/get_volume_list")
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
        data = client.request("/panel/docker/get_logs", params)
        return format_response(data)
