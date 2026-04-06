from datetime import datetime
from typing import Optional
import httpx
from core.config import settings


class GitHubService:
    """
    All GitHub API interactions.
    Instantiate once and inject as a dependency across routers.
    """

    def __init__(self):
        self.base_url = settings.github_url
        self.timeout = 10.0

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _get_headers(self) -> dict[str, str]:
        """Builds headers."""
        return {
            "Authorization": f"Bearer {settings.github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": f"{settings.github_api_version}"
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: dict | None = None,
        params: dict | None = None,
    ) -> dict | list:
        """
        Generic async HTTP handler for all GitHub API calls.
        """
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        base = str(self.base_url).rstrip('/')
        url = f"{base}{endpoint}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.request(
                method,
                url,
                headers=self._get_headers(),
                json=data,
                params=params,
            )
            response.raise_for_status()
            return response.json()

    # ── Repositories ──────────────────────────────────────────────────────────

    async def get_user_repos(
        self,
        username: str,
        type: str = "all",
        sort: str = "created",
        direction: str | None = None,
        per_page: int = 30,
        page: int = 1,
    ) -> list:

        return await self._request(
            "GET",
            f"/users/{username}/repos",
            params={
                "type": type,
                "sort": sort,
                "direction": direction,
                "per_page": per_page,
                "page": page,
            },
        )

    async def get_org_repos(
        self,
        org_name: str,
        type: str = "all",
        sort: str = "created",
        direction: str | None = None,
        per_page: int = 30,
        page: int = 1,
    ) -> list:

        return await self._request(
            "GET",
            f"/orgs/{org_name}/repos",
            params={
                "type": type,
                "sort": sort,
                "direction": direction,
                "per_page": per_page,
                "page": page,
            },
        )

    # ── Issues ────────────────────────────────────────────────────────────────

    async def list_issues(
        self,
        owner: str,
        repo: str,
        state: str = "open",
        filter: Optional[str] = None,
        labels: Optional[str] = None,
        sort: str = "created",
        direction: str = "desc",
        since: Optional[datetime] = None,
        per_page: int = 30,
        page: int = 1,
    ) -> list:

        params = {
            "state": state,
            "labels": labels,
            "sort": sort,
            "direction": direction,
            "per_page": per_page,
            "filter": filter,
            "page": page,
            "since": since.isoformat() + "Z" if since else None
        }

        return await self._request(
            "GET",
            f"/repos/{owner}/{repo}/issues",
            params=params,
        )

    async def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str = "",
        assignees: list[str] | None = None,
        labels: list[str] | None = None,
        milestone: int | None = None,
        issue_type: str | None = None,
    ) -> dict:
        """
        Create a new issue in a repository.

        Args:
            owner:      Repository owner.
            repo:       Repository name.
            title:      Issue title (required).
            body:       Issue description in Markdown.
            assignees:  List of GitHub usernames to assign.
            labels:     List of label names to apply.
            milestone:  Milestone ID to associate with the issue.
            issue_type: Custom issue type string (sent as 'type' to GitHub API).
        """
        payload: dict = {"title": title, "body": body}

        if assignees:
            payload["assignees"] = assignees
        if labels:
            payload["labels"] = labels
        if milestone is not None:
            payload["milestone"] = milestone
        if issue_type:
            payload["type"] = issue_type

        return await self._request(
            "POST", f"/repos/{owner}/{repo}/issues", data=payload
        )

    # ── Commits ───────────────────────────────────────────────────────────────

    async def get_commits(
        self,
        owner: str,
        repo: str,
        params: dict,
    ) -> list:
        return await self._request(
            "GET",
            f"/repos/{owner}/{repo}/commits",
            params=params,
        )

    # ── Pull Requests (bonus) ─────────────────────────────────────────────────

    async def create_pull_request(
        self,
        owner: str,
        repo: str,
        head: str,
        base: str,
        title: str | None = None,
        body: str | None = None,
        maintainer_can_modify: bool | None = None,
        issue: int | None = None,
        is_draft: bool = False,
    ) -> dict:
        payload = {
            "head": head,
            "base": base,
        }

        if issue is not None:
            payload["issue"] = issue
        else:
            payload["title"] = title
            if body:
                payload["body"] = body

        # Optional fields (only include if not None)
        if maintainer_can_modify:
            payload["maintainer_can_modify"] = True

        if is_draft:
            payload["draft"] = True

        return await self._request(
            "POST",
            f"/repos/{owner}/{repo}/pulls",
            data=payload,
        )


def get_github_service():
    return GitHubService()
