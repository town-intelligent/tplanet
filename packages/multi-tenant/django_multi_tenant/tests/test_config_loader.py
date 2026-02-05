"""Tests for tenant configuration loader."""

import os
import tempfile
from pathlib import Path

import pytest
import yaml

from django_multi_tenant.config.loader import TenantConfigLoader


class TestTenantConfigLoader:
    def test_load_from_dict(self):
        loader = TenantConfigLoader()
        loader.load_from_dict({
            "tenants": {
                "test-tenant": {
                    "name": "Test Tenant",
                    "domains": ["test.example.com"],
                }
            }
        })

        assert "test-tenant" in loader.tenants
        assert loader.tenants["test-tenant"]["name"] == "Test Tenant"

    def test_load_from_file(self, tmp_path):
        config_file = tmp_path / "tenants.yml"
        config_file.write_text(yaml.dump({
            "tenants": {
                "file-tenant": {
                    "name": "File Tenant",
                    "domains": ["file.example.com"],
                }
            }
        }))

        loader = TenantConfigLoader()
        loader.load_from_file(config_file)

        assert "file-tenant" in loader.tenants
        assert loader.tenants["file-tenant"]["name"] == "File Tenant"

    def test_load_file_not_found(self):
        loader = TenantConfigLoader()
        with pytest.raises(FileNotFoundError):
            loader.load_from_file("/nonexistent/path.yml")

    def test_env_var_expansion(self, monkeypatch):
        monkeypatch.setenv("TEST_DB_HOST", "db.example.com")

        loader = TenantConfigLoader()
        loader.load_from_dict({
            "tenants": {
                "env-tenant": {
                    "database": {
                        "host": "${TEST_DB_HOST}",
                    }
                }
            }
        })

        assert loader.tenants["env-tenant"]["database"]["host"] == "db.example.com"

    def test_env_var_with_default(self, monkeypatch):
        # Ensure env var is not set
        monkeypatch.delenv("UNDEFINED_VAR", raising=False)

        loader = TenantConfigLoader()
        loader.load_from_dict({
            "tenants": {
                "default-tenant": {
                    "database": {
                        "host": "${UNDEFINED_VAR:-localhost}",
                    }
                }
            }
        })

        assert loader.tenants["default-tenant"]["database"]["host"] == "localhost"

    def test_env_var_override_default(self, monkeypatch):
        monkeypatch.setenv("OVERRIDE_VAR", "overridden")

        loader = TenantConfigLoader()
        loader.load_from_dict({
            "tenants": {
                "override-tenant": {
                    "database": {
                        "host": "${OVERRIDE_VAR:-default}",
                    }
                }
            }
        })

        assert loader.tenants["override-tenant"]["database"]["host"] == "overridden"

    def test_get_tenant(self):
        loader = TenantConfigLoader()
        loader.load_from_dict({
            "tenants": {
                "tenant-a": {"name": "Tenant A"},
                "tenant-b": {"name": "Tenant B"},
            }
        })

        assert loader.get_tenant("tenant-a")["name"] == "Tenant A"
        assert loader.get_tenant("nonexistent") is None

    def test_get_tenant_ids(self):
        loader = TenantConfigLoader()
        loader.load_from_dict({
            "tenants": {
                "tenant-a": {"name": "Tenant A"},
                "tenant-b": {"name": "Tenant B"},
            }
        })

        ids = loader.get_tenant_ids()
        assert "tenant-a" in ids
        assert "tenant-b" in ids

    def test_get_database_config(self, monkeypatch):
        monkeypatch.setenv("DB_USER", "testuser")
        monkeypatch.setenv("DB_PASSWORD", "testpass")

        loader = TenantConfigLoader()
        loader.load_from_dict({
            "tenants": {
                "db-tenant": {
                    "database": {
                        "name": "tenant_db",
                        "host": "db.example.com",
                    }
                }
            }
        })

        db_config = loader.get_database_config("db-tenant")
        assert db_config["NAME"] == "tenant_db"
        assert db_config["HOST"] == "db.example.com"
        assert db_config["USER"] == "testuser"
        assert db_config["PASSWORD"] == "testpass"

    def test_generate_databases_config(self):
        loader = TenantConfigLoader()
        loader.load_from_dict({
            "tenants": {
                "tenant-a": {
                    "database": {
                        "alias": "tenant_a",
                        "name": "db_a",
                    }
                },
                "tenant-b": {
                    "database": {
                        "alias": "tenant_b",
                        "name": "db_b",
                    }
                },
            }
        })

        databases = loader.generate_databases_config()
        assert "tenant_a" in databases
        assert "tenant_b" in databases
        assert databases["tenant_a"]["NAME"] == "db_a"
        assert databases["tenant_b"]["NAME"] == "db_b"

    def test_reload(self, tmp_path):
        config_file = tmp_path / "tenants.yml"
        config_file.write_text(yaml.dump({
            "tenants": {
                "initial": {"name": "Initial"}
            }
        }))

        loader = TenantConfigLoader()
        loader.load_from_file(config_file)
        assert "initial" in loader.tenants

        # Update file
        config_file.write_text(yaml.dump({
            "tenants": {
                "updated": {"name": "Updated"}
            }
        }))

        loader.reload()
        assert "updated" in loader.tenants
        assert "initial" not in loader.tenants
