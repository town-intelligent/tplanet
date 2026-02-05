"""
Thread-local tenant context for multi-tenant applications.

This module provides thread-safe storage for the current tenant, allowing
any part of the application to access tenant information without passing
it through every function call.
"""

from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TenantInfo:
    """Information about the current tenant."""

    tenant_id: str
    name: str
    database: str = "default"
    config: dict = field(default_factory=dict)

    def get_feature(self, feature_name: str, default: Any = None) -> Any:
        """Get a feature flag value for this tenant."""
        features = self.config.get("features", {})
        return features.get(feature_name, default)

    def get_theme(self, key: str, default: Any = None) -> Any:
        """Get a theme value for this tenant."""
        theme = self.config.get("theme", {})
        return theme.get(key, default)


# Context variable for storing tenant info per-request
_current_tenant: ContextVar[TenantInfo | None] = ContextVar(
    "current_tenant", default=None
)


def get_current_tenant() -> TenantInfo | None:
    """
    Get the current tenant for this request/context.

    Returns:
        TenantInfo or None if no tenant is set.
    """
    return _current_tenant.get()


def set_current_tenant(tenant: TenantInfo | None) -> None:
    """
    Set the current tenant for this request/context.

    Args:
        tenant: TenantInfo instance or None to clear.
    """
    _current_tenant.set(tenant)


class TenantContext:
    """
    Context manager for temporarily setting a tenant.

    Usage:
        with TenantContext(tenant_info):
            # Code runs with tenant_info as current tenant
            pass
        # Original tenant is restored
    """

    def __init__(self, tenant: TenantInfo | None):
        self.tenant = tenant
        self.previous_tenant: TenantInfo | None = None

    def __enter__(self) -> TenantInfo | None:
        self.previous_tenant = get_current_tenant()
        set_current_tenant(self.tenant)
        return self.tenant

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        set_current_tenant(self.previous_tenant)
