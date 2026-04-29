# Omni CLI - Dashboard & Model Management

A command-line tool for Omni with multiple commands:
- migrate          → Export a dashboard, change its baseModelId, and re-import
- list-documents   → List all documents in the workspace
- list-models      → List all models in the workspace
- show-model       → Show the current baseModelId of a specific document

---

## ✨ Features

- Export → update `baseModelId` → import in a single command
- Full support for `.env` files (or environment variables)
- List all documents and models
- Override credentials via CLI flags
- `--dry-run` mode for safe testing
- `--verbose` output for debugging
- Clear error messages and proper exit codes
- Works on macOS, Linux, and Windows

---

## 📋 Prerequisites

- Python 3.8+
- `omni_python_sdk` package
- `python-dotenv` package

These are already defined in the `requirements.txt`

### Create and activate a virtual environment
```bash
python3 -m venv env
source env/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### 🔧 Configuration

Create a `.env` file in the same directory as the script:

```env
OMNI_API_KEY=omni_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
BASE_URL=https://your-company.omni.co
```

You can also pass credentials directly via command-line flags (see Usage).

### 📖 Usage
```bash
python migrate_omni_dashboard.py --help
```

#### Basic command (recommended)
```bash
python migrate_omni_dashboard.py migrate \
  --dashboard-id "abc123-def456-ghi789" \
  --new-model-id "new-model-uuid-here"
```

### All available options

| Flag                | Required | Description                                      | Default      |
|---------------------|----------|--------------------------------------------------|--------------|
| `--env-file`        | No       | Path to `.env` file                              | `.env`       |
| `--api-key`         | No       | Override `OMNI_API_KEY`                          | env var      |
| `--base-url`        | No       | Override `BASE_URL`                              | env var      |
| `--verbose`         | No       | Show detailed output (including exported doc)    | `false`      |
| `--dashboard-id`    | Yes      | Dashboard identifier (UUID) Migrate Specific     | -            |

`migrate` specific options

| Flag                | Required | Description                                      | Default      |
|---------------------|----------|--------------------------------------------------|--------------|
| `--new-model-id`    | Yes      | New `baseModelId` to set Migrate Specific        | -            |
| `--dry-run`         | No       | Export & update but skip import                  | `false`      |

### Examples

**Dry-run first (highly recommended!)**

```bash
python migrate_omni_dashboard.py migrate \
  --dashboard-id "abc123" \
  --new-model-id "xyz789" \
  --dry-run --verbose
```

**Use a different environment file**

```bash
python migrate_omni_dashboard.py migrate \
  --dashboard-id "prod-dashboard" \
  --new-model-id "staging-model-id" \
  --env-file .env.staging
```

**Pass credentials directly**

```bash
python migrate_omni_dashboard.py migrate \
  --dashboard-id "abc123" \
  --new-model-id "new-model" \
  --api-key "omni_..." \
  --base-url "https://staging.omni.co"
```

### 🧪 Testing & Safety

Always run with `--dry-run` first. The tool will:

1. Export the dashboard
2. Update the `baseModelId`
3. Show you exactly what will be imported
4. **Not** perform the actual import

### 📄 License

This script is provided as-is under the MIT License. Feel free to modify and use it in your projects.

---

**Made with ❤️ for the Omni community**
