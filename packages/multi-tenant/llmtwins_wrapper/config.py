# llmtwins_wrapper/config.py
"""
Configuration for LLMTwins Tenant Wrapper
"""

import os
from dataclasses import dataclass, field
from typing import Set


@dataclass
class WrapperConfig:
    # LLMTwins upstream
    llmtwins_base_url: str = field(
        default_factory=lambda: os.getenv("LLMTWINS_BASE_URL", "http://localhost:8000")
    )

    # Tenant settings
    default_tenant: str = field(
        default_factory=lambda: os.getenv("DEFAULT_TENANT", "default")
    )
    tenant_header: str = field(
        default_factory=lambda: os.getenv("TENANT_HEADER", "X-Tenant-ID")
    )
    tenant_separator: str = "__"  # session_id = {tenant}__{original_session_id}

    # Valid tenants (empty = allow all)
    valid_tenants: Set[str] = field(default_factory=lambda: _load_valid_tenants())

    # Timeouts
    upstream_timeout: int = field(
        default_factory=lambda: int(os.getenv("UPSTREAM_TIMEOUT", "180"))
    )

    # Server
    host: str = field(default_factory=lambda: os.getenv("HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(os.getenv("PORT", "8001")))


def _load_valid_tenants() -> Set[str]:
    """Load valid tenants from env or config file"""
    tenants_str = os.getenv("VALID_TENANTS", "")
    if tenants_str:
        return set(t.strip() for t in tenants_str.split(",") if t.strip())
    return set()  # Empty = allow all


config = WrapperConfig()
