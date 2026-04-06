# GitHub API Endpoints Documentation

This document lists all available endpoints in the FastAPI application. All endpoints are mounted under `/api/v1/github/` (based on standard FastAPI router prefix).

## Endpoint Summary

| Method | Path | Summary |
|--------|------|---------|
| GET | `/repos` | Fetch repositories for a user or organization |
| POST | `/{owner}/{repo}/issues` | Create a new issue in a repository |
| GET | `/{owner}/{repo}/issues` | List issues in a repository |
| GET | `/{owner}/{repo}/commits` | Fetch commits from a repository |
| POST | `/{owner}/{repo}/pulls` | Create a pull request |

## Detailed Endpoints

### GET /api/v1/github/repos
**Fetch repositories for a user or organization.**

**Path Parameters:** None

**Query Parameters:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| username | str | No | "" | Username to fetch user repos (exactly one of username or org_name) |
| org_name | str | No | "" | Organization name to fetch org repos (exactly one of username or org_name) |
| type | Literal["all", "public", "private", "forks", "sources", "member"] | No | "all" | Repo type filter |
| sort | Literal["created", "updated", "pushed", "full_name"] | No | "created" | Sort field |
| direction | Literal["asc", "desc"] | No | "desc" | Sort direction |
| per_page | int | No | 30 | Results per page (1-100) |
| page | int | No | 1 | Page number (>=1) |

**Request Body:** None

**Responses:** `200` - List of repositories (`List[Repo]`)

---

### POST /api/v1/github/{owner}/{repo}/issues
**Create a new issue in a repository.**

**Path Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| owner | str | Yes | Repository owner (user or org) |
| repo | str | Yes | Repository name |

**Query Parameters:** None

**Request Body:** `IssueCreate`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| title | str | Yes | - | Title of the issue |
| body | Optional[str] | No | None | Main content/description |
| milestone | Optional[int] | No | None | Milestone number |
| labels | Optional[List[str]] | No | None | List of labels (e.g., ['bug']) |
| assignees | Optional[List[str]] | No | None | List of usernames to assign |
| type | Optional[str] | No | None | Issue type/category |

**Responses:** `200` - `{"message": "Issue created", "issue": result}`

---

### GET /api/v1/github/{owner}/{repo}/issues
**List issues in a repository.**

**Path Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| owner | str | Yes | Repository owner |
| repo | str | Yes | Repository name |

**Query Parameters:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| issue_filter | Literal["assigned", "created", "mentioned", "subscribed", "repos", "all"] | No | "assigned" | Issue filter |
| state | Literal["open", "closed", "all"] | No | "open" | Issue state |
| labels | Optional[str] | No | None | Comma-separated labels |
| sort | Literal["created", "updated", "comments"] | No | "created" | Sort field |
| direction | Literal["asc", "desc"] | No | "desc" | Sort direction |
| since | Optional[str] | No | None | ISO 8601 datetime |
| per_page | int | No | 30 | Results per page (<=100) |
| page | int | No | 1 | Page number (>=1) |

**Request Body:** None

**Responses:** `200` - List of issues (`List[Issue]`)

---

### GET /api/v1/github/{owner}/{repo}/commits
**Fetch commits from a repository with optional filters.**

**Path Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| owner | str | Yes | Repository owner |
| repo | str | Yes | Repository name |

**Query Parameters:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| sha | Optional[str] | No | None | SHA or branch to start from |
| path | Optional[str] | No | None | Only commits affecting this path |
| committer | Optional[str] | No | None | GitHub committer username |
| author | Optional[str] | No | None | GitHub author username |
| since | Optional[str] | No | None | Only commits after this ISO 8601 date |
| until | Optional[str] | No | None | Only commits before this ISO 8601 date |
| per_page | int | No | 30 | Number of results per page (<=100) |
| page | int | No | 1 | Page number (>=1) |

**Request Body:** None

**Responses:** `200` - List of commits (`List[Commit]`)

---

### POST /api/v1/github/{owner}/{repo}/pulls
**Create a pull request.**

**Path Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| owner | str | Yes | Repository owner |
| repo | str | Yes | Repository name |

**Query Parameters:** None

**Request Body:** `PullRequestCreate`

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| title | Optional[str] | No | None | PR title (exactly one of title or issue) |
| head | str | Yes | - | Branch with changes (user:branch for cross-repo) |
| base | str | Yes | - | Target branch |
| body | Optional[str] | No | None | PR description |
| maintainer_can_modify | Optional[bool] | No | None | Allow maintainers to modify |
| issue | Optional[int] | No | None | Issue number to convert (exactly one of title or issue) |
| is_draft | bool | No | false | Create as draft PR |

**Responses:** `201` - `{"message": "PR created", "pr": result}`

## Notes
- All endpoints require authentication via GitHub token (handled in `GitHubService`).
- Validation enforced: e.g., exactly one of `username/org_name`, `title/issue`.
- Pagination consistent across list endpoints.
- Models defined in `schemas/github.py`.
