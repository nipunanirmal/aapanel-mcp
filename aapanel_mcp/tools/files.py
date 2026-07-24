"""File manager tools for aaPanel MCP server."""

from mcp.server.fastmcp import FastMCP
from ..client import client_manager
from ..utils import format_response


def register_file_tools(mcp: FastMCP) -> None:
    """Register all file management tools."""

    @mcp.tool()
    def file_list(server: str = "", path: str = "/", page: int = 1, limit: int = 100) -> str:
        """List directory contents on the server.

        Args:
            server: Server name (optional)
            path: Directory path to list (default /)
            page: Page number (default 1)
            limit: Items per page (default 100)
        """
        client = client_manager.get_client(server or None)
        params = {"path": path, "p": page, "limit": limit, "showRow": 1, "type": "dir"}
        data = client.request("/files?action=GetDir", params)
        return format_response(data)

    @mcp.tool()
    def file_read(server: str = "", path: str = "") -> str:
        """Read file content from the server.

        Args:
            server: Server name (optional)
            path: File path to read
        """
        client = client_manager.get_client(server or None)
        params = {"path": path}
        data = client.request("/files?action=GetFileBody", params)
        return format_response(data)

    @mcp.tool()
    def file_write(
        server: str = "",
        path: str = "",
        data: str = "",
        encoding: str = "utf-8",
    ) -> str:
        """Write content to a file on the server.

        Args:
            server: Server name (optional)
            path: File path to write
            data: Content to write
            encoding: File encoding (default utf-8)
        """
        client = client_manager.get_client(server or None)
        params = {"path": path, "data": data, "encoding": encoding}
        result = client.request("/files?action=SaveFileBody", params)
        return format_response(result)

    @mcp.tool()
    def file_mkdir(server: str = "", path: str = "") -> str:
        """Create a directory on the server.

        Args:
            server: Server name (optional)
            path: Directory path to create
        """
        client = client_manager.get_client(server or None)
        params = {"path": path}
        data = client.request("/files?action=CreateDir", params)
        return format_response(data)

    @mcp.tool()
    def file_delete(server: str = "", path: str = "") -> str:
        """Delete a file or directory on the server.

        Args:
            server: Server name (optional)
            path: Path to delete
        """
        client = client_manager.get_client(server or None)
        params = {"path": path}
        data = client.request("/files?action=DeleteFile", params)
        return format_response(data)

    @mcp.tool()
    def file_move(server: str = "", sfile: str = "", dpath: str = "") -> str:
        """Move or rename a file/directory.

        Args:
            server: Server name (optional)
            sfile: Source file path
            dpath: Destination path
        """
        client = client_manager.get_client(server or None)
        params = {"sfile": sfile, "dpath": dpath}
        data = client.request("/files?action=MvFile", params)
        return format_response(data)

    @mcp.tool()
    def file_copy(server: str = "", sfile: str = "", dpath: str = "") -> str:
        """Copy a file/directory.

        Args:
            server: Server name (optional)
            sfile: Source file path
            dpath: Destination path
        """
        client = client_manager.get_client(server or None)
        params = {"sfile": sfile, "dpath": dpath}
        data = client.request("/files?action=CopyFile", params)
        return format_response(data)

    @mcp.tool()
    def file_compress(
        server: str = "",
        sfile: str = "",
        dpath: str = "",
        type: str = "zip",
    ) -> str:
        """Compress a file or directory into an archive.

        Args:
            server: Server name (optional)
            sfile: Source file/directory path
            dpath: Output archive path
            type: Archive type (zip or tar.gz)
        """
        client = client_manager.get_client(server or None)
        params = {"sfile": sfile, "dpath": dpath, "type": type}
        data = client.request("/files?action=Zip", params)
        return format_response(data)

    @mcp.tool()
    def file_unzip(
        server: str = "",
        sfile: str = "",
        dpath: str = "",
        type: str = "zip",
    ) -> str:
        """Extract an archive file.

        Args:
            server: Server name (optional)
            sfile: Archive file path
            dpath: Extraction destination path
            type: Archive type (zip or tar.gz)
        """
        client = client_manager.get_client(server or None)
        params = {"sfile": sfile, "dpath": dpath, "type": type}
        data = client.request("/files?action=UnZip", params)
        return format_response(data)

    @mcp.tool()
    def file_download(server: str = "", url: str = "", path: str = "") -> str:
        """Download a file from a URL to the server.

        Args:
            server: Server name (optional)
            url: URL to download from
            path: Destination path on the server
        """
        client = client_manager.get_client(server or None)
        params = {"url": url, "path": path}
        data = client.request("/files?action=DownloadFile", params)
        return format_response(data)

    @mcp.tool()
    def file_stat(server: str = "", path: str = "") -> str:
        """Get file/directory info (size, permissions, owner, modified time).

        Args:
            server: Server name (optional)
            path: File or directory path
        """
        client = client_manager.get_client(server or None)
        params = {"path": path}
        data = client.request("/files?action=GetFileAccess", params)
        return format_response(data)

    @mcp.tool()
    def file_chmod(
        server: str = "",
        path: str = "",
        mode: str = "755",
        user: str = "",
    ) -> str:
        """Change file permissions and optionally owner.

        Args:
            server: Server name (optional)
            path: File or directory path
            mode: Permission mode (e.g. 755, 644)
            user: New owner (optional)
        """
        client = client_manager.get_client(server or None)
        params = {"path": path, "mode": mode, "user": user}
        data = client.request("/files?action=SetFileAccess", params)
        return format_response(data)

    @mcp.tool()
    def file_search(
        server: str = "",
        path: str = "",
        search: str = "",
        page: int = 1,
        limit: int = 100,
    ) -> str:
        """Search for files in a directory.

        Args:
            server: Server name (optional)
            path: Directory to search in
            search: Search keyword
            page: Page number (default 1)
            limit: Items per page (default 100)
        """
        client = client_manager.get_client(server or None)
        params = {"path": path, "search": search, "p": page, "limit": limit}
        data = client.request("/files?action=SearchFiles", params)
        return format_response(data)

    @mcp.tool()
    def file_get_dir_size(server: str = "", path: str = "") -> str:
        """Get total size of a directory.

        Args:
            server: Server name (optional)
            path: Directory path
        """
        client = client_manager.get_client(server or None)
        params = {"path": path}
        data = client.request("/files?action=GetDirSize", params)
        return format_response(data)

    @mcp.tool()
    def file_upload(
        server: str = "",
        path: str = "",
        filename: str = "",
        content: str = "",
    ) -> str:
        """Upload a file (base64 encoded content) to the server.

        Args:
            server: Server name (optional)
            path: Destination directory path
            filename: Name of the file to create
            content: Base64-encoded file content
        """
        client = client_manager.get_client(server or None)
        params = {"path": path, "filename": filename, "content": content}
        data = client.request("/files?action=UploadFile", params)
        return format_response(data)
