#!/usr/bin/env python3
"""
Omni CLI - Dashboard & Model Management

A production-ready command-line tool for Omni with multiple commands:
  • migrate      → Export a dashboard, change its baseModelId, and re-import
  • list-documents → List all documents
  • list-models    → List all models
  • show-model    → Show the current baseModelId of a specific document
"""

import argparse
import json
import os
import sys

from dotenv import load_dotenv
from omni_python_sdk import OmniAPI


def load_api(args):
    """Load credentials and initialize the Omni API client."""
    # Load environment variables
    if os.path.exists(args.env_file):
        load_dotenv(args.env_file)
        if getattr(args, "verbose", False):
            print(f"✅ Loaded environment from {args.env_file}")
    elif getattr(args, "verbose", False):
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

    api = OmniAPI(api_key=api_key, base_url=base_url)

    if getattr(args, "verbose", False):
        print(f"🔌 Connected to Omni at {base_url}")

    return api


def main():
    parser = argparse.ArgumentParser(
        description="Omni CLI - Dashboard & Model Management",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Common arguments for all subcommands
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
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print more detailed output.",
    )

    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    # ====================== MIGRATE ======================
    migrate = subparsers.add_parser(
        "migrate",
        help="Export a dashboard, change its baseModelId, and re-import it",
    )
    migrate.add_argument(
        "--dashboard-id",
        required=True,
        help="The dashboard identifier (UUID or slug) to migrate.",
    )
    migrate.add_argument(
        "--new-model-id",
        required=True,
        help="The new baseModelId (UUID) to set on the dashboard.",
    )
    migrate.add_argument(
        "--dry-run",
        action="store_true",
        help="Export and update the dashboard but do NOT perform the import.",
    )

    # ====================== LIST DOCUMENTS ======================
    list_docs = subparsers.add_parser(
        "list-documents",
        help="List all documents in the workspace",
    )

    # ====================== LIST MODELS ======================
    list_models = subparsers.add_parser(
        "list-models",
        help="List all models in the workspace",
    )

    # ====================== SHOW MODEL ======================
    show_model = subparsers.add_parser(
        "show-model",
        help="Show the current baseModelId of a specific document",
    )
    show_model.add_argument(
        "--dashboard-id",
        required=True,
        help="The dashboard identifier (UUID or slug) to inspect.",
    )

    args = parser.parse_args()

    # Initialize API (shared across all commands)
    api = load_api(args)

    # ====================== COMMAND HANDLERS ======================
    if args.command == "migrate":
        print(f"📤 Exporting dashboard: {args.dashboard_id}")
        dashboard_export = api.document_export(args.dashboard_id)

        if args.verbose:
            print("📄 Exported document preview (first 500 chars):")
            preview = (
                str(dashboard_export)[:500] + "..."
                if len(str(dashboard_export)) > 500
                else str(dashboard_export)
            )
            print(preview)

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

    elif args.command == "list-documents":
        print("📋 Fetching all documents...")
        documents = api.list_documents()
        print(json.dumps(documents, indent=2))

    elif args.command == "list-models":
        print("📋 Fetching all models...")
        models = api.list_models()
        print(json.dumps(models, indent=2))

    elif args.command == "show-model":
        print(f"🔍 Inspecting document: {args.dashboard_id}")
        dashboard_export = api.document_export(args.dashboard_id)

        # Try to extract baseModelId (works whether it's a dict or dict-like object)
        if isinstance(dashboard_export, dict):
            import ipdb

            ipdb.set_trace()
            current_model = dashboard_export.get("baseModelId")
        else:
            current_model = getattr(
                dashboard_export, "baseModelId", None
            ) or dashboard_export.get("baseModelId")

        if current_model:
            print(f"✅ Current baseModelId: {current_model}")
        else:
            print("⚠️  Could not find baseModelId in the exported document.")

        if args.verbose:
            print("\nFull exported document:")
            print(
                json.dumps(dashboard_export, indent=2)
                if isinstance(dashboard_export, dict)
                else dashboard_export
            )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
