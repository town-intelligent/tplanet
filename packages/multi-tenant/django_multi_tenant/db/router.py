"""
Database router for multi-tenant applications.

Routes queries to the appropriate database based on the current tenant context.
Shared apps (auth, sessions, contenttypes) always use the default database.
"""

from typing import Any

from django.conf import settings

from django_multi_tenant.middleware.tenant_context import get_current_tenant


class TenantDatabaseRouter:
    """
    Database router that directs queries based on tenant context.

    Configuration in settings.py:
        MULTI_TENANT = {
            "SHARED_APPS": ["auth", "contenttypes", "sessions", "admin"],
            "TENANT_APPS": ["accounts", "projects", "portal", "dashboard"],
        }

        DATABASE_ROUTERS = ["django_multi_tenant.db.router.TenantDatabaseRouter"]
    """

    def __init__(self):
        multi_tenant_settings = getattr(settings, "MULTI_TENANT", {})
        self.shared_apps = set(
            multi_tenant_settings.get(
                "SHARED_APPS",
                ["auth", "contenttypes", "sessions", "admin"],
            )
        )
        self.tenant_apps = set(
            multi_tenant_settings.get(
                "TENANT_APPS",
                [],
            )
        )

    def _get_app_label(self, model: Any) -> str:
        """Extract app label from model."""
        return model._meta.app_label

    def _get_tenant_database(self) -> str:
        """Get the database for the current tenant."""
        tenant = get_current_tenant()
        if tenant and tenant.database:
            # Verify the database exists in settings
            if tenant.database in settings.DATABASES:
                return tenant.database
        return "default"

    def _is_shared_app(self, app_label: str) -> bool:
        """Check if app should use shared database."""
        return app_label in self.shared_apps

    def _is_tenant_app(self, app_label: str) -> bool:
        """Check if app should use tenant database."""
        # If tenant_apps is empty, all non-shared apps are tenant apps
        if not self.tenant_apps:
            return not self._is_shared_app(app_label)
        return app_label in self.tenant_apps

    def db_for_read(self, model: Any, **hints: Any) -> str:
        """
        Route read queries to the appropriate database.

        Shared apps → default database
        Tenant apps → tenant-specific database
        """
        app_label = self._get_app_label(model)

        if self._is_shared_app(app_label):
            return "default"

        if self._is_tenant_app(app_label):
            return self._get_tenant_database()

        return "default"

    def db_for_write(self, model: Any, **hints: Any) -> str:
        """
        Route write queries to the appropriate database.

        Shared apps → default database
        Tenant apps → tenant-specific database
        """
        app_label = self._get_app_label(model)

        if self._is_shared_app(app_label):
            return "default"

        if self._is_tenant_app(app_label):
            return self._get_tenant_database()

        return "default"

    def allow_relation(self, obj1: Any, obj2: Any, **hints: Any) -> bool | None:
        """
        Allow relations if both objects are in the same database.

        Returns:
            True if relation is allowed
            None to defer to other routers
        """
        db1 = self.db_for_read(type(obj1))
        db2 = self.db_for_read(type(obj2))

        if db1 == db2:
            return True

        # Allow relations between shared and tenant databases
        # (e.g., User → TenantProfile)
        app1 = self._get_app_label(type(obj1))
        app2 = self._get_app_label(type(obj2))

        if self._is_shared_app(app1) or self._is_shared_app(app2):
            return True

        return None

    def allow_migrate(self, db: str, app_label: str, **hints: Any) -> bool | None:
        """
        Determine if migration is allowed on the given database.

        Shared apps → only default database
        Tenant apps → only tenant databases
        """
        if self._is_shared_app(app_label):
            return db == "default"

        if self._is_tenant_app(app_label):
            # Allow migration on default if no tenant databases configured
            if db == "default":
                return True
            # For tenant databases, allow migration
            return db != "default"

        return None
