import hashlib
import hmac
import json
import re
import time

import public


class mcp_terminal_main:
    _api_config = "/www/server/panel/config/api.json"
    _max_timeout = 60
    _max_output = 65536
    _read_only = re.compile(
        r"^\s*(?:cat|df|du|free|grep|head|hostname|id|ip|journalctl|ls|ps|pwd|ss|stat|tail|top|uname|uptime|whoami)\b",
        re.IGNORECASE,
    )

    def _get(self, args, name, default=""):
        try:
            return str(args.get(name, default))
        except AttributeError:
            return str(getattr(args, name, default))

    def _authorized(self, args):
        try:
            request_time = int(self._get(args, "request_time"))
            if abs(time.time() - request_time) > 300:
                return False
            config = json.loads(public.ReadFile(self._api_config) or "{}")
            if not config.get("open") or not config.get("token"):
                return False
            expected = hashlib.md5(f"{request_time}{config['token']}".encode()).hexdigest()
            return hmac.compare_digest(self._get(args, "request_token"), expected)
        except (TypeError, ValueError, json.JSONDecodeError):
            return False

    def execute(self, args):
        if not self._authorized(args):
            return {"status": False, "msg": "API authentication failed"}

        host = self._get(args, "host").strip()
        command = self._get(args, "command")
        confirmed = self._get(args, "confirmed").lower() in {"1", "true", "yes"}
        try:
            timeout = int(self._get(args, "timeout", "30"))
        except ValueError:
            return {"status": False, "msg": "Invalid timeout"}

        if not host or not command.strip() or len(command) > 4096:
            return {"status": False, "msg": "Invalid host or command"}
        if timeout < 1 or timeout > self._max_timeout:
            return {"status": False, "msg": f"Timeout must be between 1 and {self._max_timeout} seconds"}
        if not self._read_only.match(command) and not confirmed:
            return {"status": False, "confirmation_required": True, "msg": "Command confirmation is required"}

        import ssh_terminal

        host_admin = ssh_terminal.ssh_host_admin()
        ssh_info = host_admin.get_ssh_info(host)
        if not ssh_info:
            return {"status": False, "msg": "The specified Terminal host was not found"}

        terminal = ssh_terminal.ssh_terminal()
        terminal._host = ssh_info.get("host")
        terminal._port = int(ssh_info.get("port", 22))
        terminal._user = ssh_info.get("username")
        terminal._pass = ssh_info.get("password")
        terminal._pkey = ssh_info.get("pkey")
        terminal._key_passwd = ssh_info.get("pkey_passwd")
        connection = terminal.connect()
        if not connection.get("status"):
            return connection

        channel = terminal._tp.open_session()
        channel.settimeout(timeout)
        channel.exec_command(command)
        output = b""
        error = b""
        deadline = time.monotonic() + timeout
        try:
            while not channel.exit_status_ready():
                if channel.recv_ready():
                    output += channel.recv(min(32768, self._max_output - len(output)))
                if channel.recv_stderr_ready():
                    error += channel.recv_stderr(min(32768, self._max_output - len(error)))
                if len(output) >= self._max_output or len(error) >= self._max_output:
                    break
                if time.monotonic() >= deadline:
                    channel.close()
                    return {"status": False, "msg": "Command timed out"}
                time.sleep(0.05)
            while channel.recv_ready() and len(output) < self._max_output:
                output += channel.recv(min(32768, self._max_output - len(output)))
            while channel.recv_stderr_ready() and len(error) < self._max_output:
                error += channel.recv_stderr(min(32768, self._max_output - len(error)))
            return {
                "status": True,
                "host": host,
                "exit_code": channel.recv_exit_status(),
                "output": output.decode("utf-8", "replace"),
                "error": error.decode("utf-8", "replace"),
            }
        finally:
            channel.close()
            terminal._tp.close()
