"""Safety guard for aaPanel MCP server.

Prevents destructive operations on critical aaPanel resources.
All delete/remove/stop/uninstall operations require explicit user confirmation.

Protected categories:
- Databases (delete, drop)
- Docker (container stop/remove, image/volume delete)
- Sites (delete, stop)
- Files (delete in critical paths)
- Panel source/config files
- Software uninstall
- Process kill
- Panel close
"""

import re
from typing import Optional


# Actions that are inherently destructive and require confirmation
DESTRUCTIVE_ACTIONS = {
    # Database
    "DeleteDatabase", "DelBackup",
    # Docker
    "StopContainer", "DeleteImage", "DeleteVolume", "DeleteNetwork",
    # Site
    "DeleteSite", "SiteStop", "DelDomain",
    # Files
    "DeleteFile",
    # FTP
    "DeleteUser",
    # Firewall
    "DelAcceptPort", "DelDropAddress",
    # Crontab
    "DelCrontab",
    # SSL
    "RemoveCert",
    # Plugins
    "uninstall_plugin",
    # Software
    "UninstallSoft",
    # System
    "KillProcess", "ClearSystem", "RestartServer",
    # Panel
    "ClosePanel",
    # Tasks
    "remove_task",
    # Backup
    "DelBackup",
    # SSH
    "stop_password", "stop_root", "stop_key", "stop_jian",
    # Tamper
    "del_file_deny",
    # Session
    "DelOldSession",
    # Docker (path-style endpoints: /panel/docker/<action>)
    "stop", "delete_image", "del_network", "remove",
}

# Actions that are moderately destructive (clear/reset but not delete)
CLEANUP_ACTIONS = {
    "CloseLogs", "clean_panel_error_logs", "clear_temp_login",
    "clear_login_send", "ReMemory", "ReWeb", "RepPanel",
}

# Critical path prefixes that must never be deleted
PROTECTED_PATHS = [
    "/www/server/panel",
    "/www/server/data",
    "/www/server/mysql",
    "/www/server/redis",
    "/www/server/nginx",
    "/www/server/apache",
    "/www/server/php",
    "/www/server/docker",
    "/www/server/pgsql",
    "/www/server/mongodb",
    "/www/wwwroot",
    "/www/backup",
    "/www/database",
    "/root",
    "/etc",
    "/var/lib/mysql",
    "/var/lib/docker",
    "/var/lib/redis",
    "/var/lib/postgresql",
    "/boot",
    "/proc",
    "/sys",
    "/dev",
]

# Critical database names that should never be dropped
PROTECTED_DATABASES = {
    "mysql", "information_schema", "performance_schema",
    "sys", "postgres", "template0", "template1",
}

# Endpoints that should be completely blocked (panel source code deletion etc.)
BLOCKED_PATTERNS = [
    r"/files\?action=DeleteFile.*path=.*/www/server/panel",
    r"/files\?action=DeleteFile.*path=.*/www/server/data",
    r"/files\?action=DeleteFile.*path=.*/www/server/mysql",
    r"/files\?action=DeleteFile.*path=.*/var/lib",
    r"/files\?action=DeleteFile.*path=.*/boot",
    r"/files\?action=DeleteFile.*path=.*/etc",
    r"/files\?action=DeleteFile.*path=.*/proc",
    r"/files\?action=DeleteFile.*path=.*/sys",
    r"/files\?action=DeleteFile.*path=.*/dev",
]


class SafetyViolation(Exception):
    """Raised when a destructive operation violates safety rules."""
    pass


class ConfirmationRequired(Exception):
    """Raised when a destructive operation needs user confirmation."""
    pass


def extract_action(endpoint: str) -> Optional[str]:
    """Extract the action name from an endpoint string.
    
    Handles two patterns:
    - Query style: '/path?action=ActionName' → 'ActionName'
    - Path style: '/panel/docker/stop' → 'stop'
    """
    # Try query-style first: action=ActionName
    match = re.search(r'action=([A-Za-z_]+)', endpoint)
    if match:
        return match.group(1)
    
    # Try path-style: /panel/docker/<def_name>
    # Extract the last path segment as the action
    parts = endpoint.split('?')[0].strip('/').split('/')
    if len(parts) >= 3 and parts[0] == 'panel':
        return parts[-1]
    
    return None


def is_protected_path(path: str) -> bool:
    """Check if a path falls within protected directories."""
    if not path:
        return False
    path = path.strip()
    for protected in PROTECTED_PATHS:
        if path == protected or path.startswith(protected + "/"):
            return True
    return False


def is_protected_database(db_name: str) -> bool:
    """Check if a database name is protected (system databases)."""
    return db_name.lower() in PROTECTED_DATABASES if db_name else False


def check_request_safety(
    endpoint: str,
    params: Optional[dict] = None,
    confirmed: bool = False,
) -> tuple[bool, str]:
    """Check if a request is safe to execute.

    Args:
        endpoint: API endpoint string
        params: Request parameters
        confirmed: Whether the user has explicitly confirmed this destructive action

    Returns:
        Tuple of (is_safe, message). If is_safe is False, the request must be blocked.
    """
    if params is None:
        params = {}

    # Check blocked patterns first (hard block - never allowed)
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, endpoint, re.IGNORECASE):
            return False, (
                "BLOCKED: This operation would delete files in a critical system directory. "
                "This is permanently blocked for safety. If you need to manage panel files, "
                "use the aaPanel web interface directly."
            )

    action = extract_action(endpoint)

    # Check for file deletion in protected paths
    if action == "DeleteFile":
        path = params.get("path", "")
        if is_protected_path(path):
            return False, (
                f"BLOCKED: Cannot delete file/directory at '{path}'. "
                "This path is in a protected system directory (panel source, database storage, "
                "system config, etc.). This operation is permanently blocked for safety."
            )

    # Check for database deletion of system databases
    if action == "DeleteDatabase":
        db_name = params.get("name", "")
        if is_protected_database(db_name):
            return False, (
                f"BLOCKED: Cannot delete system database '{db_name}'. "
                "System databases (mysql, information_schema, performance_schema, sys, postgres, "
                "template0, template1) are permanently protected."
            )

    # Check destructive actions - require confirmation
    if action in DESTRUCTIVE_ACTIONS and not confirmed:
        return False, (
            f"CONFIRMATION REQUIRED: The action '{action}' is destructive and cannot be undone. "
            f"Endpoint: {endpoint}, Params: {params}. "
            "This operation will permanently modify or delete data. "
            "Please confirm explicitly in chat that you want to proceed with this action. "
            "The AI assistant must ask for your permission before executing this."
        )

    # Check cleanup actions - require confirmation
    if action in CLEANUP_ACTIONS and not confirmed:
        return False, (
            f"CONFIRMATION REQUIRED: The action '{action}' will clear/reset data. "
            f"Endpoint: {endpoint}. "
            "Please confirm explicitly in chat that you want to proceed."
        )

    return True, "OK"


def get_safety_warning(endpoint: str, params: Optional[dict] = None) -> str:
    """Get a human-readable safety warning for a destructive request without blocking it.

    Used for display purposes when the AI needs to inform the user what will happen.
    """
    if params is None:
        params = {}

    action = extract_action(endpoint)
    if not action:
        return ""

    if action in DESTRUCTIVE_ACTIONS:
        details = []
        if "name" in params:
            details.append(f"name={params['name']}")
        if "id" in params:
            details.append(f"id={params['id']}")
        if "path" in params:
            details.append(f"path={params['path']}")
        if "webname" in params:
            details.append(f"site={params['webname']}")

        detail_str = f" ({', '.join(details)})" if details else ""
        return (
            f"DESTRUCTIVE ACTION: {action}{detail_str}. "
            "This will permanently delete or stop the resource. "
            "User confirmation is required before proceeding."
        )

    if action in CLEANUP_ACTIONS:
        return (
            f"CLEANUP ACTION: {action}. "
            "This will clear or reset data. "
            "User confirmation is required before proceeding."
        )

    return ""
