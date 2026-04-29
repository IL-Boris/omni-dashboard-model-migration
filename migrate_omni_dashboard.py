#!/usr/bin/env python3
"""
Omni Dashboard Migration CLI

A simple command-line tool to export a dashboard, change its base model ID,
and re-import it (useful for migrating dashboards between models, workspaces, etc.).
"""

import argparse
import os
import sys

from dotenv import load_dotenv
from omni_python_sdk import OmniAPI


def main():
    parser = argparse.ArgumentParser(
        description="Migrate an Omni dashboard by changing its baseModelId.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Required arguments
    parser.add_argument(
        "--dashboard-id",
        required=True,
        help="The dashboard identifier (UUID or slug) to export and migrate.",
    )
    parser.add_argument(
        "--new-model-id",
        required=True,
        help="The new baseModelId (UUID) to set on the dashboard.",
    )

    # Optional configuration
    parser.add_argument(
        "--env-file",
        default=".env",
        help="Path to the .env file containing OMNI_API_KEY and BASE_URL.",
    )
    parser.add_argument(
        "--api-key",
        help="Override OMNI_API_KEY from the environment/.env file.",
    )
    parser.add_argument(
        "--base-url",
        help="Override BASE_URL from the environment/.env file.",
    )

    # Extra flags
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Export and update the dashboard but do NOT perform the import.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print more detailed output (including the full exported document).",
    )

    args = parser.parse_args()

    # Load environment variables
    if os.path.exists(args.env_file):
        load_dotenv(args.env_file)
        if args.verbose:
            print(f"✅ Loaded environment from {args.env_file}")
    else:
        if args.verbose:
            print(
                f"⚠️  .env file not found at {args.env_file} – relying on shell environment only"
            )

    # Get credentials (CLI flag > .env > environment variable)
    api_key = args.api_key or os.getenv("OMNI_API_KEY")
    base_url = args.base_url or os.getenv("BASE_URL")

    if not api_key:
        print(
            "❌ Error: OMNI_API_KEY is required. Provide it via --api-key or in your .env file.",
            file=sys.stderr,
        )
        sys.exit(1)
    if not base_url:
        print(
            "❌ Error: BASE_URL is required. Provide it via --base-url or in your .env file.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Initialize the Omni API client
    api = OmniAPI(api_key=api_key, base_url=base_url)

    if args.verbose:
        print(f"🔌 Connected to Omni at {base_url}")

    print(f"📤 Exporting dashboard: {args.dashboard_id}")
    dashboard_export = api.document_export(args.dashboard_id)

    if args.verbose:
        print("📄 Exported document (first 500 chars):")
        print(
            str(dashboard_export)[:500] + "..."
            if len(str(dashboard_export)) > 500
            else dashboard_export
        )

    # Update the model ID
    dashboard_export.update({"baseModelId": args.new_model_id})
    print(f"🔄 Updated baseModelId → {args.new_model_id}")

    if args.dry_run:
        print("🧪 Dry-run mode: skipping import.")
        print("✅ Migration preparation complete (dry-run).")
        sys.exit(0)

    # Perform the import
    print("📥 Importing updated dashboard...")
    api.document_import(dashboard_export)

    print("🎉 Migration completed successfully!")


if __name__ == "__main__":
    main()
