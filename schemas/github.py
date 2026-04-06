from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Literal
from datetime import datetime

# =============================================================================
# SHARED PARAMETERS
# =============================================================================

class PaginationParams(BaseModel):
    """Pagination parameters for Github API requests."""
    per_page: int = Field(
        30, ge=1, le=100, description="Results per page (max 100)")
    page: int = Field(1, ge=1, description="Page number")
    direction: Optional[Literal["asc", "desc"]] = "desc"


# =============================================================================
# QUERY GUIDELINES (GET Requests)
# =============================================================================

class RepoQueryParams(PaginationParams):
    username: str = ""
    org_name: str = ""
    type: Literal["all", "public", "private",
                  "forks", "sources", "member"] = "all"
    sort: Literal["created", "updated", "pushed", "full_name"] = "created"


class IssueQueryParams(PaginationParams):
    issue_filter: Literal["assigned", "created",
                          "mentioned", "subscribed", "repos", "all"] = "assigned"
    state: Literal["open", "closed", "all"] = "open"
    labels: Optional[str] = None
    sort: Literal["created", "updated", "comments"] = "created"
    since: Optional[str] = None


class CommitQueryParams(PaginationParams):
    sha: Optional[str] = Field(
        None,
        description="SHA or branch name to start listing commits from."
    )
    path: Optional[str] = Field(
        None,
        description="Only return commits that affect the specified file path."
    )
    committer: Optional[str] = Field(
        None,
        description="GitHub username of the committer to filter commits."
    )
    author: Optional[str] = Field(
        None,
        description="GitHub username of the author to filter commits."
    )
    since: Optional[str] = Field(
        None,
        description="Only return commits after this date (ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ)."
    )
    until: Optional[str] = Field(
        None,
        description="Only return commits before this date (ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ)."
    )


# =============================================================================
# RESPONSE MODELS (Output Serialization)
# =============================================================================

class Repo(BaseModel):
    id: int
    name: str
    full_name: str
    private: bool
    html_url: str
    description: Optional[str] = None
    model_config = ConfigDict(extra="allow")

class Issue(BaseModel):
    id: int
    number: int
    title: str
    state: str
    body: Optional[str] = None
    html_url: str
    created_at: datetime
    model_config = ConfigDict(extra="allow")
    

class Commit(BaseModel):
    sha: str
    html_url: str
    message: Optional[str] = None
    author_name: Optional[str] = None
    author_email: Optional[str] = None

    model_config = ConfigDict(extra="allow")

# =============================================================================
# Responses
# =============================================================================

RepoResponse = List[Repo]
IssueResponse = List[Issue]
CommitResponse = List[Commit]
class IssueCreateResponse(BaseModel):
    message: str
    issue: Issue

# =============================================================================
# REQUEST MODELS (POST/PUT/PATCH Bodies)
# =============================================================================

class IssueCreate(BaseModel):
    title: str = Field(
        ...,
        description="Required. The title of the issue. Can be a short summary describing the problem or request."
    )
    body: Optional[str] = Field(
        None,
        description="Optional. The main content or description of the issue, including details, steps to reproduce, or context."
    )
    milestone: Optional[int] = Field(
        None,
        description=(
            "Optional. The milestone number to associate with this issue. "
            "Only users with push access can set this; otherwise it will be ignored."
        )
    )
    labels: Optional[List[str]] = Field(
        None,
        description=(
            "Optional. A list of labels to assign to the issue (e.g., 'bug', 'enhancement'). "
            "Only users with push access can set labels; otherwise they will be ignored."
        )
    )
    assignees: Optional[List[str]] = Field(
        None,
        description=(
            "Optional. A list of usernames to assign to this issue. "
            "Only users with push access can set assignees; otherwise they will be ignored."
        )
    )
    type: Optional[str] = Field(
        None,
        description=(
            "Optional. The type/category of the issue (e.g., 'bug', 'feature'). "
            "Only users with push access can set this; otherwise it will be ignored."
        )
    )


class PullRequestCreate(BaseModel):
    title: Optional[str] = Field(
        None,
        description=(
            "The title of the new pull request. "
            "Required unless 'issue' is specified."
        )
    )
    head: str = Field(
        ...,
        description=(
            "Required. The name of the branch where your changes are implemented. "
            "For cross-repository pull requests, use the format 'username:branch'."
        )
    )
    base: str = Field(
        ...,
        description=(
            "Required. The name of the branch you want the changes merged into. "
            "Must be an existing branch in the current repository."
        )
    )
    body: Optional[str] = Field(
        None,
        description="The contents or description of the pull request."
    )
    maintainer_can_modify: Optional[bool] = Field(
        None,
        description="Indicates whether repository maintainers can modify the pull request."
    )
    issue: Optional[int] = Field(
        None,
        description=(
            "An existing issue number to convert into a pull request. "
            "The issue’s title, body, and comments will be used. "
            "Required unless 'title' is specified."
        )
    )
    is_draft: bool = Field(
        False,
        description="Indicates whether the pull request is created as a draft."
    )
