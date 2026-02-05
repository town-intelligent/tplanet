"""
Tenant detection middleware for Django.

Identifies the current tenant based on:
1. X-Tenant-ID header (highest priority)
2. Subdomain (e.g., nantou.tplanet.ai → nantou-gov)
3. Full domain match (e.g., cms.ntsdgs.tw → nantou-gov)
4. Default tenant (fallback)
"""

import logging
from typing import Callable

from django.conf import settings
from django.http import HttpRequest, HttpResponse

from django_multi_tenant.config.loader import TenantConfigLoader
from django_multi_tenant.middleware.tenant_context import TenantInfo, set_current_tenant

logger = logging.getLogger(__name__)


class TenantMiddleware:
    """
    Middleware that identifies the current tenant and sets it in the context.

    Configuration in settings.py:
        MULTI_TENANT = {
            "CONFIG_PATH": "/path/to/tenants.yml",
            "DEFAULT_TENANT": "default",
            "HEADER_NAME": "X-Tenant-ID",
        }
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response
        self.config_loader = TenantConfigLoader()
        self._load_config()

    def _load_config(self) -> None:
        """Load tenant configuration from settings."""
        multi_tenant_settings = getattr(settings, "MULTI_TENANT", {})
        config_path = multi_tenant_settings.get("CONFIG_PATH")

        if config_path:
            self.config_loader.load_from_file(config_path)

        self.default_tenant_id = multi_tenant_settings.get("DEFAULT_TENANT", "default")
        self.header_name = multi_tenant_settings.get("HEADER_NAME", "X-Tenant-ID")

        # Build lookup tables for fast tenant resolution
        self._build_lookup_tables()

    def _build_lookup_tables(self) -> None:
        """Build domain and subdomain lookup tables."""
        self.domain_to_tenant: dict[str, str] = {}
        self.subdomain_to_tenant: dict[str, str] = {}

        for tenant_id, config in self.config_loader.tenants.items():
            domains = config.get("domains", [])
            for domain in domains:
                self.domain_to_tenant[domain.lower()] = tenant_id

                # Extract subdomain mapping (first part before first dot)
                parts = domain.split(".")
                if len(parts) >= 2:
                    subdomain = parts[0].lower()
                    if subdomain not in ("www", "api"):
                        self.subdomain_to_tenant[subdomain] = tenant_id

    def __call__(self, request: HttpRequest) -> HttpResponse:
        tenant_info = self._resolve_tenant(request)
        set_current_tenant(tenant_info)

        # Attach tenant to request for easy access
        request.tenant = tenant_info

        try:
            response = self.get_response(request)
        finally:
            # Clear tenant context after request
            set_current_tenant(None)

        return response

    def _resolve_tenant(self, request: HttpRequest) -> TenantInfo | None:
        """
        Resolve tenant from request using priority order.

        Priority:
        1. X-Tenant-ID header
        2. Subdomain
        3. Full domain match
        4. Default tenant
        """
        # 1. Check header
        header_key = f"HTTP_{self.header_name.upper().replace('-', '_')}"
        tenant_id = request.META.get(header_key)

        if tenant_id and tenant_id in self.config_loader.tenants:
            logger.debug(f"Tenant resolved from header: {tenant_id}")
            return self._create_tenant_info(tenant_id)

        # Get host from request
        host = request.get_host().split(":")[0].lower()  # Remove port

        # 2. Check full domain match
        if host in self.domain_to_tenant:
            tenant_id = self.domain_to_tenant[host]
            logger.debug(f"Tenant resolved from domain {host}: {tenant_id}")
            return self._create_tenant_info(tenant_id)

        # 3. Check subdomain
        subdomain = host.split(".")[0]
        if subdomain in self.subdomain_to_tenant:
            tenant_id = self.subdomain_to_tenant[subdomain]
            logger.debug(f"Tenant resolved from subdomain {subdomain}: {tenant_id}")
            return self._create_tenant_info(tenant_id)

        # 4. Fall back to default tenant
        if self.default_tenant_id and self.default_tenant_id in self.config_loader.tenants:
            logger.debug(f"Using default tenant: {self.default_tenant_id}")
            return self._create_tenant_info(self.default_tenant_id)

        logger.warning(f"No tenant found for host: {host}")
        return None

    def _create_tenant_info(self, tenant_id: str) -> TenantInfo:
        """Create TenantInfo from configuration."""
        config = self.config_loader.tenants.get(tenant_id, {})

        database_config = config.get("database", {})
        database_name = database_config.get("alias", tenant_id)

        return TenantInfo(
            tenant_id=tenant_id,
            name=config.get("name", tenant_id),
            database=database_name,
            config=config,
        )
