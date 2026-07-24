"""Project management tools for aaPanel MCP server.

Supports Java, Node, Go, Python, .NET, Proxy, HTML, and Other project types.
"""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response

# Project type to endpoint mapping
PROJECT_ENDPOINTS = {
    "Java": "/mod/java/project/project_list",
    "Node": "/project/nodejs/get_project_list",
    "Go": "/project/go/get_project_list",
    "Python": "/project/python/GetProjectList",
    "net": "/project/net/get_project_list",
    "Proxy": "/mod/proxy/com/get_list",
    "HTML": "/project/html/get_project_list",
    "Other": "/project/other/get_project_list",
}


def register_project_tools(mcp: FastMCP) -> None:
    """Register all project management tools."""

    @mcp.tool()
    def project_list(
        server: str = "",
        project_type: str = "",
        page: int = 1,
        limit: int = 100,
    ) -> str:
        """List projects by type (Java, Node, Go, Python, net, Proxy, HTML, Other).

        Args:
            server: Server name (optional)
            project_type: Project type (Java/Node/Go/Python/net/Proxy/HTML/Other)
            page: Page number (default 1)
            limit: Items per page (default 100)
        """
        if not project_type:
            # Return all project types
            client = client_manager.get_client(server or None)
            results = {}
            for ptype, endpoint in PROJECT_ENDPOINTS.items():
                try:
                    params = {"search": "", "p": page, "limit": limit, "type_id": ""}
                    data = client.request(endpoint, params)
                    results[ptype] = data
                except Exception as e:
                    results[ptype] = {"error": str(e)}
            return format_response(results)

        if project_type not in PROJECT_ENDPOINTS:
            return f"Error: Unsupported project type '{project_type}'. Supported: {list(PROJECT_ENDPOINTS.keys())}"

        client = client_manager.get_client(server or None)
        params = {"search": "", "p": page, "limit": limit, "type_id": ""}
        data = client.request(PROJECT_ENDPOINTS[project_type], params)
        return format_response(data)

    @mcp.tool()
    def project_create(
        server: str = "",
        project_type: str = "",
        name: str = "",
        path: str = "",
        version: str = "",
        port: str = "",
        run_cmd: str = "",
    ) -> str:
        """Create a new project (Java/Node/Go/Python/net/Proxy/HTML).

        Args:
            server: Server name (optional)
            project_type: Project type (Java/Node/Go/Python/net/Proxy/HTML)
            name: Project name
            path: Project directory path
            version: Runtime version (e.g. node 18, python 3.10)
            port: Project port
            run_cmd: Run command (for some project types)
        """
        client = client_manager.get_client(server or None)
        params = {
            "name": name,
            "path": path,
            "version": version,
            "port": port,
            "run_cmd": run_cmd,
        }

        type_endpoints = {
            "Node": "/project/nodejs/add_project",
            "Go": "/project/go/add_project",
            "Python": "/project/python/AddProject",
            "net": "/project/net/add_project",
            "HTML": "/project/html/add_project",
            "Java": "/mod/java/project/add_project",
            "Proxy": "/mod/proxy/com/add_proxy",
        }

        endpoint = type_endpoints.get(project_type)
        if not endpoint:
            return f"Error: Cannot create project of type '{project_type}'"

        data = client.request(endpoint, params)
        return format_response(data)

    @mcp.tool()
    def project_delete(
        server: str = "",
        project_type: str = "",
        id: str = "",
    ) -> str:
        """Delete a project.

        Args:
            server: Server name (optional)
            project_type: Project type (Java/Node/Go/Python/net/Proxy/HTML)
            id: Project ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}

        type_endpoints = {
            "Node": "/project/nodejs/del_project",
            "Go": "/project/go/del_project",
            "Python": "/project/python/DelProject",
            "net": "/project/net/del_project",
            "HTML": "/project/html/del_project",
            "Java": "/mod/java/project/del_project",
            "Proxy": "/mod/proxy/com/del_proxy",
        }

        endpoint = type_endpoints.get(project_type)
        if not endpoint:
            return f"Error: Cannot delete project of type '{project_type}'"

        data = client.request(endpoint, params)
        return format_response(data)

    @mcp.tool()
    def project_start(
        server: str = "",
        project_type: str = "",
        id: str = "",
    ) -> str:
        """Start a project.

        Args:
            server: Server name (optional)
            project_type: Project type
            id: Project ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}

        type_endpoints = {
            "Node": "/project/nodejs/start_project",
            "Go": "/project/go/start_project",
            "Python": "/project/python/StartProject",
            "net": "/project/net/start_project",
            "Java": "/mod/java/project/start_project",
        }

        endpoint = type_endpoints.get(project_type)
        if not endpoint:
            return f"Error: Cannot start project of type '{project_type}'"

        data = client.request(endpoint, params)
        return format_response(data)

    @mcp.tool()
    def project_stop(
        server: str = "",
        project_type: str = "",
        id: str = "",
    ) -> str:
        """Stop a project.

        Args:
            server: Server name (optional)
            project_type: Project type
            id: Project ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}

        type_endpoints = {
            "Node": "/project/nodejs/stop_project",
            "Go": "/project/go/stop_project",
            "Python": "/project/python/StopProject",
            "net": "/project/net/stop_project",
            "Java": "/mod/java/project/stop_project",
        }

        endpoint = type_endpoints.get(project_type)
        if not endpoint:
            return f"Error: Cannot stop project of type '{project_type}'"

        data = client.request(endpoint, params)
        return format_response(data)

    @mcp.tool()
    def project_get_config(
        server: str = "",
        project_type: str = "",
        id: str = "",
    ) -> str:
        """Get project configuration.

        Args:
            server: Server name (optional)
            project_type: Project type
            id: Project ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}

        type_endpoints = {
            "Node": "/project/nodejs/get_project_config",
            "Go": "/project/go/get_project_config",
            "Python": "/project/python/GetProjectConfig",
            "net": "/project/net/get_project_config",
            "Java": "/mod/java/project/get_project_config",
        }

        endpoint = type_endpoints.get(project_type)
        if not endpoint:
            return f"Error: Cannot get config for project type '{project_type}'"

        data = client.request(endpoint, params)
        return format_response(data)

    @mcp.tool()
    def project_get_status(
        server: str = "",
        project_type: str = "",
        id: str = "",
    ) -> str:
        """Get project running status.

        Args:
            server: Server name (optional)
            project_type: Project type
            id: Project ID
        """
        client = client_manager.get_client(server or None)
        params = {"id": id}

        type_endpoints = {
            "Node": "/project/nodejs/get_project_status",
            "Go": "/project/go/get_project_status",
            "Python": "/project/python/GetProjectStatus",
            "net": "/project/net/get_project_status",
            "Java": "/mod/java/project/get_project_status",
        }

        endpoint = type_endpoints.get(project_type)
        if not endpoint:
            return f"Error: Cannot get status for project type '{project_type}'"

        data = client.request(endpoint, params)
        return format_response(data)

    @mcp.tool()
    def project_set_config(
        server: str = "",
        project_type: str = "",
        id: str = "",
        config: str = "",
    ) -> str:
        """Update project configuration.

        Args:
            server: Server name (optional)
            project_type: Project type
            id: Project ID
            config: Configuration data (JSON string)
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "config": config}

        type_endpoints = {
            "Node": "/project/nodejs/set_project_config",
            "Go": "/project/go/set_project_config",
            "Python": "/project/python/SetProjectConfig",
            "net": "/project/net/set_project_config",
            "Java": "/mod/java/project/set_project_config",
        }

        endpoint = type_endpoints.get(project_type)
        if not endpoint:
            return f"Error: Cannot set config for project type '{project_type}'"

        data = client.request(endpoint, params)
        return format_response(data)
