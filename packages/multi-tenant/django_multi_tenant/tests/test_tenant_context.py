"""Tests for tenant context management."""

import pytest

from django_multi_tenant.middleware.tenant_context import (
    TenantContext,
    TenantInfo,
    get_current_tenant,
    set_current_tenant,
)


class TestTenantInfo:
    def test_create_tenant_info(self):
        tenant = TenantInfo(
            tenant_id="test-tenant",
            name="Test Tenant",
            database="test_db",
            config={"features": {"ai_secretary": True}},
        )
        assert tenant.tenant_id == "test-tenant"
        assert tenant.name == "Test Tenant"
        assert tenant.database == "test_db"

    def test_get_feature(self):
        tenant = TenantInfo(
            tenant_id="test",
            name="Test",
            config={"features": {"ai_secretary": True, "nft": False}},
        )
        assert tenant.get_feature("ai_secretary") is True
        assert tenant.get_feature("nft") is False
        assert tenant.get_feature("unknown") is None
        assert tenant.get_feature("unknown", "default") == "default"

    def test_get_theme(self):
        tenant = TenantInfo(
            tenant_id="test",
            name="Test",
            config={"theme": {"primary_color": "#ff0000"}},
        )
        assert tenant.get_theme("primary_color") == "#ff0000"
        assert tenant.get_theme("secondary_color") is None
        assert tenant.get_theme("secondary_color", "#000000") == "#000000"


class TestTenantContextVar:
    def test_get_current_tenant_default(self):
        set_current_tenant(None)
        assert get_current_tenant() is None

    def test_set_and_get_tenant(self):
        tenant = TenantInfo(tenant_id="test", name="Test")
        set_current_tenant(tenant)
        assert get_current_tenant() == tenant
        set_current_tenant(None)

    def test_clear_tenant(self):
        tenant = TenantInfo(tenant_id="test", name="Test")
        set_current_tenant(tenant)
        set_current_tenant(None)
        assert get_current_tenant() is None


class TestTenantContextManager:
    def test_context_manager_sets_tenant(self):
        tenant = TenantInfo(tenant_id="test", name="Test")
        set_current_tenant(None)

        with TenantContext(tenant) as ctx:
            assert ctx == tenant
            assert get_current_tenant() == tenant

        assert get_current_tenant() is None

    def test_context_manager_restores_previous(self):
        original = TenantInfo(tenant_id="original", name="Original")
        temporary = TenantInfo(tenant_id="temporary", name="Temporary")

        set_current_tenant(original)

        with TenantContext(temporary):
            assert get_current_tenant() == temporary

        assert get_current_tenant() == original
        set_current_tenant(None)

    def test_nested_context_managers(self):
        tenant1 = TenantInfo(tenant_id="tenant1", name="Tenant 1")
        tenant2 = TenantInfo(tenant_id="tenant2", name="Tenant 2")

        set_current_tenant(None)

        with TenantContext(tenant1):
            assert get_current_tenant() == tenant1

            with TenantContext(tenant2):
                assert get_current_tenant() == tenant2

            assert get_current_tenant() == tenant1

        assert get_current_tenant() is None
