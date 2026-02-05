"""
Management command to create a new tenant.

Usage:
    python manage.py create_tenant tenant-id --name "Tenant Name" --domain example.com
"""

import yaml
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create a new tenant in the configuration file"

    def add_arguments(self, parser):
        parser.add_argument(
            "tenant_id",
            type=str,
            help="Unique identifier for the tenant (e.g., 'nantou-gov')",
        )
        parser.add_argument(
            "--name",
            type=str,
            required=True,
            help="Display name for the tenant",
        )
        parser.add_argument(
            "--domain",
            type=str,
            action="append",
            dest="domains",
            help="Domain(s) for the tenant (can be specified multiple times)",
        )
        parser.add_argument(
            "--config",
            type=str,
            default="config/tenants.yml",
            help="Path to tenants.yml configuration file",
        )
        parser.add_argument(
            "--db-name",
            type=str,
            help="Database name (defaults to tplanet_{tenant_id})",
        )
        parser.add_argument(
            "--db-host",
            type=str,
            default="${DB_HOST:-localhost}",
            help="Database host",
        )
        parser.add_argument(
            "--primary-color",
            type=str,
            default="#1976d2",
            help="Primary theme color",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print the configuration without saving",
        )

    def handle(self, *args, **options):
        tenant_id = options["tenant_id"]
        config_path = options["config"]

        # Load existing config or create new
        try:
            with open(config_path, encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
        except FileNotFoundError:
            config = {}

        if "tenants" not in config:
            config["tenants"] = {}

        if tenant_id in config["tenants"]:
            raise CommandError(f"Tenant '{tenant_id}' already exists")

        # Build tenant configuration
        db_name = options["db_name"] or f"tplanet_{tenant_id.replace('-', '_')}"

        tenant_config = {
            "name": options["name"],
            "domains": options["domains"] or [f"{tenant_id}.tplanet.ai"],
            "database": {
                "alias": tenant_id,
                "name": db_name,
                "host": options["db_host"],
            },
            "features": {
                "ai_secretary": True,
                "nft": False,
            },
            "theme": {
                "primary_color": options["primary_color"],
                "secondary_color": "#424242",
            },
        }

        config["tenants"][tenant_id] = tenant_config

        # Output
        yaml_output = yaml.dump(config, allow_unicode=True, default_flow_style=False)

        if options["dry_run"]:
            self.stdout.write("\n--- Configuration Preview ---\n")
            self.stdout.write(yaml_output)
            self.stdout.write("\n--- End Preview ---\n")
            self.stdout.write(
                self.style.WARNING("Dry run mode - no changes saved")
            )
        else:
            with open(config_path, "w", encoding="utf-8") as f:
                f.write(yaml_output)

            self.stdout.write(
                self.style.SUCCESS(f"Created tenant '{tenant_id}' in {config_path}")
            )

        # Print next steps
        self.stdout.write("\nNext steps:")
        self.stdout.write(f"  1. Create database: CREATE DATABASE {db_name};")
        self.stdout.write(f"  2. Run migrations: python manage.py migrate --database={tenant_id}")
        self.stdout.write(f"  3. Configure DNS for domains: {options['domains'] or [f'{tenant_id}.tplanet.ai']}")
