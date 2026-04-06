# Setup Guide

## Prerequisites
- Python 3.10+
- GitHub personal access token (PAT) with `repo` scope (for issues/PRs/commits).

## Quick Start

1. **Clone the repository:**
   ```
   git clone <repo-url>
   cd Assignment-Aventisia-
   ```

2. **Create virtual environment:**
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```
   pip install -r req.txt
   ```
   *Note: If `req.txt` missing, install core deps:*
   ```
   pip install fastapi uvicorn pydantic pydantic-settings httpx python-dotenv
   ```

4. **Set environment variables:**
   Create `.env` file in root:
   ```
   GH_TOKEN=your_github_pat_here
   ```

5. **Run the server:**
   ```
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - API Endpoints: http://localhost:8000/api/v1/github/

## Configuration
Settings loaded from `.env` (see `core/config.py`):
- `GH_TOKEN`: Required GitHub token.
- `GITHUB_URL`: GitHub API base (default: https://api.github.com).
- `GITHUB_API_VERSION`: API version (default: 2026-03-10).

## Testing
Use Swagger UI or curl:
```
curl "http://localhost:8000/api/v1/github/repos?username=octocat"
```

## Troubleshooting
- **Token errors**: Ensure PAT has `repo` scope.

- **Docs**: See `docs/api_endpoints.md` for full endpoint details.

