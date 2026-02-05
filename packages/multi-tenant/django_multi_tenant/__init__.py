"""
Django Multi-Tenant Package

Provides middleware, database router, and utilities for multi-tenant Django applications.
"""

__version__ = "0.1.0"

from django_multi_tenant.middleware.tenant_context import get_current_tenant, set_current_tenant
from django_multi_tenant.middleware.tenant_middleware import TenantMiddleware
from django_multi_tenant.db.router import TenantDatabaseRouter
from django_multi_tenant.config.loader import TenantConfigLoader

__all__ = [
    "TenantMiddleware",
    "TenantDatabaseRouter",
    "TenantConfigLoader",
    "get_current_tenant",
    "set_current_tenant",
]
