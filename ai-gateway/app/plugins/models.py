from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class PluginStatus(str, Enum):
    LOADED = "loaded"
    UNLOADED = "unloaded"
    DISABLED = "disabled"
    ERROR = "error"


class PluginPermission(str, Enum):
    FILESYSTEM = "filesystem"
    NETWORK = "network"
    DATABASE = "database"
    TOOLS = "tools"
    MODELS = "models"


class PluginMetadata(BaseModel):
    name: str
    version: str
    author: str
    description: str = ""
    homepage: str = ""
    license: str = ""
    tags: List[str] = Field(default_factory=list)


class PluginConfig(BaseModel):
    enabled: bool = True
    auto_load: bool = True
    sandbox: bool = True
    settings: Dict[str, Any] = Field(default_factory=dict)


class Plugin(BaseModel):
    metadata: PluginMetadata
    config: PluginConfig = Field(default_factory=PluginConfig)

    status: PluginStatus = PluginStatus.UNLOADED

    permissions: List[PluginPermission] = Field(default_factory=list)

    entrypoint: str

    module: Optional[Any] = None

    tools: List[str] = Field(default_factory=list)

    loaded_at: Optional[float] = None


class PluginStatistics(BaseModel):
    plugins: int = 0
    loaded: int = 0
    unloaded: int = 0
    disabled: int = 0
    errors: int = 0


class RegistryExport(BaseModel):
    plugins: List[Plugin] = Field(default_factory=list)