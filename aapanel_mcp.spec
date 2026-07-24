# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for building standalone aaPanel MCP binaries.

Usage:
    pyinstaller aapanel_mcp.spec
"""

import sys
from pathlib import Path

block_cipher = None

a_sources = ["main.py"]

a_binaries = []
a_datas = [
    ("config/servers.yaml.example", "config"),
]

# Collect all hidden imports that PyInstaller may miss
a_hiddenimports = [
    "mcp",
    "mcp.server",
    "mcp.server.fastmcp",
    "mcp.types",
    "httpx",
    "yaml",
    "anyio",
    "anyio._backends",
    "anyio._backends._asyncio",
    "pydantic",
    "pydantic_core",
    "sse_starlette",
    "starlette",
    "uvicorn",
]

# Include all aapanel_mcp core modules
a_hiddenimports += [
    "aapanel_mcp",
    "aapanel_mcp.server",
    "aapanel_mcp.client",
    "aapanel_mcp.config",
    "aapanel_mcp.safety",
    "aapanel_mcp.utils",
    "aapanel_mcp.main",
]

# Include all tool modules
import os
tools_dir = Path("aapanel_mcp/tools")
if tools_dir.exists():
    for f in tools_dir.glob("*.py"):
        if f.stem != "__init__":
            a_hiddenimports.append(f"aapanel_mcp.tools.{f.stem}")

analysis = Analysis(
    a_sources,
    pathex=["."],
    binaries=a_binaries,
    datas=a_datas,
    hiddenimports=a_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(analysis.pure, analysis.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    analysis.scripts,
    [],
    exclude_binaries=True,
    name="aapanel-mcp",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    analysis.binaries,
    analysis.zipfiles,
    analysis.datas,
    name="aapanel-mcp",
)
