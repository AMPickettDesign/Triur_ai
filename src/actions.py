"""
Triur.ai — System Actions
Allows the AI to interact with the user's PC: open apps, search files, run commands.
Safety levels: SAFE (auto-run), DANGEROUS (ask permission), BLOCKED (never run).
"""

import subprocess
import os
import glob as globmod
import shutil

# ─── Safety Classification ───

# Commands/patterns that are always safe to auto-run
SAFE_PATTERNS = {
    "open_app",       # Open an application
    "open_url",       # Open a URL in the browser
    "search_files",   # Search for files by name
    "get_file_info",  # Get info about a file (size, modified date)
    "list_directory",  # List contents of a directory
    "get_system_info", # CPU, RAM, disk info
    "screenshot",      # Take a screenshot (read-only)
}

# Commands that require user permission
DANGEROUS_PATTERNS = {
    "run_command",     # Run an arbitrary terminal command
    "move_file",       # Move/rename a file
    "copy_file",       # Copy a file
    "create_file",     # Create a new file
    "create_directory", # Create a new directory
    "delete_file",     # Delete a file
    "kill_process",    # Kill a running process
}

# These are NEVER allowed
BLOCKED_PATTERNS = {
    "format_drive",
    "modify_registry",
    "disable_firewall",
    "rm_rf",  # recursive delete
}


def classify_action(action_type):
    """Returns 'safe', 'dangerous', or 'blocked'."""
    if action_type in BLOCKED_PATTERNS:
        return "blocked"
    if action_type in SAFE_PATTERNS:
        return "safe"
    if action_type in DANGEROUS_PATTERNS:
        return "dangerous"
    return "dangerous"  # Unknown = dangerous by default


def execute_action(action_type, params=None):
    """Execute a system action. Returns dict with result or error."""
    if params is None:
        params = {}

    safety = classify_action(action_type)
    if safety == "blocked":
        return {"success": False, "error": "This action is blocked for safety.", "safety": "blocked"}

    try:
        if action_type == "open_app":
            return _open_app(params.get("app_name", ""))
        elif action_type == "open_url":
            return _open_url(params.get("url", ""))
        elif action_type == "search_files":
            return _search_files(params.get("query", ""), params.get("directory", ""))
        elif action_type == "get_file_info":
            return _get_file_info(params.get("path", ""))
        elif action_type == "list_directory":
            return _list_directory(params.get("path", ""))
        elif action_type == "get_system_info":
            return _get_system_info()
        elif action_type == "run_command":
            return _run_command(params.get("command", ""))
        elif action_type == "move_file":
            return _move_file(params.get("source", ""), params.get("destination", ""))
        elif action_type == "copy_file":
            return _copy_file(params.get("source", ""), params.get("destination", ""))
        elif action_type == "create_file":
            return _create_file(params.get("path", ""), params.get("content", ""))
        elif action_type == "create_directory":
            return _create_directory(params.get("path", ""))
        elif action_type == "delete_file":
            return _delete_file(params.get("path", ""))
        elif action_type == "kill_process":
            return _kill_process(params.get("process_name", ""))
        else:
            return {"success": False, "error": f"Unknown action: {action_type}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ─── Safe Actions ───

def _open_app(app_name):
    """Open an application by name."""
    if not app_name:
        return {"success": False, "error": "No app name provided"}

    # Common app mappings for Windows
    app_map = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "file explorer": "explorer.exe",
        "explorer": "explorer.exe",
        "task manager": "taskmgr.exe",
        "command prompt": "cmd.exe",
        "cmd": "cmd.exe",
        "powershell": "powershell.exe",
        "settings": "ms-settings:",
        "spotify": "spotify",
        "discord": "discord",
        "steam": "steam",
        "chrome": "chrome",
        "firefox": "firefox",
        "edge": "msedge",
        "brave": "brave",
    }

    exe = app_map.get(app_name.lower(), app_name)
    try:
        subprocess.Popen(f'start "" "{exe}"', shell=True)
        return {"success": True, "message": f"Opened {app_name}"}
    except Exception as e:
        return {"success": False, "error": f"Couldn't open {app_name}: {e}"}


def _open_url(url):
    """Open a URL in the default browser."""
    if not url:
        return {"success": False, "error": "No URL provided"}
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        os.startfile(url)
        return {"success": True, "message": f"Opened {url}"}
    except Exception as e:
        return {"success": False, "error": f"Couldn't open URL: {e}"}


def _search_files(query, directory=""):
    """Search for files matching a pattern."""
    if not query:
        return {"success": False, "error": "No search query provided"}
    search_dir = directory or os.path.expanduser("~")
    pattern = os.path.join(search_dir, "**", f"*{query}*")
    try:
        matches = globmod.glob(pattern, recursive=True)[:20]  # Limit results
        return {
            "success": True,
            "results": matches,
            "count": len(matches),
            "message": f"Found {len(matches)} files matching '{query}'"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def _get_file_info(path):
    """Get info about a specific file."""
    if not path or not os.path.exists(path):
        return {"success": False, "error": f"File not found: {path}"}
    stat = os.stat(path)
    size_mb = stat.st_size / (1024 * 1024)
    from datetime import datetime
    return {
        "success": True,
        "path": path,
        "size": f"{size_mb:.2f} MB" if size_mb > 1 else f"{stat.st_size} bytes",
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "is_directory": os.path.isdir(path),
    }


def _list_directory(path=""):
    """List contents of a directory."""
    target = path or os.path.expanduser("~")
    if not os.path.isdir(target):
        return {"success": False, "error": f"Not a directory: {target}"}
    try:
        entries = []
        for entry in os.scandir(target):
            entries.append({
                "name": entry.name,
                "is_dir": entry.is_dir(),
                "size": entry.stat().st_size if entry.is_file() else None,
            })
        entries.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
        return {"success": True, "path": target, "entries": entries[:50], "total": len(entries)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _get_system_info():
    """Get basic system information."""
    import platform
    total, used, free = shutil.disk_usage("/")
    return {
        "success": True,
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "disk_total_gb": f"{total / (1024**3):.1f}",
        "disk_used_gb": f"{used / (1024**3):.1f}",
        "disk_free_gb": f"{free / (1024**3):.1f}",
        "home_dir": os.path.expanduser("~"),
    }


# ─── Dangerous Actions (require permission) ───

def _run_command(command):
    """Run a terminal command and return output."""
    if not command:
        return {"success": False, "error": "No command provided"}
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout[:2000],  # Limit output
            "stderr": result.stderr[:500],
            "return_code": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out (30s limit)"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _move_file(source, destination):
    """Move or rename a file."""
    if not source or not destination:
        return {"success": False, "error": "Source and destination required"}
    if not os.path.exists(source):
        return {"success": False, "error": f"Source not found: {source}"}
    shutil.move(source, destination)
    return {"success": True, "message": f"Moved {source} to {destination}"}


def _copy_file(source, destination):
    """Copy a file."""
    if not source or not destination:
        return {"success": False, "error": "Source and destination required"}
    if not os.path.exists(source):
        return {"success": False, "error": f"Source not found: {source}"}
    if os.path.isdir(source):
        shutil.copytree(source, destination)
    else:
        shutil.copy2(source, destination)
    return {"success": True, "message": f"Copied {source} to {destination}"}


def _create_file(path, content=""):
    """Create a new file with optional content."""
    if not path:
        return {"success": False, "error": "No file path provided"}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return {"success": True, "message": f"Created {path}"}


def _create_directory(path):
    """Create a new directory."""
    if not path:
        return {"success": False, "error": "No path provided"}
    os.makedirs(path, exist_ok=True)
    return {"success": True, "message": f"Created directory {path}"}


def _delete_file(path):
    """Delete a file or empty directory."""
    if not path:
        return {"success": False, "error": "No path provided"}
    if not os.path.exists(path):
        return {"success": False, "error": f"Not found: {path}"}
    # SAFETY: Never allow deleting system directories or root
    dangerous_paths = ["C:\\Windows", "C:\\Program Files", "C:\\Users", "/", "/home", "/etc"]
    if path.rstrip("/\\") in dangerous_paths:
        return {"success": False, "error": "Cannot delete system directories"}
    if os.path.isdir(path):
        if os.listdir(path):
            return {"success": False, "error": "Directory not empty. Won't delete non-empty directories for safety."}
        os.rmdir(path)
    else:
        os.remove(path)
    return {"success": True, "message": f"Deleted {path}"}


def _kill_process(process_name):
    """Kill a process by name."""
    if not process_name:
        return {"success": False, "error": "No process name provided"}
    try:
        result = subprocess.run(
            f'taskkill /IM "{process_name}" /F',
            shell=True, capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return {"success": True, "message": f"Killed {process_name}"}
        return {"success": False, "error": result.stderr.strip() or "Process not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}
