"""Project management tools for aaPanel MCP server.

Supports Java, Node, Go, Python, .NET, Proxy, HTML, and Other project types.
Each operation tries the v8.0.7 v2 route first and falls back to the legacy
route for older panels.
"""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response, request_compat

# Project type → [v2 endpoint, legacy endpoint] for list operations
PROJECT_ENDPOINTS = {
    "Java": ["/v2/mod/java/project/project_list", "/mod/java/project/project_list"],
    "Node": ["/v2/project/nodejs/get_project_list", "/project/nodejs/get_project_list"],
    "Go": ["/v2/project/go/get_project_list", "/project/go/get_project_list"],
    "Python": ["/v2/project/python/GetProjectList", "/project/python/GetProjectList"],
    "net": ["/v2/data?action=getData", "/project/net/get_project_list"],
    "Proxy": ["/v2/mod/proxy/com/get_list", "/mod/proxy/com/get_list"],
    "HTML": ["/v2/data?action=getData", "/project/html/get_project_list"],
    "Other": ["/v2/data?action=getData", "/project/other/get_project_list"],
}

# Per-operation endpoint chains: operation → project_type → [v2, legacy]
_PROJECT_OPS = {
    "create": {
        "Node": ["/v2/project/nodejs/create_project", "/project/nodejs/add_project"],
        "Go": ["/v2/project/go/create_project", "/project/go/add_project"],
        "Python": ["/v2/project/python/CreateProject", "/project/python/AddProject"],
        "Java": ["/v2/mod/java/project/create_project", "/mod/java/project/add_project"],
        "net": ["/project/net/add_project"],
        "HTML": ["/project/html/add_project"],
        "Proxy": ["/v2/mod/proxy/com/create", "/mod/proxy/com/add_proxy"],
    },
    "delete": {
        "Node": ["/v2/project/nodejs/remove_project", "/project/nodejs/del_project"],
        "Go": ["/v2/project/go/remove_project", "/project/go/del_project"],
        "Python": ["/v2/project/python/RemoveProject", "/project/python/DelProject"],
        "Java": ["/v2/mod/java/project/remove_project", "/mod/java/project/del_project"],
        "net": ["/project/net/del_project"],
        "HTML": ["/project/html/del_project"],
        "Proxy": ["/v2/mod/proxy/com/delete", "/mod/proxy/com/del_proxy"],
    },
    "start": {
        "Node": ["/v2/project/nodejs/start_project", "/project/nodejs/start_project"],
        "Go": ["/v2/project/go/start_project", "/project/go/start_project"],
        "Python": ["/v2/project/python/StartProject", "/project/python/StartProject"],
        "Java": ["/v2/mod/java/project/start_project", "/mod/java/project/start_project"],
        "net": ["/project/net/start_project"],
    },
    "stop": {
        "Node": ["/v2/project/nodejs/stop_project", "/project/nodejs/stop_project"],
        "Go": ["/v2/project/go/stop_project", "/project/go/stop_project"],
        "Python": ["/v2/project/python/StopProject", "/project/python/StopProject"],
        "Java": ["/v2/mod/java/project/stop_project", "/mod/java/project/stop_project"],
        "net": ["/project/net/stop_project"],
    },
    "config": {
        "Node": ["/v2/project/nodejs/get_project_info", "/project/nodejs/get_project_config"],
        "Go": ["/v2/project/go/get_project_info", "/project/go/get_project_config"],
        "Python": ["/v2/project/python/GetProjectInfo", "/project/python/GetProjectConfig"],
        "Java": ["/v2/mod/java/project/get_project_info", "/mod/java/project/get_project_config"],
        "net": ["/project/net/get_project_config"],
        "Proxy": ["/v2/mod/proxy/com/get_config", "/mod/proxy/com/get_config"],
    },
    "status": {
        "Node": ["/v2/project/nodejs/get_project_info", "/project/nodejs/get_project_status"],
        "Go": ["/v2/project/go/get_project_info", "/project/go/get_project_status"],
        "Python": ["/v2/project/python/GetProjectInfo", "/project/python/GetProjectStatus"],
        "Java": ["/v2/mod/java/project/get_project_info", "/mod/java/project/get_project_status"],
        "net": ["/project/net/get_project_status"],
        "Proxy": ["/v2/mod/proxy/com/get_config", "/mod/proxy/com/get_config"],
    },
    "set_config": {
        "Node": ["/v2/project/nodejs/modify_project", "/project/nodejs/set_project_config"],
        "Go": ["/v2/project/go/modify_project", "/project/go/set_project_config"],
        "Python": ["/v2/project/python/ChangeProjectConf", "/project/python/SetProjectConfig"],
        "Java": ["/v2/mod/java/project/modify_project", "/mod/java/project/set_project_config"],
        "net": ["/project/net/set_project_config"],
        "Proxy": ["/v2/mod/proxy/com/save_config", "/mod/proxy/com/save_config"],
    },
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
        def _build_params(ptype: str) -> dict:
            base = {"search": "", "p": page, "limit": limit, "type_id": ""}
            if "getData" in PROJECT_ENDPOINTS.get(ptype, [""])[0]:
                base["table"] = "sites"
                base["project_type"] = ptype
            return base

        if not project_type:
            # Return all project types
            client = client_manager.get_client(server or None)
            results = {}
            for ptype, endpoints in PROJECT_ENDPOINTS.items():
                try:
                    data = request_compat(client, endpoints, _build_params(ptype))
                    results[ptype] = data
                except Exception as e:
                    results[ptype] = {"error": str(e)}
            return format_response(results)

        if project_type not in PROJECT_ENDPOINTS:
            return f"Error: Unsupported project type '{project_type}'. Supported: {list(PROJECT_ENDPOINTS.keys())}"

        client = client_manager.get_client(server or None)
        data = request_compat(client, PROJECT_ENDPOINTS[project_type], _build_params(project_type))
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
            "project_name": name,
            "site_name": name,
            "path": path,
            "project_cwd": path,
            "project_exe": path,
            "version": version,
            "nodejs_version": version,
            "port": port,
            "run_cmd": run_cmd,
            "project_script": run_cmd,
            "project_cmd": run_cmd,
        }

        endpoints = _PROJECT_OPS["create"].get(project_type)
        if not endpoints:
            return f"Error: Cannot create project of type '{project_type}'. Supported: {list(_PROJECT_OPS['create'].keys())}"

        data = request_compat(client, endpoints, params)
        return format_response(data)

    @mcp.tool()
    def project_delete(
        server: str = "",
        project_type: str = "",
        id: str = "",
        confirmed: bool = False,
    ) -> str:
        """Delete a project.

        Args:
            server: Server name (optional)
            project_type: Project type (Java/Node/Go/Python/net/Proxy/HTML)
            id: Project ID or project name
            confirmed: Must be True to confirm this destructive action
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "project_name": id, "name": id, "site_name": id, "remove_path": "0"}

        endpoints = _PROJECT_OPS["delete"].get(project_type)
        if not endpoints:
            return f"Error: Cannot delete project of type '{project_type}'. Supported: {list(_PROJECT_OPS['delete'].keys())}"

        data = request_compat(client, endpoints, params, confirmed=confirmed)
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
            id: Project ID or project name
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "project_name": id, "name": id}

        endpoints = _PROJECT_OPS["start"].get(project_type)
        if not endpoints:
            return f"Error: Cannot start project of type '{project_type}'. Supported: {list(_PROJECT_OPS['start'].keys())}"

        data = request_compat(client, endpoints, params)
        return format_response(data)

    @mcp.tool()
    def project_stop(
        server: str = "",
        project_type: str = "",
        id: str = "",
        confirmed: bool = False,
    ) -> str:
        """Stop a project.

        Args:
            server: Server name (optional)
            project_type: Project type
            id: Project ID or project name
            confirmed: Must be True to confirm this action
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "project_name": id, "name": id}

        endpoints = _PROJECT_OPS["stop"].get(project_type)
        if not endpoints:
            return f"Error: Cannot stop project of type '{project_type}'. Supported: {list(_PROJECT_OPS['stop'].keys())}"

        data = request_compat(client, endpoints, params, confirmed=confirmed)
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
            id: Project ID or project name
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "project_name": id, "name": id, "site_name": id}

        endpoints = _PROJECT_OPS["config"].get(project_type)
        if not endpoints:
            return f"Error: Cannot get config for project type '{project_type}'. Supported: {list(_PROJECT_OPS['config'].keys())}"

        data = request_compat(client, endpoints, params)
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
            id: Project ID or project name
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "project_name": id, "name": id, "site_name": id}

        endpoints = _PROJECT_OPS["status"].get(project_type)
        if not endpoints:
            return f"Error: Cannot get status for project type '{project_type}'. Supported: {list(_PROJECT_OPS['status'].keys())}"

        data = request_compat(client, endpoints, params)
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
            id: Project ID or project name
            config: Configuration data (JSON string)
        """
        client = client_manager.get_client(server or None)
        params = {"id": id, "project_name": id, "name": id, "site_name": id, "config": config, "data": config}

        endpoints = _PROJECT_OPS["set_config"].get(project_type)
        if not endpoints:
            return f"Error: Cannot set config for project type '{project_type}'. Supported: {list(_PROJECT_OPS['set_config'].keys())}"

        data = request_compat(client, endpoints, params)
        return format_response(data)
