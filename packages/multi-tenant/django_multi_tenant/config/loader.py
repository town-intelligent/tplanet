"""
YAML configuration loader for tenant settings.

Supports environment variable expansion in YAML values.
"""

import logging
import os
import re
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class TenantConfigLoader:
    """
    Loads tenant configuration from YAML files with environment variable support.

    YAML format:
        tenants:
          tenant-id:
            name: "Tenant Name"
            domains:
              - "tenant.example.com"
            database:
              name: "${DB_NAME:-tenant_db}"
              host: "${DB_HOST:-localhost}"
            features:
              ai_secretary: true
            theme:
              primary_color: "#2e7d32"
    """

    ENV_VAR_PATTERN = re.compile(r"\$\{([^}:]+)(?::-([^}]*))?\}")

    def __init__(self):
        self.tenants: dict[str, dict[str, Any]] = {}
        self._config_path: Path | None = None

    def load_from_file(self, path: str | Path) -> None:
        """
        Load tenant configuration from a YAML file.

        Args:
            path: Path to the YAML configuration file.

        Raises:
            FileNotFoundError: If the configuration file doesn't exist.
            yaml.YAMLError: If the YAML is invalid.
        """
        self._config_path = Path(path)

        if not self._config_path.exists():
            raise FileNotFoundError(f"Tenant config file not found: {path}")

        with open(self._config_path, encoding="utf-8") as f:
            raw_config = yaml.safe_load(f)

        if not raw_config:
            logger.warning(f"Empty tenant config file: {path}")
            return

        # Expand environment variables
        config = self._expand_env_vars(raw_config)

        self.tenants = config.get("tenants", {})
        logger.info(f"Loaded {len(self.tenants)} tenants from {path}")

    def load_from_dict(self, config: dict[str, Any]) -> None:
        """
        Load tenant configuration from a dictionary.

        Args:
            config: Configuration dictionary with 'tenants' key.
        """
        expanded = self._expand_env_vars(config)
        self.tenants = expanded.get("tenants", {})

    def _expand_env_vars(self, obj: Any) -> Any:
        """
        Recursively expand environment variables in configuration.

        Supports ${VAR_NAME} and ${VAR_NAME:-default} syntax.
        """
        if isinstance(obj, str):
            return self._expand_string(obj)
        elif isinstance(obj, dict):
            return {k: self._expand_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._expand_env_vars(item) for item in obj]
        return obj

    def _expand_string(self, value: str) -> str:
        """Expand environment variables in a string value."""

        def replace_env_var(match: re.Match) -> str:
            var_name = match.group(1)
            default_value = match.group(2) if match.group(2) is not None else ""
            return os.environ.get(var_name, default_value)

        return self.ENV_VAR_PATTERN.sub(replace_env_var, value)

    def get_tenant(self, tenant_id: str) -> dict[str, Any] | None:
        """
        Get configuration for a specific tenant.

        Args:
            tenant_id: The tenant identifier.

        Returns:
            Tenant configuration dict or None if not found.
        """
        return self.tenants.get(tenant_id)

    def get_tenant_ids(self) -> list[str]:
        """Get list of all configured tenant IDs."""
        return list(self.tenants.keys())

    def get_database_config(self, tenant_id: str) -> dict[str, Any]:
        """
        Get database configuration for a tenant.

        Returns Django-compatible database configuration dict.
        """
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            return {}

        db_config = tenant.get("database", {})

        return {
            "ENGINE": db_config.get("engine", "django.db.backends.postgresql"),
            "NAME": db_config.get("name", f"tplanet_{tenant_id.replace('-', '_')}"),
            "USER": db_config.get("user", os.environ.get("DB_USER", "postgres")),
            "PASSWORD": db_config.get("password", os.environ.get("DB_PASSWORD", "")),
            "HOST": db_config.get("host", os.environ.get("DB_HOST", "localhost")),
            "PORT": db_config.get("port", os.environ.get("DB_PORT", "5432")),
        }

    def generate_databases_config(self) -> dict[str, dict[str, Any]]:
        """
        Generate Django DATABASES configuration for all tenants.

        Returns:
            Dict suitable for Django settings.DATABASES
        """
        databases = {}

        for tenant_id in self.tenants:
            db_config = self.get_database_config(tenant_id)
            alias = self.tenants[tenant_id].get("database", {}).get("alias", tenant_id)
            databases[alias] = db_config

        return databases

    def reload(self) -> None:
        """Reload configuration from the original file."""
        if self._config_path:
            self.load_from_file(self._config_path)
